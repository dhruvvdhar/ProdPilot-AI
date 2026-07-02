"""
Reusable response builders.
"""

from app.schemas.response import APIResponse


def success_response(
    message: str,
    data=None,
):
    """
    Return a standardized success response.
    """

    return APIResponse(
        message=message,
        data=data,
    )