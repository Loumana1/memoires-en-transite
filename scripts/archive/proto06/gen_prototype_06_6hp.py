#!/usr/bin/env python3
"""Génère pd/prototype_06_fsm_6hp.pd — Proto 06 variante 6HP (sorties 1-2-4-5-6).

Géométrie actée (§3.6): rectangle 4 coins + 2 baffles au milieu du grand côté.
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
    build("6hp")
