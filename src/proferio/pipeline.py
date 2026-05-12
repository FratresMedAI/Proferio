from .config import AppConfig
from .loaders import load_text_documents, chunk_documents
from .embeddings import EmbeddingProvider
from .vectorstore import InMemoryVectorStore
from .retrieval import (
    bm25_search,
    build_bm25_index,
    fuse_scores,
    multi_query_expand,
    simple_rerank,
)
from .llm import LocalLLM, build_cited_answer


def _tokenize(text: str) -> set[str]:
    return {t.strip(".,:;!?()[]{}\"'").lower() for t in text.split() if len(t) > 2}


def _is_out_of_scope(question: str, chunks: list[dict], min_overlap: int = 2) -> bool:
    q = _tokenize(question)
    if not q:
        return False
    corpus_terms = set()
    for c in chunks[:200]:
        corpus_terms.update(_tokenize(c.get("text", "")))
    overlap = len(q.intersection(corpus_terms))
    return overlap < min_overlap


def _top_context_relevance(question: str, contexts: list[dict]) -> float:
    q = _tokenize(question)
    if not q or not contexts:
        return 0.0
    top = contexts[0].get("text", "")
    t = _tokenize(top)
    return len(q.intersection(t)) / max(1, len(q))


def build_basic_rag_pipeline(data_dir: str, cfg: AppConfig):
    docs = load_text_documents(data_dir)
    chunks = chunk_documents(docs, cfg.chunk_size, cfg.chunk_overlap)

    embedder = EmbeddingProvider(cfg.embedding_model)
    store = InMemoryVectorStore()
    loaded = False
    if cfg.persist_index:
        loaded = store.load(cfg.index_path)
        if loaded and len(store.records) != len(chunks):
            loaded = False
    if not loaded:
        vectors = embedder.encode([c["text"] for c in chunks])
        store.add(vectors, chunks)
        if cfg.persist_index:
            store.save(cfg.index_path)

    bm25_index = build_bm25_index(chunks) if cfg.use_hybrid_retrieval else None

    llm = LocalLLM(cfg.backend, cfg.model_name)

    def ask(question: str, metadata_filter: dict | None = None):
        if not chunks:
            return {
                "answer": "Insufficient evidence: no documents were loaded. Add .txt/.md files to sample_data/docs.",
                "contexts": [],
                "status": "no_documents",
            }
        token_oos = _is_out_of_scope(question, chunks, min_overlap=cfg.oos_min_overlap)
        queries = multi_query_expand(question)
        vector_hits = []
        bm25_hits = []
        for q in queries:
            qvec = embedder.encode([q])[0]
            hits = store.search(qvec, top_k=cfg.rerank_top_n, metadata_filter=metadata_filter)
            vector_hits.extend(hits)
            if bm25_index is not None:
                b_hits = bm25_search(bm25_index, chunks, q, top_k=cfg.rerank_top_n)
                if metadata_filter:
                    b_hits = [
                        h
                        for h in b_hits
                        if all(h.get("metadata", {}).get(k) == v for k, v in metadata_filter.items())
                    ]
                bm25_hits.extend(b_hits)

        fused = fuse_scores(
            vector_hits,
            bm25_hits,
            vector_weight=cfg.vector_weight,
            bm25_weight=cfg.bm25_weight,
        )
        unique = {h["id"]: h for h in fused}.values()
        reranked = simple_rerank(question, list(unique), top_n=cfg.top_k)
        if not reranked:
            return {
                "answer": "Insufficient evidence from retrieval results.",
                "contexts": [],
                "status": "no_retrieval_hits",
            }

        best_score = float(reranked[0].get("fused_score", reranked[0].get("score", 0.0)))
        top_rel = _top_context_relevance(question, reranked)
        if token_oos and (best_score < cfg.oos_score_threshold or top_rel < 0.2):
            return {
                "answer": "Out-of-scope for current knowledge base. Ask about loaded documents or add relevant files.",
                "contexts": [],
                "status": "out_of_scope",
            }

        answer = build_cited_answer(question, reranked, llm)
        return {"answer": answer, "contexts": reranked, "status": "grounded"}

    return ask
