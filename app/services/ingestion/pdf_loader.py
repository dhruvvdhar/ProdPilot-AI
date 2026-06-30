"""
Module: pdf_loader.py

Purpose:
Load PDF files and convert them into LangChain Document objects.

Why this exists:
This service is responsible only for reading PDF files.
It does not perform chunking, embedding generation,
vector storage, or LLM interactions.

Author: Dhruv
"""

from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

from app.services.ingestion.base_loader import BaseLoader
from app.utils.metadata import build_metadata


class PDFLoaderService(BaseLoader):
    """
    Service responsible for loading PDF documents.

    This class implements the BaseLoader interface, ensuring
    a consistent API across all document loaders.
    """

    def load(self, file_path: str) -> List[Document]:
        """
        Load a PDF file and return its contents as LangChain Documents.

        Args:
            file_path (str):
                Path to the PDF file.

        Returns:
            List[Document]:
                A list of LangChain Document objects,
                where each object represents one page.

        Raises:
            FileNotFoundError:
                If the specified file does not exist.

            ValueError:
                If the file is not a PDF.

            RuntimeError:
                If the PDF cannot be loaded.
        """

        # Validate that the file exists.
        pdf_path = self._validate_file(file_path)

        # Ensure the file has the correct extension.
        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Expected a '.pdf' file but received '{pdf_path.suffix}'."
            )

        try:
            # Create the LangChain PDF loader.
            loader = PyPDFLoader(str(pdf_path))

            # Convert each page into a LangChain Document.
            documents = loader.load()
            for document in documents:
                document.metadata.update(
                    build_metadata(
                        path=pdf_path,
                        file_type="pdf",
                        loader_name=self.__class__.__name__,
                    )
            )
            return documents

        except Exception as error:
            raise RuntimeError(
                f"Failed to load PDF '{pdf_path.name}'."
            ) from error