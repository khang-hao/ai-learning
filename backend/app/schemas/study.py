from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=4, ge=1, le=8)


class SummaryRequest(BaseModel):
    topic: str = Field(default="overall course material", min_length=3)
    top_k: int = Field(default=6, ge=1, le=10)


class QuizRequest(BaseModel):
    topic: str = Field(default="overall course material", min_length=3)
    question_count: int = Field(default=5, ge=3, le=10)
    top_k: int = Field(default=6, ge=1, le=10)


class Citation(BaseModel):
    filename: str
    page_number: int | None = None
    chunk_index: int
    snippet: str


class StudyResponse(BaseModel):
    answer: str
    citations: list[Citation]
