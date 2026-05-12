<p align="center">
  <img src="assets/proferio-banner.png" alt="Proferio — RAG Agent // Context Is King" width="100%" />
</p>

# Proferio

> Local-first RAG + controllable agents — grounded, auditable, runnable on consumer hardware.

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](#quick-start)
[![Local First](https://img.shields.io/badge/Local-First-0A7E3B)](#why-this-repo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Proferio is a clean, auditable, notebook-first starter kit for **local RAG + controllable agents** with grounded answers, explicit source traces, and out-of-scope routing. It is designed for learning and rapid prototyping on consumer hardware, not as a drop-in production framework.

---

## Why This Repo

Most local RAG repos are either toy demos or fragmented snippets. This project is built to be:

- **Runnable fast** on consumer hardware
- **Auditable by default** (answer + source snippets + status)
- **Modular** (notebook UX + reusable `src/` package)
- **Demo-ready** with Gradio and smoke checks

---

## What You Get

- End-to-end local RAG pipeline (`notebooks/01_local_rag_pipeline.ipynb`)
- ReAct-style agent extension (`notebooks/02_agent_extension.ipynb`)
- Advanced tracks for reranker tuning, multimodal, and benchmarks (`03-05`)
- Local LLM backend support (`ollama`, `hf`) with safe fallback
- Retrieval stack: hybrid vector + BM25 fusion, multi-query expansion, lexical/semantic rerank, diversity penalty
- Guardrails: `grounded`, `out_of_scope`, `no_documents`, `no_retrieval_hits`

---

## Architecture

See `docs/ARCHITECTURE.md` for full details.

High-level flow:

1. Load docs
2. Chunk + embed
3. Retrieve + rerank
4. Generate grounded answer with citations
5. Return structured status + contexts

---

## Quick Start

### 1) Install

```bash
pip install -r requirements.txt
```

or

```bash
conda env create -f environment.yml
conda activate proferio
```

### 2) Local Model Runtime (recommended)

```bash
ollama pull llama3.1:8b
```

### 3) Validate in one command

```bash
python scripts/smoke_test.py
```

### 4) Launch demo UI

```bash
python scripts/launch_gradio.py
```

Open `http://localhost:7860`.

---

## Status Semantics

- `grounded`: answer is backed by retrieved corpus context
- `out_of_scope`: question does not match corpus intent/coverage
- `no_documents`: corpus is empty
- `no_retrieval_hits`: retrieval produced no usable contexts

---

## Benchmarking

Run:

```bash
python scripts/run_benchmarks.py
```

Outputs a quick markdown table for README/result sharing.

## Golden Eval Set

Run:

```bash
python scripts/evaluate_golden.py
```

This executes a small labeled set and reports hit rate by status and basic answer/retrieval quality metrics.

---

## Notebooks

- `notebooks/01_local_rag_pipeline.ipynb`
- `notebooks/02_agent_extension.ipynb`
- `notebooks/03_reranker_finetuning.ipynb`
- `notebooks/04_multimodal_extension.ipynb`
- `notebooks/05_hardware_benchmarks.ipynb`

---

## Repo Structure

- `src/proferio/` — reusable runtime modules
- `sample_data/` — sample corpus + synthetic generator
- `scripts/` — smoke, demo launch, benchmarks
- `docs/` — architecture and release guidance
- `.github/` — CI + issue templates

---

## Release Checklist

See `docs/RELEASE_CHECKLIST.md`.

---

## Contributing

See `CONTRIBUTING.md`.

## License

MIT (`LICENSE`).
