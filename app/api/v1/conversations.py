"""
Conversation endpoints.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    ConversationUpdate,
)
from app.schemas.message import MessageResponse
from app.crud.message import get_messages_by_conversation
from app.services.conversation.conversation_service import (
    conversation_service,
)
from app.api.dependencies import get_current_user


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new conversation.
    """

    return conversation_service.create(
        db=db,
        current_user=current_user,
        title=request.title,
    )


@router.get(
    "",
    response_model=list[ConversationResponse],
)
def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all conversations.
    """

    return conversation_service.list(
        db,
        current_user,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve one conversation.
    """

    conversation = conversation_service.get(
        db,
        conversation_id,
        current_user,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return conversation



@router.patch(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def rename_conversation(
    conversation_id: int,
    request: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Rename a conversation.
    """

    conversation = conversation_service.get(
        db,
        conversation_id,
        current_user,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    try:
        return conversation_service.rename(
            db,
            conversation,
            request.title,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )



@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def list_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve every message belonging to a conversation
    owned by the current user, ordered oldest to newest.
    """

    conversation = conversation_service.get(
        db,
        conversation_id,
        current_user,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return get_messages_by_conversation(
        db,
        conversation_id,
    )


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a conversation.
    """

    conversation = conversation_service.get(
        db,
        conversation_id,
        current_user,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    conversation_service.delete(
        db,
        conversation,
    )