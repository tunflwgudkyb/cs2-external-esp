from __future__ import annotations

from cs2esp.core.process_handle import ProcessHandle
from cs2esp.features.base import BaseFeature
from cs2esp.lib.vec3 import Vec3
from cs2esp.offsets.resolver import resolve

MAX_PLAYERS = 64


class ESPFeature(BaseFeature):
    name = "esp"

    def tick(self, handle: ProcessHandle, overlay) -> None:
        client = handle.module_base
        view_matrix = handle.read_matrix(client + resolve("dwViewMatrix"))
        local = handle.read_int(client + resolve("dwLocalPlayerPawn"))
        if not local:
            return
        local_team = handle.read_int(local + resolve("m_iTeamNum"))
        local_pos = Vec3(*handle.read_vec3(local + resolve("m_vOldOrigin")))

        for i in range(1, MAX_PLAYERS):
            entity = handle.read_int(client + resolve("dwEntityList") + i * 0x78)
            if not entity:
                continue
            if handle.read_int(entity + resolve("m_iTeamNum")) == local_team:
                continue
            pos = Vec3(*handle.read_vec3(entity + resolve("m_vOldOrigin")))
            if pos.distance_to(local_pos) > self.options.get("max_distance_m", 250):
                continue
            screen = pos.to_screen(view_matrix, overlay.width, overlay.height)
            if screen:
                overlay.draw_box(screen[0] - 20, screen[1] - 60, 40, 100,
                                 color=self.options.get("color", "#ff3b30"))