"""Scan SONS_V3 pour le lecteur Proto 07.

Paroles : CORTEX|HIPPOCAMPE|RECONSTRUCTION / FRAGMENTS|LONG_MOYEN
Ambiances : SONS_V3/AMBIANCE/ (pool partagé)
"""
from __future__ import annotations

import glob
import os
import wave

SONS_DIR = "SONS_V3"
STATE_DIRS = ["CORTEX", "HIPPOCAMPE", "RECONSTRUCTION", "BOUCLE"]
DUR_DIRS = ["COURT", "MOYEN", "LONG"]
HIPPO_LONG_MIN = 8.0


def _rel(root, path):
    return os.path.relpath(path, root)


def _wavs(folder):
    if not os.path.isdir(folder):
        return []
    return sorted(glob.glob(os.path.join(folder, "*.wav")))


def _dur(path):
    try:
        with wave.open(path, "rb") as w:
            sr = w.getframerate() or 1
            return w.getnframes() / float(sr)
    except Exception:
        return 0.0


def _v3(root):
    return os.path.join(root, SONS_DIR)


def _pool(root, etat, bucket):
    return _wavs(os.path.join(_v3(root), etat, bucket))


def _cortex_play(root):
    """C0xx court + C0xx moyen + A deplaces dans FRAGMENTS. C devant (pas de tri A..)."""
    fr = _pool(root, "CORTEX", "FRAGMENTS")
    moyen = _pool(root, "CORTEX", "LONG_MOYEN")
    c_fr = [p for p in fr if os.path.basename(p).upper().startswith("C")]
    a_fr = [p for p in fr if not os.path.basename(p).upper().startswith("C")]
    return c_fr + moyen + a_fr


def usable_files(root, verbose=True):
    """dict[(etat_idx, duree_idx)] -> chemins relatifs. Mappe SONS_V3.

    COURT  → FRAGMENTS
    MOYEN  → LONG_MOYEN (repli FRAGMENTS)
    LONG   → LONG_MOYEN
    """
    out = {(si, di): [] for si in range(4) for di in range(3)}

    hippo_f = _pool(root, "HIPPOCAMPE", "FRAGMENTS")
    hippo_l = _pool(root, "HIPPOCAMPE", "LONG_MOYEN")
    hippo_all = hippo_f + hippo_l
    hippo_long = [p for p in hippo_all if _dur(p) >= HIPPO_LONG_MIN] or hippo_l
    hippo_short = [p for p in hippo_f if 2.0 <= _dur(p) < HIPPO_LONG_MIN]

    recon_f = _pool(root, "RECONSTRUCTION", "FRAGMENTS")
    recon_l = _pool(root, "RECONSTRUCTION", "LONG_MOYEN")

    cx = _cortex_play(root)

    out[(1, 1)] = [_rel(root, p) for p in (hippo_long or hippo_all)]
    out[(1, 0)] = [_rel(root, p) for p in (hippo_short or hippo_long or hippo_all)]
    out[(2, 0)] = [_rel(root, p) for p in recon_f]
    out[(2, 1)] = [_rel(root, p) for p in (recon_l or recon_f)]
    out[(3, 0)] = [_rel(root, p) for p in hippo_all + recon_f]
    out[(0, 0)] = [_rel(root, p) for p in cx]
    out[(0, 1)] = list(out[(0, 0)])

    if verbose:
        print(f"  HIPPO ≥{HIPPO_LONG_MIN:g}s: {len(hippo_long)}  courts: {len(hippo_short)}")
        for si, st in enumerate(STATE_DIRS):
            for di, du in enumerate(DUR_DIRS):
                n = len(out[(si, di)])
                if n:
                    print(f"  V3 {st}/{du}: {n}")
    return out


def usable_cortex_layer_pools(root, n_layers=8, verbose=True):
    files = [_rel(root, p) for p in _cortex_play(root)]
    if not files:
        if verbose:
            print("  WARN: aucun CORTEX/FRAGMENTS")
        return [[] for _ in range(n_layers)]
    pools = [files[i:] + files[:i] for i in range(n_layers)]
    if verbose:
        nc = sum(1 for f in files if os.path.basename(f).upper().startswith("C"))
        na = len(files) - nc
        print(f"  CORTEX pool: {len(files)} ({nc} C0xx court+moyen, {na} A-frag) x {n_layers} couches")
    return pools


def _ambiance_pool(root):
    return _wavs(os.path.join(_v3(root), "AMBIANCE"))


def usable_ambiance(root, etat="CORTEX"):
    """Pool partagé — etat ignoré (compat Proto 07)."""
    del etat
    files = _ambiance_pool(root)
    if not files:
        # legacy : CORTEX/AMBIANCE
        files = _pool(root, "CORTEX", "AMBIANCE")
    return [_rel(root, p) for p in files]


def usable_cortex_amb_pools(root, n=5, verbose=True):
    """n listes disjointes (modulo) pour n baffles d'ambiance differents."""
    files = usable_ambiance(root, "CORTEX")
    if not files:
        if verbose:
            print("  WARN: aucun SONS_V3/AMBIANCE")
        return [[] for _ in range(n)]
    pools = [files[i::n] or files for i in range(n)]
    if verbose:
        sizes = ", ".join(str(len(p)) for p in pools)
        print(f"  CORTEX ambiance: {len(files)} fichiers → {n} baffles ({sizes})")
    return pools
