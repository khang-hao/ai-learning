from typing import Literal

StudyAction = Literal["ask", "summarize", "quiz"]


def route_study_action(action: str) -> StudyAction:
    normalized = action.strip().lower()
    if normalized in {"ask", "question", "qa"}:
        return "ask"
    if normalized in {"summarize", "summary"}:
        return "summarize"
    if normalized in {"quiz", "questions"}:
        return "quiz"
    raise ValueError(f"Unsupported action: {action}")
