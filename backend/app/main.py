from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import documents, health, study
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Coursework Copilot API",
    version="0.1.0",
    description="RAG-first study assistant backend.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(study.router, prefix="/api/study", tags=["study"])


@app.get("/")
def read_root() -> dict[str, str]:
    return {"name": "Coursework Copilot API", "status": "ready"}
