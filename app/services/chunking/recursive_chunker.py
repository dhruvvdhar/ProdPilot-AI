"""
Module: recursive_chunker.py

Purpose:
Split LangChain Documents into smaller chunks using
RecursiveCharacterTextSplitter.

Why this exists:
Embedding models have token limits and generally produce
better vector representations for smaller chunks of text.

This service wraps LangChain's RecursiveCharacterTextSplitter
behind our own abstraction so that the rest of the application
never directly depends on LangChain's implementation.

Author: Dhruv
"""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.chunking.base_chunker import BaseChunker
from app.core.config import settings


class RecursiveChunkerService(BaseChunker):
    """
    Chunk documents using LangChain's RecursiveCharacterTextSplitter.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        """
        Initialize the Recursive Character Text Splitter.

        Args:
            chunk_size:
                Maximum number of characters per chunk.

            chunk_overlap:
                Number of overlapping characters between
                consecutive chunks.
        """

        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

    def split_documents(
        self,
        documents: List[Document],
    ) -> List[Document]:
        """
        Split documents into smaller chunks.

        Args:
            documents:
                List of LangChain Document objects.

        Returns:
            List[Document]:
                List of chunked LangChain Documents.
        """

        # Split the documents while automatically
        # preserving existing metadata.
        chunks = self._text_splitter.split_documents(documents)

        # Add chunk_id to every chunk.
        # This helps during debugging, tracing,
        # evaluation, and source citation.
        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = index

        return chunks