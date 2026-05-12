import re
from typing import List

try:
    from rank_bm25 import BM25Okapi
except Exception:  # pragma: no cover
    BM25Okapi = None


STOPWORDS = {
    "the", "a", "an", "is", "are", "to", "for", "and", "or", "of", "in", "on", "with", "what", "how"
}


def _tokens(text: str) -> set[str]:
    raw = re.findall(r"[a-zA-Z0-9_]+", text.lower())
    return {t for t in raw if t not in STOPWORDS and len(t) > 1}


def multi_query_expand(query: str) -> List[str]:
    return [
        query,
        f"Summarize evidence for: {query}",
        f"Key entities and facts about: {query}",
        f"Cited answer with source evidence: {query}",
        f"Find policy constraints and requirements for: {query}",
    ]


def simple_rerank(query: str, candidates: List[dict], top_n: int = 5) -> List[dict]:
    q_terms = _tokens(query)
    rescored = []
    for c in candidates:
        c_terms = _tokens(c["text"])
        overlap = len(q_terms.intersection(c_terms))
        lexical = overlap / max(1, len(q_terms))
        semantic = float(c.get("score", 0.0))
        rescored.append({**c, "rerank_score": (0.65 * semantic) + (0.35 * lexical)})
    rescored.sort(key=lambda x: x["rerank_score"], reverse=True)

    selected = []
    for cand in rescored:
        if not selected:
            selected.append(cand)
            if len(selected) >= top_n:
                break
            continue
        cand_terms = _tokens(cand["text"])
        max_jaccard = 0.0
        for s in selected:
            s_terms = _tokens(s["text"])
            inter = len(cand_terms.intersection(s_terms))
            union = max(1, len(cand_terms.union(s_terms)))
            max_jaccard = max(max_jaccard, inter / union)
        mmr_score = cand["rerank_score"] - (0.25 * max_jaccard)
        if mmr_score > 0:
            selected.append({**cand, "mmr_score": mmr_score})
        if len(selected) >= top_n:
            break
    return selected[:top_n]


def build_bm25_index(chunks: List[dict]):
    if BM25Okapi is None:
        return None
    corpus = [_tokens(c.get("text", "")) for c in chunks]
    if not corpus:
        return None
    return BM25Okapi([list(toks) for toks in corpus])


def bm25_search(bm25_index, chunks: List[dict], query: str, top_k: int = 10) -> List[dict]:
    if bm25_index is None or not chunks:
        return []
    q = list(_tokens(query))
    scores = bm25_index.get_scores(q)
    ranked_ids = sorted(range(len(scores)), key=lambda i: float(scores[i]), reverse=True)
    out = []
    for idx in ranked_ids[:top_k]:
        rec = chunks[idx]
        out.append({**rec, "bm25_score": float(scores[idx])})
    return out


def fuse_scores(vector_hits: List[dict], bm25_hits: List[dict], vector_weight: float = 0.65, bm25_weight: float = 0.35) -> List[dict]:
    merged = {}
    max_v = max([h.get("score", 0.0) for h in vector_hits], default=1.0) or 1.0
    max_b = max([h.get("bm25_score", 0.0) for h in bm25_hits], default=1.0) or 1.0

    for h in vector_hits:
        hid = h["id"]
        merged.setdefault(hid, {**h, "score": 0.0, "bm25_score": 0.0})
        merged[hid]["score"] = max(merged[hid].get("score", 0.0), h.get("score", 0.0))

    for h in bm25_hits:
        hid = h["id"]
        merged.setdefault(hid, {**h, "score": 0.0, "bm25_score": 0.0})
        merged[hid]["bm25_score"] = max(merged[hid].get("bm25_score", 0.0), h.get("bm25_score", 0.0))

    out = []
    for rec in merged.values():
        nv = float(rec.get("score", 0.0)) / max_v
        nb = float(rec.get("bm25_score", 0.0)) / max_b
        fused = (vector_weight * nv) + (bm25_weight * nb)
        out.append({**rec, "fused_score": fused})
    out.sort(key=lambda x: x.get("fused_score", 0.0), reverse=True)
    return out
