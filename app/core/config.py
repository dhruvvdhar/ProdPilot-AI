"""
Module: config.py

Purpose:
Centralized application configuration.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_DB_PATH = BASE_DIR / "database" / "chroma"

COLLECTION_NAME = "production_assistant"


class Settings(BaseSettings):
    """
    Application-wide configuration.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    # ======================================================
    # Database
    # ======================================================

    DATABASE_URL: str

    # ======================================================
    # Authentication
    # ======================================================

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # ======================================================
    # OCR Configuration
    # ======================================================

    USE_ANGLE_CLS: bool = True
    OCR_LANGUAGE: str = "en"

    # ======================================================
    # Chunking Configuration
    # ======================================================

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # ======================================================
    # Embedding Configuration
    # ======================================================

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    # ======================================================
    # LLM Configuration
    # ======================================================

    GROQ_API_KEY: str

    LLM_MODEL: str = "llama-3.3-70b-versatile"

    TEMPERATURE: float = 0.0

    MAX_TOKENS: int = 1024

    # ======================================================
    # Retrieval
    # ======================================================

    TOP_K: int = 15

    SIMILARITY_THRESHOLD: float = 0.70
    
    RERANK_TOP_K: int = 5


    # Guardrails
    MAX_QUERY_LENGTH: int = 1000

    MIN_QUERY_LENGTH: int = 2

    OFF_TOPIC_SIMILARITY_THRESHOLD: float = 0.35


    BM25_TOP_K: int = 8
    DENSE_TOP_K: int = 15

    BM25_INDEX_PATH: str = (
    "app/storage/bm25/bm25_index.pkl"
    )

settings = Settings()