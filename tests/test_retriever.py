"""
Test the RetrieverService end-to-end.

Flow:
PDF
    ↓
Chunking
    ↓
Embedding
    ↓
Store in Chroma
    ↓
Retrieve using semantic search
"""

from app.services.ingestion.pdf_loader import PDFLoaderService
from app.services.chunking.recursive_chunker import RecursiveChunkerService
from app.services.embedding.sentence_transformer_embedding import (
    SentenceTransformerEmbeddingService,
)
from app.services.vectorstore.chroma_service import ChromaService
from app.services.retrieval.retriever_service import RetrieverService


def main():

    # Load PDF.
    loader = PDFLoaderService()
    documents = loader.load("sample.pdf")

    # Chunk.
    chunker = RecursiveChunkerService()
    chunks = chunker.split_documents(documents)

    # Generate embeddings.
    embedding_service = SentenceTransformerEmbeddingService()

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    embeddings = embedding_service.embed_documents(texts)

    # Store inside Chroma.
    chroma = ChromaService()

    # Delete every document in the collection
    existing = chroma.collection.get()

    if existing["ids"]:
        chroma.collection.delete(
            ids=existing["ids"]
        )

    chroma.collection.add(
        ids=[
            str(i)
            for i in range(len(chunks))
        ],
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            chunk.metadata
            for chunk in chunks
        ],
    )

    print("=" * 60)
    print("VECTOR DATABASE POPULATED")
    print("=" * 60)

    retriever = RetrieverService()

    query = "Why did the payment service fail?"

    results = retriever.retrieve(
        query=query,
        top_k=3,
    )

    print()
    print("=" * 60)
    print("QUERY")
    print("=" * 60)
    print(query)

    print()
    print("=" * 60)
    print("RETRIEVED DOCUMENTS")
    print("=" * 60)

    for i, document in enumerate(results, start=1):

        print(f"\nDocument {i}")
        print("-" * 40)

        print(document.page_content)

        print()

        print(document.metadata)


if __name__ == "__main__":
    main()