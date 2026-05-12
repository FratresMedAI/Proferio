from typing import List, Dict


def context_precision(retrieved_contexts: List[dict], expected_terms: List[str]) -> float:
    if not retrieved_contexts:
        return 0.0
    total = 0
    expected = {t.lower() for t in expected_terms}
    for c in retrieved_contexts:
        words = set(c["text"].lower().split())
        total += 1 if expected.intersection(words) else 0
    return total / len(retrieved_contexts)


def faithfulness_proxy(answer: str, contexts: List[dict]) -> float:
    if not contexts or not answer:
        return 0.0
    ctx_words = set(" ".join(c["text"] for c in contexts).lower().split())
    ans_words = set(answer.lower().split())
    if not ans_words:
        return 0.0
    return len(ans_words.intersection(ctx_words)) / len(ans_words)


def evaluate_single(question: str, answer: str, contexts: List[dict], expected_terms: List[str]) -> Dict[str, float]:
    return {
        "context_precision": context_precision(contexts, expected_terms),
        "faithfulness_proxy": faithfulness_proxy(answer, contexts),
    }
