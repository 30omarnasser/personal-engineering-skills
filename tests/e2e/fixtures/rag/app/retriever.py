"""Retriever configuration for the datasheet RAG pipeline (synthetic fixture)."""

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
TOP_K = 5
EMBEDDING_MODEL = "example-embed-v2"


def chunk(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    step = max(1, size - overlap)
    return [text[i:i + size] for i in range(0, max(len(text), 1), step)]
