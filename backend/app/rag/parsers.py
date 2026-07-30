from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

from app.rag.types import PageText


def parse_document_bytes(filename: str, content: bytes) -> list[PageText]:
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        return _parse_pdf(content)
    if suffix in {".txt", ".md"}:
        text = content.decode("utf-8", errors="ignore")
        return [PageText(text=text, page_number=1)]

    raise ValueError("Unsupported file type. Use pdf, txt, or md for v1.")


def _parse_pdf(content: bytes) -> list[PageText]:
    reader = PdfReader(BytesIO(content))
    pages: list[PageText] = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        cleaned = text.strip()
        if cleaned:
            pages.append(PageText(text=cleaned, page_number=index))

    if not pages:
        raise ValueError("No readable text was found in the PDF.")

    return pages
