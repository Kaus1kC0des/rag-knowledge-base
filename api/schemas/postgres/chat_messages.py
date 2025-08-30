from api.schemas.postgres import Column, DateTime, ForeignKey, Text, Enum, JSON, Integer
from api.schemas.postgres import relationship
from api.schemas.postgres import BASE
from datetime import datetime

class ChatMessage(BASE):
    __tablename__ = "chat_messages"
    __table_args__ = ({"schema": "ragApp"})

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("ragApp.chat_sessions.id"), nullable=False)
    sender = Column(Enum("user", "ai", name="sender_enum"), nullable=False)
    content = Column(Text, nullable=False)
    chunks = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    user_metadata = Column(JSON, nullable=True)

    # Relationship: message belongs to a session
    chat_session = relationship("ChatSession", back_populates="messages")