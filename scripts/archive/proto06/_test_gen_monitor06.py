#!/usr/bin/env python3
"""Outil de test dev: génère pd/_test_engine06.pd — moniteur niveaux moteur 06.

À charger À CÔTÉ de prototype_06_fsm_*.pd. Allume le DSP, démarre la session,
puis imprime, horodaté (ms), chaque changement d'état FSM et chaque bascule
audible/silence par canal (via les sondes s6_lvl1..5 du moteur).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from proto06_lib.pdbuild import P

p = P(1000, 600)
p.obj("lb", 20, 20, "loadbang")
p.msg("dsp", 20, 50, "\\; pd dsp 1")
p.obj("tmr", 140, 50, "timer")
p.con("lb", 0, "dsp", 0)
p.con("lb", 0, "tmr", 0)
p.obj("dls", 260, 20, "delay 500")
p.msg("sess", 260, 50, "\\; s6_session bang")
p.con("lb", 0, "dls", 0)
p.con("dls", 0, "sess", 0)

# etat horodate
p.obj("r_et", 20, 110, "r s6_etat")
p.obj("et_t", 20, 140, "t f b")
p.obj("pk_et", 20, 200, "pack 0 0")
p.obj("pr_et", 20, 230, "print ETAT_T")
p.con("r_et", 0, "et_t", 0)
p.con("et_t", 1, "tmr", 1)
p.con("tmr", 0, "pk_et", 1)
p.con("et_t", 0, "pk_et", 0)
p.con("pk_et", 0, "pr_et", 0)

# audible/silence par canal, horodate
for k in range(1, 6):
    x = 200 + (k - 1) * 150
    p.obj(f"r{k}", x, 110, f"r s6_lvl{k}")
    p.obj(f"gt{k}", x, 140, "> 25")
    p.obj(f"ch{k}", x, 170, "change")
    p.obj(f"cht{k}", x, 200, "t f b")
    p.obj(f"pk{k}", x, 260, "pack 0 0")
    p.obj(f"pr{k}", x, 290, f"print CH{k}")
    p.con(f"r{k}", 0, f"gt{k}", 0)
    p.con(f"gt{k}", 0, f"ch{k}", 0)
    p.con(f"ch{k}", 0, f"cht{k}", 0)
    p.con(f"cht{k}", 1, "tmr", 1)
    p.con("tmr", 0, f"pk{k}", 1)
    p.con(f"cht{k}", 0, f"pk{k}", 0)
    p.con(f"pk{k}", 0, f"pr{k}", 0)

p.obj("dlq", 20, 320, "delay 90000")
p.msg("qt", 20, 350, "\\; pd quit")
p.con("lb", 0, "dlq", 0)
p.con("dlq", 0, "qt", 0)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pd", "_test_engine06.pd")
p.write(os.path.abspath(out))
print("OK: pd/_test_engine06.pd")
