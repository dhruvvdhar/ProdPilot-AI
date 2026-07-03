"""
Document ingestion orchestration service.
"""

from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.constants import ProcessingStatus
from app.core.exceptions import DocumentNotFoundException
from app.crud.document import get_document_by_id
from app.db.database import SessionLocal
from app.models.document import Document
from app.services.chunking.recursive_chunker import (
    RecursiveChunkerService,
)
from app.services.embedding.sentence_transformer_embedding import (
    SentenceTransformerEmbeddingService,
)
from app.services.registry.loader_registry import (
    LOADER_REGISTRY,
)
from app.services.vectorstore.chroma_service import (
    ChromaService,
)


class DocumentIngestionService:
    """
    Orchestrates the complete document ingestion pipeline.
    """

    def __init__(self) -> None:

        self.chunker = (
            RecursiveChunkerService()
        )

        self.embedding_service = (
            SentenceTransformerEmbeddingService()
        )

        self.vectorstore = (
            ChromaService()
        )

    def process_document(
        self,
        document_id: int,
    ) -> None:

        db = SessionLocal()

        document = None

        try:

            document = self._get_document(
                db,
                document_id,
            )

            self._mark_processing_started(
                db,
                document,
            )

            documents = self._load_document(
                document,
            )

            chunks = self._chunk_document(
                documents,
            )

            vector_count = (
                self._embed_and_store(
                    document=document,
                    chunks=chunks,
                )
            )

            self._mark_completed(
                db=db,
                document=document,
                chunk_count=len(chunks),
                vector_count=vector_count,
            )

        except Exception as error:

            if document is not None:

                self._mark_failed(
                    db=db,
                    document=document,
                    error=error,
                )

            raise

        finally:

            db.close()

    def _get_document(
        self,
        db: Session,
        document_id: int,
    ) -> Document:

        document = get_document_by_id(
            db,
            document_id,
        )

        if document is None:

            raise DocumentNotFoundException(
                "Document not found."
            )

        return document

    def _mark_processing_started(
        self,
        db: Session,
        document: Document,
    ) -> None:

        document.parse_status = (
            ProcessingStatus.PROCESSING
        )

        document.embedding_status = (
            ProcessingStatus.PENDING
        )

        document.vectorstore_status = (
            ProcessingStatus.PENDING
        )

        document.processing_started_at = (
            datetime.now(timezone.utc)
        )

        db.commit()

        db.refresh(document)

    def _load_document(
        self,
        document: Document,
    ):

        extension = (
            Path(document.file_path)
            .suffix
            .lower()
        )

        loader = LOADER_REGISTRY.get(
            extension
        )

        if loader is None:

            raise ValueError(
                f"No loader registered for {extension}"
            )

        return loader.load(
            document.file_path
        )

    def _chunk_document(
        self,
        documents,
    ):

        return self.chunker.split_documents(
            documents,
        )

    def _embed_and_store(
        self,
        *,
        document: Document,
        chunks,
    ) -> int:
        """
        Generate embeddings and store vectors.
        """

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = (
            self.embedding_service.embed_documents(
                texts
            )
        )

        vector_count = (
            self.vectorstore.add_chunks(
                user_id=document.uploaded_by,
                document_id=document.id,
                filename=document.filename,
                file_path=document.file_path,
                chunks=chunks,
                embeddings=embeddings,
            )
        )

        return vector_count

    def _mark_completed(
        self,
        db: Session,
        document: Document,
        chunk_count: int,
        vector_count: int,
    ) -> None:

        document.parse_status = (
            ProcessingStatus.COMPLETED
        )

        document.embedding_status = (
            ProcessingStatus.COMPLETED
        )

        document.vectorstore_status = (
            ProcessingStatus.COMPLETED
        )

        document.chunk_count = (
            chunk_count
        )

        document.vector_count = (
            vector_count
        )

        document.processing_completed_at = (
            datetime.now(timezone.utc)
        )

        db.commit()

        db.refresh(document)

    def _mark_failed(
        self,
        db: Session,
        document: Document,
        error: Exception,
    ) -> None:

        document.parse_status = (
            ProcessingStatus.FAILED
        )

        document.embedding_status = (
            ProcessingStatus.FAILED
        )

        document.vectorstore_status = (
            ProcessingStatus.FAILED
        )

        document.error_message = (
            str(error)
        )

        document.processing_completed_at = (
            datetime.now(timezone.utc)
        )

        db.commit()

        db.refresh(document)


document_ingestion_service = (
    DocumentIngestionService()
)