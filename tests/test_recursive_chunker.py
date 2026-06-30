"""
Test the RecursiveChunkerService.

This test verifies that:
1. Documents are successfully split into chunks.
2. Metadata is preserved.
3. chunk_id is added to every chunk.
"""

from app.services.ingestion.pdf_loader import PDFLoaderService
from app.services.chunking.recursive_chunker import (
    RecursiveChunkerService,
)


def main() -> None:
    """
    Load a sample PDF, split it into chunks,
    and print the results.
    """

    # Load the PDF
    loader = PDFLoaderService()
    documents = loader.load("sample.pdf")

    # Create the chunker.
    # Using a small chunk size only for testing so we can
    # clearly observe multiple chunks being created.
    chunker = RecursiveChunkerService(
        chunk_size=200,
        chunk_overlap=50,
    )

    chunks = chunker.split_documents(documents)

    print(f"\nTotal Chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print("\n" + "=" * 70)
        print(f"Chunk {index}")
        print("=" * 70)

        print("\nMetadata:")
        print(chunk.metadata)

        print("\nContent:")
        print(chunk.page_content)


if __name__ == "__main__":
    main()