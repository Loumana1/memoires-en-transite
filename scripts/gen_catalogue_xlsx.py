#!/usr/bin/env python3
"""Raccourci → scripts/proto07/gen_catalogue_xlsx.py"""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parent / "proto07" / "gen_catalogue_xlsx.py"),
    run_name="__main__",
)
