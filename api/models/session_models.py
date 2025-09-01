from .chat_models import ChatResponseModel
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatSessionCreationModel(BaseModel):
    """
    Model for creating a new chat session.
    """
    subject_id: str = Field(..., description="The ID of the subject for the chat session")
    unit_id: str = Field(..., description="The ID of the unit for the chat session")
    title: Optional[str] = Field(None, description="Optional title for the chat session")


class ChatSessionRequestModel(BaseModel):
    """
    Model for requesting chat sessions.
    """
    subject_id: str = Field(..., description="The ID of the subject for the chat session")
    unit_id: str = Field(..., description="The ID of the unit for the chat session")


class ChatSessionResponseModel(BaseModel):
    """
    Model for returning chat session details.
    """
    id: int = Field(..., description="The ID of the chat session")
    subject_id: str = Field(..., description="The ID of the subject for the chat session")
    unit_id: str = Field(..., description="The ID of the unit for the chat session")
    title: Optional[str] = Field(None, description="The title of the chat session")
    messages: List[ChatResponseModel] = Field(default_factory=list, description="List of messages in the chat session")
    last_updated: Optional[str] = Field(None, description="The timestamp of the last update to the chat session")


class ChatSessionHistoryModel(BaseModel):
    """
    Model to return all chat sessions for a user.
    """
    sessions: List[ChatSessionResponseModel] = Field(..., description="List of chat sessions for the user")
