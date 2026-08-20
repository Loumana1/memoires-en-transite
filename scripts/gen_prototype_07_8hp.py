#!/usr/bin/env python3
"""Raccourci → scripts/proto07/gen_prototype_07_8hp.py"""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parent / "proto07" / "gen_prototype_07_8hp.py"),
    run_name="__main__",
)
