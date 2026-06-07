# Acceptance Criteria — Proferio 100% Ready

Proferio is **100% ready** when **Tier A (CI)** and **Tier B (RunPod)** both pass.

## Tier A — CI / laptop (no Ollama)

| Check | Command | Pass |
|---|---|---|
| Imports | `PYTHONPATH=src python -c "from proferio import AppConfig"` | Exit 0 |
| Unit tests | `pytest tests/ -q` | All pass |
| Smoke | `python scripts/smoke_test.py --backend fallback --no-persist-index` | Exit 0 |
| Golden eval | `python scripts/evaluate_golden.py --backend fallback --no-persist-index` | Exit 0, accuracy ≥ 66% |
| Compile | `python -m compileall src scripts tests -q` | Exit 0 |
| CI | GitHub Actions `ci.yml` on `main` | Green |

## Tier B — RunPod full LLM path

| Check | Command | Pass |
|---|---|---|
| Bootstrap | `bash scripts/runpod_bootstrap.sh` | Exit 0 |
| Ollama | `curl -s localhost:11434/api/tags` | Model listed |
| Smoke | `python scripts/smoke_test.py --backend ollama --no-persist-index` | Exit 0, no `[Fallback` in answer |
| Golden eval | `python scripts/evaluate_golden.py --backend ollama --no-persist-index` | Exit 0 |
| Gradio | `python scripts/launch_gradio.py --backend ollama` | UI on `:7860` |
| Notebooks | Run `notebooks/01_local_rag_pipeline.ipynb` in Jupyter `:8888` | Top-to-bottom |

See [RUNPOD.md](RUNPOD.md) for pod setup.

## Defense branch (separate)

On branch `defense`:

- Status accuracy ≥ 80% on `sample_data/defense/golden_eval.json`
- Audit log written for every query when `enable_audit_log=True`
- See [DEFENSE_TRACK.md](DEFENSE_TRACK.md)

## Not in scope

100% ready does **not** mean production-hardened enterprise deployment. It means all documented entry points run and pass their checks.
