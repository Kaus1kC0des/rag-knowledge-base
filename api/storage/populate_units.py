import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.processors import DocumentProcessor
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from api.schemas.mongodb import Chunk, SourceDocument, Subject, Unit
from dotenv import load_dotenv
load_dotenv()


async def populate_chunks():
    client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    await init_beanie(
        client[os.getenv("MONGO_DB")],
        document_models=[
            Chunk,
            SourceDocument,
            Subject,
            Unit
        ]
    )

    all_documents = await SourceDocument.find_all().to_list()
    print(f"Found {len(all_documents)} documents in the database.")

    for document in all_documents:
        document.subject = await document.subject.fetch()
        document.unit = await document.unit.fetch()
        processor = DocumentProcessor(document)
        chunks = await processor.process_and_create_chunks(chunk_size=1000, overlap=200)
        if not chunks:
            print(f"No chunks created for document ID {document.id}. Skipping insertion.")
            continue
        try:
            await Chunk.insert_many(chunks)
            print(f"Inserted {len(chunks)} chunks for document ID {document.id}.")
        except Exception as e:
            print(f"Error inserting chunks for document ID {document.id}: {e}")

if __name__ == "__main__":
    asyncio.run(populate_chunks())