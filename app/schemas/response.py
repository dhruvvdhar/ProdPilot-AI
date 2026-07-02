"""
Standard API response schemas.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    Standard success response.
    """

    success: bool = True
    message: str
    data: T | None = None


class ErrorResponse(BaseModel):
    """
    Standard error response.
    """

    success: bool = False
    message: str