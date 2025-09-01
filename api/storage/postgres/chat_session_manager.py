from sqlalchemy.orm import Session
from sqlalchemy.exc import NoReferenceError
from api.schemas.postgres import ChatSession, ChatMessage
from sqlalchemy import desc
from api.models.session_models import ChatSessionResponseModel, ChatSessionHistoryModel
from api.models.chat_models import ChatResponseModel
from typing import List, Optional
from datetime import datetime

def _chat_message_to_pydantic(msg: ChatMessage) -> ChatResponseModel:
    return ChatResponseModel(
        query=msg.query,
        response=msg.response,
        sources=msg.chunks,
        chat_id=str(msg.chat_id),
        message_id=msg.id,
        user_metadata=msg.user_metadata
    )

def _chat_session_to_pydantic(session: ChatSession, db: Session) -> ChatSessionResponseModel:
    messages = db.query(ChatMessage).filter(ChatMessage.chat_id == session.id).order_by(desc(ChatMessage.created_at)).all()
    pydantic_messages = [_chat_message_to_pydantic(msg) for msg in messages]
    return ChatSessionResponseModel(
        id=session.id,
        subject_id=session.subject_id,
        unit_id=session.unit_id,
        title=session.title,
        messages=pydantic_messages,
        last_updated=session.updated_at.isoformat() if hasattr(session, 'updated_at') and session.updated_at else None
    )

def create_chat_session(user_id: str, subject_id: str, unit_id: str, db: Session, title: Optional[str] = None) -> ChatSessionResponseModel:
    """
    Create a new chat session for a user.

    Args:
        user_id (str): The ID of the user.
        subject_id: (str): The ID of the subject.
        unit_id: (str): The ID of the unit.
        db: (Session): The database session.
        title (str, optional): The title of the chat session. Defaults to None.
    """

    try:
        new_session = ChatSession(user_id=user_id, subject_id=subject_id, unit_id=unit_id, title=title)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return _chat_session_to_pydantic(new_session, db)
    except Exception as e:
        raise e

def get_all_chat_sessions(user_id: str, subject_id: str, unit_id: str, db: Session) -> ChatSessionHistoryModel:
    """
    Retrieve all chat sessions for a user.
    Args:
        user_id (str): The ID of the user.
        subject_id (str): The ID of the subject.
        unit_id (str): The ID of the unit.
        db (Session): The database session.
    """
    try:
        sessions = db.query(ChatSession).filter(
            ChatSession.user_id == user_id,
            ChatSession.subject_id == subject_id,
            ChatSession.unit_id == unit_id
        ).order_by(desc(ChatSession.updated_at)).all()
        pydantic_sessions = [_chat_session_to_pydantic(session, db) for session in sessions]
        return ChatSessionHistoryModel(sessions=pydantic_sessions)
    except Exception as e:
        raise e


def get_chat_session(user_id: str, chat_id: int, db: Session) -> ChatSessionResponseModel:
    """
    Retrieve all chat sessions for a user.
    Args:
        user_id (str): The ID of the user.
        chat_id: (str): The ID of the chat session.
        db (Session): The database session.
    """
    try:
        session = db.query(ChatSession).filter(
            ChatSession.user_id == user_id,
            ChatSession.id == chat_id
        ).first()
        if not session:
            raise NoReferenceError("No chat sessions found for this user")
        return _chat_session_to_pydantic(session, db)
    except Exception as e:
        raise e

def delete_chat_session(session_id: int, db: Session) -> None:
    """
    Delete a chat session and its associated messages.

    Args:
        session_id (int): The ID of the chat session to delete.
        db (Session): The database session.
    """
    try:
        # First, delete all messages associated with the chat session
        db.query(ChatMessage).filter(ChatMessage.chat_id == session_id).delete()
        # Then, delete the chat session itself
        deleted = db.query(ChatSession).filter(ChatSession.id == session_id).delete()
        if not deleted:
            raise NoReferenceError("Chat session not found")
        db.commit()
    except Exception as e:
        raise e


def delete_all_chat_sessions(user_id: str, subject_id: str, unit_id: str, db: Session) -> None:
    """
    Delete all chat sessions and their associated messages for a user.

    Args:
        user_id (str): The ID of the user.
        subject_id (str): The ID of the subject.
        unit_id (str): The ID of the unit.
        db (Session): The database session.
    """
    try:
        # First, retrieve all chat sessions for the user
        sessions = db.query(ChatSession).filter(
            ChatSession.user_id == user_id,
            ChatSession.subject_id == subject_id,
            ChatSession.unit_id == unit_id
        ).all()

        if not sessions:
            raise NoReferenceError("No chat sessions found for this user")

        # Collect all session IDs
        session_ids = [session.id for session in sessions]

        # Delete all messages associated with these chat sessions
        db.query(ChatMessage).filter(ChatMessage.chat_id.in_(session_ids)).delete(synchronize_session=False)

        # Then, delete the chat sessions themselves
        db.query(ChatSession).filter(ChatSession.id.in_(session_ids)).delete(synchronize_session=False)

        db.commit()
    except Exception as e:
        raise e