import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from _cli import add_runtime_args, config_from_args
from proferio.pipeline import build_basic_rag_pipeline
from proferio.ui import launch_gradio


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch Proferio Gradio demo")
    add_runtime_args(parser)
    args = parser.parse_args()

    cfg = config_from_args(args)
    ask = build_basic_rag_pipeline(str(args.corpus), cfg)
    demo = launch_gradio(ask)
    demo.launch(server_name="0.0.0.0", server_port=7860, theme="soft")


if __name__ == "__main__":
    main()
