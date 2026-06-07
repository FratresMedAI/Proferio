from pathlib import Path

from proferio.config import AppConfig
from proferio.pipeline import build_basic_rag_pipeline

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_CORPUS = ROOT / "sample_data" / "docs"


def test_grounded_in_domain():
    cfg = AppConfig(backend="fallback", persist_index=False)
    ask = build_basic_rag_pipeline(str(SAMPLE_CORPUS), cfg)
    out = ask("What safeguards are required for traceable AI outputs?")
    assert out["status"] == "grounded"
    assert out["contexts"]


def test_out_of_scope():
    cfg = AppConfig(backend="fallback", persist_index=False)
    ask = build_basic_rag_pipeline(str(SAMPLE_CORPUS), cfg)
    out = ask("How many planets are in the solar system?")
    assert out["status"] == "out_of_scope"
    assert out["contexts"] == []


def test_no_documents(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    cfg = AppConfig(backend="fallback", persist_index=False)
    ask = build_basic_rag_pipeline(str(empty), cfg)
    out = ask("Any question?")
    assert out["status"] == "no_documents"


def test_audit_log_written(tmp_path):
    log_path = tmp_path / "audit.jsonl"
    cfg = AppConfig(
        backend="fallback",
        persist_index=False,
        enable_audit_log=True,
        audit_log_path=str(log_path),
    )
    ask = build_basic_rag_pipeline(str(SAMPLE_CORPUS), cfg)
    ask("What should be logged for auditability?")
    assert log_path.exists()
    lines = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert "auditability" in lines[0] or "grounded" in lines[0]
