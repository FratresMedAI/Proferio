# Defense Track — Proferio

**Branch:** `defense`  
**Status:** Synthetic knowledge-grounding overlay for defense-adjacent document retrieval.

## Purpose

Proferio Defense Track adds grounded Q&A over **synthetic** tactical knowledge bases: ROE excerpts, counter-UAS SOP summaries, and sensor narrative reports. Every answer includes source traces and optional structured audit logs.

This is **not** a physics simulation stack. It does not model hypersonics, kinetic effects, reachable sets, or live sensor fusion.

## In scope

- Grounded retrieval over synthetic defense-adjacent corpora
- Verifiable source snippets per answer
- Structured JSONL audit log per query (`enable_audit_log=True`)
- Out-of-scope refusal for non-corpus questions
- Golden eval set with ≥ 80% status accuracy target

## Out of scope

- Hypersonics / kinetic effects modeling
- Reachable-set prediction
- Live sensor fusion pipelines
- Real classified or operational data

## Corpus

Synthetic documents in [`sample_data/defense/docs/`](../sample_data/defense/docs/):

- `counter_uas_sop.md` — engagement escalation and ROE references
- `sensor_report_template.md` — narrative track summaries with source IDs
- `mission_kb_glossary.md` — defined terms for eval grounding

**All content is fictional and labeled synthetic.**

## Usage

```bash
export PYTHONPATH=src
python scripts/evaluate_golden.py \
  --backend fallback \
  --corpus sample_data/defense/docs \
  --eval-set sample_data/defense/golden_eval.json \
  --no-persist-index
```

With audit logging:

```python
from proferio import AppConfig
from proferio.pipeline import build_basic_rag_pipeline

cfg = AppConfig(
    backend="fallback",
    enable_audit_log=True,
    audit_log_path="artifacts/audit.jsonl",
    persist_index=False,
)
ask = build_basic_rag_pipeline("sample_data/defense/docs", cfg)
result = ask("What ROE gate applies before kinetic engagement?")
```

Inspect audit log: `artifacts/audit.jsonl`

## Acceptance criteria (defense branch)

| Check | Pass |
|---|---|
| Golden eval status accuracy | ≥ 80% on `sample_data/defense/golden_eval.json` |
| Grounded answers | ≥ 1 context with `source` metadata |
| Audit log | 100% of queries logged when `enable_audit_log=True` |
| RunPod Tier B | Smoke + golden eval pass with `--backend ollama` |

See also [`ACCEPTANCE.md`](ACCEPTANCE.md).

## Notebook

[`notebooks/06_defense_grounded_retrieval.ipynb`](../notebooks/06_defense_grounded_retrieval.ipynb) — corpus load → query → audit inspection.
