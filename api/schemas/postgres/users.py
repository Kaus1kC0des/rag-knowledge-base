from api.schemas.postgres import Column, DateTime, ForeignKey, Text, Enum, JSON, String
from api.schemas.postgres import relationship
from api.schemas.postgres import BASE
from datetime import datetime


class Users(BASE):
    __tablename__ = "users"
    __table_args__ = ({"schema": "ragApp"})

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)