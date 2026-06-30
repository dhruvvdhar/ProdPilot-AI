"""
Module: config.py

Purpose:
Centralized application configuration.

Why this exists:
Store all configurable settings in one place so they are
easy to maintain and modify.
"""

from pathlib import Path
import os
from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_DB_PATH = BASE_DIR / "database" / "chroma"

COLLECTION_NAME = "production_assistant"


class Settings:
    """
    Application-wide configuration.
    """

    # ======================================================
    # OCR Configuration
    # ======================================================

    USE_ANGLE_CLS = True
    OCR_LANGUAGE = "en"

    # ======================================================
    # Chunking Configuration
    # ======================================================

    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # ======================================================
    # Embedding Configuration
    # ======================================================

    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


    # ======================================================
    # LLM Configuration
    # ======================================================

    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    LLM_MODEL = "llama-3.3-70b-versatile"
    TEMPERATURE = 0.0
    MAX_TOKENS = 1024

    # Retrieval
    TOP_K = 4
    SIMILARITY_THRESHOLD = 0.70