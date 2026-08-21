"""Gain de normalisation depuis docs/Matiere/registre_ids.csv."""
from __future__ import annotations

import csv
import math
import os


def gain_map_from_registre(root: str) -> dict[str, float]:
    """id fragment (sans .wav) → gain linéaire."""
    path = os.path.join(root, "docs", "Matiere", "registre_ids.csv")
    out: dict[str, float] = {}
    if not os.path.isfile(path):
        return out
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            gid = (row.get("id") or "").strip()
            gdb = (row.get("gain_db") or "").strip()
            if not gid or not gdb:
                continue
            try:
                out[gid] = 10 ** (float(gdb) / 20.0)
            except ValueError:
                pass
    return out


def linear_gain_for_rel(rel: str, gain_map: dict[str, float], default: float = 1.0) -> float:
    stem = os.path.splitext(os.path.basename(rel))[0]
    return gain_map.get(stem, default)


def fmt_gain(g: float) -> str:
    return f"{g:.4f}"
