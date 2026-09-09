"""Charge pd/lib/hippo_assoc/events.txt pour le générateur Pd."""
from __future__ import annotations

import os

DEFAULT_EVENTS = [
    {"t": 1800, "action": "play", "layer": 3},
    {"t": 3200, "action": "play", "layer": 4},
    {"t": 5500, "action": "cut", "layer": 3, "fade_ms": 50},
    {"t": 8000, "action": "motion", "recipe": 2},
]


def load_events(libdir: str) -> list[dict]:
    path = os.path.join(libdir, "hippo_assoc", "events.txt")
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
            if act == "play" and len(parts) >= 5:
                ev["slot"] = int(parts[3])
                ev["index"] = int(parts[4])
                if len(parts) >= 6:
                    p = parts[5]
                    ev["path"] = p if p != "0" else None
            elif act == "play" and len(parts) >= 4:
                # Ancien format : chemin seul (fallback index -1)
                p4 = parts[3]
                ev["path"] = p4 if p4 != "0" else None
                ev["index"] = -1
            if act == "motion" and len(parts) >= 4:
                ev["recipe"] = int(parts[3])
            out.append(ev)
    return out or list(DEFAULT_EVENTS)
