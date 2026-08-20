"""Chemins SONS_V3 — pool d'ambiances partagé à la racine."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SONS = ROOT / "SONS_V3"
AMBIANCE_DIR = SONS / "AMBIANCE"
ETATS = ("CORTEX", "HIPPOCAMPE", "RECONSTRUCTION")
ZONE_BUCKETS = ("FRAGMENTS", "LONG_MOYEN")


def is_ambiance(entry: dict) -> bool:
    return entry.get("role") == "AMBIANCE" or entry.get("bucket") == "AMBIANCE"


def wav_path(entry: dict) -> Path:
    """Chemin d'un fragment depuis une ligne du registre."""
    stem = entry["id"]
    if is_ambiance(entry):
        return AMBIANCE_DIR / f"{stem}.wav"
    return SONS / entry["etat"] / entry["bucket"] / f"{stem}.wav"


def dest_dir(etat: str, bucket: str) -> Path:
    if bucket == "AMBIANCE":
        return AMBIANCE_DIR
    return SONS / etat / bucket


def find_on_disk(etat: str, stem: str) -> Path | None:
    """Cherche un wav (pool partagé + emplacements legacy)."""
    shared = AMBIANCE_DIR / f"{stem}.wav"
    if shared.is_file():
        return shared
    for bucket in (*ZONE_BUCKETS, "AMBIANCE"):
        p = SONS / etat / bucket / f"{stem}.wav"
        if p.is_file():
            return p
    return None
