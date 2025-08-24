import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from beanie import init_beanie
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from api.schemas.mongodb import Subject

load_dotenv()

async def populate_subjects():
    # Initialize the database with Beanie
    client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
    await init_beanie(database=client[os.getenv("MONGO_DB")], document_models=[Subject])

    # Create subject documents using the Beanie model
    subjects = [
        Subject(name="Generative AI", subject_code="ML1705", description="Generative AI"),
        Subject(name="Edge AI", subject_code="ML1704", description="Edge AI"),
        Subject(name="Image Processing and Vision Techniques", subject_code="ML1703",
                description="Image Processing and Vision Techniques"),
        Subject(name="Statistical Natural Language Processing", subject_code="ML1701",
                description="Statistical NLP"),
        Subject(name="Speech Processing", subject_code="ML1722", description="Speech Processing"),
    ]

    # Insert all subjects
    inserted_count = 0
    for subject in subjects:
        try:
            await subject.insert()
            inserted_count += 1
        except Exception as e:
            print(f"Error inserting {subject.name}: {e}")

    print(f"Inserted {inserted_count} documents")

if __name__ == "__main__":
    asyncio.run(populate_subjects())