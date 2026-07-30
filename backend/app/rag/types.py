from dataclasses import dataclass


@dataclass
class PageText:
    text: str
    page_number: int | None


@dataclass
class ChunkRecord:
    chunk_id: str
    document_id: str
    filename: str
    text: str
    chunk_index: int
    page_number: int | None


@dataclass
class RetrievedChunk:
    chunk_id: str
    document_id: str
    filename: str
    text: str
    chunk_index: int
    page_number: int | None
    distance: float
