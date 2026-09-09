#!/usr/bin/env python3
"""Génère docs/Matiere/catalogue_batch4.xlsx — classeur vierge batch 4 seulement.

Ne lit pas catalogue_fragments.xlsx (collègue termine la V6 séparément).
Filtre via registre_ids.csv · src = masters SONS batch 4/.

Feuilles : Cortex · Hippocampe · Reconstruction (vide si master absent) · Ambiances.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRE = ROOT / "docs" / "Matiere" / "registre_ids.csv"
OUT = ROOT / "docs" / "Matiere" / "catalogue_batch4.xlsx"

# Masters batch 4 (reconstruction exclue — master silencieux sep. 2026)
BATCH4_SRC = (
    "new cortex last.wav",
    "new hippocampe last.wav",
    "new Ambiance",  # « général » — préfixe stable (accents normalisés côté registre)
)

NOTE_HEADER = (
    "Batch 4 — sep. 2026 · classeur neuf · ne pas confondre avec catalogue_fragments.xlsx. "
    "Reconstruction : master batch 4 vide (−91 dBFS) — pas de samples pour l'instant."
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_catalogue_xlsx import (  # noqa: E402
    AMBIANCE_COLUMNS,
    AMBIANCE_SHEET,
    BUCKET_TYPE,
    HIPPO_COLUMNS,
    NOTE_AMBIANCE,
    NOTE_PAROLE,
    PAROLE_COLUMNS,
    RECON_COLUMNS,
    ZONES,
    _natkey,
    load_registre_masters,
    scan_ambiances,
    wav_duration,
    write_sheet,
)
from openpyxl import Workbook  # noqa: E402


def _is_batch4_src(src: str) -> bool:
    s = (src or "").strip()
    return any(m in s for m in BATCH4_SRC)


def load_batch4_ids() -> dict[str, set[str]]:
    """etat -> stems · plus set ambiance."""
    if not REGISTRE.is_file():
        sys.exit(f"Registre introuvable: {REGISTRE}")
    by_etat: dict[str, set[str]] = {e: set() for e, _ in ZONES}
    amb: set[str] = set()
    with REGISTRE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not _is_batch4_src(row.get("src", "")):
                continue
            sid = (row.get("id") or "").strip()
            if not sid:
                continue
            if row.get("role") == "AMBIANCE":
                amb.add(sid)
            else:
                etat = row.get("etat", "")
                if etat in by_etat:
                    by_etat[etat].add(sid)
    return {"zones": by_etat, "amb": amb}


def scan_zone_batch4(etat: str, stems: set[str]) -> list[dict]:
    if not stems:
        return []
    rows = []
    sons = ROOT / "SONS_V3"
    for bucket, typ in BUCKET_TYPE.items():
        folder = sons / etat / bucket
        if not folder.is_dir():
            continue
        for wav in sorted(folder.glob("*.wav"), key=lambda p: _natkey(p.name)):
            if wav.stem not in stems:
                continue
            rows.append({
                "id": wav.stem,
                "type": typ,
                "duree_s": round(wav_duration(wav), 2),
                "_bucket": bucket,
            })
    rows.sort(key=lambda r: (r["type"] != "court", r["type"] != "long", _natkey(r["id"])))
    return rows


def scan_ambiances_batch4(stems: set[str], masters: dict[str, str]) -> list[dict]:
    if not stems:
        return []
    amb_dir = ROOT / "SONS_V3" / "AMBIANCE"
    rows = []
    for wav in sorted(amb_dir.glob("*.wav"), key=lambda p: _natkey(p.name)):
        if wav.stem not in stems:
            continue
        rows.append({
            "id": wav.stem,
            "duree_s": round(wav_duration(wav), 2),
            "master": masters.get(wav.stem, ""),
        })
    return rows


def main() -> None:
    ids = load_batch4_ids()
    masters = load_registre_masters()
    manual: dict = {}

    wb = Workbook()
    wb.remove(wb.active)

    print("catalogue_batch4.xlsx")
    total = 0
    for etat, title in ZONES:
        files = scan_zone_batch4(etat, ids["zones"][etat])
        total += len(files)
        if etat == "HIPPOCAMPE":
            cols, extra = HIPPO_COLUMNS, " Colonnes associatives Simon §13.1."
        elif etat == "RECONSTRUCTION":
            cols, extra = RECON_COLUMNS, " Aucun sample Recon batch 4 (master silencieux)."
        else:
            cols, extra = PAROLE_COLUMNS, ""
        note = NOTE_HEADER + extra + " " + NOTE_PAROLE if etat != "RECONSTRUCTION" else NOTE_HEADER + extra
        write_sheet(
            wb, title, f"{etat}/ batch4 · {note}",
            cols, files, manual.get(title, {}),
            type_comment_idx=2 if etat != "RECONSTRUCTION" else None,
        )
        print(f"  {title}: {len(files)} lignes (batch 4)")

    amb = scan_ambiances_batch4(ids["amb"], masters)
    write_sheet(
        wb, AMBIANCE_SHEET, NOTE_HEADER + " " + NOTE_AMBIANCE,
        AMBIANCE_COLUMNS, amb, {},
        tab_color="4A235A", type_comment_idx=None,
    )
    print(f"  {AMBIANCE_SHEET}: {len(amb)} lignes (batch 4)")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    total += len(amb)
    print(f"OK {OUT.relative_to(ROOT)}")
    print(f"Total batch 4: {total} samples")


if __name__ == "__main__":
    main()
