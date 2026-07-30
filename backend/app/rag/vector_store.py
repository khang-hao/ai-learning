from collections import defaultdict

import chromadb

from app.core.config import get_settings
from app.rag.embeddings import embed_query, embed_texts
from app.rag.types import ChunkRecord, RetrievedChunk
from app.schemas.documents import StoredDocument


def _get_collection():
    settings = get_settings()
    client = chromadb.PersistentClient(path=str(settings.chroma_dir))
    return client.get_or_create_collection(
        name=settings.chroma_collection,
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(chunks: list[ChunkRecord]) -> None:
    collection = _get_collection()
    embeddings = embed_texts([chunk.text for chunk in chunks])

    collection.add(
        ids=[chunk.chunk_id for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "document_id": chunk.document_id,
                "filename": chunk.filename,
                "chunk_index": chunk.chunk_index,
                "page_number": chunk.page_number or -1,
            }
            for chunk in chunks
        ],
    )


def query_chunks(query: str, top_k: int | None = None) -> list[RetrievedChunk]:
    settings = get_settings()
    collection = _get_collection()
    limit = top_k or settings.top_k
    query_embedding = embed_query(query)

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    ids = result.get("ids", [[]])[0]

    retrieved: list[RetrievedChunk] = []
    for chunk_id, text, metadata, distance in zip(ids, documents, metadatas, distances):
        page_number = metadata["page_number"]
        retrieved.append(
            RetrievedChunk(
                chunk_id=chunk_id,
                document_id=metadata["document_id"],
                filename=metadata["filename"],
                text=text,
                chunk_index=int(metadata["chunk_index"]),
                page_number=None if page_number == -1 else int(page_number),
                distance=float(distance),
            )
        )

    return retrieved


def list_documents() -> list[StoredDocument]:
    collection = _get_collection()
    records = collection.get(include=["metadatas"])
    grouped: dict[str, dict[str, int | str]] = defaultdict(
        lambda: {"filename": "", "chunk_count": 0}
    )

    for metadata in records.get("metadatas", []):
        document_id = str(metadata["document_id"])
        grouped[document_id]["filename"] = str(metadata["filename"])
        grouped[document_id]["chunk_count"] = int(grouped[document_id]["chunk_count"]) + 1

    return [
        StoredDocument(
            document_id=document_id,
            filename=str(data["filename"]),
            chunk_count=int(data["chunk_count"]),
        )
        for document_id, data in grouped.items()
    ]
