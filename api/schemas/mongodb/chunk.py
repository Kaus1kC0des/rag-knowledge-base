# schemas/chunk.py
from datetime import datetime
from typing import List, Dict, Any

from beanie import Document, Indexed, Link, PydanticObjectId
from pydantic import Field

from .source_document import SourceDocument


class Chunk(Document):
    """
    Stores a single chunk of text and its corresponding vector embedding.
    Optimized for vector similarity searches in MongoDB Atlas.
    """

    document: Link[SourceDocument]

    subject_id: str = Indexed(str)
    unit_id: str = Indexed(str)

    content: str = Field(
        ...,
        description="The text content of the chunk."
    )

    vector_embedding: List[float] = Field(
        ...,
        description="The vector representation of the chunk's content."
    )

    embedding_model: str = Field(
        ...,
        description="The name/version of the model used to generate the embedding."
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Flexible field for chunk-specific metadata (e.g., page number, chunk index)."
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "chunks"
        indexes = [
            "document",
            "subject_id",
            "unit_id"
        ]
        # NOTE: Vector index must be created manually in Atlas.
