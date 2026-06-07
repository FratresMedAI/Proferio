# RunPod Runtime (Primary for Tier B)

Proferio full inference, notebooks, Gradio, and real-LLM benchmarks run on RunPod. Laptop hardware is insufficient for the complete stack.

## Pod requirements

- **Recommended**: GPU pod (e.g. 1× RTX 3090) or high-RAM CPU pod (32+ vCPU, 64+ GB RAM)
- **Container disk**: 20 GB (tight constraint — models + pip cache can exceed this)
- **Jupyter Lab**: exposed on port **8888** (RunPod HTTP proxy)
- **Gradio**: port **7860** — add in pod HTTP settings if not auto-exposed

**Never commit pod IDs, SSH keys, or proxy URLs to the repository.**

## Recommended setup

1. Attach a **Network Volume** (~$7/mo) and mount it at `/workspace/models`.
2. Run bootstrap with the network-volume flag:

```bash
bash scripts/runpod_bootstrap.sh --network-volume
```

This allows `llama3.1:8b`. Without the flag (or without a mounted volume), the script defaults to `llama3.2:3b` (~2 GB) to protect the 20 GB container disk.

The script also auto-detects `/workspace/models` if the volume is already mounted.

## One-shot bootstrap

SSH into your pod, then:

```bash
cd /workspace
git clone https://github.com/FratresMedAI/Proferio.git
cd Proferio
bash scripts/runpod_bootstrap.sh
```

With Network Volume:

```bash
bash scripts/runpod_bootstrap.sh --network-volume
```

The bootstrap script:

1. Clones or updates the repo on `main`
2. Installs Python dependencies (`requirements.txt`)
3. Installs and starts Ollama (restarts daemon idempotently)
4. Pulls the configured model
5. Runs Tier B smoke + golden eval (**strict exit codes** — any failure aborts)

## Disk mitigation (pick one)

| Option | Notes |
|---|---|
| Network Volume at `/workspace/models` | Preferred — set `OLLAMA_MODELS=/workspace/models` |
| Default `llama3.2:3b` | Script default without volume |
| `pip cache purge` | Run after install (bootstrap does this) |

## Index persistence on pod restart

- `persist_index=True` (default) writes vectors to `artifacts/index` (gitignored)
- Bootstrap uses `--no-persist-index` for faster, deterministic Tier B runs
- On pod restart, the index rebuilds automatically from corpus — no manual step unless using a custom corpus path
- **Models** are lost on restart unless stored on a Network Volume via `OLLAMA_MODELS`

## After bootstrap

**Gradio demo:**

```bash
cd /workspace/Proferio
export PYTHONPATH=src
python scripts/launch_gradio.py --backend ollama --model-name llama3.2:3b
```

Open the RunPod HTTP proxy URL for port **7860**.

**Notebooks:**

Use Jupyter on port **8888** (RunPod proxy). Set kernel env:

```python
import sys
sys.path.append('/workspace/Proferio/src')
```

## Verification commands (Tier B)

```bash
curl -s localhost:11434/api/tags
python scripts/smoke_test.py --backend ollama --model-name llama3.2:3b --no-persist-index
python scripts/evaluate_golden.py --backend ollama --model-name llama3.2:3b --no-persist-index
python scripts/launch_gradio.py --backend ollama --model-name llama3.2:3b
```

Pass criteria: see [`docs/ACCEPTANCE.md`](ACCEPTANCE.md).

## Ephemeral storage warning

Container disk and models are lost on pod restart unless a Network Volume is attached and `OLLAMA_MODELS` is exported. Re-run bootstrap after any restart.

## CI vs RunPod

| Environment | Tier | Backend |
|---|---|---|
| GitHub Actions | Tier A | `fallback` (no Ollama) |
| RunPod | Tier B | `ollama` (required for v0.1.0) |

## Troubleshooting

**Ollama not responding:**

```bash
curl http://localhost:11434/api/tags
pkill ollama || true
nohup ollama serve >/tmp/ollama.log 2>&1 &
sleep 5
```

**Smoke test fails with fallback answer:**

Ensure the model is pulled (`ollama list`) and `--model-name` matches exactly.

**Disk full:**

Use `llama3.2:3b`, attach Network Volume, or run `pip cache purge`.
