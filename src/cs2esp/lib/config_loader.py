from __future__ import annotations

from pathlib import Path

import yaml


def load_config(path: str | Path) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"config not found: {p}")
    with p.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    _apply_defaults(data)
    return data


def _apply_defaults(cfg: dict) -> None:
    cfg.setdefault("app", {}).setdefault("log_level", "info")
    cfg.setdefault("process", {}).setdefault("poll_interval_ms", 16)
    cfg.setdefault("overlay", {}).setdefault("fps_cap", 144)
    cfg.setdefault("features", {})