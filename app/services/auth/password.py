"""
Password service for hashing and verifying passwords.
"""

from passlib.context import CryptContext


class PasswordService:
    """
    Service for password hashing and verification.
    """

    def __init__(self) -> None:
        self._pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    def hash_password(self, password: str) -> str:
        """
        Hash a plain text password.
        """
        return self._pwd_context.hash(password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a plain text password against its hash.
        """
        return self._pwd_context.verify(
            plain_password,
            hashed_password,
        )