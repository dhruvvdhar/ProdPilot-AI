"""
Module: groq_llm.py

Purpose:
Provide a singleton ChatGroq implementation.

Author: Dhruv
"""

from langchain_groq import ChatGroq

from app.core.config import Settings
from app.services.llm.base_llm import BaseLLMService


class GroqLLMService(BaseLLMService):
    """
    Singleton Groq LLM service.
    """

    _llm = None

    def __init__(self) -> None:

        if GroqLLMService._llm is None:

            if not Settings.GROQ_API_KEY:
                raise ValueError(
                    "GROQ_API_KEY is missing."
                )

            GroqLLMService._llm = ChatGroq(
                api_key=Settings.GROQ_API_KEY,
                model=Settings.LLM_MODEL,
                temperature=Settings.TEMPERATURE,
                max_tokens=Settings.MAX_TOKENS,
            )

    @property
    def llm(self) -> ChatGroq:
        return GroqLLMService._llm

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.llm.invoke(prompt)

        return response.content