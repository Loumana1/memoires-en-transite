#!/usr/bin/env python3
"""Précalcule les formes Reconstruction V1 pour Pure Data.

Proto sur les 287 fichiers FRAGMENTS sans tags Simon (Q32/Q33).
Silences ≤ 4 s (Q34), apparitions rapides, garde-fous R12/R13 anti fausse citation.

Sorties :
  pd/lib/recon_formes/events.txt    — séquence planifiée (~120 s d'état)
  pd/lib/recon_formes/recipe.json   — recette pour REINJECTER / Boucle (Q35)
"""
from __future__ import annotations

import json
import os
import random
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "proto08"))

from proto08_lib import sons_audit08 as audit  # noqa: E402
from proto08_lib.recon_recipes import SPATIAL_NAMES  # noqa: E402

OUT_DIR = ROOT / "pd" / "lib" / "recon_formes"
XLSX = ROOT / "docs" / "Matiere" / "catalogue_fragments.xlsx"
STATE_MS = 120_000
MAX_SILENCE_MS = 4000
MIN_GAP_MS = 400
MAX_RECOGNIZABLE_CHAIN = 2  # R12/R13 — pas plus de 2 fragments « lisibles » d'affilée


def _read_recon_catalog() -> list[dict]:
    rows: list[dict] = []
    if not XLSX.is_file():
        return rows
    try:
        import openpyxl
    except ImportError:
        print("WARN: openpyxl absent — catalogue Reconstruction ignoré")
        return rows
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    try:
        if "Reconstruction" not in wb.sheetnames:
            return rows
        ws = wb["Reconstruction"]
        hdr = list(ws.iter_rows(min_row=2, max_row=2, values_only=True))
        if not hdr or not hdr[0]:
            return rows
        headers = [str(h or "").strip().lower() for h in hdr[0]]
        key_map = {h.replace(" ", "_"): i for i, h in enumerate(headers)}

        def get(row, key: str) -> str:
            ci = key_map.get(key)
            if ci is None or ci >= len(row) or row[ci] is None:
                return ""
            return str(row[ci]).strip()

        for row in ws.iter_rows(min_row=3, values_only=True):
            if not row or not row[0]:
                continue
            sid = str(row[0]).strip()
            rows.append({
                "id": sid,
                "type_matiere": get(row, "type_matiere"),
                "role_compositionnel": get(row, "role_compositionnel"),
                "mutabilite": get(row, "mutabilite") or "2",
                "mode_lecture": get(row, "mode_lecture"),
                "charge_semantique": get(row, "charge_semantique"),
                "potentiel_compositionnel": get(row, "potentiel_compositionnel"),
            })
    finally:
        wb.close()
    return rows


def _pool_from_disk() -> tuple[list[str], list[str]]:
    u = audit.usable_files(str(ROOT), verbose=False)
    longs = u.get((2, 1), []) or []
    shorts = u.get((2, 0), []) or []
    if not longs:
        longs = [p for p in shorts if _wav_duration_sec(ROOT / p) >= 8.0]
    if not longs:
        longs = shorts[: max(1, len(shorts) // 8)]
    if not shorts:
        shorts = longs
    return longs, shorts


def _wav_duration_sec(path: Path) -> float:
    try:
        with wave.open(str(path), "rb") as w:
            rate = w.getframerate()
            if rate <= 0:
                return 0.0
            return w.getnframes() / rate
    except Exception:
        return 0.0


def _dur_ms(rel: str) -> int:
    d = _wav_duration_sec(ROOT / rel)
    return max(500, int(d * 1000))


def _stem(rel: str) -> str:
    return Path(rel).stem


def _heuristic_role(rel: str, is_long: bool) -> str:
    d = _wav_duration_sec(ROOT / rel)
    if is_long or d >= 8.0:
        return "FIL"
    if d < 2.5:
        return "TRACE"
    if d < 5.0:
        return "SUTURE"
    return "CONTRASTE"


def _semantic_weight(row: dict | None) -> int:
    if not row:
        return 1
    charge = (row.get("charge_semantique") or "").upper()
    if charge == "FORTE":
        return 3
    if charge == "MOYENNE":
        return 2
    return 1


def _pick(rng: random.Random, pool: list[str], avoid: set[str]) -> str:
    candidates = [p for p in pool if _stem(p) not in avoid]
    if not candidates:
        candidates = pool
    return rng.choice(candidates)


def build_forme(
    longs: list[str],
    shorts: list[str],
    catalog: dict[str, dict],
    rng: random.Random,
) -> tuple[list[dict], dict]:
    """Construit events + recette JSON."""
    events: list[dict] = []
    used_ids: list[str] = []
    t = 0
    recognizable_run = 0
    spatial_idx = rng.randint(0, len(SPATIAL_NAMES) - 1)
    type_forme = rng.choice(("AGENCEMENT", "SUPERPOSITION", "SUTURE_OUVERTE", "TRACE"))
    densite = rng.choice(("AEREE", "MOYENNE", "DENSE"))
    courbe = rng.choice(
        ("CLAIR_VERS_OPAQUE", "OPAQUE_VERS_CLAIR", "OSCILLANTE", "STABLE")
    )
    resolution = rng.choice(("FERMETURE", "SUSPENSION", "DISSOLUTION", "TRACE"))

    fil = _pick(rng, longs, set())
    used_ids.append(_stem(fil))
    events.append({"t": t, "action": "play", "layer": 1, "source": _stem(fil)})
    t += rng.randint(800, 1800)

    n_interrupts = rng.randint(5, 8)
    for _ in range(n_interrupts):
        if t >= STATE_MS - 8000:
            break
        src = _pick(rng, shorts, set(used_ids[-6:]))
        sid = _stem(src)
        row = catalog.get(sid)
        sem = _semantic_weight(row)
        role = (row or {}).get("role_compositionnel") or _heuristic_role(src, False)

        if sem >= 2 and recognizable_run >= MAX_RECOGNIZABLE_CHAIN:
            # R12/R13 — insérer silence ou fragment faible charge
            silence = rng.randint(800, MAX_SILENCE_MS)
            events.append({"t": t, "action": "silence", "duration_ms": silence})
            t += silence + MIN_GAP_MS
            recognizable_run = 0
            src = _pick(rng, shorts, set(used_ids[-4:]))
            sid = _stem(src)
            sem = 1

        events.append({"t": t, "action": "play", "layer": 2, "source": sid, "role": role})
        used_ids.append(sid)
        recognizable_run = recognizable_run + 1 if sem >= 2 else 0
        t += rng.randint(2200, 4800)

        if rng.random() < 0.35:
            fade = rng.randint(35, 100)
            events.append({"t": t, "action": "cut", "layer": 2, "fade_ms": fade})
            t += fade + rng.randint(200, 800)

        if rng.random() < 0.15 and t < STATE_MS - 12000:
            events.append({"t": t, "action": "spatial", "recipe": spatial_idx})
            t += rng.randint(1500, 4000)

        if rng.random() < 0.12:
            silence = rng.randint(500, MAX_SILENCE_MS)
            events.append({"t": t, "action": "silence", "duration_ms": silence})
            t += silence
            recognizable_run = 0

        t += rng.randint(800, 1800)

    # Relance fil L1 vers mi-forme si assez de longs
    if len(longs) > 1 and STATE_MS > 45000:
        t_mid = rng.randint(35000, 55000)
        fil2 = _pick(rng, longs, set(used_ids[:3]))
        events.append({"t": t_mid, "action": "play", "layer": 1, "source": _stem(fil2)})
        used_ids.append(_stem(fil2))

    events = [e for e in events if e["t"] <= STATE_MS]
    events.sort(key=lambda e: e["t"])

    recipe = {
        "version": 1,
        "type_forme": type_forme,
        "densite_composition": densite,
        "courbe_reconnaissabilite": courbe,
        "mode_spatial": SPATIAL_NAMES[spatial_idx],
        "resolution_forme": resolution,
        "silence_apres_forme_s": rng.randint(1, 4),
        "ids": used_ids,
        "spatial_recipe": spatial_idx,
        "duree_etat_ms": STATE_MS,
    }
    return events, recipe


def write_outputs(events: list[dict], recipe: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ev_path = OUT_DIR / "events.txt"
    with ev_path.open("w", encoding="utf-8") as fh:
        fh.write("# delay_ms action layer [fade_ms|recipe|duration_ms]\n")
        for e in events:
            act = e["action"]
            if act == "silence":
                fh.write(f"{e['t']} silence 0 {e.get('duration_ms', 1000)}\n")
            elif act == "spatial":
                fh.write(f"{e['t']} spatial 0 {e.get('recipe', 0)}\n")
            elif act == "cut":
                fh.write(f"{e['t']} cut {e['layer']} {e.get('fade_ms', 50)}\n")
            else:
                fh.write(f"{e['t']} play {e['layer']} 0\n")
    recipe_path = OUT_DIR / "recipe.json"
    with recipe_path.open("w", encoding="utf-8") as fh:
        json.dump(recipe, fh, ensure_ascii=False, indent=2)
    print(f"OK {ev_path.relative_to(ROOT)} ({len(events)} events)")
    print(f"OK {recipe_path.relative_to(ROOT)}")


def main() -> None:
    seed = int(os.environ.get("RECON_FORMES_SEED", "42"))
    rng = random.Random(seed)
    catalog_rows = _read_recon_catalog()
    catalog = {r["id"]: r for r in catalog_rows}
    longs, shorts = _pool_from_disk()
    if not longs and not shorts:
        raise SystemExit("RECONSTRUCTION: aucun fichier utilisable")
    events, recipe = build_forme(longs, shorts, catalog, rng)
    write_outputs(events, recipe)


if __name__ == "__main__":
    main()
