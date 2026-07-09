"""
Conversation schemas.
"""

from datetime import datetime

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    """
    Create a new conversation.
    """

    title: str | None = None


class ConversationResponse(BaseModel):
    """
    Conversation response schema.
    """

    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }

class ConversationUpdate(BaseModel):
    """
    Rename an existing conversation.
    """

    title: str