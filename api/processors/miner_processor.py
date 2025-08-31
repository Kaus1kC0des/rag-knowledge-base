import subprocess
import requests
from tempfile import NamedTemporaryFile
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document as LCDocument
from api.schemas.mongodb import SourceDocument, Chunk
from api.processors.vector_embedder import ChunkEmbedder
from beanie import Link

class MinerProcessor:
    """
    Rewritten to use MinerU for PDF parsing instead of TextNormalizer and BoilerplateStripper.
    This version:
      1) Downloads PDF if URL is given.
      2) Runs MinerU via subprocess to produce Markdown.
      3) Loads with UnstructuredMarkdownLoader.
      4) Chunks, embeds, and returns Chunk objects.
    """

    def __init__(self, source_doc: SourceDocument):
        self.source_doc = source_doc
        self.embedder = ChunkEmbedder()
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=180,
            separators=["\n\n", "\n", ". \n\n"],
            length_function=len,
            is_separator_regex=False,
        )

    def _download_pdf(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        with NamedTemporaryFile(mode="w+b", suffix=".pdf", delete=False) as tmp:
            tmp.write(response.content)
            tmp.flush()
            return tmp.name

    def _run_mineru(self, input_pdf_path: str) -> str:
        command = [
            "mineru",
            "-p", input_pdf_path,
            "-o", "tmp_output",
            "-m", "auto",
            "-b", "pipeline"
        ]
        subprocess.run(command, check=True)
        base = input_pdf_path.split("/")[-1].split(".")[0]
        return f"tmp_output/{base}/auto/{base}.md"

    async def process_and_create_chunks(
        self,
        chunk_size: int = 1000,
        overlap: int = 180,
        min_chunk_chars: int = 200,
    ) -> List[Chunk]:

        # Adjust splitter if custom chunk size is passed
        if chunk_size != self._splitter._chunk_size or overlap != self._splitter._chunk_overlap:
            self._splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=overlap,
                separators=["\n\n", "\n", ". ", " ", ""],
                length_function=len,
                is_separator_regex=False,
            )

        # Download PDF if needed
        pdf_path = self.source_doc.source_url
        if pdf_path.startswith("http://") or pdf_path.startswith("https://"):
            pdf_path = self._download_pdf(pdf_path)

        # Process PDF with MinerU
        md_path = self._run_mineru(pdf_path)
        loader = UnstructuredMarkdownLoader(md_path)
        pages: List[LCDocument] = loader.load()

        if not pages:
            return []

        # Split into chunks
        all_chunks: List[LCDocument] = []
        for page in pages:
            docs = self._splitter.split_documents([page])
            all_chunks.extend([d for d in docs if len(d.page_content) >= min_chunk_chars])

        if not all_chunks:
            return []

        # Embed chunks
        contents = [d.page_content for d in all_chunks]
        vectors = await self.embedder.aembed_documents(contents)
        embedding_model = self.embedder.get_model_name()

        subj_id = str(getattr(self.source_doc.subject, "id", None))
        unit_id = str(getattr(self.source_doc.unit, "id", None))

        # Build Chunk objects
        chunk_odms: List[Chunk] = []
        page_to_counter = {}
        for doc, vec in zip(all_chunks, vectors):
            page_num = int(doc.metadata.get("page_number", 0))
            page_to_counter.setdefault(page_num, 0)
            page_to_counter[page_num] += 1
            chunk_idx = page_to_counter[page_num]
            doc.metadata['source'] = self.source_doc.source_url
            meta = dict(doc.metadata or {})
            meta["chunk_index_in_page"] = chunk_idx
            meta["chunk_id"] = f"{page_num}-{chunk_idx}"

            chunk_odms.append(Chunk(
                document=self.source_doc,
                subject_id=subj_id,
                unit_id=unit_id,
                content=doc.page_content,
                vector_embedding=vec,
                embedding_model=embedding_model,
                metadata=meta,
            ))

        print(f"Created {len(chunk_odms)} chunks via MinerU.")
        return chunk_odms
