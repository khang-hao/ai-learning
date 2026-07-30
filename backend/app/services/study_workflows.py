from app.rag.retrieval import retrieve_context
from app.schemas.study import AskRequest, Citation, QuizRequest, StudyResponse, SummaryRequest
from app.services.llm import generate_grounded_response

SYSTEM_PROMPT = (
    "You are Coursework Copilot, a study assistant. "
    "Answer only from the provided sources. "
    "If the sources are insufficient, say that clearly. "
    "Use inline citations like [1], [2], and do not invent facts."
)


def run_ask_workflow(payload: AskRequest) -> StudyResponse:
    context = retrieve_context(payload.question, top_k=payload.top_k)
    answer = generate_grounded_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=_build_prompt(
            task=f"Answer this question: {payload.question}",
            context=context,
        ),
    )
    return StudyResponse(answer=answer, citations=_build_citations(context))


def run_summary_workflow(payload: SummaryRequest) -> StudyResponse:
    context = retrieve_context(f"Summarize material about {payload.topic}", top_k=payload.top_k)
    answer = generate_grounded_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=_build_prompt(
            task=(
                f"Write a study summary about {payload.topic}. "
                "Structure it with key ideas, definitions, and likely exam points."
            ),
            context=context,
        ),
    )
    return StudyResponse(answer=answer, citations=_build_citations(context))


def run_quiz_workflow(payload: QuizRequest) -> StudyResponse:
    context = retrieve_context(f"Create a quiz about {payload.topic}", top_k=payload.top_k)
    answer = generate_grounded_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=_build_prompt(
            task=(
                f"Create {payload.question_count} short-answer study questions about {payload.topic}. "
                "After each question, provide a concise answer key."
            ),
            context=context,
        ),
    )
    return StudyResponse(answer=answer, citations=_build_citations(context))


def _build_prompt(task: str, context: list[dict[str, str | int | None]]) -> str:
    sections: list[str] = []
    for index, chunk in enumerate(context, start=1):
        page_text = f"page {chunk['page_number']}" if chunk["page_number"] is not None else "page n/a"
        sections.append(
            f"[{index}] file={chunk['filename']} {page_text}\n{chunk['text']}"
        )

    joined_context = "\n\n".join(sections)
    return f"{task}\n\nSources:\n{joined_context}"


def _build_citations(context: list[dict[str, str | int | None]]) -> list[Citation]:
    return [
        Citation(
            filename=str(chunk["filename"]),
            page_number=chunk["page_number"] if isinstance(chunk["page_number"], int) else None,
            chunk_index=int(chunk["chunk_index"]),
            snippet=str(chunk["text"])[:220],
        )
        for chunk in context
    ]
