from dataclasses import dataclass
from typing import Literal
import re

StudyAction = Literal["ask", "summarize", "explain", "quiz", "compare", "checklist"]


@dataclass
class RoutingDecision:
    action: StudyAction
    primary_text: str
    secondary_text: str | None
    reason: str


def route_study_action(action: str) -> StudyAction:
    normalized = action.strip().lower()
    if normalized in {"ask", "question", "qa"}:
        return "ask"
    if normalized in {"summarize", "summary"}:
        return "summarize"
    if normalized in {"explain", "explain simply", "simple"}:
        return "explain"
    if normalized in {"quiz", "questions"}:
        return "quiz"
    if normalized in {"compare", "comparison"}:
        return "compare"
    if normalized in {"checklist", "revision checklist", "revise"}:
        return "checklist"
    raise ValueError(f"Unsupported action: {action}")


def route_study_request(user_input: str) -> RoutingDecision:
    raw = user_input.strip()
    normalized = _normalize(user_input)

    compare_topics = _extract_compare_topics(raw, normalized)
    if compare_topics is not None:
        return RoutingDecision(
            action="compare",
            primary_text=compare_topics[0],
            secondary_text=compare_topics[1],
            reason="Detected a compare-style request from keywords like 'compare', 'vs', or 'difference between'.",
        )

    if _contains_any(normalized, ["quiz", "practice questions", "test me", "mcq", "question set"]):
        return RoutingDecision(
            action="quiz",
            primary_text=_strip_leading_instruction(raw, ["quiz me on", "create a quiz on", "quiz on", "practice questions on", "test me on"]),
            secondary_text=None,
            reason="Detected quiz intent from request wording.",
        )

    if _contains_any(normalized, ["checklist", "revision checklist", "study checklist", "review checklist"]):
        return RoutingDecision(
            action="checklist",
            primary_text=_strip_leading_instruction(raw, ["create a revision checklist for", "revision checklist for", "checklist for"]),
            secondary_text=None,
            reason="Detected checklist intent from request wording.",
        )

    if _contains_any(normalized, ["explain simply", "explain like", "simple explanation", "in simple terms"]):
        return RoutingDecision(
            action="explain",
            primary_text=_strip_leading_instruction(raw, ["explain simply", "explain like i am a beginner", "explain in simple terms", "simple explanation of"]),
            secondary_text=None,
            reason="Detected simplify/explain intent from request wording.",
        )

    if _contains_any(normalized, ["summarize", "summary", "summarise"]):
        return RoutingDecision(
            action="summarize",
            primary_text=_strip_leading_instruction(raw, ["summarize", "summary of", "summarise"]),
            secondary_text=None,
            reason="Detected summary intent from request wording.",
        )

    return RoutingDecision(
        action="ask",
        primary_text=raw,
        secondary_text=None,
        reason="No special workflow keyword was detected, so the request falls back to grounded Q&A.",
    )


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _contains_any(text: str, candidates: list[str]) -> bool:
    return any(candidate in text for candidate in candidates)


def _strip_leading_instruction(text: str, prefixes: list[str]) -> str:
    normalized = _normalize(text)
    for prefix in prefixes:
        if normalized.startswith(prefix):
            return text[len(prefix):].strip(" :.-") or text
    return text


def _extract_compare_topics(raw: str, normalized: str) -> tuple[str, str] | None:
    patterns = [
        r"compare (?P<a>.+?) and (?P<b>.+)$",
        r"compare (?P<a>.+?) vs (?P<b>.+)$",
        r"compare (?P<a>.+?) versus (?P<b>.+)$",
        r"difference between (?P<a>.+?) and (?P<b>.+)$",
        r"(?P<a>.+?) vs (?P<b>.+)$",
        r"(?P<a>.+?) versus (?P<b>.+)$",
    ]

    for pattern in patterns:
        match = re.search(pattern, normalized)
        if not match:
            continue

        topic_a = _slice_from_raw(raw, match.start("a"), match.end("a"))
        topic_b = _slice_from_raw(raw, match.start("b"), match.end("b"))
        if topic_a and topic_b:
            return topic_a, topic_b

    return None


def _slice_from_raw(raw: str, start: int, end: int) -> str:
    sliced = raw[start:end].strip(" .,:;!?")
    return sliced
