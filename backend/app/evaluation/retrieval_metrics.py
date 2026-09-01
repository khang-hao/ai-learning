from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RetrievalEvalCase:
    """One question and words that should appear in a relevant source chunk."""

    query: str
    expected_terms: list[str]


@dataclass(frozen=True)
class RetrievalEvalResult:
    query: str
    hit: bool
    first_relevant_rank: int | None


def evaluate_retrieval_case(
    case: RetrievalEvalCase,
    chunks: Sequence[Any],
) -> RetrievalEvalResult:
    """Find the first retrieved chunk containing any expected term."""
    normalized_terms = [term.casefold().strip() for term in case.expected_terms if term.strip()]
    if not normalized_terms:
        raise ValueError("Each evaluation case needs at least one expected term.")

    for index, chunk in enumerate(chunks, start=1):
        text = _get_chunk_text(chunk).casefold()
        if any(term in text for term in normalized_terms):
            return RetrievalEvalResult(
                query=case.query,
                hit=True,
                first_relevant_rank=index,
            )

    return RetrievalEvalResult(query=case.query, hit=False, first_relevant_rank=None)


def summarize_retrieval_results(
    results: Sequence[RetrievalEvalResult],
    top_k: int,
) -> dict[str, float | int]:
    """Return Hit@K and MRR for a set of retrieval results."""
    if not results:
        raise ValueError("Cannot summarize an empty evaluation set.")

    hit_count = sum(result.hit for result in results)
    reciprocal_rank_sum = sum(
        1 / result.first_relevant_rank
        for result in results
        if result.first_relevant_rank is not None
    )
    case_count = len(results)

    return {
        "case_count": case_count,
        "top_k": top_k,
        "hit_at_k": hit_count / case_count,
        "mean_reciprocal_rank": reciprocal_rank_sum / case_count,
    }


def _get_chunk_text(chunk: Any) -> str:
    if isinstance(chunk, dict):
        return str(chunk.get("text", ""))
    return str(getattr(chunk, "text", ""))
