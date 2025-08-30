from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequestModel(BaseModel):
    message: str = Field(..., description="The user message for the chat")
    chat_id: str = Field(..., description="The ID of the chat session")
    subject: str = Field(..., description="The subject of the chat message")
    unit: str = Field(..., description="The unit associated with the chat message")
    timestamp: str = Field(..., description="The timestamp of the message")


class ChatResponseModel(BaseModel):
    query: str = Field(..., description="The original user message")
    response: str = Field(..., description="The AI-generated response to the chat message")
    sources: Optional[List[Dict[str, Any]]] = Field(None, description="List of sources used for generating the response")
    chat_id: Optional[str] = Field(None, description="The ID of the chat session")
    message_id: Optional[int] = Field(None, description="The ID of the chat message")
    user_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the user")