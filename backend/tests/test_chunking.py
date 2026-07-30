from app.rag.chunking import chunk_pages
from app.rag.types import PageText


def test_chunk_pages_creates_overlapping_windows():
    text = " ".join(f"word{i}" for i in range(50))
    pages = [PageText(text=text, page_number=1)]

    chunks = chunk_pages(
        pages=pages,
        document_id="doc-1",
        filename="sample.txt",
        chunk_size=10,
        chunk_overlap=2,
    )

    assert len(chunks) >= 5
    assert chunks[0].page_number == 1
    assert chunks[1].text.split()[0] == "word8"
