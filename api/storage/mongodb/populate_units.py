import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.schemas.mongodb import Subject, Unit
from api.loaders.gcs_loader import get_all_files_from_bucket
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv()

def get_order_index(name: str) -> int:
    # Extract number from "Unit X: Title"
    try:
        parts = name.split(".")[0].split(" ")
        if len(parts) > 1 and parts[0].lower() == "unit":
            return int(parts[1])
    except ValueError:
        pass
    return 0

async def populate_units():
    client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    await init_beanie(
        client[os.getenv("MONGO_DB")],
        document_models=[
            Subject,
            Unit
        ]
    )
    file_paths = get_all_files_from_bucket(
        os.getenv("GCS_BUCKET_NAME"),
        os.getenv("GCP_PROJECT_ID")
    )
    for file, public_url in file_paths.items():
        subject_name, unit_name = file.split('/')
        order_index = get_order_index(unit_name)
        subject_doc = await Subject.find_one(Subject.name == subject_name)
        if not subject_doc:
            print("No subject found for", subject_name)
        else:
            existing_unit = await Unit.find_one(
                Unit.subject.id == subject_doc.id,
                Unit.title == unit_name
            )
            if existing_unit:
                print(f"Unit '{unit_name}' already exists under subject '{subject_name}'. Skipping.")
                continue
            unit_doc = Unit(
                subject=subject_doc,
                title=unit_name,
                description=f"Auto-generated unit for {unit_name} under subject {subject_name}.",
                order_index=order_index
            )
            try:
                await unit_doc.insert()
                print(f"Inserted unit '{unit_name}' under subject '{subject_name}'.")
            except Exception as e:
                print(f"Error inserting unit '{unit_name}': {e}")


if __name__ == "__main__":
    asyncio.run(populate_units())