#!/usr/bin/env bash
# Proferio RunPod Bootstrap — Tier B validation
# Run from /workspace (default RunPod working dir)
# Usage: bash scripts/runpod_bootstrap.sh [--network-volume]
set -euo pipefail

REPO_DIR="/workspace/Proferio"
PYTHONPATH="${REPO_DIR}/src"
DEFAULT_MODEL="llama3.2:3b"
FULL_MODEL="llama3.1:8b"
USE_NETWORK_VOLUME=false
OLLAMA_MODELS_DIR="/workspace/models"
REPO_URL="${REPO_URL:-https://github.com/FratresMedAI/Proferio.git}"
BRANCH="${BRANCH:-main}"

while [[ $# -gt 0 ]]; do
  case $1 in
    --network-volume) USE_NETWORK_VOLUME=true; shift ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# Auto-detect mounted network volume
if [[ -d "${OLLAMA_MODELS_DIR}" ]]; then
  USE_NETWORK_VOLUME=true
fi

echo "=== Proferio RunPod Bootstrap ==="
echo "Working dir: $(pwd)"
echo "Target repo: ${REPO_DIR}"

# 1. Clone or update repo
if [[ ! -d "${REPO_DIR}/.git" ]]; then
  echo "Cloning repository..."
  git clone --branch "${BRANCH}" "${REPO_URL}" "${REPO_DIR}"
else
  echo "Repo exists. Pulling latest ${BRANCH}..."
  cd "${REPO_DIR}"
  git fetch origin "${BRANCH}"
  git checkout "${BRANCH}"
  git pull --ff-only origin "${BRANCH}" || true
fi

cd "${REPO_DIR}"
export PYTHONPATH="${PYTHONPATH}"

# 2. Install Python deps (runtime only)
echo "Installing runtime requirements..."
python -m pip install --upgrade pip
pip install -r requirements.txt
pip cache purge 2>/dev/null || true

# 3. Ollama install + start (idempotent)
if ! command -v ollama &>/dev/null; then
  echo "Installing Ollama..."
  curl -fsSL https://ollama.com/install.sh | sh
fi

echo "Starting Ollama daemon..."
pkill ollama 2>/dev/null || true
nohup ollama serve >/tmp/ollama.log 2>&1 &
sleep 5

# 4. Model selection and pull
MODEL="${DEFAULT_MODEL}"
if [[ "${USE_NETWORK_VOLUME}" == "true" ]]; then
  mkdir -p "${OLLAMA_MODELS_DIR}"
  export OLLAMA_MODELS="${OLLAMA_MODELS_DIR}"
  MODEL="${FULL_MODEL}"
  echo "Network Volume detected. Using ${MODEL} (OLLAMA_MODELS=${OLLAMA_MODELS})"
else
  echo "No Network Volume. Using safe default ${MODEL} to stay under 20 GB disk."
  echo "To use ${FULL_MODEL}, attach a volume at ${OLLAMA_MODELS_DIR} and re-run with --network-volume"
fi

# Allow override via env
MODEL="${OLLAMA_MODEL:-${MODEL}}"

echo "Pulling model: ${MODEL} (this may take several minutes)..."
ollama pull "${MODEL}"

# 5. Verify Ollama
echo "Verifying Ollama..."
curl -sf localhost:11434/api/tags | head -5 || {
  echo "Ollama not responding. Check /tmp/ollama.log"
  exit 1
}

# 6. Run Tier B smoke (strict — bootstrap fails on error)
echo "Running Tier B smoke_test with ollama backend..."
python scripts/smoke_test.py \
  --backend ollama \
  --model-name "${MODEL}" \
  --no-persist-index

echo "Running Tier B golden eval..."
python scripts/evaluate_golden.py \
  --backend ollama \
  --model-name "${MODEL}" \
  --no-persist-index

echo ""
echo "=== Bootstrap complete ==="
echo "Ollama model: ${MODEL}"
echo "Jupyter: http://<your-runpod-proxy>:8888"
echo "Gradio:  http://<your-runpod-proxy>:7860"
echo ""
echo "Next manual commands:"
echo "  python scripts/smoke_test.py --backend ollama --model-name ${MODEL} --no-persist-index"
echo "  python scripts/launch_gradio.py --backend ollama --model-name ${MODEL}"
echo "  # Open notebooks/01_local_rag_pipeline.ipynb in Jupyter"
