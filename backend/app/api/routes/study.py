from fastapi import APIRouter, HTTPException

from app.schemas.study import (
    AskRequest,
    StudyResponse,
    SummaryRequest,
    QuizRequest,
)
from app.services.study_workflows import run_ask_workflow, run_quiz_workflow, run_summary_workflow

router = APIRouter()


@router.post("/ask", response_model=StudyResponse)
def ask_question(payload: AskRequest) -> StudyResponse:
    try:
        return run_ask_workflow(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/summarize", response_model=StudyResponse)
def summarize_topic(payload: SummaryRequest) -> StudyResponse:
    try:
        return run_summary_workflow(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/quiz", response_model=StudyResponse)
def generate_quiz(payload: QuizRequest) -> StudyResponse:
    try:
        return run_quiz_workflow(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
