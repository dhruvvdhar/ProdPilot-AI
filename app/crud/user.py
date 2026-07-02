"""
CRUD operations for users.
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    """
    Retrieve a user by email.
    """

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    """
    Retrieve a user by username.
    """

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def create_user(
    db: Session,
    user: UserCreate,
    hashed_password: str,
) -> User:
    """
    Create a new user.
    """

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user