"""
CRUD operations for documents.
"""

from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    document: Document,
) -> Document:
    """
    Save document metadata.
    """

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_document_by_id(
    db: Session,
    document_id: int,
) -> Document | None:
    """
    Retrieve document by ID.
    """

    return (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )


def get_documents_by_user(
    db: Session,
    user_id: int,
) -> list[Document]:
    """
    Retrieve all documents for a user.
    """

    return (
        db.query(Document)
        .filter(Document.uploaded_by == user_id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )


def delete_document_record(
    db: Session,
    document: Document,
) -> None:
    """
    Delete document metadata.
    """

    db.delete(document)
    db.commit()


def get_document_by_user(
    db: Session,
    document_id: int,
    user_id: int,
) -> Document | None:
    """
    Retrieve a document owned by a specific user.
    """

    return (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.uploaded_by == user_id,
        )
        .first()
    )


def get_all_documents(
    db: Session,
    user_id: int,
) -> list[Document]:
    """
    Retrieve all documents belonging to a user.
    """

    return (
        db.query(Document)
        .filter(
            Document.uploaded_by == user_id
        )
        .order_by(
            Document.uploaded_at.desc()
        )
        .all()
    )