from app.evaluation.dataset import evaluation_dataset
from app.services.hybrid_search.hybrid_retriever_service import hybrid_retriever_service

total_precision = 0
total_recall = 0
exact_matches = 0
count = 0

print("=" * 70)
print("Citation Evaluation")
print("=" * 70)

for sample in evaluation_dataset:

    expected = set(sample["source_documents"])

    if not expected:
        continue

    docs = hybrid_retriever_service.retrieve(sample["question"])

    retrieved = {
        doc.metadata.get("filename")
        for doc in docs
        if doc.metadata.get("filename")
    }

    tp = len(expected & retrieved)

    recall = tp / len(expected)

    precision = (
        tp / len(retrieved)
        if retrieved
        else 0
    )

    exact = expected == retrieved

    total_precision += precision
    total_recall += recall

    if exact:
        exact_matches += 1

    count += 1

    print(f"\nQuestion {count}")
    print(sample["question"])
    print("Expected :", expected)
    print("Retrieved:", retrieved)
    print(f"Recall   : {recall:.2f}")
    print(f"Precision: {precision:.2f}")
    print("Exact Match:", exact)

print("\n" + "=" * 70)
print("Overall Citation Metrics")
print("=" * 70)
print(f"Citation Recall    : {(total_recall/count)*100:.2f}%")
print(f"Citation Precision : {(total_precision/count)*100:.2f}%")
print(f"Exact Match Rate   : {(exact_matches/count)*100:.2f}%")