"""
Module: base_ocr.py

Purpose:
Defines the common interface for all OCR services.

Why this exists:
Different OCR providers (PaddleOCR, Azure AI Vision, GPT Vision)
should expose the same public interface. This allows the rest of
the application to remain independent of the OCR implementation.

Author: Dhruv
"""

from abc import ABC, abstractmethod


class BaseOCR(ABC):
    """
    Abstract base class for OCR services.
    """

    @abstractmethod
    def extract_text(self, image_path: str) -> str:
        """
        Extract text from an image.

        Args:
            image_path:
                Path to the image.

        Returns:
            The extracted text as a single string.
        """
        raise NotImplementedError