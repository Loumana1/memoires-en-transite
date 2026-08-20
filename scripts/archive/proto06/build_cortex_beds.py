#!/usr/bin/env python3
"""Construit des lits CORTEX de 13–30 s à partir de SONS_FINAL.

Les masters sont découpés en atomes (séparés par silence), puis les atomes
sont concaténés pour former des fragments utilisables en densité 8HP.

Assemblage: atomes **non consécutifs** (tirage espacé / aléatoire), avec
quelques voisinages autorisés (~28 %) pour garder un peu de proximité.

Installation (8HP) — 1 fragment / baffle sur HP1–8 + 2e sur HP1 et HP5 :
  SONS/CORTEX/B1/ … B8/   (plusieurs alts exclusifs / couche, défaut 4)
  → 10 couches via CORTEX_LAYER_MAP_8HP ; chaque couche alterne ses alts au loop

Legacy 4/6HP : copie aussi dans MOYEN/ (pool partagé OK hors parcours artiste).

Usage:
  python3 scripts/build_cortex_beds.py
  python3 scripts/build_cortex_beds.py --alts 4 --seed 7
"""
from __future__ import annotations

import argparse
import hashlib
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from proto06_lib import presets06 as PR  # noqa: E402

SRC_DIR = ROOT / "SONS_FINAL"
SONS_CORTEX = ROOT / "SONS" / "CORTEX"
TMP_ATOMS = SRC_DIR / "parts" / "_cortex_atoms"
N_BAFFLES = 8
N_LAYERS = len(PR.CORTEX_LAYER_MAP_8HP)  # 10

SIL_START = re.compile(r"silence_start:\s*([0-9.]+)")
SIL_END = re.compile(r"silence_end:\s*([0-9.]+)")


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def find_cortex_master() -> Path:
    for p in sorted(SRC_DIR.glob("*.wav")):
        if "cortex" in p.name.lower():
            return p
    raise SystemExit(f"Aucun master CORTEX dans {SRC_DIR}")


def duration(path: Path) -> float:
    r = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ])
    return float(r.stdout.strip())


def detect_silences(path: Path, noise_db: float, min_sil: float):
    af = f"silencedetect=noise={noise_db}dB:d={min_sil}"
    r = run(["ffmpeg", "-i", str(path), "-af", af, "-f", "null", "-"], check=False)
    log = (r.stderr or "") + (r.stdout or "")
    starts = [float(m.group(1)) for m in SIL_START.finditer(log)]
    ends = [float(m.group(1)) for m in SIL_END.finditer(log)]
    pairs, ei = [], 0
    for s in starts:
        while ei < len(ends) and ends[ei] <= s:
            ei += 1
        if ei < len(ends):
            pairs.append((s, ends[ei]))
            ei += 1
    return pairs


def atoms_from_silences(dur: float, silences, min_seg: float = 0.4):
    segs, cursor = [], 0.0
    for s0, s1 in sorted(silences):
        if s0 > cursor + min_seg:
            segs.append((cursor, s0))
        cursor = max(cursor, s1)
    if dur > cursor + min_seg:
        segs.append((cursor, dur))
    return [(a, b) for a, b in segs if b - a >= min_seg]


def export_mono(src: Path, dst: Path, start: float, end: float):
    dst.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-y", "-ss", f"{start:.4f}", "-i", str(src),
        "-t", f"{max(0.05, end - start):.4f}",
        "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(dst),
    ])


def concat_wavs(parts: list[Path], out: Path):
    """Concatène via concat demuxer (re-encode mono 48k pour homogénéité)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in parts:
            f.write(f"file '{p.resolve()}'\n")
        list_path = f.name
    try:
        run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", list_path,
            "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(out),
        ])
    finally:
        Path(list_path).unlink(missing_ok=True)


def pack_beds(
    atom_paths: list[Path],
    min_s: float,
    max_s: float,
    count: int,
    seed: int = 42,
    min_gap: int = 2,
) -> list[Path]:
    """Assemble `count` lits distincts en mélangeant des atomes non consécutifs.

    - ancre primaire espacée par lit (répartition sur la timeline master) ;
    - atomes suivants tirés au hasard avec écart circulaire ≥ min_gap
      (parfois gap=1 pour garder quelques voisinages) ;
    - ordre de concat ≠ ordre chronologique du master.
    """
    if not atom_paths:
        raise SystemExit("Aucun atome CORTEX détecté")
    beds_dir = SRC_DIR / "parts" / "CORTEX_BEDS"
    if beds_dir.exists():
        shutil.rmtree(beds_dir)
    beds_dir.mkdir(parents=True)

    adurs = [duration(p) for p in atom_paths]
    n = len(atom_paths)
    rng = random.Random(seed)

    def circ_dist(a: int, b: int) -> int:
        d = abs(a - b) % n
        return min(d, n - d)

    def pick_next(chosen: list[int], last: int, allow_close: bool) -> int:
        gap = 1 if allow_close else max(1, min_gap)
        candidates = []
        for j in range(n):
            if chosen.count(j) >= 2:
                continue
            if j == last:
                continue
            if circ_dist(last, j) < gap:
                continue
            score = circ_dist(last, j) * 3.0
            if chosen:
                score += sum(circ_dist(j, c) for c in chosen) / len(chosen)
            score += rng.random()
            candidates.append((score, j))
        if not candidates:
            pool = [j for j in range(n) if j != last]
            return rng.choice(pool) if pool else last
        candidates.sort(reverse=True)
        top = candidates[: max(1, min(4, len(candidates)))]
        return rng.choice([j for _, j in top])

    beds: list[Path] = []
    recipes: list[list[int]] = []
    used_sets: list[frozenset[int]] = []  # ensembles déjà vus (anti miroir 3↔9)
    anchors = [(i * n) // count for i in range(count)]
    rng.shuffle(anchors)

    def recipe_too_close(chosen: list[int]) -> bool:
        s = frozenset(chosen)
        for prev in used_sets:
            if s == prev:
                return True
            inter = len(s & prev)
            union = len(s | prev)
            if union and inter / union >= 0.66:
                return True
        return False

    for bi in range(count):
        chosen: list[int] = []
        for attempt in range(12):
            anchor = (anchors[bi % len(anchors)] + attempt * 3) % n
            trial = [anchor]
            acc = adurs[anchor]
            while acc < min_s and len(trial) < 12:
                allow_close = rng.random() < 0.28
                nxt = pick_next(trial, trial[-1], allow_close)
                trial.append(nxt)
                acc += adurs[nxt]
                if acc >= max_s and acc >= min_s:
                    break
            while len(trial) > 1 and acc > max_s:
                acc -= adurs[trial[-1]]
                trial.pop()
                if acc < min_s:
                    trial.append((anchor + bi + len(trial) + attempt) % n)
                    acc = sum(adurs[i] for i in trial)
                    break
            if not recipe_too_close(trial):
                chosen = trial
                break
            chosen = trial  # dernier essai si tout overlap
        used_sets.append(frozenset(chosen))

        parts = [atom_paths[i] for i in chosen]
        out = beds_dir / f"final_cortex_bed_{bi + 1:02d}.wav"
        concat_wavs(parts, out)
        d = duration(out)
        if d > max_s + 0.05:
            trimmed = beds_dir / f"_trim_{bi + 1:02d}.wav"
            run([
                "ffmpeg", "-y", "-i", str(out), "-t", f"{max_s:.3f}",
                "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(trimmed),
            ])
            trimmed.replace(out)
            d = duration(out)
        if d < min_s - 0.05:
            while duration(out) < min_s - 0.05 and len(chosen) < 16:
                allow_close = rng.random() < 0.2
                nxt = pick_next(chosen, chosen[-1], allow_close)
                chosen.append(nxt)
                concat_wavs([atom_paths[i] for i in chosen], out)
            d = duration(out)
            if d > max_s:
                trimmed = beds_dir / f"_trim2_{bi + 1:02d}.wav"
                run([
                    "ffmpeg", "-y", "-i", str(out), "-t", f"{max_s:.3f}",
                    "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(trimmed),
                ])
                trimmed.replace(out)
                d = duration(out)

        gaps = [circ_dist(chosen[i], chosen[i + 1]) for i in range(len(chosen) - 1)]
        mean_gap = sum(gaps) / len(gaps) if gaps else 0.0
        idx_str = ",".join(str(i + 1) for i in chosen)
        print(
            f"  bed {bi + 1:02d}: {d:.2f}s  atomes=[{idx_str}]  "
            f"écart_moy={mean_gap:.1f}"
        )
        beds.append(out)
        recipes.append(chosen)

    seen: dict[str, int] = {}
    for bi, bed in enumerate(beds):
        h = hashlib.md5(bed.read_bytes()).hexdigest()
        tries = 0
        while h in seen and tries < 5:
            prev = seen[h] + 1
            base = list(recipes[bi])
            rng.shuffle(base)
            extra = [(bi * 5 + tries * 3 + k) % n for k in range(2)]
            alt = beds_dir / f"_alt_{bi + 1:02d}_{tries}.wav"
            concat_wavs([atom_paths[i] for i in base + extra], alt)
            trim_t = min(max_s, min_s + 2.0 + bi * 1.1 + tries)
            run([
                "ffmpeg", "-y", "-i", str(alt), "-t", f"{trim_t:.2f}",
                "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(bed),
            ])
            h = hashlib.md5(bed.read_bytes()).hexdigest()
            print(f"  bed {bi + 1:02d}: dédoublonné (était = bed {prev}, try {tries + 1})")
            tries += 1
        if h in seen:
            raise SystemExit(f"Impossible de dédoublonner bed {bi + 1} vs {seen[h] + 1}")
        seen[h] = bi
    return beds


def _clear_final_cortex(folder: Path):
    if not folder.exists():
        return
    for f in folder.glob("final_cortex*.wav"):
        f.unlink()


def install_beds(beds: list[Path], alts_per_layer: int = 4):
    """Répartit les lits selon CORTEX_LAYER_MAP_8HP dans B1..B8 + MOYEN."""
    layer_map = list(PR.CORTEX_LAYER_MAP_8HP)
    n_layers = len(layer_map)
    need = n_layers * alts_per_layer
    if len(beds) < need:
        raise SystemExit(f"Il faut ≥ {need} lits uniques (reçu {len(beds)})")

    for sub in ("COURT", "MOYEN", "LONG"):
        d = SONS_CORTEX / sub
        d.mkdir(parents=True, exist_ok=True)
        _clear_final_cortex(d)

    for bi in range(1, N_BAFFLES + 1):
        d = SONS_CORTEX / f"B{bi}"
        d.mkdir(parents=True, exist_ok=True)
        _clear_final_cortex(d)

    for i, bed in enumerate(beds[:need]):
        layer = i // alts_per_layer  # 0..9
        alt = (i % alts_per_layer) + 1
        baffle, frag = layer_map[layer]
        name = f"final_cortex_b{baffle}_f{frag}_a{alt:02d}.wav"
        dest = SONS_CORTEX / f"B{baffle}" / name
        shutil.copy2(bed, dest)
        shutil.copy2(bed, SONS_CORTEX / "MOYEN" / name)
        # symlink legacy (session Pd encore sur anciens noms sans _aNN)
        if alt == 1:
            legacy = SONS_CORTEX / f"B{baffle}" / f"final_cortex_b{baffle}_f{frag}.wav"
            if legacy.exists() or legacy.is_symlink():
                legacy.unlink()
            legacy.symlink_to(name)
        d = duration(bed)
        print(f"  → B{baffle}/{name} ({d:.2f}s)  [L{layer + 1} alt {alt}/{alts_per_layer}]")

    for bed in beds[need:]:
        shutil.copy2(bed, SONS_CORTEX / "MOYEN" / bed.name)
        print(f"  → MOYEN/{bed.name} (extra legacy)")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min", type=float, default=13.0)
    ap.add_argument("--max", type=float, default=30.0)
    ap.add_argument(
        "--alts", type=int, default=4,
        help="nombre de lits alternés par couche (défaut 4 → moins répétitif)",
    )
    ap.add_argument(
        "--count", type=int, default=0,
        help="nombre total de lits (0 = 10 couches × --alts)",
    )
    ap.add_argument("--noise", type=float, default=-40.0)
    ap.add_argument("--min-silence", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=7, help="graine tirage atomes")
    ap.add_argument(
        "--min-gap", type=int, default=2,
        help="écart min. entre atomes successifs (indices, circulaire)",
    )
    args = ap.parse_args()

    alts = max(2, args.alts)
    need = N_LAYERS * alts
    count = args.count if args.count > 0 else need
    if count < need:
        raise SystemExit(f"--count doit être ≥ {need} ({N_LAYERS} couches × {alts} alts)")

    master = find_cortex_master()
    print(f"Master: {master.name}")
    dur = duration(master)
    sil = detect_silences(master, args.noise, args.min_silence)
    atoms = atoms_from_silences(dur, sil)
    print(f"Atomes détectés: {len(atoms)}  ({', '.join(f'{b-a:.1f}s' for a,b in atoms)})")

    if TMP_ATOMS.exists():
        shutil.rmtree(TMP_ATOMS)
    TMP_ATOMS.mkdir(parents=True)
    atom_paths = []
    for i, (a, b) in enumerate(atoms, 1):
        p = TMP_ATOMS / f"atom_{i:02d}.wav"
        export_mono(master, p, a, b)
        atom_paths.append(p)

    print(
        f"\nAssemblage de {count} lits [{args.min}–{args.max}] s "
        f"(seed={args.seed}, min_gap={args.min_gap}, alts/couche={alts})…"
    )
    beds = pack_beds(
        atom_paths, args.min, args.max, count,
        seed=args.seed, min_gap=args.min_gap,
    )
    print(f"\nInstallation dans SONS/CORTEX/B1..B{N_BAFFLES} ({alts} alts / couche)…")
    install_beds(beds, alts_per_layer=alts)
    print("OK — relancer: python3 scripts/gen_prototype_06_8hp.py")


if __name__ == "__main__":
    main()
