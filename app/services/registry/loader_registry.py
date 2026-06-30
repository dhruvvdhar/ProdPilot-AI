"""
Module: loader_registry.py

Purpose:
Maintain a registry mapping supported file extensions
to their corresponding loader services.

Why this exists:
Separates file-type routing from the ingestion pipeline,
making the application easier to extend with new document
formats.

Author: Dhruv
"""

from app.services.ingestion.image_loader import ImageLoaderService
from app.services.ingestion.log_loader import LogLoaderService
from app.services.ingestion.pdf_loader import PDFLoaderService
from app.services.ingestion.text_loader import TextLoaderService
from app.services.ocr.paddle_ocr_service import PaddleOCRService

LOADER_REGISTRY = {
    ".pdf": PDFLoaderService(),
    ".txt": TextLoaderService(),
    ".log": LogLoaderService(),
    ".png": ImageLoaderService(PaddleOCRService()),
    ".jpg": ImageLoaderService(PaddleOCRService()),
    ".jpeg": ImageLoaderService(PaddleOCRService()),
}