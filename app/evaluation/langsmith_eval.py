"""
Run ProdPilot AI against the LangSmith dataset.
"""

from langsmith import Client
from langsmith.evaluation import evaluate

from app.services.rag.rag_service import RAGService

DATASET_NAME = "ProdPilot AI Evaluation"

client = Client()

rag = RAGService()


def target(inputs):
    try:
        result = rag.ask(
            question=inputs["question"]
        )

        return {
            "answer": result["answer"]
        }

    except ValueError:
        return {
            "answer": "I couldn't find relevant information in the uploaded production documents."
        }


experiment_results = evaluate(
    target,
    data=DATASET_NAME,
    experiment_prefix="ProdPilot AI Baseline",
)

print(experiment_results)