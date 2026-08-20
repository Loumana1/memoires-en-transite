#!/usr/bin/env python3
"""Découpe Opacité V6 → SONS_V3/. **Incrémental, ID stables** (Q21 = option A).

Les masters sont dans SONS_V3/WIP/ : ce script n'y touche jamais, et ne supprime
jamais SONS_V3/. Il ajoute, il ne renumérote pas.

Chaque zone a FRAGMENTS / LONG_MOYEN ; les ambiances vivent dans un pool partagé :
  SONS_V3/AMBIANCE/

Masters (WIP Opacité V6) :
  *Cortex ambiance* → SONS_V3/AMBIANCE/ (tous les atomes ≥ 2 s)
  *Cortex*          → FRAGMENTS (< 13 s) ou LONG_MOYEN (≥ 13 s)
  *Hippocampe*      → idem (collage trou ≤ 1,8 s)
  *Reconstruction*  → idem (pas de collage)

ID stables : docs/Matiere/registre_ids.csv associe chaque segment détecté à un
nom de fichier définitif, via (master, état, rôle, temps de début ± 0,3 s).
Un segment déjà connu garde son nom, même si la détection de silence bouge un
peu. Un segment nouveau reçoit le numéro suivant, jamais un numéro déjà pris.
Le travail de classification à l'oreille est donc conservé.

Usage:
  python3 scripts/slice_opacite_v3.py --dry-run
  python3 scripts/slice_opacite_v3.py
  python3 scripts/slice_opacite_v3.py --only hippocampe   # un seul master
  python3 scripts/slice_opacite_v3.py --reset --yes       # tout refaire (perd les ID)
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from sons_v3_paths import AMBIANCE_DIR, dest_dir, find_on_disk

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "SONS_V3"
MASTERS_PARENT = OUT_DIR / "WIP"
JOURNAL = ROOT / "docs" / "Matiere" / "inventaire_SONS_V3.md"
CSV_PATH = ROOT / "docs" / "Matiere" / "inventaire_SONS_V3.csv"
REGISTRE = ROOT / "docs" / "Matiere" / "registre_ids.csv"

SIL_START = re.compile(r"silence_start:\s*([0-9.]+)")
SIL_END = re.compile(r"silence_end:\s*([0-9.]+)")
ID_RE = re.compile(r"^([A-Z]+)(\d+)_v3_")

NOISE_DB = -40.0
PAD = 0.02
MIN_SEG = 0.45
LONG_MOYEN_MIN = 13.0
AMBI_MIN_SEG = 2.0
AMBI_MIN_SIL = 1.0

HIPPO_MERGE_GAP = 1.8
HIPPO_MERGE_MAX = 12.0

# Tolérance d'appariement avec le registre. Un segment dont le début a bougé de
# moins que ça est considéré comme le même segment, et garde son ID.
MATCH_TOL = 0.30

ETATS = ("CORTEX", "HIPPOCAMPE", "RECONSTRUCTION")
ZONE_BUCKETS = ("FRAGMENTS", "LONG_MOYEN")
BUCKETS = ("FRAGMENTS", "LONG_MOYEN", "AMBIANCE")  # AMBIANCE = dossier racine partagé
REG_FIELDS = ["id", "etat", "role", "bucket", "src", "start", "end", "dur", "ajoute_le",
              # Écrites par scripts/normaliser_niveaux.py, jamais par ce script.
              # Doivent rester déclarées ici, sinon la découpe les effacerait.
              "niveau_db", "gain_db"]

PREFIX = {
    ("CORTEX", "TRACK"): "C",
    ("HIPPOCAMPE", "TRACK"): "H",
    ("RECONSTRUCTION", "TRACK"): "R",
    ("CORTEX", "AMBIANCE"): "A",
    ("HIPPOCAMPE", "AMBIANCE"): "HA",
    ("RECONSTRUCTION", "AMBIANCE"): "RA",
}


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def find_src_dir() -> Path:
    """Les masters vivent dans SONS_V3/WIP/ (et non SONS_V2/, disparu le 20 août)."""
    if MASTERS_PARENT.is_dir():
        for p in sorted(MASTERS_PARENT.iterdir()):
            if p.is_dir() and "v6" in p.name.lower() and list(p.glob("*.wav")):
                return p
    raise SystemExit(f"Dossier Opacité V6 introuvable sous {MASTERS_PARENT}")


def classify_master(name: str) -> tuple[str, str] | None:
    """(etat, role) role = AMBIANCE | TRACK. Le préfixe 'ambiance' des V6 n'est pas un rôle."""
    low = name.lower()
    if "hippocamp" in low or "hipo" in low:
        return "HIPPOCAMPE", "TRACK"
    if "recons" in low:
        return "RECONSTRUCTION", "TRACK"
    if "cortex" in low and "cortex ambiance" in low:
        return "CORTEX", "AMBIANCE"
    if "cortex" in low:
        return "CORTEX", "TRACK"
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


def bucket_track(dur: float) -> str:
    if dur >= LONG_MOYEN_MIN:
        return "LONG_MOYEN"
    return "FRAGMENTS"


def ensure_tree() -> None:
    AMBIANCE_DIR.mkdir(parents=True, exist_ok=True)
    for etat in ETATS:
        for bucket in ZONE_BUCKETS:
            dest_dir(etat, bucket).mkdir(parents=True, exist_ok=True)


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


# ---------------------------------------------------------------- registre

def load_registre() -> list[dict]:
    if not REGISTRE.is_file():
        return []
    with REGISTRE.open(newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def save_registre(entries: list[dict]) -> None:
    REGISTRE.parent.mkdir(parents=True, exist_ok=True)
    entries = sorted(entries, key=lambda e: (e["etat"], e["role"], natkey(e["id"])))
    with REGISTRE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=REG_FIELDS, restval="")
        w.writeheader()
        w.writerows(entries)


def natkey(name: str):
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", name)]


def next_index(entries: list[dict], prefix: str) -> int:
    """Plus grand numéro déjà attribué à ce préfixe + 1. Jamais de réattribution."""
    top = 0
    for e in entries:
        m = ID_RE.match(e["id"])
        if m and m.group(1) == prefix:
            top = max(top, int(m.group(2)))
    return top + 1


def match_existing(
    entries: list[dict], etat: str, role: str, src: str, start: float, used: set[str]
) -> dict | None:
    best, best_d = None, MATCH_TOL
    for e in entries:
        if e["id"] in used or e["etat"] != etat or e["role"] != role or e["src"] != src:
            continue
        d = abs(float(e["start"]) - start)
        if d <= best_d:
            best, best_d = e, d
    return best


def find_on_disk_for(etat: str, stem: str) -> Path | None:
    return find_on_disk(etat, stem)


# ---------------------------------------------------------------- découpe

def segments_for(
    path: Path, etat: str, role: str, duration: float
) -> list[tuple[float, float]]:
    if role == "AMBIANCE":
        silences = detect_silences(path, NOISE_DB, AMBI_MIN_SIL)
        segs = silences_to_segments(duration, silences, MIN_SEG)
        kept = [(a, b) for a, b in segs if (b - a) >= AMBI_MIN_SEG]
        print(f"  silences≥{AMBI_MIN_SIL:g}s: {len(silences)}  atomes: {len(segs)}  "
              f"gardés≥{AMBI_MIN_SEG:g}s: {len(kept)}")
        segs = kept
    else:
        min_sil = {"CORTEX": 1.0, "HIPPOCAMPE": 0.5, "RECONSTRUCTION": 0.45}[etat]
        silences = detect_silences(path, NOISE_DB, min_sil)
        segs = silences_to_segments(duration, silences, MIN_SEG)
        if etat == "HIPPOCAMPE":
            before = len(segs)
            segs = merge_adjacent(segs, HIPPO_MERGE_GAP, HIPPO_MERGE_MAX)
            print(f"  merge gap≤{HIPPO_MERGE_GAP}s → {before} atomes → {len(segs)} chaînes")
        print(f"  silences={len(silences)}  fragments={len(segs)}")
    return [
        (max(0.0, a - PAD), min(duration, b + PAD)) for a, b in segs
    ]


def process_master(
    path: Path, etat: str, role: str, duration: float,
    entries: list[dict], dry: bool, stats: Counter, reclass: bool = False,
) -> None:
    print(f"\n=== {path.name} → {etat}/{role} ({duration:.1f}s) ===")
    segs = segments_for(path, etat, role, duration)
    prefix = PREFIX[(etat, role)]
    width = 2 if role == "AMBIANCE" else 3
    suffix = "_ambiance" if role == "AMBIANCE" else ""
    by_id = {e["id"]: e for e in entries}
    used: set[str] = set()

    for a, b in segs:
        dur = b - a
        bucket = "AMBIANCE" if role == "AMBIANCE" else bucket_track(dur)
        prev = match_existing(entries, etat, role, path.name, a, used)
        if prev:
            stem = prev["id"]
            tag = "="
            stats["reutilises"] += 1
        else:
            i = next_index(entries, prefix)
            stem = f"{prefix}{i:0{width}d}_v3_{etat.lower()}{suffix}"
            tag = "+"
            stats["nouveaux"] += 1
            entry = {"id": stem, "etat": etat, "role": role, "bucket": bucket,
                     "src": path.name, "start": round(a, 3), "end": round(b, 3),
                     "dur": round(dur, 3), "ajoute_le": date.today().isoformat()}
            entries.append(entry)
            by_id[stem] = entry
        used.add(stem)

        existing = find_on_disk_for(etat, stem)
        target_dir = dest_dir(etat, bucket)
        if existing is None:
            export_seg(path, target_dir / f"{stem}.wav", a, b, dry)
            if prev:
                tag = "!"
                stats["reexportes"] += 1
        else:
            disque = existing.parent.name
            if disque == bucket:
                stats["inchanges"] += 1
            elif reclass:
                target = target_dir / f"{stem}.wav"
                if not dry:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(existing), str(target))
                tag = ">"
                stats["deplaces"] += 1
            else:
                # Le rangement manuel gagne : ne jamais défaire un déplacement
                # décidé à l'oreille (ex. les 42 A0xx passés en FRAGMENTS).
                tag = "m"
                bucket = disque
                stats["ranges_a_la_main"] += 1

        e = by_id[stem]
        if role == "AMBIANCE":
            bucket = "AMBIANCE"
        e.update(bucket=bucket, src=path.name, start=round(a, 3),
                 end=round(b, 3), dur=round(dur, 3))
        print(f"  {tag} {stem:34s} {dur:7.2f}s  {bucket:11s} {a:8.2f}–{b:8.2f}")

    orphans = [
        e for e in entries
        if e["src"] == path.name and e["etat"] == etat and e["id"] not in used
    ]
    if orphans:
        stats["orphelins"] += len(orphans)
        print(f"  ⚠ {len(orphans)} entrée(s) du registre sans segment correspondant "
              f"(fichiers conservés, rien n'est supprimé) :")
        for e in orphans[:10]:
            print(f"      ? {e['id']}  (début {e['start']}s)")
        if len(orphans) > 10:
            print(f"      … et {len(orphans) - 10} autres")


# ---------------------------------------------------------------- sorties

def write_journal(entries: list[dict], src_dir: Path, stats: Counter) -> None:
    c = Counter((e["etat"], e["bucket"]) for e in entries)
    lines = [
        "# Inventaire — SONS_V3 (découpe Opacité V6)",
        "",
        f"**Généré le :** {date.today().isoformat()}",
        f"**Source :** `SONS_V3/WIP/{src_dir.name}/`",
        "**Sortie :** `SONS_V3/<ÉTAT>/{FRAGMENTS,LONG_MOYEN}/` · ambiances → `SONS_V3/AMBIANCE/`",
        "**Script :** `scripts/slice_opacite_v3.py`",
        "",
        "Downmix **mono 48 kHz**. Table brute : "
        "[`inventaire_SONS_V3.csv`](./inventaire_SONS_V3.csv) · "
        "registre des ID : [`registre_ids.csv`](./registre_ids.csv).",
        "",
        "## Compteurs",
        "",
        "| État | Dossier | N |",
        "|------|---------|---|",
    ]
    for etat in ETATS:
        for bucket in BUCKETS:
            if bucket == "AMBIANCE":
                n = sum(1 for e in entries if e["role"] == "AMBIANCE")
                if etat == ETATS[0]:
                    lines.append(f"| *(partagé)* | AMBIANCE | {n} |")
            else:
                lines.append(f"| {etat} | {bucket} | {c.get((etat, bucket), 0)} |")
    lines += [
        "",
        f"**Total fichiers :** {len(entries)}",
        "",
        "## Dernière exécution",
        "",
        "| | N |",
        "|--|--|",
        f"| ID réutilisés | {stats['reutilises']} |",
        f"| nouveaux ID | {stats['nouveaux']} |",
        f"| inchangés sur le disque | {stats['inchanges']} |",
        f"| rangés à la main, respectés | {stats['ranges_a_la_main']} |",
        f"| déplacés (`--reclasser`) | {stats['deplaces']} |",
        f"| ré-exportés (fichier manquant) | {stats['reexportes']} |",
        f"| entrées sans segment (conservées) | {stats['orphelins']} |",
        "",
        "## Règles",
        "",
        "| Master | Destination |",
        "|--------|-------------|",
        "| Cortex ambiance | `SONS_V3/AMBIANCE/` (atomes ≥ 2 s) |",
        "| Cortex / Hippo / Recon | `FRAGMENTS` si < 13 s · `LONG_MOYEN` si ≥ 13 s |",
        "| Hippo | collage trou ≤ 1,8 s, max 12 s |",
        "",
        "## ID stables",
        "",
        "La découpe est **incrémentale** : elle ne vide jamais `SONS_V3/` et ne "
        "renumérote jamais. Un segment déjà connu garde son nom, apparié via "
        f"(master, état, rôle, début ± {MATCH_TOL:g} s). Un nouveau segment reçoit "
        "le numéro suivant. Le travail de classification à l'oreille est conservé.",
        "",
        "Les masters sont dans `SONS_V3/WIP/` et ne sont jamais touchés.",
        "",
        "Moteur 07 : relancer `python3 scripts/gen_prototype_07_8hp.py` après chaque découpe.",
        "Pipeline : [`Pipeline.md`](./Pipeline.md) · attributs : [`Attributs.md`](./Attributs.md).",
        "",
        "⚠ Fichier **généré**, écrasé à chaque découpe.",
        "",
    ]
    JOURNAL.write_text("\n".join(lines) + "\n", encoding="utf-8")
    fields = ["etat", "bucket", "file", "dur", "start", "end", "src"]
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for e in sorted(entries, key=lambda x: (x["etat"], x["bucket"], natkey(x["id"]))):
            w.writerow({"etat": e["etat"], "bucket": e["bucket"],
                        "file": e["id"] + ".wav", "dur": e["dur"],
                        "start": e["start"], "end": e["end"], "src": e["src"]})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="ne rien écrire, montrer ce qui serait fait")
    ap.add_argument("--only", metavar="MOTIF",
                    help="ne traiter que les masters dont le nom contient MOTIF")
    ap.add_argument("--reclasser", action="store_true",
                    help="déplacer les wav dont le bucket calculé a changé "
                         "(par défaut le rangement manuel est respecté)")
    ap.add_argument("--reset", action="store_true",
                    help="tout refaire à zéro — PERD les ID et la classification")
    ap.add_argument("--yes", action="store_true", help="confirmer --reset")
    args = ap.parse_args()

    if args.reset and not args.yes:
        print("--reset supprime les wav découpés et le registre : les ID seront "
              "réattribués et la classification à l'oreille sera perdue.\n"
              "Relancer avec --reset --yes si c'est bien voulu.", file=sys.stderr)
        return 2

    src_dir = find_src_dir()
    wavs = sorted(p for p in src_dir.glob("*.wav") if not p.name.startswith("."))
    if args.only:
        motif = args.only.lower()
        wavs = [w for w in wavs if motif in w.name.lower()]
    if not wavs:
        print(f"Aucun .wav retenu dans {src_dir}", file=sys.stderr)
        return 1

    print(f"Source: {src_dir}")
    print(f"Sortie: {OUT_DIR}  dry={args.dry_run}  incrémental={not args.reset}")
    print(f"Masters ({MASTERS_PARENT.name}/) : jamais modifiés")

    if args.reset and not args.dry_run:
        for etat in ETATS:
            for bucket in ZONE_BUCKETS:
                shutil.rmtree(dest_dir(etat, bucket), ignore_errors=True)
        shutil.rmtree(AMBIANCE_DIR, ignore_errors=True)
        REGISTRE.unlink(missing_ok=True)
        print("RESET : dossiers de découpe et registre supprimés (WIP/ intact)")

    ensure_tree()
    entries = [] if args.reset else load_registre()
    stats: Counter = Counter()

    for w in wavs:
        kind = classify_master(w.name)
        if not kind:
            print(f"SKIP: {w.name}")
            continue
        etat, role = kind
        process_master(w, etat, role, ffprobe_duration(w), entries,
                       args.dry_run, stats, args.reclasser)

    print("\n--- Résumé ---")
    c = Counter((e["etat"], e["bucket"]) for e in entries)
    for etat in ETATS:
        for bucket in BUCKETS:
            n = c.get((etat, bucket), 0)
            if n:
                print(f"  {etat}/{bucket}: {n}")
    print(f"Total registre: {len(entries)}")
    for k in ("nouveaux", "reutilises", "inchanges", "ranges_a_la_main",
              "deplaces", "reexportes", "orphelins"):
        print(f"  {k}: {stats[k]}")

    if args.dry_run:
        print("\ndry-run : rien écrit.")
        return 0

    save_registre(entries)
    write_journal(entries, src_dir, stats)
    print(f"\nRegistre: {REGISTRE.relative_to(ROOT)}")
    print(f"Journal:  {JOURNAL.relative_to(ROOT)}")
    print(f"CSV:      {CSV_PATH.relative_to(ROOT)}")
    print("Classement à l'oreille : docs/Matiere/catalogue_fragments.xlsx "
          "(python3 scripts/gen_catalogue_xlsx.py)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
