"""Pool d'ambiances Proto 08 — musicale vs texture (Cortex).

Historique : 22 août — pool mélodique unique A45–A69 pour les deux nappes
(anti-doublon patch). Problème à l'écoute : deux nappes **musicales**
différentes en même temps, peu plaisant.

24 août 2026 — Loumana désigne deux listes :
  · **musicale** (HP7) : `FAVORIS_CORTEX` (A53, A54, A59, A64–A68)
  · **texture** (HP5) : `FAVORIS_TEXTURE_CORTEX` (A04, A16–A21, A38–A41, A49–A50)

Les slots 32 / 33 tirent dans des pools **disjoints**. L'anti-doublon du patch
reste utile si deux tirages identiques dans un même pool.

Pool mélodique large A45–A69 : Hippocampe / Reconstruction (slot 40 / 41).
Seuil durée mélodique : [Q3](docs/Backlog/Q&A.md#q3) — 25 s (A53 à 29,5 s inclus).
Les textures désignées explicitement ne passent pas ce filtre (segments courts OK).
"""
from __future__ import annotations

import csv
import os
import re

SONS_AMB = "SONS_V3/AMBIANCE"
REGISTRE = os.path.join("docs", "Matiere", "registre_ids.csv")

# Bornes de la sélection mélodique, sur le numéro d'ID (A45 … A69).
ID_MIN = 45
ID_MAX = 69
# En dessous, un fichier ne tient pas comme nappe (voir en-tête).
MIN_DUR_S = 25.0

# Préférées Loumana — nappe **musicale** Cortex (HP7), slot 32.
FAVORIS_CORTEX = ("A53", "A54", "A59", "A64", "A65", "A66", "A67", "A68")

# Préférées Loumana — nappe **texture** Cortex (HP8), slot 33. 24 août 2026.
FAVORIS_TEXTURE_CORTEX = (
    "A04", "A16", "A17", "A18", "A19", "A20", "A21",
    "A38", "A39", "A40", "A41", "A49", "A50",
)

# Correctif pics à l'oreille (RMS normalisé mais transitoires forts) — dB relatif slot 33.
TEXTURE_TRIM_DB: dict[str, float] = {
    "A17": -4.0,
    "A18": -6.0,
    "A19": -5.0,
    "A21": -3.0,
}

# Loumana fournira la liste (stems Axx). Tant que vide → comportement actuel
# (usable_ambiance HIPPOCAMPE tire dans le pool mélodique complet A45–A69).
# TO DO : coller la liste ici quand Loumana la désigne, ex. :
#   FAVORIS_HIPPO = ("A48", "A52", "A61")
FAVORIS_HIPPO: tuple[str, ...] = ()

_ID_RE = re.compile(r"^A(\d+)")


def _id_num(sid: str) -> int | None:
    m = _ID_RE.match(sid.strip().upper())
    return int(m.group(1)) if m else None


def _read_registre_amb(root: str) -> list[dict]:
    path = os.path.join(root, REGISTRE)
    if not os.path.isfile(path):
        return []
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("role") != "AMBIANCE":
                continue
            sid = (row.get("id") or "").strip()
            if not sid:
                continue
            try:
                dur = float(row.get("dur") or 0)
            except ValueError:
                continue
            rows.append(dict(id=sid, dur=dur))
    return rows


def _rel_wav(root: str, sid: str) -> str | None:
    folder = os.path.join(root, SONS_AMB)
    if not os.path.isdir(folder):
        return None
    exact = os.path.join(folder, f"{sid}.wav")
    if os.path.isfile(exact):
        return os.path.relpath(exact, root)
    stem = sid.split("_")[0]
    hits = [
        p for p in sorted(os.listdir(folder))
        if p.upper().startswith(stem.upper() + "_") and p.lower().endswith(".wav")
    ]
    return os.path.join(SONS_AMB, hits[0]) if len(hits) == 1 else None


def melodic_pool(root: str, verbose: bool = True) -> list[str]:
    """Chemins relatifs des ambiances mélodiques, triés par ID."""
    keep: list[tuple[int, str]] = []
    rejected_short: list[str] = []
    for row in _read_registre_amb(root):
        num = _id_num(row["id"])
        if num is None or not (ID_MIN <= num <= ID_MAX):
            continue
        if row["dur"] < MIN_DUR_S:
            rejected_short.append(row["id"].split("_")[0])
            continue
        rel = _rel_wav(root, row["id"])
        if rel:
            keep.append((num, rel))
    keep.sort()
    pool = [rel for _, rel in keep]
    if not pool:
        raise SystemExit(
            f"{SONS_AMB}: aucune ambiance A{ID_MIN}-A{ID_MAX} d'au moins "
            f"{MIN_DUR_S:g} s — vérifier la matière et le registre"
        )

    stems = {os.path.basename(p).split("_")[0].upper() for p in pool}
    manquants = [f for f in FAVORIS_CORTEX if f not in stems]
    if manquants:
        raise SystemExit(
            f"{SONS_AMB}: favoris Cortex absents du pool : {', '.join(manquants)}"
        )

    if verbose:
        print(f"  Ambiance mélodique A{ID_MIN}-A{ID_MAX} ≥ {MIN_DUR_S:g}s : "
              f"{len(pool)} fichiers · écartés trop courts : "
              f"{', '.join(sorted(set(rejected_short))) or 'aucun'}")
    return pool


def _pool_from_stems(root: str, stems: tuple[str, ...], label: str,
                     verbose: bool = True) -> list[str]:
    """Résout une liste de stems Axx en chemins relatifs (ordre conservé)."""
    pool: list[str] = []
    missing: list[str] = []
    for stem in stems:
        rel = _rel_wav(root, stem)
        if rel:
            pool.append(rel)
        else:
            missing.append(stem)
    if missing:
        raise SystemExit(
            f"{SONS_AMB}: {label} — stems absents : {', '.join(missing)}"
        )
    if verbose:
        print(f"  Ambiance {label} : {len(pool)} fichiers")
    return pool


def texture_pool(root: str, verbose: bool = True) -> list[str]:
    """Nappe texture Cortex (HP5) — liste explicite Loumana."""
    return _pool_from_stems(root, FAVORIS_TEXTURE_CORTEX, "Cortex texture", verbose)


def cortex_pool(root: str, verbose: bool = True) -> list[str]:
    """Nappe musicale Cortex (HP7) — préférées Loumana (A53–A68 mélodiques)."""
    full = melodic_pool(root, verbose=False)
    by_stem = {os.path.basename(p).split("_")[0].upper(): p for p in full}
    pool = [by_stem[f] for f in FAVORIS_CORTEX if f in by_stem]
    if len(pool) != len(FAVORIS_CORTEX):
        manquants = [f for f in FAVORIS_CORTEX if f not in by_stem]
        raise SystemExit(f"{SONS_AMB}: favoris musicaux Cortex absents : {', '.join(manquants)}")
    if verbose:
        print(f"  Ambiance Cortex musicale : {len(pool)} · "
              f"texture : {len(FAVORIS_TEXTURE_CORTEX)} · "
              f"Hippo/Recon pool large : {len(full)}")
    return pool


def ambiance_paths_by_type(root: str, verbose: bool = True) -> tuple[list[str], list[str]]:
    """(musicale slot 32, texture slot 33) — pools disjoints."""
    return cortex_pool(root, verbose=verbose), texture_pool(root, verbose=verbose)
