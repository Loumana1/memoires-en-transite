#!/usr/bin/env python3
"""Génère pd/prototype_08_fsm_8hp.pd — Proto 08 8HP (SONS_V3).

Ne touche pas au Proto 07. Cycle AUTO: Cortex 40 s → Hippo 50 s → Recon 120 s.
12 voix Cortex + 2 nappes ambiance globales.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from proto08_lib import gen_libs08
from proto08_lib.gen_patch08 import build

if __name__ == "__main__":
    gen_libs08.ensure()
    build()
