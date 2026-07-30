from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.rag.ingest import ingest_uploaded_file
from app.rag.vector_store import list_documents
from app.schemas.documents import DocumentIngestResponse, DocumentListResponse

router = APIRouter()


@router.get("", response_model=DocumentListResponse)
def get_documents() -> DocumentListResponse:
    return DocumentListResponse(documents=list_documents())


@router.post(
    "/upload",
    response_model=DocumentIngestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(file: UploadFile = File(...)) -> DocumentIngestResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="File must have a name.")

    try:
        return await ingest_uploaded_file(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
