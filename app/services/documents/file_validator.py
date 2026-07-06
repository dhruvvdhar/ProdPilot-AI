"""
File validation service.
"""

from pathlib import Path

from fastapi import UploadFile

from app.core.exceptions import InvalidFileException
from app.services.registry.loader_registry import (
    LOADER_REGISTRY,
)


class FileValidator:
    """
    Validates uploaded files.
    """

    MAX_FILE_SIZE = 20 * 1024 * 1024

    @classmethod
    async def validate(
        cls,
        file: UploadFile,
    ) -> None:

        extension = Path(file.filename).suffix.lower()

        if extension not in LOADER_REGISTRY:

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

        await file.seek(0)