from api.models import ChatResponseModel
from api.schemas.postgres import ChatMessage, ChatSession
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException
from sqlalchemy.exc import NoReferenceError
import traceback

def create_message(chat_session: ChatSession, chat_response: ChatResponseModel, db: Session) -> ChatMessage:
    try:
        id = chat_session.id
        print(f"Recieved Session ID: {id}")

        new_message = ChatMessage(
            chat_id=id,
            query=chat_response.query,
            response=chat_response.response,
            chunks=chat_response.sources,
            user_metadata=chat_response.user_metadata
        )
        print(f"Creating new message: {new_message}")
        db.add(new_message)
        print("Added new message to session")
        db.commit()
        print("Committed new message to database")
        db.refresh(new_message)
        print(f"Refreshed new message: {new_message}")
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