import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from _cli import add_runtime_args, config_from_args
from proferio.pipeline import build_basic_rag_pipeline
from proferio.evals import evaluate_single


def main() -> int:
    parser = argparse.ArgumentParser(description="Proferio end-to-end smoke test")
    add_runtime_args(parser)
    args = parser.parse_args()

    cfg = config_from_args(args)
    ask = build_basic_rag_pipeline(str(args.corpus), cfg)

    question = "What AI safeguards are required for traceable outputs?"
    result = ask(question)
    metrics = evaluate_single(
        question=question,
        answer=result["answer"],
        contexts=result["contexts"],
        expected_terms=["citation", "source", "traceability", "audit"],
    )

    print("=== SMOKE TEST RESULT ===")
    print("Answer preview:\n", result["answer"][:600])
    print("Status:", result.get("status"))
    print("Context count:", len(result["contexts"]))
    print("Metrics:", metrics)

    oos_question = "How many planets are in the solar system?"
    oos = ask(oos_question)
    print("\n=== OUT-OF-SCOPE CHECK ===")
    print("Question:", oos_question)
    print("Status:", oos.get("status"))
    print("Answer:", oos.get("answer"))

    if result.get("status") != "grounded":
        print("FAIL: expected grounded status for in-domain question", file=sys.stderr)
        return 1
    if oos.get("status") != "out_of_scope":
        print("FAIL: expected out_of_scope status for OOS question", file=sys.stderr)
        return 1
    if args.backend == "ollama" and "[Fallback" in result.get("answer", ""):
        print("FAIL: ollama backend returned fallback answer", file=sys.stderr)
        return 1

    print("\nPASS: smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
