#!/usr/bin/env python3
"""Amorce docs/Matiere/registre_ids.csv depuis les wav déjà présents dans SONS_V3/.

Migration unique du 20 août 2026, pour la réponse A à Q21 (ID stables).

Sans registre, la première découpe incrémentale ne reconnaîtrait aucun des 526
fichiers existants et en créerait autant de doublons. On reconstruit donc le
registre à partir de deux sources :

  - les temps de début/fin, depuis l'inventaire de la découpe du 18 août
    (archivé dans docs/archive/matiere_v2_v3/) ;
  - le bucket réel, depuis **le disque** et non l'inventaire — 42 fichiers
    d'ambiance ont été déplacés à la main vers CORTEX/FRAGMENTS le 18 août,
    et ce rangement à l'oreille doit être préservé.

Le rôle (TRACK / AMBIANCE) est déduit du master d'origine, pas du dossier :
un A0xx rangé dans FRAGMENTS reste un segment du master d'ambiance.

Idempotent : relancer ne change rien si le registre est déjà complet.

Usage:
  python3 scripts/proto07/amorcer_registre_ids.py --dry-run
  python3 scripts/proto07/amorcer_registre_ids.py
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SONS = ROOT / "SONS_V3"
INVENTAIRE_ARCHIVE = (
    ROOT / "docs" / "archive" / "matiere_v2_v3" / "19_proto_07_journal_decoupe_v3.csv"
)
REGISTRE = ROOT / "docs" / "Matiere" / "registre_ids.csv"

ETATS = ("CORTEX", "HIPPOCAMPE", "RECONSTRUCTION")
BUCKETS = ("FRAGMENTS", "AMBIANCE", "LONG_MOYEN")
REG_FIELDS = ["id", "etat", "role", "bucket", "src", "start", "end", "dur", "ajoute_le"]


def role_du_master(src: str) -> str:
    """Le master 'Cortex ambiance' produit des segments de rôle AMBIANCE."""
    return "AMBIANCE" if "cortex ambiance" in src.lower() else "TRACK"


def wavs_sur_disque() -> dict[str, tuple[str, str]]:
    """id -> (etat, bucket) tel que rangé aujourd'hui."""
    out = {}
    for etat in ETATS:
        for bucket in BUCKETS:
            folder = SONS / etat / bucket
            if not folder.is_dir():
                continue
            for wav in folder.glob("*.wav"):
                out[wav.stem] = (etat, bucket)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not INVENTAIRE_ARCHIVE.is_file():
        print(f"Inventaire archivé introuvable : {INVENTAIRE_ARCHIVE}", file=sys.stderr)
        return 1

    disque = wavs_sur_disque()
    if not disque:
        print(f"Aucun wav sous {SONS} : rien à amorcer.", file=sys.stderr)
        return 1

    with INVENTAIRE_ARCHIVE.open(newline="", encoding="utf-8") as f:
        inventaire = {r["file"].removesuffix(".wav"): r for r in csv.DictReader(f)}

    deja = {}
    if REGISTRE.is_file():
        with REGISTRE.open(newline="", encoding="utf-8") as f:
            deja = {r["id"]: r for r in csv.DictReader(f)}

    entries, sans_temps, deplaces = [], [], 0
    for stem, (etat, bucket) in sorted(disque.items()):
        if stem in deja:
            entries.append(deja[stem])
            continue
        inv = inventaire.get(stem)
        if inv is None:
            sans_temps.append(stem)
            continue
        if inv["bucket"] != bucket:
            deplaces += 1
        entries.append({
            "id": stem,
            "etat": etat,
            "role": role_du_master(inv["src"]),
            "bucket": bucket,
            "src": inv["src"],
            "start": inv["start"],
            "end": inv["end"],
            "dur": inv["dur"],
            "ajoute_le": "2026-08-18",
        })

    orphelins_inv = sorted(set(inventaire) - set(disque))

    print(f"wav sur le disque      : {len(disque)}")
    print(f"lignes dans l'inventaire: {len(inventaire)}")
    print(f"entrées écrites        : {len(entries)}")
    print(f"  dont déjà au registre: {sum(1 for e in entries if e['id'] in deja)}")
    print(f"rangés à la main (bucket ≠ inventaire, disque conservé) : {deplaces}")
    if sans_temps:
        print(f"\n⚠ {len(sans_temps)} wav sans temps connus (absents de l'inventaire) :")
        for s in sans_temps[:15]:
            print(f"    {s}")
        if len(sans_temps) > 15:
            print(f"    … et {len(sans_temps) - 15} autres")
        print("  Ces fichiers ne seront pas reconnus par la découpe incrémentale.")
    if orphelins_inv:
        print(f"\n{len(orphelins_inv)} ligne(s) d'inventaire sans wav sur le disque "
              f"(supprimés à la main, ignorés)")
        for s in orphelins_inv[:10]:
            print(f"    {s}")

    if args.dry_run:
        print("\ndry-run : rien écrit.")
        return 0

    REGISTRE.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=REG_FIELDS)
        w.writeheader()
        w.writerows(entries)
    print(f"\nOK {REGISTRE.relative_to(ROOT)}  ({date.today().isoformat()})")
    print("Vérifier ensuite : python3 scripts/slice_opacite_v3.py --dry-run")
    print("→ doit annoncer 0 nouveau et ~526 réutilisés.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
