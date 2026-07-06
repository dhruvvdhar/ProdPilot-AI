"""
Chat API endpoints.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.schemas.response import APIResponse
from app.services.chat.chat_service import (
    chat_service,
)
from fastapi.responses import StreamingResponse
import json

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=APIResponse[ChatResponse],
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Chat with ProdPilot AI.
    """

    try:

        response = chat_service.chat(
            db=db,
            conversation_id=request.conversation_id,
            question=request.question,
            current_user=current_user,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return APIResponse(
        message="Response generated successfully.",
        data=ChatResponse(
            answer=response["answer"],
            citations=response["citations"],
        ),
    )


@router.post("/stream")
def stream_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    def event_generator():

        try:

            for event in chat_service.stream_chat(
                db=db,
                conversation_id=request.conversation_id,
                question=request.question,
                current_user=current_user,
            ):

                yield (
                    f"event: {event['type']}\n"
                    f"data: {json.dumps(event['data'])}\n\n"
                )

            yield (
                "event: done\n"
                "data: complete\n\n"
            )

        except ValueError as e:

            raise HTTPException(
                status_code=400,
                detail=str(e),
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )