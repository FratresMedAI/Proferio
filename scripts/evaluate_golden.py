import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from _cli import add_runtime_args, config_from_args
from proferio.pipeline import build_basic_rag_pipeline
from proferio.evals import evaluate_single


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Proferio golden evaluation set")
    add_runtime_args(parser)
    parser.add_argument(
        "--min-status-accuracy",
        type=float,
        default=0.66,
        help="Minimum fraction of expected statuses that must match",
    )
    args = parser.parse_args()

    with open(args.eval_set, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    cfg = config_from_args(args)
    ask = build_basic_rag_pipeline(str(args.corpus), cfg)

    rows = []
    status_correct = 0

    for item in dataset:
        q = item["question"]
        expected_status = item["expected_status"]
        expected_terms = item.get("expected_terms", [])

        out = ask(q)
        status = out.get("status", "unknown")
        is_status_ok = status == expected_status
        status_correct += 1 if is_status_ok else 0

        metrics = evaluate_single(
            question=q,
            answer=out.get("answer", ""),
            contexts=out.get("contexts", []),
            expected_terms=expected_terms,
        )

        rows.append(
            {
                "question": q,
                "expected_status": expected_status,
                "actual_status": status,
                "status_match": is_status_ok,
                "context_precision": round(metrics["context_precision"], 4),
                "faithfulness_proxy": round(metrics["faithfulness_proxy"], 4),
            }
        )

    total = len(rows)
    status_accuracy = status_correct / total if total else 0.0

    print("| Question | Expected | Actual | Match | Context Precision | Faithfulness |")
    print("|---|---|---|---:|---:|---:|")
    for r in rows:
        q_short = (r["question"][:50] + "...") if len(r["question"]) > 53 else r["question"]
        print(
            f"| {q_short} | {r['expected_status']} | {r['actual_status']} | {int(r['status_match'])} | {r['context_precision']} | {r['faithfulness_proxy']} |"
        )

    print(f"\nStatus accuracy: {status_accuracy:.2%} ({status_correct}/{total})")

    if status_accuracy < args.min_status_accuracy:
        print(
            f"FAIL: status accuracy {status_accuracy:.2%} below threshold {args.min_status_accuracy:.2%}",
            file=sys.stderr,
        )
        return 1

    print("PASS: golden eval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
