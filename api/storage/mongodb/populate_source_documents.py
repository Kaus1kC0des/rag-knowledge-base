import asyncio
import os
import sys
import re

from beanie import init_beanie
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from api.schemas.mongodb import Subject, Unit, SourceDocument
from api.loaders.gcs_loader import get_all_files_from_bucket

load_dotenv()


def extract_unit_number(filename):
    """Extract unit number from filename like 'Unit 1.pdf', 'UNIT I.pdf', etc."""
    # Remove .pdf extension first
    name_without_ext = filename.replace('.pdf', '')

    # Try to find numbers in the filename
    numbers = re.findall(r'\d+', name_without_ext)
    if numbers:
        return int(numbers[0])

    # Handle Roman numerals (I, II, III, etc.)
    roman_match = re.search(r'\b(I{1,3}|IV|V|VI{0,3}|IX|X)\b', name_without_ext)
    if roman_match:
        roman_to_int = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
        return roman_to_int.get(roman_match.group(1), 1)

    # Default fallback
    return 1


async def populate_units():
    client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    await init_beanie(database=client[os.getenv("MONGO_DB")], document_models=[Unit, Subject, SourceDocument])

    # First, let's see what subjects are actually in the database
    all_subjects = await Subject.find_all().to_list()
    print("Subjects in database:")
    for subject in all_subjects:
        print(f"  - '{subject.name}'")
    print()

    file_names = get_all_files_from_bucket(os.getenv("GCS_BUCKET_NAME"), os.getenv("GCP_PROJECT_ID"))

    for file_name, public_url in file_names.items():
        subject_name = file_name.split("/")[0].strip()
        title = file_name.split("/")[1]

        print(f"Looking for subject: '{subject_name}'")

        subject_doc = await Subject.find_one(Subject.name == subject_name)
        if not subject_doc:
            # If exact match fails, try case-insensitive search
            subject_doc = await Subject.find_one(Subject.name.regex(f'^{re.escape(subject_name)}$', flags=re.IGNORECASE))
        if not subject_doc:
            print(f"Subject {subject_name} not found in DB. Skipping {title}.")
            continue
        else:
            print(f"Subject Found: '{subject_doc.name}'")
            unit_doc = await Unit.find_one(Unit.title == title and Unit.subject.id == subject_doc.id)
            if unit_doc:
                print(f"Subject: {subject_name} | Unit: {unit_doc.title}")
                source_doc = SourceDocument(
                    subject=subject_doc,
                    unit=unit_doc,
                    source_url=public_url,
                    file_type="application/pdf",
                    processing_status="pending"
                )
                try:
                    await source_doc.insert()
                    source_doc.save()
                    print(f"Inserted SourceDocument for '{title}' under subject '{subject_name}'")
                except Exception as e:
                    print(f"Error inserting SourceDocument for '{title}': {e}")
            else:
                print(f"Unit '{title}' under subject '{subject_name}' not found")

    client.close()


if __name__ == "__main__":
    asyncio.run(populate_units())