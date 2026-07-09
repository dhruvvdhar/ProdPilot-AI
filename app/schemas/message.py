"""
Message schemas.
"""

import json
from datetime import datetime

from pydantic import BaseModel, field_validator

from app.schemas.chat import Citation


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
    citations: list[Citation] = []

    model_config = {
        "from_attributes": True,
    }

    @field_validator("citations", mode="before")
    @classmethod
    def parse_citations(cls, value):
        """
        Citations are stored as a raw JSON string in the
        database column, so decode them here for the response.
        """

        if value is None:
            return []

        if isinstance(value, str):
            try:
                return json.loads(value)
            except (ValueError, TypeError):
                return []

        return value