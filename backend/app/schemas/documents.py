from pydantic import BaseModel


class DocumentIngestResponse(BaseModel):
    document_id: str
    filename: str
    chunk_count: int
    page_count: int
    saved_path: str


class StoredDocument(BaseModel):
    document_id: str
    filename: str
    chunk_count: int


class DocumentListResponse(BaseModel):
    documents: list[StoredDocument]
