"""
Unit tests for PasswordValidator.
"""

import pytest

from app.core.exceptions import InvalidPasswordException
from app.services.auth.password_validator import PasswordValidator


def test_valid_password():

    PasswordValidator.validate(
        "Dhruv@123"
    )


@pytest.mark.parametrize(
    "password",
    [
        "abc",
        "abcdefgh",
        "ABCDEFGH",
        "Abcdefgh",
        "Abcdefg1",
        "12345678",
        "",
    ],
)
def test_invalid_password(password):

    with pytest.raises(
        InvalidPasswordException,
    ):
        PasswordValidator.validate(password)


def test_password_returns_all_errors():

    with pytest.raises(
        InvalidPasswordException,
    ) as exc:

        PasswordValidator.validate("abc")

    assert len(exc.value.errors) > 1