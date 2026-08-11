from fastapi import APIRouter, HTTPException

from app.schemas.study import (
    AskRequest,
    ChecklistRequest,
    CompareRequest,
    ExplainSimpleRequest,
    RoutedStudyRequest,
    StudyResponse,
    SummaryRequest,
    QuizRequest,
)
from app.services.study_workflows import (
    run_ask_workflow,
    run_checklist_workflow,
    run_compare_workflow,
    run_explain_simple_workflow,
    run_quiz_workflow,
    run_routed_workflow,
    run_summary_workflow,
)

router = APIRouter()


@router.post("/ask", response_model=StudyResponse)
def ask_question(payload: AskRequest) -> StudyResponse:
    try:
        return run_ask_workflow(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/route", response_model=StudyResponse)
def route_study_request(payload: RoutedStudyRequest) -> StudyResponse:
    try:
        return run_routed_workflow(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/summarize", response_model=StudyResponse)
def summarize_topic(payload: SummaryRequest) -> StudyResponse:
    try:
        return run_summary_workflow(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/explain-simple", response_model=StudyResponse)
def explain_simple(payload: ExplainSimpleRequest) -> StudyResponse:
    try:
        return run_explain_simple_workflow(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/quiz", response_model=StudyResponse)
def generate_quiz(payload: QuizRequest) -> StudyResponse:
    try:
        return run_quiz_workflow(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/compare", response_model=StudyResponse)
def compare_topics(payload: CompareRequest) -> StudyResponse:
    try:
        return run_compare_workflow(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/checklist", response_model=StudyResponse)
def revision_checklist(payload: ChecklistRequest) -> StudyResponse:
    try:
        return run_checklist_workflow(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
