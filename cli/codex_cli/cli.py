from __future__ import annotations

import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.theme import Theme

from .embeddings import EmbeddingConfig, Embeddings
from .lancedb_store import LanceDBStore
from .utils.context_manager import ContextManager, RetrievalConfig
from .utils.logger import setup_logger
from gutil.CodexBridge import CodexCLI, CodexCLIError


def load_config(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Fallback to package resource if using the default path
        default_rel = str(Path(__file__).with_name("config.yaml"))
        candidate = ["cli/codex_cli/config.yaml", default_rel]
        if path in candidate or os.path.abspath(path) in map(os.path.abspath, candidate):
            try:
                import importlib.resources as ir

                with ir.files("cli.codex_cli").joinpath("config.yaml").open("r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            except Exception as e:  # noqa: BLE001
                raise
        raise


def ensure_dirs(*paths: str) -> None:
    for p in paths:
        if p:
            Path(p).parent.mkdir(parents=True, exist_ok=True)


def open_history(sqlite_path: str):
    ensure_dirs(sqlite_path)
    conn = sqlite3.connect(sqlite_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts REAL NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            tags TEXT,
            tokens INTEGER
        );
        """
    )
    return conn


def build_prompt(user_text: str, retrieved: List[dict]) -> str:
    if not retrieved:
        return user_text
    examples = []
    for r in retrieved:
        p = r.get("prompt", "").strip()
        a = r.get("response", "").strip()
        examples.append(f"User:\n{p}\n\nAssistant:\n{a}")
    prefix = (
        "You are a coding assistant. Consider the following prior examples as context.\n"
        "Use them only when relevant and avoid repeating mistakes.\n\n"
    )
    return prefix + "\n\n".join(examples) + "\n\nCurrent instruction:\n" + user_text


def run_repl(config_path: str) -> int:
    cfg = load_config(config_path)
    theme = Theme({"info": "cyan", "ok": "green", "err": "red"})
    console = Console(theme=theme)
    logger = setup_logger()

    # Initialize components
    db_uri = cfg.get("db_uri", "./data/codex_memory")
    table = cfg.get("table", "interactions")
    store = LanceDBStore(db_uri, table)

    ecfg = cfg.get("embeddings", {})
    embeddings = Embeddings(
        EmbeddingConfig(provider=ecfg.get("provider", "fastembed"), model=ecfg.get("model"))
    )

    rcfg = cfg.get("retrieval", {})
    cm = ContextManager(store, embeddings, RetrievalConfig(top_k=int(rcfg.get("top_k", 5))))

    # Optional SQLite history
    history_cfg = cfg.get("history", {})
    hist_enabled = bool(history_cfg.get("enable", True))
    hist_db = None
    if hist_enabled:
        hist_db = open_history(history_cfg.get("sqlite_path", "./data/history.db"))

    codex_args = cfg.get("codex", {}).get("args", ["--oss"])  # default to local model via codex
    codex = CodexCLI()

    console.print(Panel("Codex REPL with LanceDB Memory. Type :q to quit.", title="gutil codex-repl"))
    while True:
        try:
            user_text = Prompt.ask("[info]You[/info]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[info]Goodbye![/info]")
            break
        if not user_text:
            continue
        if user_text.strip() in {":q", ":quit", ":exit"}:
            break

        # Retrieve related context
        try:
            retrieved = cm.retrieve(user_text)
        except Exception as e:  # noqa: BLE001
            logger.exception("Retrieval failed: %s", e)
            retrieved = []

        full_prompt = build_prompt(user_text, retrieved)

        # Generate via Codex CLI (exec mode for non-interactive)
        try:
            code, out, err = codex.run(["exec", *codex_args, full_prompt])
        except CodexCLIError as e:
            console.print(f"[err]Codex CLI error: {e}[/err]")
            return 2

        if err:
            logger.warning("codex stderr: %s", err.strip())

        # Display assistant response
        response = out if out else ""
        console.print(Panel(response.strip(), title="Assistant", border_style="ok"))

        # Learn: store new pair
        try:
            cm.remember(user_text, response)
        except Exception as e:  # noqa: BLE001
            logger.exception("Failed to store memory: %s", e)

        # Also store lightweight history
        if hist_db is not None:
            hist_db.execute(
                "INSERT INTO history (ts, prompt, response, tags, tokens) VALUES (strftime('%s','now'), ?, ?, ?, ?)",
                (user_text, response, json.dumps([]), len(user_text.split()) + len(response.split())),
            )
            hist_db.commit()

    if hist_db is not None:
        hist_db.close()
    return 0


if __name__ == "__main__":
    # Allow running standalone: python -m cli.codex_cli.cli
    cfg_path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).with_name("config.yaml"))
    sys.exit(run_repl(cfg_path))

