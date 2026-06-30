"""
Module: base_embedding.py

Purpose:
Define a common interface for embedding services.

Why this exists:
Different embedding models may be used throughout the project
(e.g. BGE, E5, Azure OpenAI, OpenAI).

The rest of the application should depend only on this
interface rather than a specific embedding implementation.

Author: Dhruv
"""

from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingService(ABC):
    """
    Abstract base class for embedding services.
    """

    @abstractmethod
    def embed_documents(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.

        Args:
            texts:
                List of document texts.

        Returns:
            List of embedding vectors.
        """
        pass

    @abstractmethod
    def embed_query(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate an embedding for a single query.

        Args:
            text:
                User query.

        Returns:
            Embedding vector.
        """
        pass