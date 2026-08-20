#!/usr/bin/env python3
"""Génère pd/prototype_06_fsm_4hp.pd — Proto 06 variante 4HP (sorties 1-2-3-4).

Régénère aussi les libs communes pd/lib/*_06.pd (idempotent).
Référence: docs/10_proto_06_handoff_technique.md — proto 05 figé, jamais modifié.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from proto06_lib import gen_libs06
from proto06_lib.gen_patch06 import build

if __name__ == "__main__":
    gen_libs06.ensure()
    build("4hp")
