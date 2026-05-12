import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from proferio.benchmarks import benchmark_call
from proferio.config import AppConfig
from proferio.pipeline import build_basic_rag_pipeline
from proferio.evals import evaluate_single


def run_mode(name: str, top_k: int, rerank_top_n: int):
    cfg = AppConfig(backend="ollama", model_name="llama3.1:8b", top_k=top_k, rerank_top_n=rerank_top_n)
    ask = build_basic_rag_pipeline(str(ROOT / "sample_data" / "docs"), cfg)
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


def main():
    rows = [
        run_mode("Baseline", top_k=2, rerank_top_n=4),
        run_mode("Advanced", top_k=5, rerank_top_n=12),
    ]

    print("| Mode | Latency (s) | Memory % | Context Precision | Faithfulness | Status |")
    print("|---|---:|---:|---:|---:|---|")
    for r in rows:
        print(
            f"| {r['mode']} | {r['latency_sec']} | {r['memory_percent']} | {r['context_precision']} | {r['faithfulness_proxy']} | {r['status']} |"
        )


if __name__ == "__main__":
    main()
