from pathlib import Path
from typing import Iterable, List


def load_text_documents(data_dir: str) -> List[dict]:
    base = Path(data_dir)
    docs = []
    for p in base.rglob("*"):
        if p.suffix.lower() in {".txt", ".md"} and p.is_file():
            docs.append(
                {
                    "id": str(p.relative_to(base)),
                    "text": p.read_text(encoding="utf-8", errors="ignore"),
                    "metadata": {"source": str(p), "ext": p.suffix.lower()},
                }
            )
    return docs


def chunk_documents(docs: Iterable[dict], chunk_size: int = 800, overlap: int = 120) -> List[dict]:
    chunks = []
    for doc in docs:
        text = doc["text"]
        start = 0
        i = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end]
            chunks.append(
                {
                    "id": f"{doc['id']}::chunk-{i}",
                    "text": chunk_text,
                    "metadata": {**doc["metadata"], "doc_id": doc["id"], "chunk": i},
                }
            )
            if end == len(text):
                break
            start = max(0, end - overlap)
            i += 1
    return chunks
