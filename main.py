"""
Suchak — Entry Point
=====================
Run this file to start the interactive chat session.

Usage:
    python main.py
    python main.py --model mistral
"""

import argparse

from suchak.config import DEFAULT_MODEL, WORKSPACE_DIR
from suchak import chat


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Suchak — A minimal CLI chatbot powered by Ollama."
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Ollama model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=str(WORKSPACE_DIR),
        help=f"Workspace directory for sandboxed tools (default: {WORKSPACE_DIR})",
    )
    args = parser.parse_args()

    chat.start(model=args.model, workspace_dir=args.workspace)


if __name__ == "__main__":
    main()
