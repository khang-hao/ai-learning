from app.rag.vector_store import query_chunks


def retrieve_context(query: str, top_k: int) -> list[dict[str, str | int | None]]:
    chunks = query_chunks(query=query, top_k=top_k)
    if not chunks:
        raise RuntimeError("No indexed content found. Upload a document first.")

    return [
        {
            "chunk_id": chunk.chunk_id,
            "filename": chunk.filename,
            "page_number": chunk.page_number,
            "chunk_index": chunk.chunk_index,
            "text": chunk.text,
        }
        for chunk in chunks
    ]
