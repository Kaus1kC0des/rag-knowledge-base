from api.schemas.postgres import Column, DateTime, ForeignKey, Text, Enum, JSON, UUID
from api.schemas.postgres import relationship
from api.schemas.postgres import BASE
from datetime import datetime
import uuid

class ChatMessage(BASE):
    __tablename__ = "chat_messages"
    __table_args__ = ({"schema": "ragApp"})

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("ragApp.chat_sessions.id"), nullable=False)
    sender = Column(Enum("user", "ai", name="sender_enum"), nullable=False)
    content = Column(Text, nullable=False)
    chunks = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    user_metadata = Column(JSON, nullable=True)

    # Relationship: message belongs to a session
    chat_session = relationship("ChatSession", back_populates="messages")