#!/usr/bin/env python3
"""Découpe Opacité fin V2 → SONS_V2/ (Proto 07). N'écrase pas SONS/.

Règles (Q&A 16 août 2026) :
  - downmix mono 48 kHz
  - Cortex fragments : viser 13–30 s (silences) ; hors plage → ECART/
  - Cortex ambiance : tranches 2–3 min (120–180 s), pas de silencedetect
  - Hippocampe : viser 5–10 s ; 4.5–12 s acceptés ; sinon ECART/
  - Reconstruction : ≥30 s PRINCIPAL · 1–5 s COURT · 5–30 s MOYEN

Usage:
  python3 scripts/slice_opacite_v2.py --dry-run
  python3 scripts/slice_opacite_v2.py
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "SONS_V2"
JOURNAL = ROOT / "docs" / "16_proto_07_journal_decoupe.md"
CSV_PATH = ROOT / "docs" / "16_proto_07_journal_decoupe.csv"

SIL_START = re.compile(r"silence_start:\s*([0-9.]+)")
SIL_END = re.compile(r"silence_end:\s*([0-9.]+)")

NOISE_DB = -40.0
PAD = 0.02
MIN_SEG = 0.45

# Plages artiste
CORTEX_MIN, CORTEX_MAX = 13.0, 30.0
HIPPO_MIN, HIPPO_MAX = 5.0, 10.0
HIPPO_SOFT_MIN, HIPPO_SOFT_MAX = 4.5, 12.0
RECON_COURT_MAX = 5.0
RECON_MOYEN_MAX = 30.0
AMBI_MIN, AMBI_MAX = 120.0, 180.0
AMBI_TARGET = 160.0  # legacy V2 equal-slice (plus utilisé pour V3)
AMBI_MIN_SEG = 2.0   # V3: ignorer les micros < 2 s
AMBI_MIN_SIL = 1.0   # même seuil que Cortex fragments
PRINCIPAL_SPLIT = 180.0  # découpe un principal trop long
# Recoller uniquement un souffle / jitter de détection — jamais un silence technique.
# (16 août: merge Recon 8 s recollait plusieurs samples dans MOYEN/PRINCIPAL — retiré)
HIPPO_MERGE_GAP = 1.8
HIPPO_MERGE_MAX = 12.0
RECON_MERGE_GAP = None
RECON_MERGE_MAX = None


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def find_src_dir() -> Path:
    seen = []
    for base in (ROOT, ROOT / "SONS_FINAL"):
        if not base.is_dir():
            continue
        for p in base.iterdir():
            if p.is_dir() and "opacit" in p.name.lower() and "v2" in p.name.lower():
                if list(p.glob("*.wav")):
                    return p
                seen.append(p)
    raise SystemExit(
        f"Dossier Opacité fin V2 introuvable sous {ROOT} (vu: {seen})"
    )


def classify_master(name: str) -> str | None:
    low = name.lower()
    if "ambiance" in low or "ambience" in low:
        return "AMBIANCE"
    if "hipo" in low or "hippo" in low:
        return "HIPPOCAMPE"
    if "recons" in low or "recon" in low:
        return "RECONSTRUCTION"
    if "cortex" in low:
        return "CORTEX"
    return None


def ffprobe_duration(path: Path) -> float:
    r = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ])
    return float(r.stdout.strip())


def detect_silences(path: Path, noise_db: float, min_sil: float) -> list[tuple[float, float]]:
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


def silences_to_segments(
    duration: float, silences: list[tuple[float, float]], min_seg: float
) -> list[tuple[float, float]]:
    segs = []
    cursor = 0.0
    for s0, s1 in sorted(silences):
        if s0 > cursor + min_seg:
            segs.append((cursor, s0))
        cursor = max(cursor, s1)
    if duration > cursor + min_seg:
        segs.append((cursor, duration))
    return [(a, b) for a, b in segs if (b - a) >= min_seg]


def merge_adjacent(
    segs: list[tuple[float, float]], max_gap: float, max_dur: float
) -> list[tuple[float, float]]:
    """Colle les régions séparées par un trou ≤ max_gap, sans dépasser max_dur."""
    if not segs:
        return []
    out: list[tuple[float, float]] = []
    a, b = segs[0]
    for s0, s1 in segs[1:]:
        gap = s0 - b
        if 0 <= gap <= max_gap and (s1 - a) <= max_dur:
            b = s1
        else:
            out.append((a, b))
            a, b = s0, s1
    out.append((a, b))
    return out


def split_long(seg: tuple[float, float], max_len: float) -> list[tuple[float, float]]:
    a, b = seg
    out = []
    while b - a > max_len + 0.01:
        out.append((a, a + max_len))
        a += max_len
    if b - a >= MIN_SEG:
        out.append((a, b))
    return out


def ambiance_chunks(duration: float) -> list[tuple[float, float]]:
    n = max(1, round(duration / AMBI_TARGET))
    chunk = duration / n
    if chunk < AMBI_MIN:
        n = max(1, int(duration // AMBI_MIN))
        chunk = duration / n
    if chunk > AMBI_MAX:
        n = int(duration // AMBI_MAX) + (0 if duration % AMBI_MAX == 0 else 1)
        chunk = duration / n
    segs = []
    t = 0.0
    for i in range(n):
        t1 = duration if i == n - 1 else (i + 1) * chunk
        segs.append((t, t1))
        t = t1
    return segs


def export_seg(src: Path, dst: Path, start: float, end: float, dry: bool) -> None:
    dur = max(0.01, end - start)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dry:
        return
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", f"{start:.4f}", "-i", str(src), "-t", f"{dur:.4f}",
        "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le",
        str(dst),
    ])


def bucket_cortex(dur: float) -> str:
    if CORTEX_MIN <= dur <= CORTEX_MAX:
        return "FRAGMENTS"
    return "ECART"


def bucket_hippo(dur: float) -> str:
    if HIPPO_MIN <= dur <= HIPPO_MAX:
        return "OK"
    if HIPPO_SOFT_MIN <= dur <= HIPPO_SOFT_MAX:
        return "SOUPLE"
    return "ECART"


def bucket_recon(dur: float) -> str:
    """Simon: TRACE/MICRO ≤5 s · RESTER 5–30 s · FULL ≥30 s. Pas de collage."""
    if dur < 0.2:
        return "ECART"
    if dur <= RECON_COURT_MAX:
        return "COURT"
    if dur < RECON_MOYEN_MAX:
        return "MOYEN"
    return "PRINCIPAL"


def dest_dir(etat: str, bucket: str) -> Path:
    if etat == "AMBIANCE":
        return OUT_DIR / "CORTEX" / "AMBIANCE"
    if etat == "CORTEX":
        return OUT_DIR / "CORTEX" / bucket
    if etat == "HIPPOCAMPE":
        return OUT_DIR / "HIPPOCAMPE" / bucket
    return OUT_DIR / "RECONSTRUCTION" / bucket


def process_ambiance(path: Path, duration: float, dry: bool, ver: str = "v2") -> list[dict]:
    """Découpe sur silences (comme Cortex), pas en tranches de durée fixe."""
    silences = detect_silences(path, NOISE_DB, AMBI_MIN_SIL)
    segs = silences_to_segments(duration, silences, MIN_SEG)
    kept = [(a, b) for a, b in segs if (b - a) >= AMBI_MIN_SEG]
    skipped = len(segs) - len(kept)
    print(f"\n=== {path.name} → AMBIANCE ({duration:.1f}s) ===")
    print(f"  silences≥{AMBI_MIN_SIL:g}s: {len(silences)}  "
          f"atomes: {len(segs)}  gardés≥{AMBI_MIN_SEG:g}s: {len(kept)}  skip: {skipped}")
    rows = []
    for i, (a, b) in enumerate(kept, start=1):
        a2 = max(0.0, a - PAD)
        b2 = min(duration, b + PAD)
        dur = b2 - a2
        stem = f"A{i:02d}_{ver}_cortex_ambiance"
        dest = dest_dir("AMBIANCE", "") / f"{stem}.wav"
        export_seg(path, dest, a2, b2, dry)
        note = "OK"
        print(f"  [{i:02d}] {dur:7.2f}s  {note:11s}  {a2:7.1f}–{b2:7.1f}")
        rows.append(row("AMBIANCE", note, stem, a2, b2, dur, path.name))
    return rows


def replace_ambiance_only(src: Path, dry: bool) -> list[dict]:
    """Remplace SONS_V2/CORTEX/AMBIANCE sans toucher aux autres pools."""
    duration = ffprobe_duration(src)
    dest = dest_dir("AMBIANCE", "")
    dest.mkdir(parents=True, exist_ok=True)
    if not dry:
        for old in dest.glob("*.wav"):
            old.unlink()
            print(f"  rm {old.name}")
    ver = "v3" if "v3" in src.name.lower() else "v2"
    return process_ambiance(src, duration, dry, ver=ver)


def process_silenced(
    path: Path,
    etat: str,
    duration: float,
    min_sil: float,
    dry: bool,
    split_max: float | None,
    merge_gap: float | None = None,
    merge_max: float | None = None,
    court_only: bool = False,
    skip_court: bool = False,
) -> list[dict]:
    print(f"\n=== {path.name} → {etat} ({duration:.1f}s) ===")
    silences = detect_silences(path, NOISE_DB, min_sil)
    segs = silences_to_segments(duration, silences, MIN_SEG)
    if merge_gap is not None and merge_max is not None:
        before = len(segs)
        segs = merge_adjacent(segs, merge_gap, merge_max)
        print(f"  merge gap≤{merge_gap}s → {before} atomes → {len(segs)} chaînes")
    if split_max:
        expanded = []
        for seg in segs:
            expanded.extend(split_long(seg, split_max))
        segs = expanded
    print(f"  silences={len(silences)}  fragments={len(segs)}")
    rows = []
    for i, (a, b) in enumerate(segs, start=1):
        a2 = max(0.0, a - PAD)
        b2 = min(duration, b + PAD)
        dur = b2 - a2
        if etat == "CORTEX":
            bucket = bucket_cortex(dur)
        elif etat == "HIPPOCAMPE":
            bucket = bucket_hippo(dur)
        else:
            bucket = bucket_recon(dur)
        if court_only and bucket != "COURT":
            continue
        if skip_court and bucket == "COURT":
            continue
        prefix = "c" if court_only else ("m" if skip_court else "")
        id_letter = {"CORTEX": "C", "HIPPOCAMPE": "H", "RECONSTRUCTION": "R"}.get(etat, "X")
        stem = f"{id_letter}{i:03d}{prefix}_v2_{etat.lower()}"
        dest = dest_dir(etat, bucket) / f"{stem}.wav"
        export_seg(path, dest, a2, b2, dry)
        print(f"  [{i:03d}] {dur:6.2f}s  {bucket:11s}  {a2:7.2f}–{b2:7.2f}")
        rows.append(row(etat, bucket, stem, a2, b2, dur, path.name))
    return rows


def row(etat, bucket, stem, a, b, dur, src) -> dict:
    return {
        "etat": etat, "bucket": bucket, "file": stem + ".wav",
        "start": round(a, 3), "end": round(b, 3), "dur": round(dur, 3),
        "src": src,
    }


def write_journal(rows: list[dict], src_dir: Path) -> None:
    c = Counter((r["etat"], r["bucket"]) for r in rows)
    lines = [
        "# Journal de découpe — Opacité fin V2 (Proto 07)",
        "",
        "**Date :** 17 août 2026 — ambiance remplacée par Opacité fin V3 (WIP)",
        f"**Source :** `{src_dir.name}/`",
        "**Sortie :** `SONS_V2/` (l’ancien `SONS/` n’est pas touché)",
        "**Script :** `scripts/slice_opacite_v2.py`",
        "",
        "Downmix **mono 48 kHz**. Table brute : "
        "[`16_proto_07_journal_decoupe.csv`](./16_proto_07_journal_decoupe.csv).",
        "",
        "## Compteurs",
        "",
        "| État | Dossier | N |",
        "|------|---------|---|",
    ]
    for (etat, bucket), n in sorted(c.items()):
        lines.append(f"| {etat} | {bucket} | {n} |")
    lines += [
        "",
        f"**Total fichiers :** {len(rows)}",
        "",
        "## Plages visées vs hors plage",
        "",
        "| Pool | Cible | Accepté ici |",
        "|------|-------|-------------|",
        "| Cortex FRAGMENTS | 13–30 s | strict |",
        "| Cortex ECART | — | hors 13–30 s (à écouter, pas recollés) |",
        "| Ambiance | silences ≥1 s (comme Cortex) | atomes ≥ 2 s |",
        "| Hippo OK | 5–10 s | après collage des atomes (trou ≤ 1,8 s) |",
        "| Hippo SOUPLE | — | 4,5–12 s |",
        "| Recon COURT | 0,2–5 s (MICRO/TRACE) | atomes isolés, **sans collage** |",
        "| Recon MOYEN / PRINCIPAL | 5–30 s / ≥ 30 s | **une région continue** (silence technique = coupe) |",
        "",
        "## Minimums UC-A04",
        "",
    ]
    n_cx = c.get(("CORTEX", "FRAGMENTS"), 0)
    n_hi = c.get(("HIPPOCAMPE", "OK"), 0) + c.get(("HIPPOCAMPE", "SOUPLE"), 0)
    n_pr = c.get(("RECONSTRUCTION", "PRINCIPAL"), 0)
    n_ct = c.get(("RECONSTRUCTION", "COURT"), 0)
    n_am = sum(n for (e, _), n in c.items() if e == "AMBIANCE")
    lines += [
        f"- Cortex fragments 13–30 s : **{n_cx}** "
        f"{'OK' if n_cx >= 6 else 'INSUFFISANT (besoin ≥ 6)'}",
        f"- Hippo 4,5–12 s (OK+SOUPLE) : **{n_hi}** "
        f"{'OK' if n_hi >= 8 else 'INSUFFISANT (besoin ≥ 8)'}",
        f"- Recon PRINCIPAL : **{n_pr}** "
        f"{'OK' if n_pr >= 2 else 'INSUFFISANT (besoin ≥ 2)'}",
        f"- Recon COURT : **{n_ct}** "
        f"{'OK' if n_ct >= 8 else 'INSUFFISANT (besoin ≥ 8)'}",
        f"- Ambiance lits : **{n_am}**",
        "",
        "## Suite",
        "",
        "Le collage Recon (trou ≤ 8 s) a été retiré : un silence technique "
        "sépare deux fichiers. Il n’y a **pas** de PRINCIPAL ≥ 30 s continu "
        "dans le master actuel — à préparer dans Ableton (piste RECONSTRUCTION, "
        "une phrase / texture d’une traite, silences seulement *entre* les clips).",
        "",
        "Moteur 07 : relancer `python3 scripts/gen_prototype_07_8hp.py` après chaque découpe.",
        "",
    ]
    JOURNAL.write_text("\n".join(lines), encoding="utf-8")
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["etat", "bucket", "file", "dur", "start", "end", "src"])
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ambiance", type=Path, default=None,
                    help="Remplacer seulement CORTEX/AMBIANCE depuis ce master")
    args = ap.parse_args()

    if args.ambiance:
        src = args.ambiance
        if not src.is_file():
            print(f"Introuvable: {src}", file=sys.stderr)
            return 1
        print(f"Source ambiance: {src}")
        print(f"Sortie: {OUT_DIR / 'CORTEX' / 'AMBIANCE'}  dry={args.dry_run}")
        amb_rows = replace_ambiance_only(src, args.dry_run)
        existing: list[dict] = []
        if CSV_PATH.is_file():
            with CSV_PATH.open(newline="", encoding="utf-8") as f:
                existing = [r for r in csv.DictReader(f) if r.get("etat") != "AMBIANCE"]
        all_rows = existing + amb_rows
        print("\n--- Résumé ambiance ---")
        for r in amb_rows:
            print(f"  {r['file']}: {r['dur']}s")
        print(f"Lits: {len(amb_rows)}")
        if not args.dry_run:
            write_journal(all_rows, src.parent)
            print(f"Journal: {JOURNAL}")
        return 0

    src_dir = find_src_dir()
    wavs = sorted(p for p in src_dir.glob("*.wav") if not p.name.startswith("."))
    if not wavs:
        print(f"Aucun .wav dans {src_dir}", file=sys.stderr)
        return 1

    print(f"Source: {src_dir}")
    print(f"Sortie: {OUT_DIR}  dry={args.dry_run}")

    if not args.dry_run:
        if OUT_DIR.exists():
            shutil.rmtree(OUT_DIR)
        OUT_DIR.mkdir(parents=True)

    all_rows: list[dict] = []
    for w in wavs:
        kind = classify_master(w.name)
        if not kind:
            print(f"SKIP: {w.name}")
            continue
        duration = ffprobe_duration(w)
        if kind == "AMBIANCE":
            all_rows.extend(process_ambiance(w, duration, args.dry_run))
        elif kind == "CORTEX":
            all_rows.extend(process_silenced(
                w, "CORTEX", duration, min_sil=1.0, dry=args.dry_run, split_max=None
            ))
        elif kind == "HIPPOCAMPE":
            all_rows.extend(process_silenced(
                w, "HIPPOCAMPE", duration, min_sil=0.5, dry=args.dry_run,
                split_max=None, merge_gap=HIPPO_MERGE_GAP, merge_max=HIPPO_MERGE_MAX,
            ))
        else:
            all_rows.extend(process_silenced(
                w, "RECONSTRUCTION", duration, min_sil=0.45, dry=args.dry_run,
                split_max=None,
            ))

    print("\n--- Résumé ---")
    c = Counter((r["etat"], r["bucket"]) for r in all_rows)
    for (etat, bucket), n in sorted(c.items()):
        print(f"  {etat}/{bucket}: {n}")
    print(f"Total: {len(all_rows)}")

    if not args.dry_run:
        write_journal(all_rows, src_dir)
        print(f"Journal: {JOURNAL}")
        print(f"CSV:     {CSV_PATH}")
        print("SONS/ (proto 06) intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
