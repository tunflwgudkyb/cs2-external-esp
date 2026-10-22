from __future__ import annotations

import time

import keyboard

from cs2esp.core.process_handle import ProcessHandle
from cs2esp.features.feature_registry import build_enabled_features
from cs2esp.lib.logger import get_logger
from cs2esp.overlay.win32_overlay import Win32Overlay


class OverlayLoop:
    def __init__(self, handle: ProcessHandle, cfg: dict):
        self.handle = handle
        self.cfg = cfg
        self.log = get_logger(cfg["app"]["log_level"])
        self.features = build_enabled_features(cfg)
        self.overlay = Win32Overlay(cfg["overlay"])
        self._running = True

    def run(self) -> None:
        keyboard.add_hotkey("f8", self._shutdown)
        interval = self.cfg["process"]["poll_interval_ms"] / 1000.0
        self.log.info("overlay loop started, press F8 to stop")
        while self._running:
            frame = self.overlay.begin_frame()
            for feat in self.features:
                try:
                    feat.tick(self.handle, self.overlay)
                except Exception as exc:  # noqa: BLE001
                    self.log.warning("feature %s error: %s", feat.name, exc)
            self.overlay.end_frame(frame)
            time.sleep(interval)

    def _shutdown(self) -> None:
        self._running = False