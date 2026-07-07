"""
Module: rag_service.py

Purpose:
Execute the complete Retrieval-Augmented Generation (RAG)
pipeline using LangChain Expression Language (LCEL).

Author: Dhruv
"""

from operator import itemgetter

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
)

from app.services.llm.groq_llm import GroqLLMService
from app.services.prompt.prompt_service import PromptService
from app.services.hybrid_search.hybrid_retriever_service import (
    HybridRetrieverService,
)
from app.services.reranking.reranker_service import RerankerService
from langsmith import traceable

class RAGService:
    """
    Service responsible for executing the RAG pipeline.
    """

    def __init__(self) -> None:

        self._retriever = HybridRetrieverService()

        self._reranker = RerankerService()

        self._llm = GroqLLMService()

        self._prompt = PromptService.get_prompt()

        self._chain = (
            RunnableParallel(
                history=itemgetter("history"),
                context=(
                    itemgetter("documents")
                    | RunnableLambda(self._retrieve_context)
                ),
                question=itemgetter("question"),
            )
            | self._prompt
            | self._llm.llm
            | StrOutputParser()
        )

    def _retrieve_documents(
        self,
        question: str,
        user_id: int,
    ) -> list[Document]:

        documents = self._retriever.retrieve(
            query=question,
            user_id=user_id,
        )

        documents = self._reranker.rerank(
            query=question,
            documents=documents,
        )

        return documents

    def _retrieve_context(
        self,
        documents: list[Document],
    ) -> str:

        return "\n\n".join(
            document.page_content
            for document in documents
        )
    

    @traceable(name="ProdPilot RAG")
    def ask(
        self,
        question: str,
        user_id: int,
        history: str = "",
    ):

        documents = self._retrieve_documents(
            question,
            user_id,
        )

        if not documents:
            raise ValueError(
                "This question is outside the scope of the uploaded production documents."
            )

        answer = self._chain.invoke(
            {
                "question": question,
                "history": history,
                "documents": documents,
            }
        )

        return {
            "answer": answer,
            "documents": documents,
            "contexts": [
                doc.page_content
                for doc in documents
            ],
        }


    @traceable(name="ProdPilot Stream RAG")
    def stream(
        self,
        question: str,
        user_id: int,
        history: str = "",
    ):

        documents = self._retrieve_documents(
            question,
            user_id,
        )

        if not documents:
            raise ValueError(
                "This question is outside the scope of the uploaded production documents."
            )

        for chunk in self._chain.stream(
            {
                "question": question,
                "history": history,
                "documents": documents,
            }
        ):
            yield {
                "type": "token",
                "data": chunk,
            }
        yield {
            "type": "documents",
            "data": documents,
        }