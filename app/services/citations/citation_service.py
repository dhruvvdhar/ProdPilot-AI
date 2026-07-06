"""
Citation service.

Converts retrieved LangChain documents into API citations.
"""

from langchain_core.documents import Document

from app.schemas.chat import Citation


class CitationService:
    """
    Builds citations from retrieved documents.
    """

    @staticmethod
    def build(
        documents: list[Document],
    ) -> list[Citation]:

        citations = []

        seen = set()

        for document in documents:
            filename = document.metadata.get(
                "filename",
                "Unknown",
            )

            page = document.metadata.get("page")

            key = (
                filename,
                page,
            )

            if key in seen:
                continue

            seen.add(key)

            citations.append(
                Citation(
                    filename=filename,
                    page=page,
                )
            )



        return citations


citation_service = CitationService()