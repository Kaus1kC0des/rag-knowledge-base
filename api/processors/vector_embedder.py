import os
from typing import List

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from lazy_object_proxy.utils import await_


class ChunkEmbedder:
    """
    A dedicated class for creating vector embeddings from text.
    """

    def __init__(self, model_name: str = "models/embedding-001"):
        """Initializes the VectorEmbedder with a specified embedding model."""
        self.model_name = model_name
        self.embedder = GoogleGenerativeAIEmbeddings(
            model=self.model_name,
            task_type="RETRIEVAL_DOCUMENT",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        print(f"VectorEmbedder initialized with model: {self.model_name}")

    def get_model_name(self) -> str:
        """Returns the name of the embedding model being used."""
        return self.model_name

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Takes a list of texts and returns a list of vector embeddings.

        Args:
            texts: A list of string content to embed.

        Returns:
            A list of vector embeddings.
        """
        if not texts:
            return []

        print(f"Embedding {len(texts)} chunks of text...")
        vectors = await self.embedder.aembed_documents(texts)
        print("Embedding complete.")
        return vectors



class QueryEmbedder():
    def __init__(self):
        self.model = GoogleGenerativeAIEmbeddings(
            model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"),
            task_type="RETRIEVAL_QUERY",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    async def embed_query(self, query: str) -> List[float]:
        """
        Takes a single query string and returns its vector embedding.

        Args:
            query: A single string query to embed.

        Returns:
            A vector embedding.
        """
        if not query:
            return []

        vector = await self.embedder.aembed_query(query)
        return vector