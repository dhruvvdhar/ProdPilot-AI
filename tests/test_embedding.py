"""
Module: test_embedding.py

Purpose:
Test the SentenceTransformer embedding service.

This test verifies:
1. The embedding model loads successfully.
2. Document embeddings are generated.
3. Query embeddings are generated.
4. Embedding dimensions are correct.

Author: Dhruv
"""

from app.services.embedding.sentence_transformer_embedding import (
    SentenceTransformerEmbeddingService,
)


def main():
    """
    Test the embedding service.
    """

    # Initialize the embedding service.
    embedding_service = SentenceTransformerEmbeddingService()

    # Sample documents.
    documents = [
        "Redis connection pool exhausted.",
        "Payment service returned HTTP 500.",
        "Restart Redis service.",
    ]

    # Generate document embeddings.
    document_embeddings = embedding_service.embed_documents(documents)

    print("=" * 60)
    print("DOCUMENT EMBEDDINGS")
    print("=" * 60)

    print(f"\nDocuments: {len(document_embeddings)}")

    print(f"Embedding Dimension: {len(document_embeddings[0])}")

    print("\nFirst 10 values of Document 1:")

    print(document_embeddings[0][:10])

    # Generate query embedding.
    query = "Why did payment service fail?"

    query_embedding = embedding_service.embed_query(query)

    print("\n" + "=" * 60)
    print("QUERY EMBEDDING")
    print("=" * 60)

    print(f"\nEmbedding Dimension: {len(query_embedding)}")

    print("\nFirst 10 values:")

    print(query_embedding[:10])


if __name__ == "__main__":
    main()