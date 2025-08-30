from fastapi import APIRouter, Depends, HTTPException, Request
from api.utils import authenticate_user
from api.schemas import *
from api.models import *
from api.models.chat_models import ChatRequestModel, ChatResponseModel
from api.schemas.mongodb.unit import Unit
from api.schemas.mongodb.subject import Subject
from beanie.operators import And
from api.loaders.data_retriever import get_vector_search_dependency
from api.models.ai_response_generator import get_ai_response_dependency  # AI response generator

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/message")
async def chat_message(
    request_data: ChatRequestModel,
    user=Depends(authenticate_user),
    search_engine=Depends(get_vector_search_dependency),  # Vector search
    ai_generator=Depends(get_ai_response_dependency)      # AI response generator
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
        else:
            ai_response = await ai_generator.generate_fallback_response(
                question=request_data.message,
                subject=request_data.subject,
                unit=request_data.unit,
                error_message="No relevant chunks found in vector search"
            )

        return {
            "response": ai_response,
            "enhanced_processing": True,
            "user_id": user.id if hasattr(user, 'id') else None,
            "subject": request_data.subject,
            "unit": request_data.unit,
            "chunks_found": len(relevant_chunks),
            "chunks": [chunk.page_content for chunk in relevant_chunks[:3]]
        }

    except HTTPException:
        raise
    except Exception as e:
        # Return a controlled 500 error rather than raising arbitrary exceptions
        raise HTTPException(status_code=500, detail=str(e))
