#!/usr/bin/env python3
"""Découpe batch 4 — masters dans SONS batch 4/ · mode précis.

Usage:
  python3 scripts/slice_batch4.py --dry-run    # prévisualiser
  python3 scripts/slice_batch4.py              # écrire dans SONS_V3/ (incrémental)
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "SONS batch 4"
SCRIPT = ROOT / "scripts" / "proto07" / "slice_opacite_v3.py"

if not BATCH.is_dir():
    sys.exit(f"Dossier introuvable: {BATCH}")

cmd = [
    sys.executable, str(SCRIPT),
    "--source", str(BATCH),
    "--precise",
    *sys.argv[1:],
]
raise SystemExit(subprocess.run(cmd, cwd=ROOT).returncode)
