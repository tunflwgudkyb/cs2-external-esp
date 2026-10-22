"""Entry point: parse args, load config, spin up the overlay loop."""
from __future__ import annotations

import argparse
import sys

from cs2esp.lib.config_loader import load_config
from cs2esp.lib.logger import get_logger
from cs2esp.core.process_handle import ProcessHandle
from cs2esp.core.overlay_loop import OverlayLoop
from cs2esp.features.feature_registry import build_enabled_features


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cs2esp")
    parser.add_argument("--config", default="config/default.yaml")
    parser.add_argument("--dry-run", action="store_true",
                        help="load config and features without attaching")
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    log = get_logger(cfg["app"]["log_level"])
    log.info("cs2-external-esp v%s starting", cfg["app"]["version"])

    if args.dry_run:
        feats = build_enabled_features(cfg)
        log.info("dry-run: %d feature(s) enabled: %s",
                 len(feats), [f.name for f in feats])
        return 0

    try:
        handle = ProcessHandle.attach(cfg["process"]["executable"],
                                      cfg["process"]["module"])
    except Exception as exc:  # noqa: BLE001
        log.error("failed to attach to %s: %s", cfg["process"]["executable"], exc)
        return 2

    loop = OverlayLoop(handle, cfg)
    try:
        loop.run()
    except KeyboardInterrupt:
        log.info("shutdown requested")
    finally:
        handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())