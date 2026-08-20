#!/usr/bin/env python3
"""Génère pd/prototype_06_fsm_8hp.pd — Proto 06 variante 8HP (sorties 1..8).

Géométrie: octogone régulier. Panneau VISU: samples en cours + historique
cerveau (état + durée). Régénère aussi les libs communes pd/lib/*_06.pd.

Cycle 1 artiste (docs/13): CORTEX opaque → HIPPO → RECON.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from proto06_lib import gen_libs06
from proto06_lib.gen_patch06 import build

if __name__ == "__main__":
    gen_libs06.ensure()
    build("8hp")
