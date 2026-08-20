"""Audit RMS des segments SONS/ — exclusion des fichiers silencieux (Q7).

Un segment est écarté du lecteur 06 s'il est entièrement silencieux ou s'il
contient une plage silencieuse >= 10 s. Les fichiers ne sont PAS déplacés:
ils sont seulement ignorés à la génération (relancer le générateur après
toute re-découpe de SONS/).
"""
import array
import glob
import math
import os
import wave

THRESH_RMS = 150      # 16 bits, ~ -47 dBFS
MAX_SILENT_RUN_S = 5

STATE_DIRS = ["CORTEX", "HIPPOCAMPE", "RECONSTRUCTION", "BOUCLE"]
DUR_DIRS = ["COURT", "MOYEN", "LONG"]


def _rms16(frames):
    a = array.array("h")
    a.frombytes(frames[: len(frames) // 2 * 2])
    if not a:
        return 0.0
    return math.sqrt(sum(x * x for x in a) / len(a))


def silent_runs(path):
    """Liste de (debut_s, fin_s) des plages silencieuses, par pas de 1 s."""
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        nsec = max(w.getnframes() // sr, 1)
        quiet = []
        for _ in range(nsec):
            frames = w.readframes(sr)
            if not frames:
                break
            quiet.append(_rms16(frames) < THRESH_RMS)
    runs, start = [], None
    for i, q in enumerate(quiet):
        if q and start is None:
            start = i
        if not q and start is not None:
            runs.append((start, i))
            start = None
    if start is not None:
        runs.append((start, len(quiet)))
    return runs, len(quiet)


def is_usable(path):
    try:
        runs, dur = silent_runs(path)
    except Exception:
        return False, "illisible"
    if any(a == 0 and b >= dur for a, b in runs):
        return False, "entierement silencieux"
    for a, b in runs:
        if b - a >= MAX_SILENT_RUN_S:
            return False, f"silence {b - a}s [{a}-{b}s]"
    return True, ""


def usable_files(root, verbose=True):
    """dict[(etat_idx, duree_idx)] -> [chemins relatifs utilisables]."""
    out = {}
    for si, state in enumerate(STATE_DIRS):
        for di, dur in enumerate(DUR_DIRS):
            keep = []
            for path in sorted(glob.glob(os.path.join(root, "SONS", state, dur, "*.wav"))):
                ok, why = is_usable(path)
                rel = os.path.relpath(path, root)
                if ok:
                    keep.append(rel)
                elif verbose:
                    print(f"  ECARTE (audio): {rel} — {why}")
            out[(si, di)] = keep
    return out


def usable_cortex_layer_pools(root, n_layers=10, n_baffles=8, verbose=True):
    """Pools exclusifs CORTEX 8HP : liste de fichiers par couche (slots 20+).

    Mapping: presets06.CORTEX_LAYER_MAP_8HP → SONS/CORTEX/B{n}/*_f{k}_a*.wav
    """
    try:
        from . import presets06 as PR
        layer_map = list(PR.CORTEX_LAYER_MAP_8HP)
    except Exception:
        layer_map = [(i + 1, 1) for i in range(min(n_layers, n_baffles))]
        while len(layer_map) < n_layers:
            layer_map.append((1, 2))

    pools = []
    for li in range(n_layers):
        bi, fi = layer_map[li] if li < len(layer_map) else (1, 1)
        folder = os.path.join(root, "SONS", "CORTEX", f"B{bi}")
        keep = []
        if os.path.isdir(folder):
            for path in sorted(glob.glob(os.path.join(folder, "*.wav"))):
                base = os.path.basename(path)
                if f"_f{fi}_a" not in base:
                    continue
                ok, why = is_usable(path)
                rel = os.path.relpath(path, root)
                if ok:
                    keep.append(rel)
                elif verbose:
                    print(f"  ECARTE (audio): {rel} — {why}")
        if not keep:
            if os.path.isdir(folder):
                all_b = [
                    p for p in sorted(glob.glob(os.path.join(folder, "*.wav")))
                    if not os.path.islink(p)
                ]
                if all_b:
                    pick = all_b[min(fi - 1, len(all_b) - 1)]
                    ok, why = is_usable(pick)
                    if ok:
                        keep = [os.path.relpath(pick, root)]
            if not keep and verbose:
                print(f"  WARN CORTEX B{bi} f{fi}: aucun fragment pour couche {li + 1}")
        pools.append(keep)
    return pools
