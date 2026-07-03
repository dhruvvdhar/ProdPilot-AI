"""
Document API endpoints.
"""

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.document import (
    DocumentListResponse,
    DocumentResponse,
)
from app.schemas.response import APIResponse
from app.services.documents.document_service import (
    document_service,
)
from app.services.ingestion.document_ingestion_service import (
    document_ingestion_service,
)





router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=APIResponse[DocumentResponse],
)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a document.
    """

    document = await document_service.upload_document(
        db=db,
        file=file,
        current_user=current_user,
    )

    background_tasks.add_task(
        document_ingestion_service.process_document,
        document.id,
    )

    return APIResponse(
        message="Document uploaded successfully.",
        data=document,
    )

@router.get(
    "/",
    response_model=APIResponse[DocumentListResponse],
)
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all uploaded documents.
    """

    documents = document_service.list_documents(
        db=db,
        current_user=current_user,
    )

    return APIResponse(
        message="Documents retrieved successfully.",
        data=documents,
    )

@router.get(
    "/{document_id}",
    response_model=APIResponse[DocumentResponse],
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a single document.
    """

    document = document_service.get_document(
        db=db,
        document_id=document_id,
        current_user=current_user,
    )

    return APIResponse(
        message="Document retrieved successfully.",
        data=document,
    )


@router.delete(
    "/{document_id}",
    response_model=APIResponse[None],
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a document.
    """

    document_service.delete_document(
        db=db,
        document_id=document_id,
        current_user=current_user,
    )

    return APIResponse(
        message="Document deleted successfully.",
        data=None,
    )