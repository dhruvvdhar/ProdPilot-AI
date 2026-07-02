"""
Global exception handlers for ProdPilot AI.
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ProdPilotException
from app.core.logger import get_logger

logger = get_logger(__name__)


async def prodpilot_exception_handler(
    request: Request,
    exc: ProdPilotException,
):
    """
    Handle all custom application exceptions.
    """

    logger.error(
        f"{request.method} {request.url} -> {exc.message}"
    )

    response = {
        "success": False,
        "message": exc.message,
    }

    if hasattr(exc, "errors"):
        response["errors"] = exc.errors

    return JSONResponse(
        status_code=400,
        content=response,
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected exceptions.
    """

    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
        },
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    """
    Handle FastAPI HTTP exceptions.
    """

    logger.warning(
        f"{request.method} {request.url} -> {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": str(exc.detail),
        },
    )