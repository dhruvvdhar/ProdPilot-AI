"""
Module: ingestion_service.py

Purpose:
Coordinate the complete document ingestion pipeline.

Author: Dhruv
"""

from pathlib import Path

from app.services.chunking.recursive_chunker import (
    RecursiveChunkerService,
)
from app.services.embedding.sentence_transformer_embedding import (
    SentenceTransformerEmbeddingService,
)
from app.services.registry.loader_registry import (
    LOADER_REGISTRY,
)
from app.services.vectorstore.chroma_service import (
    ChromaService,
)


class IngestionService:

    def __init__(self) -> None:

        self._chunker = RecursiveChunkerService()

        self._embedding = (
            SentenceTransformerEmbeddingService()
        )

        self._chroma = ChromaService()

    def _get_loader(
        self,
        file_path: str,
    ):

        extension = Path(file_path).suffix.lower()

        loader = LOADER_REGISTRY.get(extension)

        if loader is None:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return loader
    

    def ingest_file(
        self,
        file_path: str,
    ) -> int:
        
        if self._document_exists(file_path):

            old_documents = self._chroma.collection.get(
                where={
                    "file_path": str(
                        Path(file_path).resolve()
                    )
                }
            )

            if old_documents["ids"]:

                self._chroma.collection.delete(
                    ids=old_documents["ids"]
                )

            print(
                f"Updating '{Path(file_path).name}'..."
            )

        loader = self._get_loader(file_path)

        documents = loader.load(file_path)

        chunks = self._chunker.split_documents(
            documents
        )

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = (
            self._embedding.embed_documents(texts)
        )

        ids = [
            f"{Path(file_path).stem}_{i}"
            for i in range(len(chunks))
        ]

        metadatas = []

        for chunk in chunks:

            metadata = dict(chunk.metadata)

            metadata["source"] = Path(file_path).name

            metadata["domain"] = "production"

            metadata["file_path"] = str(
                Path(file_path).resolve()
            )

            metadatas.append(metadata)

        self._chroma.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return len(chunks)

    def ingest_directory(
        self,
        directory: str,
    ) -> int:

        directory = Path(directory)

        total_chunks = 0

        for file in directory.rglob("*"):

            if (
                file.is_file()
                and file.suffix.lower()
                in LOADER_REGISTRY
            ):

                print(f"Ingesting {file.name}")

                try:

                    chunks = self.ingest_file(
                        str(file)
                    )

                    total_chunks += chunks

                    print(
                        f"✓ Stored {chunks} chunks"
                    )

                except Exception as error:

                    print(
                        f"✗ Skipped {file.name}: {error}"
                    )

        print()

        print(
            f"Total chunks stored: {total_chunks}"
        )

        return total_chunks
    
    def _document_exists(
        self,
        file_path: str,
    ) -> bool:
        """
        Check whether the document has already been indexed.
        """

        results = self._chroma.collection.get(
            where={
                "file_path": str(
                    Path(file_path).resolve()
                )
            }
        )

        return len(results["ids"]) > 0