import os
import re
import sys
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document as LangchainDocument

from api.schemas.mongodb import SourceDocument, Chunk
from .vector_embedder import ChunkEmbedder


class DocumentProcessor:
    def __init__(self, source_doc: SourceDocument):
        self.source_doc = source_doc
        # The processor now owns the embedder
        self.embedder = ChunkEmbedder()

    def _clean_page_content(self, text: str) -> str:
        # ... (cleaning logic remains the same) ...
        text = re.sub(r"St\. Joseph’s College of Engineering\s+\d+\s+Dept of AML", "", text, flags=re.IGNORECASE)
        text = re.sub(r"ML\d{4}\s+[A-Za-z0-9\s\-:]+?\s+\d{4}-\d{4}\s+Unit[-\s]?[IVXLC]+\s+Class Notes", "", text,
                      flags=re.IGNORECASE)
        text = re.sub(r"\n{2,}", "\n", text)
        text = re.sub(r"\s{2,}", " ", text)
        return text.strip()

    async def process_and_create_chunks(
            self,
            chunk_size: int = 800,
            overlap: int = 100
    ) -> List[Chunk]:
        """
        Loads a PDF, cleans it, splits it, embeds it, and returns a list of
        Chunk ODM objects ready for database insertion.
        """
        loader = PyPDFLoader(self.source_doc.source_url)
        pages: List[LangchainDocument] = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)

        all_langchain_chunks: List[LangchainDocument] = []
        for i, page in enumerate(pages):
            cleaned_text = self._clean_page_content(page.page_content)
            if not cleaned_text:
                continue  # Skip empty pages

            page.page_content = cleaned_text
            page.metadata["page_number"] = i + 1

            # Use the original source document's URL in the metadata
            page.metadata["source"] = self.source_doc.source_url

            chunks = splitter.split_documents([page])
            all_langchain_chunks.extend(chunks)

        if not all_langchain_chunks:
            return []

        # 1. Extract content to pass to the embedder
        all_content = [doc .page_content for doc in all_langchain_chunks]

        # 2. Get vectors from our dedicated embedder class
        all_vectors = await self.embedder.aembed_documents(all_content)

        # 3. Create the final list of Chunk ODMs
        chunk_odm_list: List[Chunk] = []
        embedding_model = self.embedder.get_model_name()
        for i, doc in enumerate(all_langchain_chunks):
            chunk = Chunk(
                document=self.source_doc,
                subject_id=self.source_doc.subject.id,
                unit_id=self.source_doc.unit.id,
                content=doc.page_content,
                vector_embedding=all_vectors[i],
                embedding_model=embedding_model,
                metadata=doc.metadata,
            )
            chunk_odm_list.append(chunk)

        print(f"Created {len(chunk_odm_list)} Chunk ODM objects.")
        return chunk_odm_list