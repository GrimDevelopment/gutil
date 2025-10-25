from __future__ import annotations

import json
import os
from typing import Any, Dict


CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".gutil")
CONFIG_PATH = os.path.join(CONFIG_DIR, "app.json")


def ensure_config_dir() -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)


def load_app_config() -> Dict[str, Any]:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_app_config(cfg: Dict[str, Any]) -> None:
    ensure_config_dir()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

