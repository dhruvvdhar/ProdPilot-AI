"""
Hybrid Retriever Service.

Combines dense retrieval and BM25 retrieval.
"""

from annotated_types import doc
from langchain_core.documents import Document

from app.core.config import settings
from app.services.hybrid_search.bm25_service import (
    bm25_service,
)
from app.services.retrieval.retriever_service import (
    RetrieverService,
)


class HybridRetrieverService:

    def __init__(self):

        self._dense = RetrieverService()

    def retrieve(
        self,
        query: str,
    ) -> list[Document]:

        dense_documents = self._dense.retrieve(
            query=query,
            top_k=settings.DENSE_TOP_K,
        )
        # print("===== DENSE =====")

        # for doc in dense_documents:
        #     print(doc.metadata)

        bm25_documents = bm25_service.retrieve(
            query=query,
            top_k=settings.BM25_TOP_K,
        )
        # print("===== BM25 =====")

        # for doc in bm25_documents:
        #     print(doc.metadata)


        merged = []

        seen = set()

        for document in (
            dense_documents + bm25_documents
        ):

            key = (
                document.metadata.get(
                    "document_id"
                ),
                document.metadata.get(
                    "chunk_number"
                ),
            )

            if key in seen:
                continue

            seen.add(key)

            merged.append(document)
        return merged


hybrid_retriever_service = HybridRetrieverService()