import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from proferio.config import AppConfig
from proferio.pipeline import build_basic_rag_pipeline
from proferio.evals import evaluate_single


def main():
    cfg = AppConfig(backend="ollama", model_name="llama3.1:8b", top_k=4)
    ask = build_basic_rag_pipeline(str(ROOT / "sample_data" / "docs"), cfg)

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


if __name__ == "__main__":
    main()
