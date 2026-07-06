from app.evaluation.dataset import evaluation_dataset
from app.evaluation.langsmith_eval import client, DATASET_NAME

try:
    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Evaluation dataset for ProdPilot AI"
    )
except Exception:
    dataset = client.read_dataset(dataset_name=DATASET_NAME)

for row in evaluation_dataset:
    client.create_example(
        dataset_id=dataset.id,
        inputs={
            "question": row["question"]
        },
        outputs={
            "answer": row["expected_answer"],
            "source_documents": row["source_documents"]
        }
    )

print("Dataset uploaded successfully.")