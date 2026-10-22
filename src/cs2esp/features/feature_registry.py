from __future__ import annotations

from cs2esp.features.base import BaseFeature
from cs2esp.features.esp import ESPFeature
from cs2esp.features.aimbot import AimbotFeature
from cs2esp.features.radar import RadarFeature
from cs2esp.features.triggerbot import TriggerbotFeature

_REGISTRY: dict[str, type[BaseFeature]] = {
    "esp": ESPFeature,
    "aimbot": AimbotFeature,
    "radar": RadarFeature,
    "triggerbot": TriggerbotFeature,
}


def build_enabled_features(cfg: dict) -> list[BaseFeature]:
    feats: list[BaseFeature] = []
    for name, cls in _REGISTRY.items():
        sub = cfg.get("features", {}).get(name, {})
        if sub.get("enabled"):
            feats.append(cls(sub))
    return feats