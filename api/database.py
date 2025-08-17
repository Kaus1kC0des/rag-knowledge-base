import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from api.schemas import Subjects, Units, Materials
from dotenv import load_dotenv

import asyncio
load_dotenv()


async def init_db(
        mongodb_url: str = "mongodb://localhost:27017",
        db_name: str = "knowledge_base"
):
    client = AsyncIOMotorClient(mongodb_url)
    await init_beanie(
        database=client[db_name],
        document_models=[
            Subjects,
            Units,
            Materials
        ]
    )

    # Force creation of the Materials collection by inserting and then deleting a document
    test_material = Materials(
        unit_id="test_unit_id",
        title="Test Material",
        content="This is test content",
        file_path="/path/to/test.pdf"
    )
    await test_material.insert()
    await test_material.delete()

    print(f"Connected to MongoDB at {mongodb_url}, database: {db_name}")
    return client

if __name__ == "__main__":
    asyncio.run(init_db(os.getenv("MONGO_URL"), os.getenv("MONGO_DB")))