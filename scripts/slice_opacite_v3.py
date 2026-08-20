#!/usr/bin/env python3
"""Raccourci → scripts/proto07/slice_opacite_v3.py"""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parent / "proto07" / "slice_opacite_v3.py"),
    run_name="__main__",
)
