"""
Document schemas.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """
    Response schema for a document.
    """

    id: int
    filename: str
    file_type: str
    file_size: int
    uploaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class DocumentUploadResponse(BaseModel):
    """
    Response returned after uploading a document.
    """

    filename: str
    message: str


class DocumentListResponse(BaseModel):
    """
    List of uploaded documents.
    """

    documents: list[DocumentResponse]