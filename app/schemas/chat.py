"""
Chat request/response schemas.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Incoming chat request.
    """

    conversation_id: int
    question: str


class Citation(BaseModel):
    """
    Citation for an answer.
    """

    filename: str
    page: int | None = None


class ChatResponse(BaseModel):
    """
    Chat response.
    """

    answer: str
    citations: list[Citation]