"""
File validation service.
"""

from pathlib import Path

from fastapi import UploadFile

from app.core.exceptions import InvalidFileException, ProdPilotException


class FileValidator:
    """
    Validates uploaded files.
    """

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
    }

    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

    @classmethod
    async def validate(
        cls,
        file: UploadFile,
    ) -> None:
        """
        Validate uploaded file.
        """

        extension = Path(file.filename).suffix.lower()

        if extension not in cls.ALLOWED_EXTENSIONS:
            raise InvalidFileException(
                "Unsupported file type."
            )

        contents = await file.read()

        if len(contents) == 0:
            raise InvalidFileException(
                "Uploaded file is empty."
            )

        if len(contents) > cls.MAX_FILE_SIZE:
            raise InvalidFileException(
                "File exceeds maximum allowed size (20 MB)."
            )

        # Reset pointer after reading
        await file.seek(0)