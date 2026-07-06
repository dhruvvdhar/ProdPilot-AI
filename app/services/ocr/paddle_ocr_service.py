"""
Module: paddle_ocr_service.py

Purpose:
Provides an OCR service implementation using PaddleOCR.

Why this exists:
This service encapsulates all interactions with the PaddleOCR
library. The rest of the application communicates only through
the BaseOCR interface and never depends directly on PaddleOCR.

Design Decisions:
- Uses Singleton-style model loading.
- Loads the OCR model only once.
- Returns plain text instead of PaddleOCR's raw output.
- Keeps third-party library details isolated.

Author: Dhruv
"""
import cv2
from matplotlib import image
from matplotlib.pyplot import gray
import numpy as np
from pathlib import Path
from paddleocr import PaddleOCR
from app.services.ocr.base_ocr import BaseOCR



class PaddleOCRService(BaseOCR):
    """
    OCR service implementation using PaddleOCR.

    The OCR model is loaded only once and reused across every
    instance of this class to minimize startup time and memory usage.
    """

    # Shared OCR model across all instances.
    _ocr_model = None

    def __init__(self) -> None:
        """
        Initialize the OCR service.

        The PaddleOCR model is created only once. Any future
        instances reuse the already-loaded model.
        """

        if PaddleOCRService._ocr_model is None:
            PaddleOCRService._ocr_model = PaddleOCR(
                use_angle_cls=True,
                lang="en",
            )

    def _preprocess_image(self, image_path: str):
        image = cv2.imread(image_path)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.fastNlMeansDenoising(gray)

        gray = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )

        return gray

    def extract_text(self, image_path: str) -> str:
        """
        Extract text from an image.

        Args:
            image_path:
                Path to the image.

        Returns:
            Extracted text as a single string.

        Raises:
            FileNotFoundError:
                If the image does not exist.

            ValueError:
                If no readable text is detected.
        """

        image = Path(image_path)

        if not image.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        processed = self._preprocess_image(str(image))

        result = PaddleOCRService._ocr_model.ocr(
            processed,
            cls=True,
        )

        ocr_blocks = []

        # PaddleOCR returns:
        #
        # [
        #     [
        #         [
        #             bounding_box,
        #             ("Detected Text", confidence)
        #         ],
        #         ...
        #     ]
        # ]
        #
        # We only care about the detected text.

        for block in result[0]:
            box = block[0]
            text = block[1][0]
            confidence = block[1][1]

            if confidence < 0.50:
                continue

            y = min(point[1] for point in box)
            x = min(point[0] for point in box)

            ocr_blocks.append((y, x, text))

        ocr_blocks.sort(key=lambda item: (item[0], item[1]))

        extracted_text = "\n".join(
            block[2]
            for block in ocr_blocks
        ).strip()

        if not extracted_text:
            raise ValueError(
                "No readable text found in the image."
            )

        return extracted_text