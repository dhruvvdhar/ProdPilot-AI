"""
Document service.
"""

from chromadb import db
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.logger import get_logger
from app.crud.document import create_document
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.documents.file_storage import FileStorage
from app.services.documents.file_validator import FileValidator
from app.core.exceptions import DocumentNotFoundException
from app.crud.document import (
    create_document,
    delete_document_record,
    get_all_documents,
    get_document_by_user

)
from app.schemas.document import (
    DocumentListResponse,
)
from pathlib import Path


logger = get_logger(__name__)


class DocumentService:
    """
    Business logic for document operations.
    """

    async def upload_document(
        self,
        db: Session,
        file: UploadFile,
        current_user: User,
    ) -> DocumentResponse:
        """
        Upload a document.
        """

        # Validate file
        await FileValidator.validate(file)

        # Store file
        metadata = await FileStorage.save(file)

        # Create database object
        document = Document(
            filename=metadata["filename"],
            stored_filename=metadata["stored_filename"],
            file_type=metadata["file_type"],
            file_size=metadata["file_size"],
            file_path=metadata["file_path"],
            uploaded_by=current_user.id,
        )

        # Save metadata
        document = create_document(
            db=db,
            document=document,
        )

        logger.info(
            f"Document uploaded successfully: "
            f"{document.filename} "
            f"by user {current_user.email}"
        )

        return DocumentResponse.model_validate(
            document
        )
    

    def list_documents(
        self,
        db: Session,
        current_user: User,
    ) -> DocumentListResponse:
        """
        Return all uploaded documents for the current user.
        """

        documents = get_all_documents(
            db=db,
            user_id=current_user.id,
        )

        return DocumentListResponse(
            documents=[
                DocumentResponse.model_validate(doc)
                for doc in documents
            ]
        )
    
    def get_document(
        self,
        db: Session,
        document_id: int,
        current_user: User,
    ) -> DocumentResponse:
        """
        Retrieve a single document.
        """

        document = get_document_by_user(
            db=db,
            document_id=document_id,
            user_id=current_user.id,
        )

        if document is None:
            raise DocumentNotFoundException(
                "Document not found."
            )

        return DocumentResponse.model_validate(
            document
        )
    

    def delete_document(
        self,
        db: Session,
        document_id: int,
        current_user: User,
    ) -> None:
        """
        Delete a document.
        """

        document = get_document_by_user(
            db=db,
            document_id=document_id,
            user_id=current_user.id,
        )

        if document is None:
            raise DocumentNotFoundException(
                "Document not found."
            )

        file_path = Path(document.file_path)

        if file_path.exists():
            file_path.unlink()

        delete_document_record(
            db=db,
            document=document,
        )

        logger.info(
            f"Document deleted: {document.filename}"
        )


document_service = DocumentService()