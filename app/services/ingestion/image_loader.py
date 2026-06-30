"""
Module: image_loader.py

Purpose:
Load image files and convert them into LangChain Document objects
using an OCR service.

Why this exists:
Images cannot be embedded directly into our text-based RAG pipeline.
This loader extracts textual content from images through an OCR
service and converts it into a standardized LangChain Document.

Author: Dhruv
"""

from typing import List

from langchain_core.documents import Document

from app.services.ingestion.base_loader import BaseLoader
from app.services.ocr.base_ocr import BaseOCR
from app.utils.metadata import build_metadata


class ImageLoaderService(BaseLoader):
    """
    Service responsible for loading image documents.
    """

    SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}

    def __init__(self, ocr_service: BaseOCR) -> None:
        """
        Initialize the image loader.

        Args:
            ocr_service:
                OCR implementation used to extract text
                from images.
        """
        self._ocr_service = ocr_service

    def load(self, file_path: str) -> List[Document]:
        """
        Load an image and convert it into a LangChain Document.

        Args:
            file_path:
                Path to the image.

        Returns:
            List containing one LangChain Document.
        """

        image_path = self._validate_image(file_path)

        extracted_text = self._ocr_service.extract_text(
            str(image_path)
        )

        document = Document(
            page_content=extracted_text,
            metadata=build_metadata(
                path=image_path,
                file_type="image",
                loader_name=self.__class__.__name__,
            ),
        )

        return [document]

    def _validate_image(self, file_path: str):
        """
        Validate image existence and extension.
        """

        image_path = self._validate_file(file_path)

        if image_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported image format: {image_path.suffix}"
            )

        return image_path