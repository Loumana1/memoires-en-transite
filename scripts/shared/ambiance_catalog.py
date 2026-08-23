"""Pool d'ambiances Proto 08 — sélection mélodique A45–A69.

Historique : la sélection était une liste blanche de 15 stems écrite à la main
(A38, A41, A43, A44 puis quelques-uns au-dessus de A45), coupée en deux pools
« musicale » et « texture » par une heuristique sur la position dans le master.
Résultat : le pool texture ne contenait plus que 5 fichiers, dont 4 sous A45,
et cinq des ambiances préférées de Loumana (A54, A65, A66, A67, A68)
n'appartenaient à aucun pool — elles ne pouvaient jamais sortir.

Décision du 22 août 2026 : **un seul pool mélodique**, les ambiances A45 à A69
qui tiennent au moins `MIN_DUR_S`. La séparation musicale / texture de
[Q25](docs/Backlog/Q&A.md#q25) tombe, puisque toute cette matière est mélodique.
Les deux nappes du Cortex tirent dans le même pool ; c'est le patch qui garantit
qu'elles ne prennent pas le même fichier au même moment.

Seuil de durée : [Q3](docs/Backlog/Q&A.md#q3) fixe 30 s pour une nappe, mais à
30 s strict on perdrait A53 (29,5 s) qui fait partie des préférées, ainsi que
A55 (28,7 s) et A46 (25,9 s). Le seuil est donc à 25 s, ce qui n'exclut que le
vraiment court — A47 ne dure que 3,9 s.
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

# Préférées Loumana pour le Cortex — toutes dans les bornes ci-dessus. Sert de
# garde-fou : si l'une disparaît du pool, la matière a bougé sans qu'on le voie.
FAVORIS_CORTEX = ("A53", "A54", "A59", "A64", "A65", "A66", "A67", "A68")

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


def cortex_pool(root: str, verbose: bool = True) -> list[str]:
    """Les seules ambiances des deux nappes du Cortex : les préférées Loumana.

    Le Cortex est plus étroit que le reste : sur ses 40 secondes, deux nappes
    seulement, et Loumana a désigné celles qui marchent. L'Hippocampe et la
    Reconstruction gardent le pool mélodique complet, où ces huit figurent
    aussi.
    """
    full = melodic_pool(root, verbose=False)
    by_stem = {os.path.basename(p).split("_")[0].upper(): p for p in full}
    pool = [by_stem[f] for f in FAVORIS_CORTEX if f in by_stem]
    if verbose:
        print(f"  Ambiance Cortex (préférées) : {len(pool)} · "
              f"Hippocampe / Reconstruction : {len(full)}")
    return pool


def ambiance_paths_by_type(root: str, verbose: bool = True) -> tuple[list[str], list[str]]:
    """(nappe 1, nappe 2) — mêmes préférées pour les deux slots 32 / 33.

    Les deux nappes partagent la matière ; l'anti-doublon est fait dans le
    patch, qui retire une carte à la seconde nappe si elle tombe sur le même
    fichier que la première.
    """
    pool = cortex_pool(root, verbose=verbose)
    return list(pool), list(pool)
