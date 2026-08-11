from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=4, ge=1, le=8)


class SummaryRequest(BaseModel):
    topic: str = Field(default="overall course material", min_length=3)
    top_k: int = Field(default=6, ge=1, le=10)


class ExplainSimpleRequest(BaseModel):
    topic: str = Field(default="overall course material", min_length=3)
    top_k: int = Field(default=6, ge=1, le=10)


class QuizRequest(BaseModel):
    topic: str = Field(default="overall course material", min_length=3)
    question_count: int = Field(default=5, ge=3, le=10)
    top_k: int = Field(default=6, ge=1, le=10)


class CompareRequest(BaseModel):
    topic_a: str = Field(min_length=2)
    topic_b: str = Field(min_length=2)
    top_k: int = Field(default=8, ge=2, le=12)


class ChecklistRequest(BaseModel):
    topic: str = Field(default="overall course material", min_length=3)
    top_k: int = Field(default=6, ge=1, le=10)


class RoutedStudyRequest(BaseModel):
    user_input: str = Field(min_length=3)
    top_k: int = Field(default=6, ge=1, le=12)
    quiz_question_count: int = Field(default=5, ge=3, le=10)


class Citation(BaseModel):
    filename: str
    page_number: int | None = None
    chunk_index: int
    snippet: str


class StudyResponse(BaseModel):
    answer: str
    citations: list[Citation]
    workflow: str | None = None
    routing_reason: str | None = None
