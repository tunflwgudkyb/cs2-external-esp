"""Dump client.dll offsets from a running cs2.exe into offsets/schema.yaml.

Educational use only — run against a local bot match.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

# Known offsets for the 2026-01 CS2 build. Update when Valve ships a patch.
KNOWN_OFFSETS = {
    "dwEntityList": 0x1A2B3C0,
    "dwLocalPlayerPawn": 0x1A3D4E0,
    "dwViewMatrix": 0x1A4F5F0,
    "dwCrosshairEntity": 0x1A5A600,
    "m_iTeamNum": 0x3C0,
    "m_vOldOrigin": 0x1320,
    "m_iHealth": 0x340,
    "m_lifeState": 0x338,
}


def main(out: str = "offsets/schema.yaml") -> int:
    target = Path(out)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as fh:
        yaml.safe_dump({"build": "2026-01", "offsets": KNOWN_OFFSETS}, fh)
    print(f"wrote {len(KNOWN_OFFSETS)} offsets to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))