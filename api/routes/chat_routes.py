from fastapi.exceptions import RequestValidationError

from api.routes import APIRouter, Depends
from fastapi import APIRouter
from api.utils import authenticate_user, get_pg_db, get_mongo_db
from api.schemas import *
from api.models import *
from api.models.chat_models import ChatRequestModel, ChatResponseModel
from api.schemas.mongodb.unit import Unit
from api.schemas.mongodb.subject import Subject
from beanie.operators import And
from api.loaders.data_retriever import get_vector_search_dependency
from api.models.ai_response_generator import get_ai_response_dependency  # NEW: AI response generator

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("/message")
async def chat_message(
    request_data: ChatRequestModel,
    user=Depends(authenticate_user),
    search_engine=Depends(get_vector_search_dependency),  # Vector search
    ai_generator=Depends(get_ai_response_dependency)      # NEW: AI response generator
):
    print(f"Received request: {request_data}")
    print(f"User: {user}")

    try:
        # Validate subject and unit exist
        subject = await Subject.find_one(Subject.name == request_data.subject)
        if not subject:
            return {
                "response": f"Sorry, I couldn't find information about '{request_data.subject}'",
                "enhanced_processing": True,
                "error": "Subject not found"
            }

        specific_unit = await Unit.find_one(
            And(
                Unit.subject.id == subject.id,
                Unit.title == request_data.unit
            )
        )

        if not specific_unit:
            return {
                "response": f"Sorry, I couldn't find '{request_data.unit}' for '{request_data.subject}'",
                "enhanced_processing": True,
                "error": "Unit not found"
            }

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

        print(f"Found {len(relevant_chunks)} relevant chunks")

        # 🎯 Generate AI response using retrieved chunks
        if relevant_chunks:
            # Convert LangChain documents to dictionaries for the generator
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
            # No chunks found - use fallback response
            ai_response = await ai_generator.generate_fallback_response(
                question=request_data.message,
                subject=request_data.subject,
                unit=request_data.unit,
                error_message="No relevant chunks found in vector search"
            )

        return {
            "response": ai_response,  # 🎯 AI-generated response instead of raw chunks
            "enhanced_processing": True,
            "user_id": user.id,
            "subject": request_data.subject,
            "unit": request_data.unit,
            "chunks_found": len(relevant_chunks),
            "chunks": [chunk.page_content for chunk in relevant_chunks[:3]]  # Keep for debugging
        }

    except Exception as e:
        return {
            "response": "Sorry, I encountered an error processing your request.",
            "enhanced_processing": False,
            "error": str(e)
        }