from beanie import Document, Indexed
from pydantic import Field
from typing import Optional
from datetime import datetime

class Units(Document):
    subject_id: str = Indexed(str, unique=True)
    title: str = Indexed(str, unique=True)
    file_path: str = Field(description="Path or URL to the file")
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "units"  # Make sure this is a string, not a tuple
        indexes = [
            "subject_id",
            "title"
        ]