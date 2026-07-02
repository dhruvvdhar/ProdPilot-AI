"""
Password validation utilities.
"""

import re

from app.core.exceptions import InvalidPasswordException


class PasswordValidator:
    """
    Validate password strength.
    """

    MIN_LENGTH = 8
    MAX_LENGTH = 64

    @classmethod
    def validate(
        cls,
        password: str,
    ) -> None:
        """
        Validate password according to security policy.
        """

        errors = []

        password = password.strip()

        if len(password) < cls.MIN_LENGTH:
            errors.append(
                "Password must be at least 8 characters long."
            )

        if len(password) > cls.MAX_LENGTH:
            errors.append(
                "Password cannot exceed 64 characters."
            )

        if not re.search(r"[A-Z]", password):
            errors.append(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password):
            errors.append(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", password):
            errors.append(
                "Password must contain at least one number."
            )

        if not re.search(
            r"[!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/~`]",
            password,
        ):
            errors.append(
                "Password must contain at least one special character."
            )

        if errors:
            raise InvalidPasswordException(errors)