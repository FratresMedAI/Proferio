import argparse
from pathlib import Path

from proferio.config import AppConfig

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "sample_data" / "docs"
DEFAULT_EVAL = ROOT / "sample_data" / "golden_eval.json"


def add_runtime_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--backend",
        default="ollama",
        choices=["ollama", "hf", "fallback"],
        help="LLM backend (use fallback for CI / no-Ollama runs)",
    )
    parser.add_argument("--model-name", default="llama3.1:8b")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--eval-set", type=Path, default=DEFAULT_EVAL)
    parser.add_argument("--no-persist-index", action="store_true")


def config_from_args(args: argparse.Namespace) -> AppConfig:
    return AppConfig(
        backend=args.backend,
        model_name=args.model_name,
        persist_index=not args.no_persist_index,
    )
