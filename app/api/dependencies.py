"""
Shared API dependencies.
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.crud.user import get_user_by_email

from app.models.user import User

from app.core.exceptions import (
    InvalidCredentialsException,
)

from app.services.auth.auth_service import jwt_service

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Return the currently authenticated user.
    """

    email = jwt_service.get_subject(token)

    user = get_user_by_email(
        db,
        email,
    )

    if user is None:

        raise InvalidCredentialsException(
            "User no longer exists."
        )

    return user