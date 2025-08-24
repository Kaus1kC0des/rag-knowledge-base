# schemas/unit.py

from datetime import datetime
from typing import Optional

from beanie import Document, Indexed, Link, PydanticObjectId
from pydantic import Field, model_validator
from pymongo import IndexModel

from .subject import Subject


class Unit(Document):
    """
    Represents a unit, chapter, or module within a Subject.
    e.g., "Unit 1: Search Algorithms"
    """

    subject: Link[Subject]

    title: str = Field(
        ...,
        description="The title of the unit.",
        max_length=250
    )

    description: Optional[str] = Field(
        None,
        description="A brief description of the unit's content.",
        max_length=1000
    )

    order_index: int = Field(default=0, description="Order of the unit within the subject.")

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "units"
        indexes = [
            IndexModel([("subject", 1), ("title", 1)], unique=True)
        ]