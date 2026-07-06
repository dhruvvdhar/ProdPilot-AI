from statistics import mean

from app.evaluation.dataset import evaluation_dataset
from app.services.hybrid_search.hybrid_retriever_service import (
    hybrid_retriever_service,
)


def evaluate_retrieval():
    recalls = []
    precisions = []
    hit_rates = []

    print("=" * 70)
    print("Retrieval Evaluation")
    print("=" * 70)

    for i, sample in enumerate(evaluation_dataset, start=1):

        question = sample["question"]
        expected_docs = set(sample["source_documents"])

        retrieved_docs = hybrid_retriever_service.retrieve(question)

        retrieved_filenames = {
            doc.metadata.get("filename")
            for doc in retrieved_docs
            if doc.metadata.get("filename") is not None
        }

        # Skip questions that intentionally have no expected documents
        if len(expected_docs) == 0:
            continue

        correct = expected_docs.intersection(retrieved_filenames)

        recall = len(correct) / len(expected_docs)

        if len(retrieved_filenames):
            precision = len(correct) / len(retrieved_filenames)
        else:
            precision = 0

        hit = 1 if len(correct) > 0 else 0

        recalls.append(recall)
        precisions.append(precision)
        hit_rates.append(hit)

        print(f"\nQuestion {i}")
        print(f"Q: {question}")
        print(f"Expected : {sorted(expected_docs)}")
        print(f"Retrieved: {sorted(retrieved_filenames)}")
        print(f"Recall   : {recall:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Hit      : {'YES' if hit else 'NO'}")

    print("\n" + "=" * 70)
    print("Overall Retrieval Metrics")
    print("=" * 70)

    print(f"Questions Evaluated : {len(recalls)}")
    print(f"Average Recall@K    : {mean(recalls):.2%}")
    print(f"Average Precision@K : {mean(precisions):.2%}")
    print(f"Hit Rate            : {mean(hit_rates):.2%}")


if __name__ == "__main__":
    evaluate_retrieval()