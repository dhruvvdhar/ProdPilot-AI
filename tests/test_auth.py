"""
Unit tests for AuthService.
"""

import pytest
from unittest.mock import MagicMock

from app.core.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)
from app.schemas.user import (
    UserCreate,
    UserLogin,
)
from app.services.auth.auth_service import AuthService
from app.services.auth.jwt_service import JWTService
from app.services.auth.password import PasswordService


password_service = PasswordService()
jwt_service = JWTService()

auth_service = AuthService(
    password_service=password_service,
    jwt_service=jwt_service,
)


def create_test_user() -> UserCreate:
    """
    Create a reusable test registration request.
    """

    return UserCreate(
        username="dhruv",
        email="dhruv@example.com",
        password="Dhruv123",
    )


def create_test_login() -> UserLogin:
    """
    Create a reusable login request.
    """

    return UserLogin(
        email="dhruv@example.com",
        password="Dhruv123",
    )


def create_fake_db_user():
    """
    Create a fake database user.
    """

    user = MagicMock()

    user.id = 1
    user.username = "dhruv"
    user.email = "dhruv@example.com"

    user.hashed_password = password_service.hash_password(
        "Dhruv123"
    )

    return user


def test_register_user_success(mocker):

    db = MagicMock()

    user = create_test_user()

    mocker.patch(
        "app.services.auth.auth_service.get_user_by_email",
        return_value=None,
    )

    mocker.patch(
        "app.services.auth.auth_service.get_user_by_username",
        return_value=None,
    )

    fake_user = create_fake_db_user()

    mocker.patch(
        "app.services.auth.auth_service.create_user",
        return_value=fake_user,
    )

    response = auth_service.register_user(
        db=db,
        user=user,
    )

    assert response.email == user.email
    assert response.username == user.username


def test_register_duplicate_email(mocker):

    db = MagicMock()

    mocker.patch(
        "app.services.auth.auth_service.get_user_by_email",
        return_value=create_fake_db_user(),
    )

    with pytest.raises(UserAlreadyExistsException):

        auth_service.register_user(
            db=db,
            user=create_test_user(),
        )


def test_register_duplicate_username(mocker):

    db = MagicMock()

    mocker.patch(
        "app.services.auth.auth_service.get_user_by_email",
        return_value=None,
    )

    mocker.patch(
        "app.services.auth.auth_service.get_user_by_username",
        return_value=create_fake_db_user(),
    )

    with pytest.raises(UserAlreadyExistsException):

        auth_service.register_user(
            db=db,
            user=create_test_user(),
        )


def test_login_success(mocker):

    db = MagicMock()

    mocker.patch(
        "app.services.auth.auth_service.get_user_by_email",
        return_value=create_fake_db_user(),
    )

    token = auth_service.login_user(
        db=db,
        user=create_test_login(),
    )

    assert token.access_token is not None
    assert token.token_type == "bearer"


def test_login_wrong_password(mocker):

    db = MagicMock()

    login = UserLogin(
        email="dhruv@example.com",
        password="WrongPassword",
    )

    mocker.patch(
        "app.services.auth.auth_service.get_user_by_email",
        return_value=create_fake_db_user(),
    )

    with pytest.raises(
        InvalidCredentialsException,
    ):

        auth_service.login_user(
            db=db,
            user=login,
        )


def test_login_user_not_found(mocker):

    db = MagicMock()

    mocker.patch(
        "app.services.auth.auth_service.get_user_by_email",
        return_value=None,
    )

    with pytest.raises(
        InvalidCredentialsException,
    ):

        auth_service.login_user(
            db=db,
            user=create_test_login(),
        )