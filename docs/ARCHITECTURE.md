# Architecture

## System Overview

`Proferio` is a local-first Retrieval-Augmented Generation stack designed for controllability and auditability.

Pipeline flow:

1. Load local files (`.txt`, `.md`) from a corpus path.
2. Chunk text into overlapping segments.
3. Embed chunks using sentence-transformers or deterministic hashing fallback.
4. Store vectors in in-memory index.
5. Expand query into multiple retrieval intents.
6. Retrieve + rerank with lexical/semantic hybrid scoring and diversity penalty.
7. Generate grounded answer with source citations.
8. Return structured payload:
   - `answer`
   - `contexts`
   - `status` (`grounded`, `out_of_scope`, `no_documents`, `no_retrieval_hits`)

## Design Goals

- Local execution by default
- Citation-oriented responses
- Hallucination resistance via out-of-scope routing
- Graceful fallbacks when heavy dependencies are unavailable
- Notebook-first + module-backed architecture

## Module Map

- `config.py` — runtime settings
- `loaders.py` — corpus ingestion and chunking
- `embeddings.py` — embedding providers + fallback
- `vectorstore.py` — vector index/search
- `retrieval.py` — query expansion + rerank
- `llm.py` — local model backends and answer construction
- `pipeline.py` — end-to-end orchestration
- `agent.py` / `tools.py` — controllable tool-using agent loop
- `evals.py` — lightweight quality metrics
- `ui.py` — Gradio demo interface
- `benchmarks.py` — latency/memory benchmarking utility

## Operational Guardrails

- Out-of-domain questions return `out_of_scope` instead of fabricated answers.
- Empty corpus state returns `no_documents` with remediation guidance.
- Retrieval failure returns `no_retrieval_hits`.
- Source snippets are exposed in the UI for manual verification.
