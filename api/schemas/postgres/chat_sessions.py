from api.schemas.postgres import Column, DateTime, ForeignKey, String, UUID
from api.schemas.postgres import relationship
from api.schemas.postgres import BASE
from datetime import datetime
import uuid

class ChatSession(BASE):
    __tablename__ = "chat_sessions"
    __table_args__ = ({"schema": "ragApp"})

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(String, ForeignKey("ragApp.users.id"), nullable=False, index=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship("Users", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="chat_session", cascade="all, delete-orphan")