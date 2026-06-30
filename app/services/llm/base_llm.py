"""
Module: base_llm.py

Purpose:
Define a common interface for Large Language Models.

Why this exists:
Different LLM providers (Groq, OpenAI, Azure OpenAI, Ollama)
can be swapped without changing the rest of the application.

Author: Dhruv
"""

from abc import ABC, abstractmethod


class BaseLLMService(ABC):
    """
    Abstract base class for LLM providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from the language model.

        Args:
            prompt:
                Fully formatted prompt.

        Returns:
            Generated response.
        """
        pass