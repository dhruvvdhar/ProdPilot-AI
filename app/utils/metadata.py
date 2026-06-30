from pathlib import Path


def build_metadata(
    path: Path,
    file_type: str,
    loader_name: str,
    **extra
) -> dict:
    """
    Build standardized metadata for LangChain documents.

    Args:
        path: Path to the source file.
        file_type: Type of the file (pdf, txt, log, image).
        loader_name: Name of the loader creating the document.
        **extra: Additional metadata specific to the loader.

    Returns:
        Standardized metadata dictionary.
    """

    metadata = {
        "source": path.name,
        "file_name": path.name,
        "file_type": file_type,
        "loader": loader_name,
    }

    metadata.update(extra)

    return metadata