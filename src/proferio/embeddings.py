import hashlib
from typing import Iterable, List

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover
    SentenceTransformer = None


class EmbeddingProvider:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._mode = "sentence_transformers" if SentenceTransformer is not None else "hashing"
        self.model = SentenceTransformer(model_name) if SentenceTransformer is not None else None

    @staticmethod
    def _hash_embed(text: str, dim: int = 384) -> np.ndarray:
        vec = np.zeros(dim, dtype=np.float32)
        for token in text.lower().split():
            h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
            vec[h % dim] += 1.0
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        return vec

    def encode(self, texts: Iterable[str]) -> List[np.ndarray]:
        if self._mode == "sentence_transformers":
            return self.model.encode(list(texts), show_progress_bar=False, normalize_embeddings=True)
        return [self._hash_embed(t) for t in texts]
