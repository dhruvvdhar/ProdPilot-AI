"""
File storage service.
"""

import uuid
from pathlib import Path

from fastapi import UploadFile


BASE_DIR = Path(__file__).resolve().parents[3]
UPLOAD_DIR = BASE_DIR / "database" / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


class FileStorage:
    """
    Handles storing uploaded files.
    """

    @classmethod
    async def save(
        cls,
        file: UploadFile,
    ) -> dict:
        """
        Save uploaded file and return metadata.
        """

        extension = Path(file.filename).suffix.lower()

        stored_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        file_path = (
            UPLOAD_DIR / stored_filename
        )

        contents = await file.read()

        with open(
            file_path,
            "wb",
        ) as buffer:
            buffer.write(contents)

        return {
            "filename": file.filename,
            "stored_filename": stored_filename,
            "file_type": extension.replace(".", ""),
            "file_size": len(contents),
            "file_path": str(file_path),
        }