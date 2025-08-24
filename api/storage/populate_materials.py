"""
Enhanced materials population using optimized schema.
Processes documents and stores them in Documents + Chunks collections.
"""

import asyncio
import os
from pathlib import Path
import sys

# Ensure top-level packages (loaders, processors, etc.) are on the import path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from api.loaders.gcs_loader import get_all_files_from_bucket
from api.processors import DocumentProcessor
from api.processors.chunkers import chunk_documents_by_character
from api.processors.vector_embedder import VectorEmbedder
from api.schemas import Documents, Chunks, Subjects, Units
from api.storage.database_manager import DatabaseManager
from api.storage.file_downloader import FileDownloader
from langchain_core.documents import Document


async def download_files_step():
    """Step 1: Download files from GCS"""
    downloader = FileDownloader(
        project_id=os.getenv("GCP_PROJECT_ID"),
        bucket_name=os.getenv("GCS_BUCKET_NAME")
    )
    return await downloader.download_files(get_all_files_from_bucket)


async def process_file_step(processor, file_path):
    """Step 2: Process file and extract content + metadata"""
    try:
        print(f"Processing {Path(file_path).parent.name}/{Path(file_path).name}...")
        return await processor.process_file(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None


async def create_chunks_step(doc_data, chunk_size=1000, chunk_overlap=200):
    """Step 3: Create document chunks using LangChain chunkers"""
    if not doc_data or not doc_data.get("content"):
        return []
    
    # Create LangChain Document object
    document = Document(
        page_content=doc_data["content"],
        metadata=doc_data["metadata"]
    )
    
    # Create chunks
    chunks = chunk_documents_by_character(
        [document],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    print(f"Created {len(chunks)} chunks from {len(doc_data['content'])} characters")
    return chunks


async def embed_chunks_step(embedder, chunks):
    """Step 4: Create vector embeddings for chunks"""
    if not chunks:
        return []
    
    # Extract text content from chunks
    chunk_texts = [chunk.page_content for chunk in chunks]
    
    # Generate embeddings
    embeddings = await embedder.embed_documents(chunk_texts)
    
    # Combine chunks with embeddings
    embedded_chunks = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        embedded_chunks.append({
            "chunk": chunk,
            "embedding": embedding,
            "chunk_index": i
        })
    
    print(f"Generated embeddings for {len(embedded_chunks)} chunks")
    return embedded_chunks


async def database_steps(db, file_path, gcs_url, doc_data, embedded_chunks):
    """Step 5: Store everything in the optimized database schema"""
    try:
        # Extract subject name from path
        path = Path(file_path)
        subject_name = path.parent.name
        
        # Get or create subject
        subject_id = await db.get_or_create_subject(name=subject_name)
        
        # Get or create unit
        unit_title = doc_data["metadata"].get("unit_title") or path.stem
        unit_id = await db.get_or_create_unit(
            subject_id=subject_id,
            title=unit_title,
            file_path=gcs_url,
            file_type=path.suffix.lower()
        )
        
        # Store document
        document = Documents(
            title=doc_data["title"],
            file_name=path.name,
            file_path=gcs_url,
            file_type=path.suffix.lower(),
            content=doc_data["content"],
            content_length=doc_data["content_length"],
            subject_id=subject_id,
            unit_id=unit_id,
            processing_engine=doc_data.get("processing_engine", "unknown"),
            processing_status="completed",
            metadata=doc_data["metadata"]
        )
        await document.save()
        
        print(f"Stored document: {document.id}")
        
        # Store chunks
        chunks_stored = 0
        for chunk_data in embedded_chunks:
            chunk = chunk_data["chunk"]
            embedding = chunk_data["embedding"]
            chunk_index = chunk_data["chunk_index"]
            
            # Create chunk document
            chunk_doc = Chunks(
                document_id=str(document.id),
                subject_id=subject_id,
                unit_id=unit_id,
                content=chunk.page_content,
                chunk_index=chunk_index,
                chunk_size=len(chunk.page_content),
                vector_embedding=embedding,
                vector_dimension=len(embedding),
                metadata={
                    **chunk.metadata,
                    "source_file": path.name,
                    "gcs_url": gcs_url
                }
            )
            await chunk_doc.save()
            chunks_stored += 1
        
        print(f"Stored {chunks_stored} chunks for document {document.id}")
        return chunks_stored
        
    except Exception as e:
        print(f"Database error for {file_path}: {e}")
        return 0


async def process_all_materials():
    """Main function to process all materials using optimized schema."""
    try:
        # Initialize components
        processor = DocumentProcessor()
        embedder = VectorEmbedder()
        db = DatabaseManager(
            os.getenv("MONGO_URL"), 
            [Documents, Chunks, Units, Subjects]
        )
        
        print("🚀 Enhanced Materials Processing with Optimized Schema")
        print("=" * 60)
        print("📊 New Schema: Documents + Chunks collections")
        print("🎯 Enhanced Processing: Content-core integration")
        print("🧩 Smart Chunking: LangChain chunkers")
        print("🔍 Vector Search: Optimized for similarity queries")
        print("=" * 60)
        
        print("\nStep 1: Initializing database...")
        await db.initialize()
        
        print("Step 2: Downloading files...")
        local_file_map = await download_files_step()
        
        total_files = len(local_file_map)
        successful_files = 0
        total_chunks = 0
        
        print(f"\n📁 Processing {total_files} files...")
        
        # Process each file step by step
        for local_path, gcs_url in local_file_map.items():
            try:
                print(f"\n🔄 Processing: {Path(local_path).name}")
                print("-" * 40)
                
                print("📄 Step 3: Extracting content and metadata...")
                doc_data = await process_file_step(processor, local_path)
                if not doc_data:
                    print("❌ Content extraction failed")
                    continue
                
                print(f"✅ Extracted: {doc_data['content_length']:,} characters")
                print(f"🎯 Engine: {doc_data.get('processing_engine', 'unknown')}")
                
                print("🧩 Step 4: Creating chunks...")
                chunks = await create_chunks_step(doc_data)
                if not chunks:
                    print("❌ No chunks created")
                    continue
                
                print("🎯 Step 5: Generating embeddings...")
                embedded_chunks = await embed_chunks_step(embedder, chunks)
                if not embedded_chunks:
                    print("❌ No embeddings created")
                    continue
                
                print("💾 Step 6: Storing in optimized database...")
                chunks_stored = await database_steps(
                    db, local_path, gcs_url, doc_data, embedded_chunks
                )
                
                if chunks_stored > 0:
                    successful_files += 1
                    total_chunks += chunks_stored
                    print(f"✅ Successfully processed: {chunks_stored} chunks stored")
                else:
                    print("❌ Failed to store chunks")
                
            except Exception as e:
                print(f"💥 Error processing {local_path}: {str(e)}")
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 PROCESSING COMPLETE!")
        print(f"📊 Files processed: {successful_files}/{total_files}")
        print(f"🧩 Total chunks stored: {total_chunks}")
        print(f"💾 Collections used: Documents + Chunks")
        print("🚀 Ready for vector search and RAG operations!")
        print("=" * 60)
        
    finally:
        print("\nStep 7: Cleaning up...")
        FileDownloader.cleanup()


if __name__ == "__main__":
    asyncio.run(process_all_materials())