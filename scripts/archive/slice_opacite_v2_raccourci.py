#!/usr/bin/env python3
"""Raccourci → scripts/archive/slice_opacite_v2.py (découpe V2, figée).

Conservé pour mémoire. Ce script écrit des inventaires numérotés dans docs/
selon l'ancienne convention : ne pas le relancer sans le repointer.
"""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parent / "slice_opacite_v2.py"),
    run_name="__main__",
)
