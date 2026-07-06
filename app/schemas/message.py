"""
Message schemas.
"""

from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    """
    Create message schema.
    """

    role: str
    content: str


class MessageResponse(BaseModel):
    """
    Message response schema.
    """

    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }