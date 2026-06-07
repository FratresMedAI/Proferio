# RunPod Setup — Proferio Tier B

RunPod is the **primary runtime** for full LLM inference when local hardware is insufficient.

## Pod requirements

- **Recommended**: GPU pod (e.g. 1× RTX 3090) or high-RAM CPU pod (32+ vCPU, 64+ GB RAM)
- **Disk**: 20 GB container disk is tight — attach a **Network Volume** at `/workspace/models` and set `OLLAMA_MODELS=/workspace/models`
- **Ports**: Jupyter `:8888` (often pre-exposed); add `:7860` for Gradio in pod HTTP settings

## One-shot bootstrap

SSH into your pod, then:

```bash
cd /workspace
git clone https://github.com/FratresMedAI/Proferio.git
cd Proferio
bash scripts/runpod_bootstrap.sh
```

Environment overrides:

```bash
export OLLAMA_MODEL=llama3.1:8b   # if disk allows; default is llama3.2:3b
export WORKSPACE=/workspace
bash scripts/runpod_bootstrap.sh
```

The bootstrap script:

1. Clones or updates the repo
2. Installs Python dependencies
3. Installs and starts Ollama
4. Pulls the configured model
5. Runs Tier B smoke + golden eval

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

## Disk tips

| Issue | Fix |
|---|---|
| Out of disk during `pip install` | `pip cache purge` after install |
| Model pull fails | Use `OLLAMA_MODEL=llama3.2:3b` or attach Network Volume |
| Pod restart loses models | Persist models on Network Volume via `OLLAMA_MODELS` |

## Security

Do not commit pod IPs, SSH keys, or pod IDs to the repository. Use RunPod's SSH key management in the dashboard.

## Troubleshooting

**Ollama not responding:**

```bash
curl http://localhost:11434/api/tags
nohup ollama serve >/tmp/ollama.log 2>&1 &
```

**Smoke test fails with fallback answer:**

Ensure the model is pulled: `ollama list` and re-run with `--backend ollama --model-name <listed-model>`.
