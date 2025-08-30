from api.schemas.postgres import Column, DateTime, ForeignKey, String, Integer
from api.schemas.postgres import relationship
from api.schemas.postgres import BASE
from datetime import datetime

class ChatSession(BASE):
    __tablename__ = "chat_sessions"
    __table_args__ = ({"schema": "ragApp"})

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Removed user relationship - using Clerk user IDs directly
    messages = relationship("ChatMessage", back_populates="chat_session", cascade="all, delete-orphan")