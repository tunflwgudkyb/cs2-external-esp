from __future__ import annotations

from cs2esp.core.process_handle import ProcessHandle
from cs2esp.features.base import BaseFeature
from cs2esp.offsets.resolver import resolve


class RadarFeature(BaseFeature):
    name = "radar"

    def tick(self, handle: ProcessHandle, overlay) -> None:
        client = handle.module_base
        local = handle.read_int(client + resolve("dwLocalPlayerPawn"))
        if not local:
            return
        scale = self.options.get("scale", 0.35)
        overlay.begin_radar(scale)
        for i in range(1, 64):
            ent = handle.read_int(client + resolve("dwEntityList") + i * 0x78)
            if not ent:
                continue
            pos = handle.read_vec3(ent + resolve("m_vOldOrigin"))
            overlay.plot_radar_point(pos[0], pos[1])
        overlay.end_radar()