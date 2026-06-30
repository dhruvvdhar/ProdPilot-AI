"""
Module: rag_service.py

Purpose:
Execute the complete Retrieval-Augmented Generation (RAG)
pipeline using LangChain Expression Language (LCEL).

Author: Dhruv
"""

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
)

from app.services.llm.groq_llm import GroqLLMService
from app.services.prompt.prompt_service import PromptService
from app.services.retrieval.retriever_service import RetrieverService


class RAGService:
    """
    Service responsible for executing the RAG pipeline.
    """

    def __init__(self) -> None:

        self._retriever = RetrieverService()

        self._llm = GroqLLMService()

        self._prompt = PromptService.get_prompt()

        self._chain = (
            RunnableParallel(
                context=(
                    itemgetter("question")
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
    ):

        return self._retriever.retrieve(
            query=question
        )

    def _retrieve_context(
        self,
        question: str,
    ) -> str:

        documents = self._retrieve_documents(
            question
        )

        return "\n\n".join(
            document.page_content
            for document in documents
        )

    def ask(
        self,
        question: str,
    ) -> str:
        """
        Execute the complete RAG pipeline.
        """

        documents = self._retrieve_documents(
            question
        )

        if not documents:
            return (
                "I couldn't find relevant information "
                "in the uploaded production documents."
            )

        return self._chain.invoke(
            {
                "question": question,
            }
        )

    def stream(
        self,
        question: str,
    ):

        documents = self._retrieve_documents(
            question
        )

        if not documents:
            yield (
                "I couldn't find relevant information "
                "in the uploaded production documents."
            )
            return

        yield from self._chain.stream(
            {
                "question": question,
            }
        )