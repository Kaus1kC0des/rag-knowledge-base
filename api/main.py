"""
FastAPI application for the RAG Knowledge Base API.
Integrates the enhanced document processor for comprehensive file support.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import tempfile
import os
from typing import List, Dict, Any

from api.processors import DocumentProcessor
from api.processors.chunkers import chunk_documents_by_character
from langchain_core.documents import Document


app = FastAPI(
    title="RAG Knowledge Base API",
    description="API for processing documents and creating knowledge bases",
    version="1.0.0"
)

# Initialize the enhanced document processor
processor = DocumentProcessor()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "RAG Knowledge Base API",
        "version": "1.0.0",
        "enhanced_processing": True
    }


@app.get("/capabilities")
async def get_capabilities():
    """Get processing capabilities and supported file types."""
    capabilities = processor.get_processing_capabilities()
    return {
        "enhanced_processor": True,
        "content_core_available": capabilities["content_core_available"],
        "supported_extensions": capabilities["supported_extensions"],
        "processing_engines": capabilities["processing_engines"]
    }


@app.post("/process-file")
async def process_file(
    file: UploadFile = File(...),
    chunk_size: int = 1000,
    chunk_overlap: int = 200
):
    """Process a single file and return extracted content with chunks."""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Process the file
            result = await processor.process_file(temp_file_path)
            
            if not result["success"]:
                raise HTTPException(
                    status_code=400, 
                    detail=f"File processing failed: {result.get('error', 'Unknown error')}"
                )
            
            # Create chunks if content is substantial
            chunks = []
            if result["content_length"] > chunk_size:
                document = Document(
                    page_content=result["content"],
                    metadata=result["metadata"]
                )
                chunks = chunk_documents_by_character(
                    [document],
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
                
                # Convert chunks to serializable format
                chunks_data = []
                for i, chunk in enumerate(chunks):
                    chunks_data.append({
                        "chunk_id": i,
                        "content": chunk.page_content,
                        "metadata": chunk.metadata
                    })
            else:
                chunks_data = [{
                    "chunk_id": 0,
                    "content": result["content"],
                    "metadata": result["metadata"]
                }]
            
            return {
                "success": True,
                "file_info": {
                    "filename": file.filename,
                    "file_type": result["file_type"],
                    "content_length": result["content_length"],
                    "processing_engine": result["processing_engine"]
                },
                "content": result["content"],
                "chunks": chunks_data,
                "total_chunks": len(chunks_data)
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.post("/process-multiple")
async def process_multiple_files(
    files: List[UploadFile] = File(...),
    max_concurrent: int = 3,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
):
    """Process multiple files concurrently."""
    try:
        # Save uploaded files temporarily
        temp_files = []
        try:
            for file in files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
                    content = await file.read()
                    temp_file.write(content)
                    temp_files.append((temp_file.name, file.filename))
            
            # Process files
            file_paths = [temp_path for temp_path, _ in temp_files]
            results = await processor.process_multiple_files(
                file_paths, 
                max_concurrent=max_concurrent
            )
            
            # Process results and create chunks
            processed_results = []
            for result in results:
                if result["success"]:
                    # Create chunks
                    document = Document(
                        page_content=result["content"],
                        metadata=result["metadata"]
                    )
                    chunks = chunk_documents_by_character(
                        [document],
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap
                    )
                    
                    chunks_data = []
                    for i, chunk in enumerate(chunks):
                        chunks_data.append({
                            "chunk_id": i,
                            "content": chunk.page_content,
                            "metadata": chunk.metadata
                        })
                    
                    processed_results.append({
                        "filename": result["file_path"],
                        "success": True,
                        "content_length": result["content_length"],
                        "processing_engine": result["processing_engine"],
                        "chunks": chunks_data,
                        "total_chunks": len(chunks_data)
                    })
                else:
                    processed_results.append({
                        "filename": result["file_path"],
                        "success": False,
                        "error": result.get("error", "Unknown error")
                    })
            
            return {
                "success": True,
                "total_files": len(files),
                "successful": sum(1 for r in processed_results if r["success"]),
                "failed": sum(1 for r in processed_results if not r["success"]),
                "results": processed_results
            }
            
        finally:
            # Clean up temporary files
            for temp_path, _ in temp_files:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "enhanced_processor": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
