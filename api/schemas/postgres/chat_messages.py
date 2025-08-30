from api.schemas.postgres import Column, DateTime, ForeignKey, Text, Enum, JSON, Integer, String
from api.schemas.postgres import relationship
from api.schemas.postgres import BASE
from datetime import datetime

class ChatMessage(BASE):
    __tablename__ = "chat_messages"
    __table_args__ = ({"schema": "ragapp"})

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("ragapp.chat_sessions.id"), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    chunks = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    user_metadata = Column(JSON, nullable=True)

    # Relationship: message belongs to a session
    chat_session = relationship("ChatSession", back_populates="messages")