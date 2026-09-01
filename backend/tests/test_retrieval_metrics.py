from app.evaluation.retrieval_metrics import (
    RetrievalEvalCase,
    evaluate_retrieval_case,
    summarize_retrieval_results,
)


def test_evaluation_finds_first_relevant_chunk():
    case = RetrievalEvalCase(
        query="What order does a stack use?",
        expected_terms=["lifo"],
    )
    chunks = [
        {"text": "A queue uses first-in, first-out order."},
        {"text": "A stack uses LIFO order for push and pop operations."},
    ]

    result = evaluate_retrieval_case(case, chunks)

    assert result.hit is True
    assert result.first_relevant_rank == 2


def test_evaluation_reports_missed_case_and_summary_metrics():
    hit = evaluate_retrieval_case(
        RetrievalEvalCase(query="stack order", expected_terms=["lifo"]),
        [{"text": "LIFO is used by a stack."}],
    )
    miss = evaluate_retrieval_case(
        RetrievalEvalCase(query="queue order", expected_terms=["fifo"]),
        [{"text": "This chunk discusses a linked list."}],
    )

    metrics = summarize_retrieval_results([hit, miss], top_k=4)

    assert metrics["hit_at_k"] == 0.5
    assert metrics["mean_reciprocal_rank"] == 0.5
