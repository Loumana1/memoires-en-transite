#!/usr/bin/env python3
"""Génère pd/prototype_07_fsm_8hp.pd — Proto 07 8HP (SONS_V3).

Ne touche pas au Proto 06. Cycle AUTO: Cortex 40 s → Hippo 50 s → Recon 120 s.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from proto07_lib import gen_libs07
from proto07_lib.gen_patch07 import build

if __name__ == "__main__":
    gen_libs07.ensure()
    build()
