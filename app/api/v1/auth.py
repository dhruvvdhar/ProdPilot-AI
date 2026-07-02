"""
Authentication API endpoints.
"""

from fastapi import APIRouter, Depends, status
from app.schemas.user import UserLogin
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.schemas.response import APIResponse

from app.services.auth.auth_service import auth_service
from app.schemas.token import Token
from app.api.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[UserResponse],
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    created_user = auth_service.register_user(
        db=db,
        user=user,
    )

    return APIResponse(
        message="User registered successfully.",
        data=UserResponse.model_validate(created_user),
    )


@router.post(
    "/login",
    response_model=APIResponse[Token],
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate a user.
    """

    token = auth_service.login_user(
        db=db,
        user=user,
    )

    return APIResponse(
        message="Login successful.",
        data=token,
    )

@router.get(
    "/me",
    response_model=APIResponse[UserResponse],
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """

    return APIResponse(
        message="Current user retrieved successfully.",
        data=UserResponse.model_validate(current_user),
    )