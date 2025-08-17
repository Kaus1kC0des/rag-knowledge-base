from beanie import Document, Indexed
from pydantic import Field
from typing import Optional

from datetime import datetime

class Subjects(Document):
    name: Indexed(str, unique=True) = Field(description="Name of the Subject")
    subject_id: Indexed(str, unique=True) = Field(description="Subject ID")
    description: Optional[str] = Field(None, description="Description of the Subject")
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "subjects"
        indexes = [
            "name",
            "subject_id"
        ]