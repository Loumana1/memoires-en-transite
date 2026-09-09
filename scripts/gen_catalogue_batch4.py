#!/usr/bin/env python3
"""Raccourci → scripts/proto07/gen_catalogue_batch4.py"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "proto07" / "gen_catalogue_batch4.py"
raise SystemExit(subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT).returncode)
