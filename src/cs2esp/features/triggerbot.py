from __future__ import annotations

import time

import keyboard

from cs2esp.core.process_handle import ProcessHandle
from cs2esp.features.base import BaseFeature
from cs2esp.offsets.resolver import resolve


class TriggerbotFeature(BaseFeature):
    name = "triggerbot"

    def tick(self, handle: ProcessHandle, overlay) -> None:
        if not keyboard.is_pressed("alt"):
            return
        client = handle.module_base
        crosshair_id = handle.read_int(client + resolve("dwCrosshairEntity"))
        if crosshair_id == -1:
            return
        time.sleep(self.options.get("delay_ms", 45) / 1000.0)
        overlay.click()