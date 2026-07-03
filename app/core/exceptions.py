"""
Centralized custom exceptions for ProdPilot AI.
"""


class ProdPilotException(Exception):
    """
    Base exception for the application.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# ======================================================
# Authentication Exceptions
# ======================================================


class AuthenticationException(ProdPilotException):
    """
    Base authentication exception.
    """

    pass


class InvalidCredentialsException(AuthenticationException):
    """
    Invalid email or password.
    """

    pass


class InvalidTokenException(AuthenticationException):
    """
    JWT token is invalid.
    """

    pass


class ExpiredTokenException(AuthenticationException):
    """
    JWT token has expired.
    """

    pass


class UserAlreadyExistsException(AuthenticationException):
    """
    User already exists.
    """

    pass


class UserNotFoundException(AuthenticationException):
    """
    User not found.
    """

    pass


class InvalidPasswordException(AuthenticationException):
    """
    Raised when password validation fails.
    """

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("Password validation failed.")



# ======================================================
# Document Exceptions
# ======================================================

class InvalidFileException(ProdPilotException):
    """Raised when uploaded file validation fails."""



class DocumentNotFoundException(
    ProdPilotException
):
    """
    Document not found.
    """

    def __init__(
        self,
        message: str = "Document not found.",
    ):
        super().__init__(message)