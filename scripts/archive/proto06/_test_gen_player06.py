#!/usr/bin/env python3
"""Outil de test dev: pd/_test_player06_slots.pd — lecteur seul, slots enchaînés.

Simule les transitions FSM sur player_state_06 1: BOUCLE(9) -> HIPPO(3) ->
RECON(7) -> CORTEX(0), slot froid + bang, niveau imprimé toutes les 500 ms.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from proto06_lib.pdbuild import P

p = P(800, 500)
p.obj("lb", 20, 20, "loadbang")
p.msg("dsp", 20, 50, "\\; pd dsp 1")
p.con("lb", 0, "dsp", 0)
p.obj("pl", 20, 100, "lib/player_state_06 1")
p.obj("env", 20, 140, "env~ 16384")
p.obj("f", 20, 170, "f")
p.obj("i", 20, 200, "int")
p.obj("pr", 20, 230, "print LVL")
p.obj("met", 200, 140, "metro 500")
p.msg("m1", 200, 110, "1")
p.con("lb", 0, "m1", 0)
p.con("m1", 0, "met", 0)
p.con("pl", 0, "env", 0)
p.con("env", 0, "f", 1)
p.con("met", 0, "f", 0)
p.con("f", 0, "i", 0)
p.con("i", 0, "pr", 0)

steps = [(500, 9, "BOUCLE9"), (6000, 3, "HIPPO3"), (12000, 7, "RECON7"),
         (18000, 0, "CORTEX0")]
for k, (ms, slot, tag) in enumerate(steps):
    x = 20 + k * 190
    p.obj(f"dl{k}", x, 300, f"delay {ms}")
    p.obj(f"tt{k}", x, 330, "t b b b")
    p.msg(f"sl{k}", x + 60, 360, str(slot))
    p.msg(f"tg{k}", x, 420, f"MARK_{tag}")
    p.obj(f"pt{k}", x, 450, "print")
    p.con("lb", 0, f"dl{k}", 0)
    p.con(f"dl{k}", 0, f"tt{k}", 0)
    p.con(f"tt{k}", 2, f"tg{k}", 0)
    p.con(f"tg{k}", 0, f"pt{k}", 0)
    p.con(f"tt{k}", 1, f"sl{k}", 0)
    p.con(f"sl{k}", 0, "pl", 1)
    p.con(f"tt{k}", 0, "pl", 0)

p.obj("dlq", 620, 300, "delay 24000")
p.msg("qt", 620, 330, "\\; pd quit")
p.con("lb", 0, "dlq", 0)
p.con("dlq", 0, "qt", 0)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pd", "_test_player06_slots.pd")
p.write(os.path.abspath(out))
print("OK: pd/_test_player06_slots.pd")
