from beanie import Document, Indexed
from pydantic import Field
from typing import Optional, List
from datetime import datetime

class Materials(Document):
    unit_id: str = Indexed(str)  # Reference to the Units collection
    title: str = Field(description="Title of the material")
    content: str = Field(description="Extracted text content from PDF")
    file_path: Optional[str] = Field(description="Original PDF file path")
    page_numbers: Optional[List[int]] = None
    vector_embedding: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "materials"