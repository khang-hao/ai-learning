from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings
from app.rag.chunking import chunk_pages
from app.rag.parsers import parse_document_bytes
from app.rag.vector_store import add_chunks
from app.schemas.documents import DocumentIngestResponse


async def ingest_uploaded_file(file: UploadFile) -> DocumentIngestResponse:
    settings = get_settings()
    document_id = str(uuid4())
    filename = file.filename or f"{document_id}.bin"
    content = await file.read()

    pages = parse_document_bytes(filename=filename, content=content)
    chunks = chunk_pages(
        pages=pages,
        document_id=document_id,
        filename=filename,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    save_path = settings.raw_data_dir / _build_storage_name(document_id, filename)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with save_path.open("wb") as output:
        output.write(content)

    add_chunks(chunks)

    return DocumentIngestResponse(
        document_id=document_id,
        filename=filename,
        chunk_count=len(chunks),
        page_count=len(pages),
        saved_path=str(save_path),
    )


def _build_storage_name(document_id: str, filename: str) -> str:
    clean_name = Path(filename).name.replace(" ", "_")
    return f"{document_id}_{clean_name}"
