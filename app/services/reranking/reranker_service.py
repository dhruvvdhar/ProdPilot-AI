"""
CrossEncoder reranking service.
"""

from sentence_transformers import CrossEncoder

from app.core.config import settings


class RerankerService:

    _model = None

    def __init__(self):

        if RerankerService._model is None:

            RerankerService._model = CrossEncoder(
                settings.RERANKER_MODEL
            )

    @property
    def model(self):

        return RerankerService._model

    def rerank(
        self,
        query,
        documents,
    ):

        if not documents:
            return []

        pairs = [
            (
                query,
                document.page_content,
            )
            for document in documents
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return [
            document
            for document, _
            in ranked[
                : settings.RERANK_TOP_K
            ]
        ]
