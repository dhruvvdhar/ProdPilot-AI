"""
Module: sentence_transformer_embedding.py

Purpose:
Generate dense vector embeddings using SentenceTransformers.

Author: Dhruv
"""

from typing import List

from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.services.embedding.base_embedding import BaseEmbeddingService


class SentenceTransformerEmbeddingService(BaseEmbeddingService):
    """
    Singleton embedding service powered by SentenceTransformers.
    """

    _model = None

    def __init__(
        self,
        model_name: str = settings.EMBEDDING_MODEL,
    ) -> None:

        if SentenceTransformerEmbeddingService._model is None:

            try:
                SentenceTransformerEmbeddingService._model = (
                    SentenceTransformer(model_name)
                )

            except Exception as error:
                raise RuntimeError(
                    f"Failed to load embedding model '{model_name}'."
                ) from error

        self._model = SentenceTransformerEmbeddingService._model

    def embed_documents(
        self,
        texts: List[str],
    ) -> List[List[float]]:

        embeddings = self._model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    def embed_query(
        self,
        text: str,
    ) -> List[float]:

        embedding = self._model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embedding.tolist()