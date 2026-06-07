#!/usr/bin/env bash
# Bootstrap Proferio on RunPod (or any Linux GPU/CPU pod).
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/FratresMedAI/Proferio.git}"
WORKSPACE="${WORKSPACE:-/workspace}"
PROJ="${WORKSPACE}/Proferio"
OLLAMA_MODEL="${OLLAMA_MODEL:-llama3.2:3b}"
BRANCH="${BRANCH:-main}"

echo "==> Proferio RunPod bootstrap"
echo "    workspace: ${WORKSPACE}"
echo "    model:     ${OLLAMA_MODEL}"

mkdir -p "${WORKSPACE}"
cd "${WORKSPACE}"

if [ ! -d Proferio/.git ]; then
  git clone --branch "${BRANCH}" "${REPO_URL}" Proferio
else
  cd Proferio
  git fetch origin "${BRANCH}"
  git checkout "${BRANCH}"
  git pull --ff-only origin "${BRANCH}" || true
  cd ..
fi

cd Proferio
python -m pip install --upgrade pip
pip install -r requirements.txt
pip cache purge 2>/dev/null || true

if [ -d /workspace/models ]; then
  export OLLAMA_MODELS=/workspace/models
  echo "    using network volume for models: ${OLLAMA_MODELS}"
fi

if ! command -v ollama >/dev/null 2>&1; then
  echo "==> Installing Ollama"
  curl -fsSL https://ollama.com/install.sh | sh
fi

if ! curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "==> Starting Ollama daemon"
  nohup ollama serve >/tmp/ollama.log 2>&1 &
  sleep 5
fi

echo "==> Pulling model ${OLLAMA_MODEL}"
ollama pull "${OLLAMA_MODEL}"

export PYTHONPATH=src
echo "==> Tier B smoke test"
python scripts/smoke_test.py --backend ollama --model-name "${OLLAMA_MODEL}" --no-persist-index

echo "==> Tier B golden eval"
python scripts/evaluate_golden.py --backend ollama --model-name "${OLLAMA_MODEL}" --no-persist-index

echo ""
echo "PASS: RunPod bootstrap complete"
echo "  Jupyter:  port 8888 (RunPod HTTP proxy)"
echo "  Gradio:   python scripts/launch_gradio.py --backend ollama --model-name ${OLLAMA_MODEL}"
echo "  Notebooks: notebooks/01_local_rag_pipeline.ipynb"
