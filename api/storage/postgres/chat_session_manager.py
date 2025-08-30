from sqlalchemy.orm import Session
from sqlalchemy.exc import NoReferenceError
from api.schemas.postgres import ChatSession, ChatMessage
from sqlalchemy import desc

def create_chat_session(user_id: str, title: str, db: Session) -> ChatSession:
    """"
    Create a new chat session for a user.

    Args:
        user_id (str): The ID of the user.
        title (str): The title of the chat session.
        db (Session): The database session.
    """

    try:
        new_session = ChatSession(user_id=user_id, title=title)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session
    except Exception as e:
        raise e


def get_chat_session(user_id: str, db: Session) -> list[ChatSession]:
    """
    Retrieve all chat sessions for a user.
    Args:
        user_id (str): The ID of the user.
        db (Session): The database session.
    """
    try:
        sessions = db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(desc(ChatSession.updated_at)).all()
        if not sessions:
            raise NoReferenceError("No chat sessions found for this user")
        return sessions
    except Exception as e:
        raise e
