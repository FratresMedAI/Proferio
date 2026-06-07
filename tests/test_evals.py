from proferio.evals import context_precision, faithfulness_proxy, evaluate_single


def test_context_precision():
    contexts = [{"text": "citation source lineage required"}]
    score = context_precision(contexts, ["citation", "missing"])
    assert score == 1.0


def test_faithfulness_proxy():
    contexts = [{"text": "audit log operations traceability"}]
    answer = "Operations must be logged for audit traceability"
    score = faithfulness_proxy(answer, contexts)
    assert score > 0.4


def test_evaluate_single_returns_both_metrics():
    metrics = evaluate_single(
        question="q",
        answer="source citation audit",
        contexts=[{"text": "source citation audit policy"}],
        expected_terms=["citation", "audit"],
    )
    assert "context_precision" in metrics
    assert "faithfulness_proxy" in metrics
