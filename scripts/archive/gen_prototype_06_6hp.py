#!/usr/bin/env python3
"""Raccourci → scripts/proto06/"""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parent / "proto06" / Path(__file__).name),
    run_name="__main__",
)
