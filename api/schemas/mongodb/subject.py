# schemas/subject.py

from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field


class Subject(Document):
    """
    Represents a top-level subject or course.

    Examples: 'Data Structures and Algorithms', 'Linear Algebra'
    """
    # Using a more descriptive name for the human-readable identifier.
    subject_code: Indexed(str, unique=True) = Field(
        ...,
        description="A unique code for the subject, e.g., 'CS201'."
    )

    name: str = Field(
        ...,
        description="The full, human-readable name of the subject."
    )

    description: Optional[str] = Field(
        None,
        description="A brief description of the subject."
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp of when the subject was created."
    )

    class Settings:
        name = "subjects"