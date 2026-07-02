"""
JWT Service for authentication.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, ExpiredSignatureError, jwt

from app.core.config import settings
from app.core.exceptions import (
    ExpiredTokenException,
    InvalidTokenException,
)
from app.core.logger import get_logger


logger = get_logger(__name__)


class JWTService:
    """
    Service for creating and verifying JWT access tokens.
    """

    def create_access_token(
        self,
        subject: str,
    ) -> str:
        """
        Create a JWT access token.
        """

        expire = datetime.now(
            timezone.utc
        ) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": subject,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    def verify_access_token(
        self,
        token: str,
    ) -> dict:
        """
        Verify and decode a JWT token.
        """

        try:

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            subject = payload.get("sub")

            if subject is None:

                logger.warning(
                    "JWT missing subject."
                )

                raise InvalidTokenException(
                    "Token subject is missing."
                )

            return payload

        except ExpiredSignatureError:

            logger.warning(
                "Expired JWT received."
            )

            raise ExpiredTokenException(
                "Token has expired."
            )

        except JWTError:

            logger.warning(
                "Invalid JWT received."
            )

            raise InvalidTokenException(
                "Invalid token."
            )

    def get_subject(
        self,
        token: str,
    ) -> str:
        """
        Extract the subject (email) from the JWT.
        """

        payload = self.verify_access_token(token)

        return payload["sub"]