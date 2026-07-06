"""
Answer Accuracy Evaluation

Evaluates whether the generated answer is factually correct
compared to the expected answer using an LLM judge.
"""

from dotenv import load_dotenv

load_dotenv()

import json
from app.core.config import settings
from app.evaluation.dataset import evaluation_dataset
from app.services.rag.rag_service import RAGService
from langchain_groq import ChatGroq



judge_llm = ChatGroq(
    model=settings.LLM_MODEL,
    temperature=0,
    groq_api_key=settings.GROQ_API_KEY,
)

rag = RAGService()


def judge_answer(
    question: str,
    expected_answer: str,
    generated_answer: str,
):

    prompt = f"""
You are evaluating a Retrieval-Augmented Generation (RAG) system.

Question:
{question}

Expected Answer:
{expected_answer}

Generated Answer:
{generated_answer}

Determine whether the generated answer correctly answers the question.

Rules:

- Ignore wording differences.
- Ignore formatting differences.
- Focus only on factual correctness.
- If the generated answer contains the same facts as the expected answer,
  return score=1.
- If important facts are missing or incorrect,
  return score=0.

Return ONLY valid JSON.

Example:

{{
    "score": 1,
    "reason": "Generated answer matches the expected answer."
}}
"""

    response = judge_llm.invoke(prompt)

    return json.loads(response.content)

def main():

    correct = 0
    incorrect = 0

    failed_examples = []

    print("=" * 70)
    print("Answer Accuracy Evaluation")
    print("=" * 70)

    for idx, sample in enumerate(evaluation_dataset, start=1):

        question = sample["question"]
        expected_answer = sample["expected_answer"]

        try:

            rag_result = rag.ask(question)

            generated_answer = rag_result["answer"]

        except Exception as e:

            generated_answer = str(e)

        judgement = judge_answer(
            question=question,
            expected_answer=expected_answer,
            generated_answer=generated_answer,
        )

        if judgement["score"] == 1:

            correct += 1

        else:

            incorrect += 1

            failed_examples.append(
                {
                    "question": question,
                    "expected": expected_answer,
                    "generated": generated_answer,
                    "reason": judgement["reason"],
                }
            )

    total = len(evaluation_dataset)

    accuracy = (
        correct / total * 100
        if total > 0
        else 0
    )

    print(f"Questions : {total}")
    print(f"Correct   : {correct}")
    print(f"Incorrect : {incorrect}")
    print(f"Accuracy  : {accuracy:.2f}%")

    print("\n")

    if failed_examples:

        print("=" * 70)
        print("Failed Examples")
        print("=" * 70)

        for idx, failure in enumerate(failed_examples, start=1):

            print(f"\nFailure #{idx}")
            print("-" * 70)

            print(f"Question : {failure['question']}\n")

            print(f"Expected :\n{failure['expected']}\n")

            print(f"Generated :\n{failure['generated']}\n")

            print(f"Reason :\n{failure['reason']}")

    else:

        print("No failed examples 🎉")


if __name__ == "__main__":
    main()