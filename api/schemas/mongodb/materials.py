"""
Optimized MongoDB schemas for RAG systems.
Separates documents and chunks for better performance and scalability.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from beanie import Document, Indexed
from pydantic import Field


class Documents(Document):
    """Store original document content and metadata."""
    subject_id: str = Indexed(str)
    unit_id: str = Indexed(str)
    content: str = Field(description="Full document content")
    file_path: str = Field(description="Path to original file")
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "documents"
        indexes = [
            "subject_id",
            "unit_id",
            "file_type",
        ]


class Chunks(Document):
    """Store vectorized chunks for semantic search."""
    document_id: str = Indexed(str, description="Reference to Documents collection")
    subject_id: str = Indexed(str, description="Subject for quick filtering")
    unit_id: str = Indexed(str, description="Unit for quick filtering")
    content: str = Field(description="Chunk content text")
    chunk_index: int = Field(description="Position of chunk in document")
    chunk_size: int = Field(description="Character count of chunk")
    vector_embedding: List[float] = Field(description="Vector representation")
    vector_dimension: int = Field(description="Dimension of vector")
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "chunks"
        indexes = [
            "document_id",
            "subject_id",
            "unit_id",
            "chunk_index",
            "chunk_size"
        ]


class Subjects(Document):
    """Store subject information."""
    name: str = Indexed(str, unique=True)
    subject_id: str = Indexed(str, unique=True)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "subjects"


class Units(Document):
    """Store unit information."""
    subject_id: str = Indexed(str)
    title: str = Indexed(str)
    file_path: str
    file_type: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "units"
        indexes = [
            "subject_id",
            "title"
        ]


# Hybrid approach: Keep original Materials for backward compatibility
class Materials(Document):
    """Legacy Materials collection - for backward compatibility."""
    unit_id: str = Indexed(str)
    title: str
    content: str
    file_path: Optional[str] = None
    page_numbers: Optional[List[int]] = None
    vector_embedding: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, str]

    class Settings:
        name = "materials"
