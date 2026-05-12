import json
from pathlib import Path
from typing import List
import numpy as np


class InMemoryVectorStore:
    def __init__(self):
        self.embeddings = None
        self.records = []

    def add(self, embeddings, records: List[dict]):
        vecs = np.array(embeddings, dtype=np.float32)
        if vecs.size == 0 or not records:
            return
        if self.embeddings is None:
            self.embeddings = vecs
        else:
            self.embeddings = np.vstack([self.embeddings, vecs])
        self.records.extend(records)

    def search(self, query_embedding, top_k: int = 5, metadata_filter: dict | None = None):
        if self.embeddings is None or len(self.records) == 0:
            return []
        q = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        sims = (self.embeddings @ q.T).flatten()
        idxs = np.argsort(-sims)
        out = []
        for idx in idxs:
            rec = self.records[int(idx)]
            if metadata_filter:
                ok = all(rec["metadata"].get(k) == v for k, v in metadata_filter.items())
                if not ok:
                    continue
            out.append({"score": float(sims[int(idx)]), **rec})
            if len(out) >= top_k:
                break
        return out

    def save(self, base_path: str):
        path = Path(base_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.save(str(path) + ".npy", self.embeddings if self.embeddings is not None else np.array([]))
        with open(str(path) + ".json", "w", encoding="utf-8") as f:
            json.dump(self.records, f)

    def load(self, base_path: str) -> bool:
        path = Path(base_path)
        vec_path = Path(str(path) + ".npy")
        rec_path = Path(str(path) + ".json")
        if not vec_path.exists() or not rec_path.exists():
            return False
        self.embeddings = np.load(vec_path)
        with open(rec_path, "r", encoding="utf-8") as f:
            self.records = json.load(f)
        if self.embeddings.size == 0:
            self.embeddings = None
        return True
