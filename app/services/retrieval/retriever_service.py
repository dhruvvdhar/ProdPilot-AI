"""
Module: retriever_service.py

Purpose:
Retrieve the most relevant documents from ChromaDB.

Author: Dhruv
"""

from typing import List

from langchain_core.documents import Document

from app.services.embedding.base_embedding import BaseEmbeddingService
from app.services.embedding.sentence_transformer_embedding import (
    SentenceTransformerEmbeddingService,
)
from app.services.vectorstore.chroma_service import ChromaService
from app.core.config import settings


class RetrieverService:
    """
    Retrieve relevant documents from ChromaDB.
    """

    def __init__(
        self,
        embedding_service: BaseEmbeddingService | None = None,
    ) -> None:

        self._embedding_service = (
            embedding_service
            or SentenceTransformerEmbeddingService()
        )

        self._chroma_service = ChromaService()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Document]:

        query_embedding = (
            self._embedding_service.embed_query(query)
        )

        results = self._chroma_service.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = []

        retrieved_texts = results["documents"][0]
        retrieved_metadata = results["metadatas"][0]
        retrieved_distances = results["distances"][0]

        for text, metadata, distance in zip(
            retrieved_texts,
            retrieved_metadata,
            retrieved_distances,
        ):

            if distance > settings.SIMILARITY_THRESHOLD:
                continue

            metadata = dict(metadata)
            metadata["distance"] = distance

            documents.append(
                Document(
                    page_content=text,
                    metadata=metadata,
                )
            )

        return documents