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

    # Additive fields (non-breaking): expose existing
    # pipeline-status columns already present on the
    # Document model so the frontend can render real
    # ingestion progress instead of placeholder data.
    parse_status: str = "pending"
    embedding_status: str = "pending"
    vectorstore_status: str = "pending"
    vector_count: int = 0
    chunk_count: int = 0
    error_message: str | None = None
    processing_started_at: datetime | None = None
    processing_completed_at: datetime | None = None

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