import argparse
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.evaluation.retrieval_metrics import (
    RetrievalEvalCase,
    evaluate_retrieval_case,
    summarize_retrieval_results,
)
from app.rag.vector_store import query_chunks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure whether RAG retrieval finds expected course-material chunks."
    )
    parser.add_argument(
        "--dataset",
        default="data/evaluation/retrieval_eval.sample.jsonl",
        help="JSONL file with fields: query, expected_terms",
    )
    parser.add_argument("--top-k", type=int, default=4, help="Number of chunks to retrieve.")
    parser.add_argument(
        "--output",
        default="data/processed/evaluation/retrieval_metrics.json",
        help="Where to save the metrics report.",
    )
    args = parser.parse_args()

    if args.top_k < 1:
        raise ValueError("--top-k must be at least 1.")

    cases = load_cases(Path(args.dataset))
    results = []

    for case in cases:
        chunks = query_chunks(query=case.query, top_k=args.top_k)
        result = evaluate_retrieval_case(case, chunks)
        results.append(result)
        rank = result.first_relevant_rank if result.first_relevant_rank is not None else "not found"
        print(f"{case.query}: relevant chunk at rank {rank}")

    metrics = summarize_retrieval_results(results, top_k=args.top_k)
    report = {
        "metrics": metrics,
        "results": [
            {
                "query": result.query,
                "hit": result.hit,
                "first_relevant_rank": result.first_relevant_rank,
            }
            for result in results
        ],
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"\nHit@{args.top_k}: {metrics['hit_at_k']:.1%}")
    print(f"MRR: {metrics['mean_reciprocal_rank']:.3f}")
    print(f"Saved report to {output_path}")


def load_cases(path: Path) -> list[RetrievalEvalCase]:
    if not path.exists():
        raise FileNotFoundError(f"Evaluation dataset was not found: {path}")

    cases: list[RetrievalEvalCase] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue

        record = json.loads(line)
        query = str(record.get("query", "")).strip()
        expected_terms = record.get("expected_terms", [])
        if not query or not isinstance(expected_terms, list):
            raise ValueError(
                f"Invalid evaluation case on line {line_number}. Use query and expected_terms."
            )

        cases.append(
            RetrievalEvalCase(
                query=query,
                expected_terms=[str(term) for term in expected_terms],
            )
        )

    if not cases:
        raise ValueError("The evaluation dataset did not contain any cases.")
    return cases


if __name__ == "__main__":
    main()
