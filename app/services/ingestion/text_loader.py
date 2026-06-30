"""
Module: text_loader.py

Purpose:
Load plain text (.txt) files and convert them into LangChain
Document objects.

Why this exists:
This service is responsible only for reading text files.
It does not perform chunking, embedding generation,
vector storage, or LLM interactions.

Author: Dhruv
"""

from typing import List

from langchain_core.documents import Document

from app.services.ingestion.base_loader import BaseLoader

from app.utils.metadata import build_metadata


class TextLoaderService(BaseLoader):
    """
    Service responsible for loading plain text documents.

    This class implements the BaseLoader interface and reuses
    common validation logic from the BaseLoader.
    """

    def load(self, file_path: str) -> List[Document]:
        """
        Load a text file and convert it into a LangChain Document.

        Args:
            file_path:
                Path to the text file.

        Returns:
            List[Document]:
                A list containing a single LangChain Document.
        """

        # Validate the input file.
        text_path = self._validate_file(file_path)

        if text_path.suffix.lower() != ".txt":
            raise ValueError(
                f"Expected a '.txt' file but received '{text_path.suffix}'."
            )
        
        # Read the complete file content.
        content = self._read_text_file(text_path)

        # Convert the text into a LangChain Document.
        document = Document(
            page_content=content,
            metadata=build_metadata(
            path=text_path,
            file_type="txt",
            loader_name=self.__class__.__name__,
            )
        )

        return [document]