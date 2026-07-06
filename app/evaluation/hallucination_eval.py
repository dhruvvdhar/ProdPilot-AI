"""
Hallucination Evaluation

Checks whether the generated answer is completely supported
by the retrieved context.
"""

import json
import re

from langchain_groq import ChatGroq

from app.core.config import settings
from app.evaluation.dataset import evaluation_dataset
from app.services.hybrid_search.hybrid_retriever_service import (
    hybrid_retriever_service,
)
from app.services.rag.rag_service import RAGService


judge_llm = ChatGroq(
    model=settings.LLM_MODEL,
    temperature=0,
    groq_api_key=settings.GROQ_API_KEY,
)

rag = RAGService()


def judge_hallucination(
    question: str,
    context: str,
    answer: str,
):
    """
    Returns:
        score = 1 -> Fully grounded
        score = 0 -> Hallucinated
    """

    prompt = f"""
You are evaluating a Retrieval-Augmented Generation (RAG) system.

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Determine whether EVERY factual statement in the generated answer
is supported by the retrieved context.

Rules:

- Ignore wording differences.
- Ignore formatting.
- Ignore missing information.
- ONLY determine whether the answer invents information.

Score:

1 = Every factual claim is supported.

0 = At least one factual claim is NOT supported.

Return ONLY JSON.

Example:

{{
    "score": 1,
    "reason": "All claims are supported by the retrieved context."
}}
"""

    response = judge_llm.invoke(prompt)

    text = response.content.strip()

    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    return json.loads(text.strip())


def main():

    grounded = 0
    hallucinated = 0

    failed_examples = []

    print("=" * 70)
    print("Hallucination Evaluation")
    print("=" * 70)

    for idx, sample in enumerate(evaluation_dataset, start=1):

        question = sample["question"]

        try:

            docs = hybrid_retriever_service.retrieve(question)

            context = "\n\n".join(
                doc.page_content
                for doc in docs
            )

            rag_result = rag.ask(question)

            answer = rag_result["answer"]

        except Exception as e:

            context = ""

            answer = str(e)

        judgement = judge_hallucination(
            question=question,
            context=context,
            answer=answer,
        )

        if judgement["score"] == 1:

            grounded += 1

        else:

            hallucinated += 1

            failed_examples.append(
                {
                    "question": question,
                    "answer": answer,
                    "reason": judgement["reason"],
                }
            )

    total = grounded + hallucinated

    hallucination_rate = (
        hallucinated / total * 100
        if total
        else 0
    )

    groundedness = (
        grounded / total * 100
        if total
        else 0
    )

    print(f"Questions             : {total}")
    print(f"Grounded Answers      : {grounded}")
    print(f"Hallucinated Answers  : {hallucinated}")
    print(f"Groundedness Score    : {groundedness:.2f}%")
    print(f"Hallucination Rate    : {hallucination_rate:.2f}%")

    if failed_examples:

        print("\n")
        print("=" * 70)
        print("Hallucinated Examples")
        print("=" * 70)

        for idx, example in enumerate(failed_examples, start=1):

            print(f"\nFailure #{idx}")
            print("-" * 70)

            print(f"Question:\n{example['question']}\n")

            print(f"Generated Answer:\n{example['answer']}\n")

            print(f"Reason:\n{example['reason']}\n")


if __name__ == "__main__":
    main()