import json
import time
from pathlib import Path
from typing import Any


def append_audit_log(
    log_path: str,
    *,
    question: str,
    status: str,
    contexts: list[dict],
    latency_ms: float,
    extra: dict[str, Any] | None = None,
) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": question,
        "status": status,
        "context_ids": [c.get("id") for c in contexts],
        "sources": [
            c.get("metadata", {}).get("source", c.get("metadata", {}).get("doc_id", "unknown"))
            for c in contexts
        ],
        "latency_ms": round(latency_ms, 2),
    }
    if extra:
        record.update(extra)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=True) + "\n")
