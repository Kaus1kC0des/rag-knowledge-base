import os
import re
import sys
from typing import List, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, OnlinePDFLoader, PagedPDFSplitter
from langchain_core.documents import Document as LCDocument

from api.schemas.mongodb import SourceDocument, Chunk
from api.processors.vector_embedder import ChunkEmbedder


# ---------------------------
# Text Cleaning & Normalization
# ---------------------------

class TextNormalizer:
    """
    Normalize Unicode, replace smart punctuation, remove control chars,
    collapse whitespace/newlines.
    """
    _replacements = {
        "–": "-", "—": "-", "―": "-", "−": "-",
        "“": '"', "”": '"', "„": '"',
        "‘": "'", "’": "'",
        "…": "...",
        "\u00A0": " ",  # non-breaking space
        "\u200B": "",   # zero-width space
    }

    _ctrl_re = re.compile(r"[\u0000-\u001F\u007F]")
    _multi_nl_re = re.compile(r"\n{2,}")
    _multi_space_re = re.compile(r"[ \t]{2,}")

    @staticmethod
    def normalize(text: str) -> str:
        # NFKC via built-in (avoid extra deps)
        import unicodedata
        text = unicodedata.normalize("NFKC", text)
        for bad, good in TextNormalizer._replacements.items():
            text = text.replace(bad, good)
        text = TextNormalizer._ctrl_re.sub("", text)
        text = TextNormalizer._multi_nl_re.sub("\n", text)
        text = TextNormalizer._multi_space_re.sub(" ", text)
        return text.strip()


class BoilerplateStripper:
    """
    Remove page headers/footers and repetitive junk.
    - Static footer (college line).
    - Dynamic subject header lines: "ML<4digits> <subject name> <year-year> Unit-<roman> Class Notes"
    - Page numbers or isolated repeated lines.
    """
    # Static footer pattern (appears in all docs)
    FOOTER_RE = re.compile(
        r"St\.?\s*Joseph’s\s*College\s*of\s*Engineering\s+\d+\s+Dept\s*of\s*AML",
        flags=re.IGNORECASE
    )

    # Dynamic header like:
    # ML1703- Image Processing and Vision Techniques 2025-2026 Unit-II Class Notes
    HEADER_DYNAMIC_RE = re.compile(
        r"ML\d{4}[\s\-:]+[A-Za-z0-9&(),\.\- ]+?\s+\d{4}\s*-\s*\d{4}\s+Unit[\s\-]?[IVXLC]+(?:\s+Class\s+Notes)?",
        flags=re.IGNORECASE
    )

    # Loose page-number lines like "Page 12", "- 12 -", "12"
    PAGE_NUMBERISH_RE = re.compile(
        r"^(?:page\s*)?\d{1,4}\s*$|^[-–—]?\s*\d{1,4}\s*[-–—]?$",
        flags=re.IGNORECASE
    )

    @staticmethod
    def strip(text: str) -> str:
        # Remove specific header/footer anywhere in the text first
        text = BoilerplateStripper.FOOTER_RE.sub("", text)
        text = BoilerplateStripper.HEADER_DYNAMIC_RE.sub("", text)

        # Line-by-line filtering for repetitive cruft
        cleaned_lines: List[str] = []
        seen_in_page = set()

        for raw_line in text.splitlines():
            line = raw_line.strip()

            if not line:
                continue

            # Drop obvious page numbers
            if BoilerplateStripper.PAGE_NUMBERISH_RE.match(line):
                continue

            # Kill exact repeats within the same page block
            if line in seen_in_page:
                continue

            # Sometimes the dynamic header sneaks in with dashes/extra spaces
            if BoilerplateStripper.HEADER_DYNAMIC_RE.search(line):
                continue

            seen_in_page.add(line)
            cleaned_lines.append(line)

        # Rebuild with single newlines
        return "\n".join(cleaned_lines).strip()


# ---------------------------
# Document Processor
# ---------------------------

class DocumentProcessor:
    """
    End-to-end:
      1) Load PDF (local or URL).
      2) Clean & normalize per page.
      3) Split with semantic-friendly splitter.
      4) Embed via ChunkEmbedder.
      5) Produce Chunk ODMs with stable metadata & chunk_ids.
    """

    def __init__(self, source_doc: SourceDocument):
        self.source_doc = source_doc
        self.embedder = ChunkEmbedder()
        self._normalizer = TextNormalizer()

        # Tuned to preserve paragraphs/sentences before characters
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=180,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
            is_separator_regex=False,
        )

    # --- helpers ---

    @staticmethod
    def _resolve_loader(source_url: str):
        if source_url.startswith("http://") or source_url.startswith("https://"):
            return OnlinePDFLoader(source_url)
        return PyPDFLoader(source_url)

    def _clean_page_content(self, text: str) -> str:
        text = self._normalizer.normalize(text)
        text = BoilerplateStripper.strip(text)
        # Final collapse of extra blank lines after stripping
        text = re.sub(r"\n{2,}", "\n", text).strip()
        return text

    @staticmethod
    def _get_id_from(obj) -> Optional[str]:
        """
        Safely extract an id from either a Beanie Document or a Link[Document] that has been fetched.
        Assumes caller has fetched links if they were lazy.
        """
        return getattr(obj, "id", None)

    # --- main ---

    async def process_and_create_chunks(
        self,
        chunk_size: int = 1000,
        overlap: int = 180,
        min_chunk_chars: int = 200,
    ) -> List[Chunk]:
        # Allow runtime override of splitter sizing
        if (chunk_size != self._splitter._chunk_size) or (overlap != self._splitter._chunk_overlap):
            self._splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=overlap,
                separators=["\n\n", "\n", ". ", " ", ""],
                length_function=len,
                is_separator_regex=False,
            )

        loader = self._resolve_loader(self.source_doc.source_url)
        pages: List[LCDocument] = loader.load()

        # 1) Clean & enrich page docs
        per_page_docs: List[LCDocument] = []
        for i, page in enumerate(pages):
            cleaned = self._clean_page_content(page.page_content)
            if not cleaned:
                continue

            page.page_content = cleaned
            md = dict(page.metadata or {})
            md["page_number"] = i + 1
            md["source"] = self.source_doc.source_url
            page.metadata = md
            per_page_docs.append(page)

        if not per_page_docs:
            return []

        # 2) Split page docs into semantic chunks
        all_chunks: List[LCDocument] = []
        for page_doc in per_page_docs:
            chunks = self._splitter.split_documents([page_doc])
            # Filter tiny scraps
            for c in chunks:
                if len(c.page_content) >= min_chunk_chars:
                    all_chunks.append(c)

        if not all_chunks:
            return []

        # 3) Embed
        contents = [d.page_content for d in all_chunks]
        vectors = await self.embedder.aembed_documents(contents)
        embedding_model = self.embedder.get_model_name()

        # 4) Build ODM chunk objects with stable chunk_ids and metadata
        chunk_odms: List[Chunk] = []
        subj_id = self._get_id_from(self.source_doc.subject)
        unit_id = self._get_id_from(self.source_doc.unit)

        # Stable per-page chunk indexing
        page_to_counter = {}

        for doc, vec in zip(all_chunks, vectors):
            page_num = int(doc.metadata.get("page_number", 0))
            page_to_counter.setdefault(page_num, 0)
            page_to_counter[page_num] += 1
            chunk_idx = page_to_counter[page_num]

            # Add robust metadata
            meta = dict(doc.metadata or {})
            meta["chunk_index_in_page"] = chunk_idx
            meta["chunk_id"] = f"{page_num}-{chunk_idx}"  # stable: page-chunk

            chunk = Chunk(
                document=self.source_doc,
                subject_id=subj_id,
                unit_id=unit_id,
                content=doc.page_content,
                vector_embedding=vec,
                embedding_model=embedding_model,
                metadata=meta,
            )
            chunk_odms.append(chunk)

        print(f"Created {len(chunk_odms)} clean chunks.")
        return chunk_odms
