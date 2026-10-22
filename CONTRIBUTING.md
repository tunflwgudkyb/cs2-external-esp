# Contributing to cs2-external-esp

Thanks for wanting to help. This project is a **purely educational** external
cheat framework for CS2 — used to study how memory reading, overlay rendering,
and offset resolution work in practice. Do not use it on live servers.

## Ground rules

1. **Educational only.** PRs that add anti-cheat bypasses against Valve's
   VAC / VAC Live, or that target live matchmaking, will be rejected.
2. Keep modules **external** — no DLL injection, no kernel drivers.
3. Every new feature module lives under `src/cs2esp/features/` and must
   register itself through `feature_registry.py`.
4. Offsets go in `offsets/schema.yaml`, never hardcoded in feature code.

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m cs2esp --dry-run
```

## Style

- Ruff + black, 100 col.
- Type hints on public functions.
- No `print()` in feature code — use `cs2esp.lib.logger`.

## Testing

```bash
pytest tests/ -v
```

Offsets and memory readers are mocked in `tests/` so nothing touches a real
`cs2.exe` process during CI.