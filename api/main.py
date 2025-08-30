from api.models import UserModel, UserModelOutput, UserEditModel
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import tempfile
import os
from typing import List, Dict, Any
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from api.loaders.data_retriever import get_vector_search_engine
from api.routes.chat_routes import router as chat_router

# Global retriever instance
_retriever = None

# Lifespan context manager for modern FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    global _retriever
    try:
        # Startup: Initialize Beanie models first
        from motor.motor_asyncio import AsyncIOMotorClient
        from beanie import init_beanie
        from api.schemas.mongodb.chunk import Chunk
        from api.schemas.mongodb.subject import Subject
        from api.schemas.mongodb.unit import Unit
        from api.schemas.mongodb.source_document import SourceDocument
        
        mongo_url = os.getenv("MONGO_URL")
        db_name = os.getenv("MONGO_DB")
        
        # Initialize Beanie with async motor client
        mongo_client = AsyncIOMotorClient(mongo_url)
        mongo_db = mongo_client[db_name]
        
        await init_beanie(
            database=mongo_db,
            document_models=[Chunk, Subject, Unit, SourceDocument]
        )
        print("✅ Beanie models initialized")
        
        # Then initialize data retriever
        from api.loaders.data_retriever import MongoVectorSearchEngine
        _retriever = MongoVectorSearchEngine()
        await _retriever.initialize()
        print("🚀 Data retriever initialized on startup")
        
        # Initialize AI response generator
        from api.models.ai_response_generator import GeminiResponseGenerator
        _ai_generator = GeminiResponseGenerator()
        await _ai_generator.initialize()
        print("🤖 AI Response Generator initialized on startup")
        
        yield
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        raise e
    finally:
        # Shutdown: Cleanup if needed
        if _retriever:
            await _retriever.close()
        print("🔄 Application shutdown complete")

app = FastAPI(
    title="RAG Knowledge Base API",
    description="API for processing documents and creating knowledge bases",
    version="1.0.0",
    lifespan=lifespan  # Use modern lifespan instead of deprecated on_event
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat routes
app.include_router(router=chat_router)
        

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # Handle the body properly - it might be bytes
    body_content = exc.body
    if isinstance(exc.body, bytes):
        try:
            body_content = exc.body.decode('utf-8')
        except:
            body_content = str(exc.body)
    
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": body_content},
    )

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "RAG Knowledge Base API",
        "version": "1.0.0",
        "enhanced_processing": True
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "enhanced_processor": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
