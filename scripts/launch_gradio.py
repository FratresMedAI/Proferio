import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from proferio.config import AppConfig
from proferio.pipeline import build_basic_rag_pipeline
from proferio.ui import launch_gradio


def main():
    cfg = AppConfig(backend="ollama", model_name="llama3.1:8b")
    ask = build_basic_rag_pipeline(str(ROOT / "sample_data" / "docs"), cfg)
    demo = launch_gradio(ask)
    demo.launch(server_name="0.0.0.0", server_port=7860, theme="soft")


if __name__ == "__main__":
    main()
