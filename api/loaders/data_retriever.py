import os
import asyncio
from typing import Optional, Dict, Any, AsyncGenerator
from contextlib import asynccontextmanager

from pymongo import MongoClient  # Changed from motor to pymongo
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_mongodb.retrievers import MongoDBAtlasHybridSearchRetriever
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from dotenv import load_dotenv

load_dotenv()

class MongoVectorSearchEngine:
    def __init__(self):
        # Use pymongo client (not async motor)
        self.client: MongoClient = MongoClient(os.getenv("MONGO_URL"))
        self.database = self.client.get_database(os.getenv("MONGO_DB"))
        self.collection = self.database["chunks"]
        
        # Initialize embedding model
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model=os.getenv("EMBEDDING_MODEL", "models/embedding-001"),
            task_type="retrieval_query",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Initialize vector store (will be set in initialize())
        self.vector_store = None
        self.hybrid_retriever = None

    async def initialize(self):
        """Async initialization of vector store and retriever."""
        try:
            # Note: Beanie models are initialized in main.py lifespan
            # Use pymongo collection object directly
            self.vector_store = MongoDBAtlasVectorSearch(
                collection=self.collection,  # Pass pymongo collection object
                embedding=self.embedding_model,
                index_name="chunks_hybrid_index",
                text_key="content",
                embedding_key="vector_embedding",
                dimensions=3072,
            )

            self.hybrid_retriever = MongoDBAtlasHybridSearchRetriever(
                vectorstore=self.vector_store,
                search_index_name="chunk_search_index",
                k=5,
                vector_weight=0.7,
                fulltext_weight=0.3,
                top_k=5
            )
            
            print("✅ MongoDB Vector Search Engine initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize MongoDB Vector Search Engine: {e}")
            raise

    async def hybrid_search(self, query: str, k: int = 5, filters: Optional[Dict[str, Any]] = None):
        """Perform hybrid search using the retriever."""
        if not self.hybrid_retriever:
            raise RuntimeError("Retriever not initialized. Call initialize() first.")
        
        return await self.hybrid_retriever.ainvoke(query, filters=filters)

    async def vector_search(self, query: str, filters: Optional[Dict[str, Any]] = None):
        """Perform vector search using the vector store."""
        if not self.vector_store:
            raise RuntimeError("Vector store not initialized. Call initialize() first.")
        
        return await self.vector_store.asimilarity_search(query, pre_filter=filters)

    async def close(self):
        """Close the MongoDB client connection."""
        if self.client:
            self.client.close()
            print("🔌 MongoDB connection closed")# Global instance for singleton pattern with thread safety
_retriever_instance: Optional[MongoVectorSearchEngine] = None
_retriever_lock = asyncio.Lock()

@asynccontextmanager
async def get_vector_search_engine() -> AsyncGenerator[MongoVectorSearchEngine, None]:
    """FastAPI dependency that provides the vector search engine with thread safety."""
    global _retriever_instance
    
    async with _retriever_lock:
        if _retriever_instance is None:
            _retriever_instance = MongoVectorSearchEngine()
            await _retriever_instance.initialize()
    
    try:
        yield _retriever_instance
    finally:
        # Singleton doesn't close per request - keep connection alive
        pass

# Optional: Cleanup function for app shutdown
async def cleanup_vector_search_engine():
    """Call this during app shutdown to properly close connections."""
    global _retriever_instance
    if _retriever_instance:
        await _retriever_instance.close()
        _retriever_instance = None

async def get_vector_search_engine():
    """Simple async function to get the vector search engine instance."""
    global _retriever_instance
    
    async with _retriever_lock:
        if _retriever_instance is None:
            _retriever_instance = MongoVectorSearchEngine()
            await _retriever_instance.initialize()
    
    return _retriever_instance

# FastAPI Dependency Function
async def get_vector_search_dependency() -> MongoVectorSearchEngine:
    """FastAPI dependency that provides the vector search engine."""
    return await get_vector_search_engine()