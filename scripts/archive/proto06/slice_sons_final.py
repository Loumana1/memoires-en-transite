#!/usr/bin/env python3
"""Découpe SONS_FINAL → fragments individuels → classifie dans SONS/ → prêt 8HP.

Les 3 masters (CORTEX / HIPO / RECONS) contiennent des fragments séparés
par des silences. Ce script :
  1. détecte les silences (ffmpeg silencedetect)
  2. exporte chaque fragment en mono 48 kHz
  3. classe COURT (<15 s) / MOYEN (15–90 s) / LONG (>90 s, plafonné K5)
  4. place dans SONS/<ETAT>/<DUREE>/final_*.wav

Usage:
  python3 scripts/slice_sons_final.py
  python3 scripts/slice_sons_final.py --dry-run
  python3 scripts/slice_sons_final.py --keep-old   # ne pas vider les dossiers état
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "SONS_FINAL"
PARTS_DIR = SRC_DIR / "parts"
SONS_DIR = ROOT / "SONS"

# Fichier source → état FSM
SOURCE_MAP = {
    "cortex": "CORTEX",
    "hipo": "HIPPOCAMPE",
    "hippo": "HIPPOCAMPE",
    "recons": "RECONSTRUCTION",
    "recon": "RECONSTRUCTION",
}

NOISE_DB = -40.0
MIN_SILENCE = 1.0  # s — séparateur entre fragments
MIN_SEG = 0.45  # s — ignore micro-bruits
PAD = 0.02  # s — marge autour du fragment
MAX_SEG = 90.0  # K5
COURT_MAX = 15.0
MOYEN_MAX = 90.0
# Fragments ≥ ce seuil sont aussi copiés en MOYEN (fond couche 1),
# même s'ils font < 15 s — le stock FINAL n'a pas de prises longues.
MOYEN_PROMOTE = 4.0

SIL_START = re.compile(r"silence_start:\s*([0-9.]+)")
SIL_END = re.compile(r"silence_end:\s*([0-9.]+)")


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def ffprobe_duration(path: Path) -> float:
    r = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ])
    return float(r.stdout.strip())


def detect_silences(path: Path, noise_db: float, min_sil: float) -> list[tuple[float, float]]:
    """Retourne liste (start, end) des silences."""
    af = f"silencedetect=noise={noise_db}dB:d={min_sil}"
    r = run(["ffmpeg", "-i", str(path), "-af", af, "-f", "null", "-"], check=False)
    log = (r.stderr or "") + (r.stdout or "")
    starts, ends = [], []
    for line in log.splitlines():
        m = SIL_START.search(line)
        if m:
            starts.append(float(m.group(1)))
        m = SIL_END.search(line)
        if m:
            ends.append(float(m.group(1)))
    # Apparier start/end (ffmpeg peut démarrer mid-silence)
    pairs = []
    ei = 0
    for s in starts:
        while ei < len(ends) and ends[ei] <= s:
            ei += 1
        if ei < len(ends):
            pairs.append((s, ends[ei]))
            ei += 1
    return pairs


def silences_to_segments(
    duration: float, silences: list[tuple[float, float]], min_seg: float
) -> list[tuple[float, float]]:
    """Inverse silences → régions sonores [start, end)."""
    segs = []
    cursor = 0.0
    for s0, s1 in sorted(silences):
        if s0 > cursor + min_seg:
            segs.append((cursor, s0))
        cursor = max(cursor, s1)
    if duration > cursor + min_seg:
        segs.append((cursor, duration))
    # filtre durée min
    return [(a, b) for a, b in segs if (b - a) >= min_seg]


def split_long(seg: tuple[float, float], max_len: float) -> list[tuple[float, float]]:
    a, b = seg
    out = []
    while b - a > max_len + 0.01:
        out.append((a, a + max_len))
        a += max_len
    if b - a >= MIN_SEG:
        out.append((a, b))
    return out


def dur_buckets(sec: float) -> list[str]:
    """Un fragment peut aller dans COURT et/ou MOYEN (fond 8HP)."""
    buckets = []
    if sec < COURT_MAX:
        buckets.append("COURT")
    if MOYEN_PROMOTE <= sec <= MOYEN_MAX:
        buckets.append("MOYEN")
    elif sec > MOYEN_MAX:
        buckets.append("LONG")
    # Si uniquement très court : COURT seulement (déjà ajouté)
    if not buckets:
        buckets.append("COURT")
    # Dédupe en gardant l'ordre
    seen = set()
    out = []
    for b in buckets:
        if b not in seen:
            seen.add(b)
            out.append(b)
    return out


def etat_from_name(name: str) -> str | None:
    low = name.lower()
    for key, etat in SOURCE_MAP.items():
        if key in low:
            return etat
    return None


def export_seg(src: Path, dst: Path, start: float, end: float, dry: bool) -> None:
    dur = max(0.01, end - start)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dry:
        print(f"  [dry] {dst.name}  {start:.2f}–{end:.2f} ({dur:.2f}s)")
        return
    run([
        "ffmpeg", "-y",
        "-ss", f"{start:.4f}", "-i", str(src), "-t", f"{dur:.4f}",
        "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le",
        str(dst),
    ])


def clear_etat(etat: str) -> None:
    for bucket in ("COURT", "MOYEN", "LONG"):
        d = SONS_DIR / etat / bucket
        d.mkdir(parents=True, exist_ok=True)
        for f in d.glob("*.wav"):
            f.unlink()


def process_file(
    path: Path,
    noise_db: float,
    min_sil: float,
    dry: bool,
) -> list[dict]:
    etat = etat_from_name(path.name)
    if not etat:
        print(f"SKIP (état inconnu): {path.name}")
        return []
    duration = ffprobe_duration(path)
    silences = detect_silences(path, noise_db, min_sil)
    segs = silences_to_segments(duration, silences, MIN_SEG)
    expanded = []
    for seg in segs:
        expanded.extend(split_long(seg, MAX_SEG))

    print(f"\n=== {path.name} → {etat} ({duration:.1f}s) ===")
    print(f"  silences={len(silences)}  fragments={len(expanded)}")

    rows = []
    parts_etat = PARTS_DIR / etat
    if not dry:
        if parts_etat.exists():
            shutil.rmtree(parts_etat)
        parts_etat.mkdir(parents=True, exist_ok=True)

    for i, (a, b) in enumerate(expanded, start=1):
        a2 = max(0.0, a - PAD)
        b2 = min(duration, b + PAD)
        dur = b2 - a2
        buckets = dur_buckets(dur)
        stem = f"final_{etat.lower()}_{i:02d}"
        part = parts_etat / f"{stem}.wav"
        export_seg(path, part, a2, b2, dry)
        for bucket in buckets:
            dest = SONS_DIR / etat / bucket / f"{stem}.wav"
            if dry:
                print(f"  → SONS/{etat}/{bucket}/{stem}.wav")
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(part, dest)
            rows.append({
                "etat": etat, "bucket": bucket, "file": stem + ".wav",
                "start": a2, "end": b2, "dur": dur,
            })
        print(f"  [{i:02d}] {dur:6.2f}s  {','.join(buckets):11s}  {a2:6.2f}–{b2:6.2f}")
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--keep-old", action="store_true",
                    help="Ne pas vider SONS/<ETAT> avant copie")
    ap.add_argument("--noise", type=float, default=NOISE_DB)
    ap.add_argument("--min-silence", type=float, default=MIN_SILENCE)
    args = ap.parse_args()

    if not SRC_DIR.is_dir():
        print(f"Dossier manquant: {SRC_DIR}", file=sys.stderr)
        return 1
    wavs = sorted(SRC_DIR.glob("*.wav"))
    if not wavs:
        print("Aucun .wav dans SONS_FINAL", file=sys.stderr)
        return 1

    etats_touched = set()
    all_rows = []
    for w in wavs:
        etat = etat_from_name(w.name)
        if etat:
            etats_touched.add(etat)

    if not args.keep_old and not args.dry_run:
        for etat in sorted(etats_touched):
            print(f"Clear SONS/{etat}/{{COURT,MOYEN,LONG}}")
            clear_etat(etat)

    for w in wavs:
        all_rows.extend(process_file(w, args.noise, args.min_silence, args.dry_run))

    print("\n--- Résumé ---")
    from collections import Counter
    c = Counter((r["etat"], r["bucket"]) for r in all_rows)
    for (etat, bucket), n in sorted(c.items()):
        print(f"  {etat}/{bucket}: {n}")
    print(f"Total fragments: {len(all_rows)}")
    if not args.dry_run:
        print(f"Parts: {PARTS_DIR}")
        print(f"SONS:  {SONS_DIR}")
        print("Ensuite: python3 scripts/gen_prototype_06_8hp.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
