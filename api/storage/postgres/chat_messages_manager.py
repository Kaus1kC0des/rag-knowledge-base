from api.models import ChatResponseModel
from api.schemas.postgres import ChatMessage, ChatSession
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException
from typing import List, Dict, Any
from sqlalchemy.exc import NoReferenceError
import traceback

def create_message(id: int, query: str, response: str, chunks: List[Dict[str, Any]], db: Session, user_metadata = None) -> ChatMessage:
    try:

        new_message = ChatMessage(
            chat_id=id,
            query=query,
            response=response,
            chunks=chunks,
            user_metadata=user_metadata
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message
    except Exception as e:
        print(e)
        traceback.print_exc()

def get_messages_by_chat_id(chat_id: int, db: Session) -> List[ChatMessage]:
    try:
        all_messages = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(desc(ChatMessage.created_at)).all()
        if not all_messages:
            raise NoReferenceError("No messages found for this chat session")
        return all_messages
    except Exception as e:
        print(e)
        traceback.print_exc()