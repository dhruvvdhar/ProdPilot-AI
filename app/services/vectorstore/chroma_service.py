"""
Module: chroma_service.py

Purpose:
Manage the application's persistent ChromaDB instance.

Author: Dhruv
"""

from pathlib import Path

from chromadb import PersistentClient
from chromadb.api.models.Collection import Collection
from langchain_core.documents import Document

from app.core.config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
)


class ChromaService:
    """
    Singleton service responsible for interacting
    with ChromaDB.
    """

    _client = None
    _collection = None

    def __init__(self) -> None:

        if ChromaService._client is None:

            ChromaService._client = PersistentClient(
                path=str(CHROMA_DB_PATH)
            )

        if ChromaService._collection is None:

            ChromaService._collection = (
                ChromaService._client.get_or_create_collection(
                    name=COLLECTION_NAME
                )
            )

    @property
    def collection(self) -> Collection:
        """
        Return the Chroma collection.
        """
        return ChromaService._collection

    def add_chunks(
        self,
        *,
        user_id: int,
        document_id: int,
        filename: str,
        file_path: str,
        chunks: list[Document],
        embeddings: list[list[float]],
    ) -> int:
        """
        Store document chunks inside ChromaDB.
        """

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        ids = [
            f"doc_{document_id}_chunk_{i}"
            for i in range(len(chunks))
        ]

        metadatas = []

        for index, chunk in enumerate(chunks):

            metadata = dict(chunk.metadata)

            metadata.update(
                {
                    "user_id": user_id,
                    "document_id": document_id,
                    "filename": filename,
                    "file_path": str(
                        Path(file_path).resolve()
                    ),
                    "chunk_number": index,
                }
            )

            metadatas.append(metadata)

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return len(ids)

    def delete_document(
        self,
        document_id: int,
    ) -> None:
        """
        Remove all vectors belonging to a document.
        """

        results = self.collection.get(
            where={
                "document_id": document_id,
            }
        )

        if results["ids"]:
            self.collection.delete(
                ids=results["ids"]
            )

    def document_exists(
        self,
        document_id: int,
    ) -> bool:
        """
        Check whether vectors already exist
        for a document.
        """

        results = self.collection.get(
            where={
                "document_id": document_id,
            }
        )

        return len(results["ids"]) > 0

    def get_document_chunks(
        self,
        document_id: int,
    ):
        """
        Return all chunks belonging to a document.
        """

        return self.collection.get(
            where={
                "document_id": document_id,
            }
        )

    def get_user_chunks(
        self,
        user_id: int,
    ):
        """
        Return all vectors belonging to a user.
        """

        return self.collection.get(
            where={
                "user_id": user_id,
            }
        )