from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

from beanie import Document, Link, PydanticObjectId
from pydantic import Field, model_validator

from .subject import Subject
from .unit import Unit


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class SourceDocument(Document):
    subject: Link[Subject]
    unit: Link[Unit]

    source_url: str = Field(..., description="URL of the source document")

    file_type: str = Field(description="MIME type of the file (e.g., application/pdf)", default="application/pdf")

    processing_status: ProcessingStatus = Field(description="Current processing status of the document", default=ProcessingStatus.PENDING)

    metadata: Optional[Dict[str, Any]] = Field(description="Additional metadata about the document", default_factory=dict)

    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the document was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the document was last updated")

    @model_validator(mode="before")
    def set_updated_at(cls, values):
        values['updated_at'] = datetime.utcnow()
        return values

    class Settings:
        name="source_documents"
        indexes = [
            "subject",
            "unit",
            "processing_status"
        ]
