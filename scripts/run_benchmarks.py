import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from _cli import add_runtime_args, config_from_args
from proferio.benchmarks import benchmark_call
from proferio.pipeline import build_basic_rag_pipeline
from proferio.evals import evaluate_single


def run_mode(ask, name: str, top_k: int, rerank_top_n: int):
    q = "What AI safeguards are required for traceable outputs?"
    run = benchmark_call(ask, q)
    out = run["output"]
    metrics = evaluate_single(
        question=q,
        answer=out.get("answer", ""),
        contexts=out.get("contexts", []),
        expected_terms=["citation", "source", "traceability", "audit"],
    )
    return {
        "mode": name,
        "latency_sec": run["latency_sec"],
        "memory_percent": run["memory_percent"],
        "context_precision": round(metrics["context_precision"], 4),
        "faithfulness_proxy": round(metrics["faithfulness_proxy"], 4),
        "status": out.get("status", "unknown"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Proferio retrieval benchmarks")
    add_runtime_args(parser)
    args = parser.parse_args()

    cfg = config_from_args(args)
    cfg.top_k = 2
    cfg.rerank_top_n = 4
    ask_baseline = build_basic_rag_pipeline(str(args.corpus), cfg)

    cfg_adv = config_from_args(args)
    cfg_adv.top_k = 5
    cfg_adv.rerank_top_n = 12
    ask_advanced = build_basic_rag_pipeline(str(args.corpus), cfg_adv)

    rows = [
        run_mode(ask_baseline, "Baseline", top_k=2, rerank_top_n=4),
        run_mode(ask_advanced, "Advanced", top_k=5, rerank_top_n=12),
    ]

    print("| Mode | Latency (s) | Memory % | Context Precision | Faithfulness | Status |")
    print("|---|---:|---:|---:|---:|---|")
    for r in rows:
        print(
            f"| {r['mode']} | {r['latency_sec']} | {r['memory_percent']} | {r['context_precision']} | {r['faithfulness_proxy']} | {r['status']} |"
        )

    if any(r["status"] != "grounded" for r in rows):
        print("FAIL: benchmark run did not return grounded status", file=sys.stderr)
        return 1

    print("PASS: benchmarks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
