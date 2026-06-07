from proferio.retrieval import fuse_scores, simple_rerank, multi_query_expand


def test_multi_query_expand_includes_original():
    q = "AI governance requirements"
    expanded = multi_query_expand(q)
    assert q in expanded
    assert len(expanded) >= 3


def test_simple_rerank_orders_by_relevance():
    candidates = [
        {"id": "a", "text": "Unrelated sports tournament schedule", "score": 0.9},
        {"id": "b", "text": "Citation source traceability audit governance", "score": 0.5},
    ]
    ranked = simple_rerank("traceability audit citation", candidates, top_n=2)
    assert ranked[0]["id"] == "b"


def test_fuse_scores_combines_vector_and_bm25():
    vector_hits = [{"id": "1", "text": "alpha", "score": 0.8}]
    bm25_hits = [{"id": "1", "text": "alpha", "bm25_score": 1.0}]
    fused = fuse_scores(vector_hits, bm25_hits)
    assert len(fused) == 1
    assert fused[0]["fused_score"] > 0
