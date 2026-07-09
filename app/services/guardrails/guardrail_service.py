"""
Guardrail service.

Responsible for validating incoming user queries
before they reach the RAG pipeline.
"""

import re

from app.core.config import settings
from app.services.retrieval.retriever_service import RetrieverService


class GuardrailService:

    PROMPT_INJECTION_PATTERNS = [
        r"ignore previous instructions",
        r"ignore all previous",
        r"system prompt",
        r"reveal prompt",
        r"developer message",
        r"act as",
        r"jailbreak",
        r"bypass",
        r"forget previous",
    ]

    def __init__(self):
        self._retriever = RetrieverService()

    def validate(
        self,
        question: str,
    ):

        self._check_empty(question)

        self._check_length(question)

        self._check_prompt_injection(question)

    def _check_empty(
        self,
        question: str,
    ):

        question = question.strip()

        if len(question) < settings.MIN_QUERY_LENGTH:
            raise ValueError(
                "Question is too short."
            )

    def _check_length(
        self,
        question: str,
    ):

        if len(question) > settings.MAX_QUERY_LENGTH:

            raise ValueError(
                "Question exceeds maximum length."
            )

    def _check_prompt_injection(
        self,
        question: str,
    ):

        lower = question.lower()

        for pattern in self.PROMPT_INJECTION_PATTERNS:

            if re.search(pattern, lower):

                raise ValueError(
                    "Prompt injection attempt detected."
                )


guardrail_service = GuardrailService()