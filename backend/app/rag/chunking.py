from app.rag.types import ChunkRecord, PageText


def chunk_pages(
    pages: list[PageText],
    document_id: str,
    filename: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[ChunkRecord]:
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: list[ChunkRecord] = []
    chunk_index = 0
    step = chunk_size - chunk_overlap

    for page in pages:
        words = page.text.split()
        if not words:
            continue

        for start in range(0, len(words), step):
            window = words[start : start + chunk_size]
            if not window:
                continue

            text = " ".join(window).strip()
            if len(text) < 40:
                continue

            chunks.append(
                ChunkRecord(
                    chunk_id=f"{document_id}-chunk-{chunk_index}",
                    document_id=document_id,
                    filename=filename,
                    text=text,
                    chunk_index=chunk_index,
                    page_number=page.page_number,
                )
            )
            chunk_index += 1

    if not chunks:
        raise ValueError("The document did not produce any valid chunks.")

    return chunks
