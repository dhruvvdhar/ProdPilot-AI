"""
Module: log_loader.py

Purpose:
Load log (.log) files and convert them into LangChain
Document objects.

Why this exists:
Production logs are one of the primary knowledge sources
for Root Cause Analysis (RCA). This service is responsible
only for loading log files.

Author: Dhruv
"""

from typing import List

from langchain_core.documents import Document

from app.services.ingestion.base_loader import BaseLoader
from app.utils.metadata import build_metadata


class LogLoaderService(BaseLoader):
    """
    Service responsible for loading log documents.
    """

    def load(self, file_path: str) -> List[Document]:
        """
        Load a log file and convert it into a LangChain Document.

        Args:
            file_path:
                Path to the log file.

        Returns:
            List[Document]:
                A list containing one LangChain Document.
        """

        # Validate the input file.
        log_path = self._validate_file(file_path)

        if log_path.suffix.lower() != ".log":
            raise ValueError(
                f"Expected a '.log' file but received '{log_path.suffix}'."
            )

        # Read the complete log file.
        content = self._read_text_file(log_path)

        # Convert the content into a LangChain Document.
        document = Document(
            page_content=content,
            metadata=build_metadata(
                path=log_path,
                file_type="log",
                loader_name=self.__class__.__name__,
            ),
        )

        return [document]