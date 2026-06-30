"""
Module: base_loader.py

Purpose:
Defines the common interface and shared functionality for all document loaders.

Why this exists:
Every document loader (PDF, TXT, LOG, Image, etc.) should expose
the same public API while reusing common validation logic.

Author: Dhruv
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from langchain_core.documents import Document


class BaseLoader(ABC):
    """
    Abstract base class for all document loaders.
    """

    @abstractmethod
    def load(self, file_path: str) -> List[Document]:
        """
        Load a document and return LangChain Document objects.
        """
        pass

    def _validate_file(
        self,
        file_path: str,
    ) -> Path:
        """
        Validate that the file exists.

        Args:
            file_path:
                Path to the input file.

        Returns:
            Path object.

        Raises:
        FileNotFoundError:
            If the file does not exist.
                
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        return path

    def _read_text_file(
        self,
        path: Path,
        encoding: str = "utf-8"
    ) -> str:
        """
        Read a text-based file.

        Args:
            path:
                Validated file path.

            encoding:
                File encoding.

        Returns:
            Complete file content.
        """

        return path.read_text(
            encoding=encoding
        )