from fastapi import APIRouter, Depends, HTTPException
from api.models.session_models import (
    ChatSessionRequestModel, ChatSessionHistoryModel, ChatSessionResponseModel, ChatSessionCreationModel
)
from api.storage.postgres.chat_session_manager import (
    get_all_chat_sessions, create_chat_session, get_chat_session, delete_chat_session, delete_all_chat_sessions
)
from api.utils import authenticate_user, get_pg_db

router = APIRouter(
    prefix="/session",
    tags=["session"]
)

@router.post("/all_sessions", response_model=ChatSessionHistoryModel)
async def get_all_sessions(
    request_data: ChatSessionRequestModel,
    user=Depends(authenticate_user),
    pg_db=Depends(get_pg_db)
):
    """
    Retrieve all chat sessions for a user, subject, and unit.
    """
    try:
        sessions = get_all_chat_sessions(user.id, request_data.subject_id, request_data.unit_id, pg_db)
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create_session", response_model=ChatSessionResponseModel)
async def create_session(
    request_data: ChatSessionCreationModel,
    user=Depends(authenticate_user),
    pg_db=Depends(get_pg_db)
):
    """
    Create a new chat session for a user.
    """
    try:
        session = create_chat_session(user.id, request_data.subject_id, request_data.unit_id, pg_db, request_data.title)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{chat_id}", response_model=ChatSessionResponseModel)
async def get_session(
    chat_id: int,
    user=Depends(authenticate_user),
    pg_db=Depends(get_pg_db)
):
    """
    Retrieve a specific chat session by ID.
    """
    try:
        session = get_chat_session(user.id, chat_id, pg_db)
        return session
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/session/{chat_id}")
async def delete_session(
    chat_id: int,
    user=Depends(authenticate_user),
    pg_db=Depends(get_pg_db)
):
    """
    Delete a specific chat session by ID.
    """
    try:
        delete_chat_session(chat_id, pg_db)
        return {"detail": "Session deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/all_sessions")
async def delete_all_sessions(
    request_data: ChatSessionRequestModel,
    user=Depends(authenticate_user),
    pg_db=Depends(get_pg_db)
):
    """
    Delete all chat sessions for a user, subject, and unit.
    """
    try:
        delete_all_chat_sessions(user.id, request_data.subject_id, request_data.unit_id, pg_db)
        return {"detail": "All sessions deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
