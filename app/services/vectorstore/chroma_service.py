"""
Module: chroma_service.py

Purpose:
Manage the application's persistent ChromaDB instance.

Author: Dhruv
"""

from chromadb import PersistentClient
from chromadb.api.models.Collection import Collection

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