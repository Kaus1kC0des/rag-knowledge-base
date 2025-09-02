from fastapi import APIRouter, Depends, HTTPException, Request
from api.utils import authenticate_user, get_pg_db, get_mongo_db
from api.utils import get_redis_db
from api.processors import QueryEmbedder
from api.models.chat_models import ChatRequestModel, ChatResponseModel
from api.schemas.mongodb.unit import Unit
from api.schemas.mongodb.subject import Subject
from beanie.operators import And
from api.loaders.data_retriever import get_vector_search_dependency
from api.models.ai_response_generator import get_ai_response_dependency
from api.storage.postgres.chat_session_manager import (
    get_all_chat_sessions, create_chat_session, get_chat_session, delete_chat_session, delete_all_chat_sessions
)
from api.storage.postgres import *
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/message")
async def chat_message(
    request_data: ChatRequestModel,
    user=Depends(authenticate_user),
    search_engine=Depends(get_vector_search_dependency),
    ai_generator=Depends(get_ai_response_dependency),
    pg_db=Depends(get_pg_db),
    mongo_db=Depends(get_mongo_db),
    query_embedder=Depends(QueryEmbedder)
):
    """Handle chat messages. Expect a ChatRequestModel (Pydantic) in the body."""
    try:
        # Validate subject and unit exist
        subject = await Subject.find_one(Subject.name == request_data.subject)
        if not subject:
            raise HTTPException(status_code=404, detail=f"Subject '{request_data.subject}' not found")
        specific_unit = await Unit.find_one(
            And(
                Unit.subject.id == subject.id,
                Unit.title == request_data.unit
            )
        )

        if not specific_unit:
            raise HTTPException(status_code=404, detail=f"Unit '{request_data.unit}' not found for subject '{request_data.subject}'")

        # Use filters to narrow search to specific subject/unit
        filters = {
            "subject_id": str(subject.id),
            "unit_id": str(specific_unit.id)
        }

        # Perform vector search with filters
        relevant_chunks = await search_engine.vector_search(
            query=request_data.message,
            filters=filters
        )
        
        metadata = defaultdict(list)
        for chunk in relevant_chunks:
            document = str(chunk.metadata.get("document").id)
            metadata[document].append(chunk.id)

        # Generate AI response using retrieved chunks
        if relevant_chunks:
            context_chunks = [
                {
                    "content": chunk.page_content,
                    "metadata": chunk.metadata,
                    "score": getattr(chunk, 'score', 0) if hasattr(chunk, 'score') else 0
                }
                for chunk in relevant_chunks
            ]

            ai_response = await ai_generator.generate_response(
                question=request_data.message,
                context_chunks=context_chunks,
                subject=request_data.subject,
                unit=request_data.unit
            )
            
            # Get or create chat session based on chat_id
            chat_session = None
            if request_data.chat_id:
                try:
                    # Try to get existing session
                    chat_session = get_chat_session(user.id, int(request_data.chat_id), pg_db)
                except:
                    # If session doesn't exist, create a new one
                    chat_session = create_chat_session(
                        user.id, 
                        str(subject.id), 
                        str(specific_unit.id), 
                        pg_db,
                        f"{request_data.subject} - {request_data.unit}"
                    )
            else:
                # Create new session if no chat_id provided
                chat_session = create_chat_session(
                    user.id, 
                    str(subject.id), 
                    str(specific_unit.id), 
                    pg_db,
                    f"{request_data.subject} - {request_data.unit}"
                )

            new_chat_message = create_message(
                id=chat_session.id,
                query=request_data.message,
                response=ai_response,
                chunks=[metadata],
                db=pg_db
            )
        else:
            ai_response = await ai_generator.generate_fallback_response(
                question=request_data.message,
                subject=request_data.subject,
                unit=request_data.unit,
                error_message="No relevant chunks found in vector search"
            )
            
            # Get or create chat session even when no chunks found
            chat_session = None
            if request_data.chat_id:
                try:
                    # Try to get existing session
                    chat_session = get_chat_session(user.id, int(request_data.chat_id), pg_db)
                except:
                    # If session doesn't exist, create a new one
                    chat_session = create_chat_session(
                        user.id, 
                        str(subject.id), 
                        str(specific_unit.id), 
                        pg_db,
                        f"{request_data.subject} - {request_data.unit}"
                    )
            else:
                # Create new session if no chat_id provided
                chat_session = create_chat_session(
                    user.id, 
                    str(subject.id), 
                    str(specific_unit.id), 
                    pg_db,
                    f"{request_data.subject} - {request_data.unit}"
                )

            new_chat_message = create_message(
                id=chat_session.id,
                query=request_data.message,
                response=ai_response,
                chunks=[],
                db=pg_db
            )

        return {
            "response": ai_response,
            "enhanced_processing": True,
            "user_id": user.id if hasattr(user, 'id') else None,
            "subject": request_data.subject,
            "unit": request_data.unit,
            "chunks_found": len(relevant_chunks),
            "chunks": metadata
        }

    except HTTPException:
        raise
    except Exception as e:
        # Return a controlled 500 error rather than raising arbitrary exceptions
        raise HTTPException(status_code=500, detail=str(e))
