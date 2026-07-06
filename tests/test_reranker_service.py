from langchain_core.documents import Document

from app.services.reranking.reranker_service import (
    RerankerService,
)


documents = [
    Document(
        page_content="Redis connection pool was exhausted causing payment outage."
    ),
    Document(
        page_content="Kubernetes deployment uses rolling updates."
    ),
    Document(
        page_content="Redis was restarted and pool size increased."
    ),
    Document(
        page_content="Docker images are stored in registry."
    ),
]

query = "What caused Redis outage?"

results = RerankerService().rerank(
    query=query,
    documents=documents,
)

print("\n===== RERANK RESULTS =====\n")

for i, doc in enumerate(results, start=1):
    print(f"{i}. {doc.page_content}")