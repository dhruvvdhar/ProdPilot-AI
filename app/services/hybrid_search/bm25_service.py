"""
BM25 retrieval service.
"""

import pickle
from pathlib import Path

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from app.core.config import settings


class BM25Service:

    def __init__(self):

        self._bm25 = None

        self._documents = []

    def build_index(
        self,
        documents: list[Document],
    ):

        self._documents = documents

        corpus = [
            document.page_content.split()
            for document in documents
        ]

        self._bm25 = BM25Okapi(corpus)

    def add_documents(
        self,
        documents: list[Document],
    ):

        self._documents.extend(documents)

        self.build_index(
            self._documents
        )

    def retrieve(
        self,
        query: str,
        top_k: int,
    ) -> list[Document]:

        if self._bm25 is None:
            return []

        scores = self._bm25.get_scores(
            query.split()
        )

        ranked = sorted(
            zip(self._documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return [
            document
            for document, _
            in ranked[:top_k]
        ]

    def save_index(self):

        Path(
            settings.BM25_INDEX_PATH
        ).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            settings.BM25_INDEX_PATH,
            "wb",
        ) as file:

            pickle.dump(
                    self._documents,
                    file,
            )

    def load_index(self):

        path = Path(settings.BM25_INDEX_PATH)

        if not path.exists():
            return

        with open(path, "rb") as file:

            self._documents = pickle.load(file)
            print(self._documents[0].metadata)
        self.build_index(
            self._documents
        )


bm25_service = BM25Service()