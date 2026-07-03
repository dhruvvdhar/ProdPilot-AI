"""
Document database model.
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class Document(Base):
    """
    Stores uploaded document metadata.
    """

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    filename = Column(
        String(255),
        nullable=False,
    )

    stored_filename = Column(
        String(255),
        nullable=False,
        unique=True,
    )

    file_type = Column(
        String(20),
        nullable=False,
    )

    file_size = Column(
        Integer,
        nullable=False,
    )

    file_path = Column(
        String(500),
        nullable=False,
    )

    uploaded_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="documents",
    )

    parse_status = Column(
    String(20),
    default="pending",
    nullable=False,
    )

    embedding_status = Column(
        String(20),
        default="pending",
        nullable=False,
    )

    vectorstore_status = Column(
        String(20),
        default="pending",
        nullable=False,
    )

    vector_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    chunk_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    error_message = Column(
        String(1000),
        nullable=True,
    )

    processing_started_at = Column(
        DateTime,
        nullable=True,
    )

    processing_completed_at = Column(
        DateTime,
        nullable=True,
    )