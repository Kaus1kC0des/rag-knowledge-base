from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
import os
from api.schemas.mongodb.chunk import Chunk
from api.schemas.mongodb.materials import Materials
from api.schemas.mongodb.source_document import SourceDocument
from api.schemas.mongodb.subject import Subject
from api.schemas.mongodb.unit import Unit

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

async def get_mongo_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        client[os.getenv("MONGO_DB")],
        document_models=[Chunk, Materials, SourceDocument, Subject, Unit]
    )
    try:
        yield client.get_database(os.getenv("MONGO_DB"))
    finally:
        client.close()
