"""
Module: base_chunker.py

Purpose:
Define a common interface for all document chunking strategies.

Why this exists:
Different chunking techniques may be used throughout the project
(e.g., Recursive Character, Semantic, Markdown, Code-aware chunking).

By defining an abstract base class, the rest of the application
depends only on this interface rather than any specific
LangChain implementation.

This follows the Dependency Inversion Principle (DIP).

Author: Dhruv
"""

from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document


class BaseChunker(ABC):
    """
    Abstract base class for all chunking services.

    Every chunker must implement the `split_documents()` method.
    """

    @abstractmethod
    def split_documents(
        self,
        documents: List[Document]
    ) -> List[Document]:
        """
        Split one or more LangChain Documents into
        smaller chunks suitable for embedding.

        Args:
            documents:
                List of LangChain Document objects.

        Returns:
            List[Document]:
                Chunked LangChain Document objects.
        """
        pass