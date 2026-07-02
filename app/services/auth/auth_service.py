"""
Authentication service.
"""

from sqlalchemy.orm import Session

from app.core.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)
from app.core.logger import get_logger
from app.crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.schemas.token import Token
from app.schemas.user import (
    UserCreate,
    UserLogin,
)
from app.models.user import User
from app.services.auth.jwt_service import JWTService
from app.services.auth.password import PasswordService
from app.services.auth.password_validator import PasswordValidator


logger = get_logger(__name__)


class AuthService:
    """
    Authentication business logic.
    """

    def __init__(
        self,
        password_service: PasswordService,
        jwt_service: JWTService,
    ):
        self.password_service = password_service
        self.jwt_service = jwt_service

    def register_user(
        self,
        db: Session,
        user: UserCreate,
    ) -> User:
        """
        Register a new user.
        """

        if get_user_by_email(db, user.email):

            logger.warning(
                f"Registration failed. Email already exists: {user.email}"
            )

            raise UserAlreadyExistsException(
                "Email already registered."
            )

        if get_user_by_username(db, user.username):

            logger.warning(
                f"Registration failed. Username already exists: {user.username}"
            )

            raise UserAlreadyExistsException(
                "Username already exists."
            )
        PasswordValidator.validate(user.password)

        hashed_password = self.password_service.hash_password(
            user.password
        )

        db_user = create_user(
            db=db,
            user=user,
            hashed_password=hashed_password,
        )

        logger.info(
            f"User registered successfully: {db_user.email}"
        )

        return db_user

    def login_user(
        self,
        db: Session,
        user: UserLogin,
    ) -> Token:
        """
        Authenticate user.
        """

        db_user = get_user_by_email(
            db,
            user.email,
        )

        if (
            db_user is None
            or not self.password_service.verify_password(
                user.password,
                db_user.hashed_password,
            )
        ):

            logger.warning(
                f"Failed login attempt: {user.email}"
            )

            raise InvalidCredentialsException(
                "Invalid email or password."
            )

        access_token = self.jwt_service.create_access_token(
            subject=db_user.email,
        )

        logger.info(
            f"User logged in successfully: {db_user.email}"
        )

        return Token(
            access_token=access_token,
        )
    
password_service = PasswordService()
jwt_service = JWTService()

auth_service = AuthService(
    password_service=password_service,
    jwt_service=jwt_service,
)