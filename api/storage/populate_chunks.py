import asyncio
import os
import sys
import time

from torch.onnx.symbolic_opset9 import addcmul

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

    all_source_docs = await SourceDocument.find_all().to_list()
    for doc in all_source_docs:
        await asyncio.gather(doc.fetch_all_links())

        print(f"Doc: {doc.subject.id}")


if __name__ == "__main__":
    asyncio.run(populate_chunks())