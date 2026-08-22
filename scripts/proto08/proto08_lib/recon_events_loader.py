"""Charge pd/lib/recon_formes/events.txt pour le générateur Pd."""
from __future__ import annotations

import os

DEFAULT_EVENTS = [
    {"t": 0, "action": "play", "layer": 1},
    {"t": 2500, "action": "play", "layer": 2},
    {"t": 5200, "action": "cut", "layer": 2, "fade_ms": 70},
    {"t": 7000, "action": "spatial", "recipe": 2},
    {"t": 9500, "action": "play", "layer": 2},
    {"t": 14000, "action": "silence", "duration_ms": 2000},
]


def load_events(libdir: str) -> list[dict]:
    path = os.path.join(libdir, "recon_formes", "events.txt")
    if not os.path.isfile(path):
        return list(DEFAULT_EVENTS)
    out: list[dict] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                t = int(parts[0])
            except ValueError:
                continue
            act = parts[1]
            ev: dict = {"t": t, "action": act}
            if act in ("play", "cut") and len(parts) >= 3:
                ev["layer"] = int(parts[2])
            if act == "cut" and len(parts) >= 4:
                ev["fade_ms"] = int(parts[3])
            if act == "spatial" and len(parts) >= 4:
                ev["recipe"] = int(parts[3])
            if act == "silence" and len(parts) >= 4:
                ev["duration_ms"] = int(parts[3])
            out.append(ev)
    return out or list(DEFAULT_EVENTS)
