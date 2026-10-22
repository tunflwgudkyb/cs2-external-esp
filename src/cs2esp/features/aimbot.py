from __future__ import annotations

import math

import keyboard

from cs2esp.core.process_handle import ProcessHandle
from cs2esp.features.base import BaseFeature
from cs2esp.lib.vec3 import Vec3
from cs2esp.offsets.resolver import resolve


class AimbotFeature(BaseFeature):
    """Educational aimbot demo — moves the mouse toward the nearest enemy
    bone within an FOV cone while a hotkey is held."""

    name = "aimbot"

    def tick(self, handle: ProcessHandle, overlay) -> None:
        if not keyboard.is_pressed("shift"):
            return
        client = handle.module_base
        local = handle.read_int(client + resolve("dwLocalPlayerPawn"))
        if not local:
            return
        local_pos = Vec3(*handle.read_vec3(local + resolve("m_vOldOrigin")))
        local_team = handle.read_int(local + resolve("m_iTeamNum"))

        best = None
        best_dist = float("inf")
        for i in range(1, 64):
            ent = handle.read_int(client + resolve("dwEntityList") + i * 0x78)
            if not ent or handle.read_int(ent + resolve("m_iTeamNum")) == local_team:
                continue
            head = Vec3(*handle.read_vec3(ent + resolve("m_vOldOrigin")))
            d = local_pos.distance_to(head)
            if d < best_dist:
                best, best_dist = head, d

        if best is None:
            return
        delta = best - local_pos
        yaw = math.degrees(math.atan2(delta.y, delta.x))
        overlay.move_mouse_smooth(yaw, self.options.get("smoothing", 4.0))