#!/usr/bin/env python3
"""Outil de test dev: génère pd/_test_router06.pd — sonde le routeur spatial 06.

noise~ -> spatial_router_06, balaye les 4 modes via sends, imprime quelles
sorties (W/X/Y ambi + HP directs) deviennent audibles (env~ > seuil).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from proto06_lib.pdbuild import P

p = P(900, 700)
p.obj("lb", 20, 20, "loadbang")
p.msg("dsp", 20, 50, "\\; pd dsp 1")
p.con("lb", 0, "dsp", 0)
p.obj("noise", 20, 100, "noise~")
p.obj("rt", 20, 140, "lib/spatial_router_06 1 60 1 5 4")
p.con("noise", 0, "rt", 0)

names = ["W", "X", "Y", "H1", "H2", "H3", "H4", "H5"]
for i, nm in enumerate(names):
    x = 20 + i * 120
    p.obj(f"env{i}", x, 220, "env~ 16384")
    p.obj(f"gt{i}", x, 250, "> 30")
    p.obj(f"ch{i}", x, 280, "change")
    p.obj(f"pr{i}", x, 310, f"print {nm}")
    p.con("rt", i, f"env{i}", 0)
    p.con(f"env{i}", 0, f"gt{i}", 0)
    p.con(f"gt{i}", 0, f"ch{i}", 0)
    p.con(f"ch{i}", 0, f"pr{i}", 0)

seq = [
    (500, "\\; s6_l1_step 300 \\; s6_l1_xfade 20 \\; s6_l1_rot 0.2 \\; s6_l1_sens 0 \\; s6_l1_mode 2", "MODE2_SAUT"),
    (4000, "\\; s6_l1_mode 3", "MODE3_SEQ"),
    (8000, "\\; s6_l1_mode 1", "MODE1_ROT"),
    (11000, "\\; s6_l1_mode 0", "MODE0_DRY"),
]
for k, (ms, body, tag) in enumerate(seq):
    x = 20 + k * 210
    p.obj(f"dl{k}", x, 400, f"delay {ms}")
    p.msg(f"mg{k}", x, 430, body)
    p.msg(f"tg{k}", x, 460, f"MARK_{tag}")
    p.obj(f"pt{k}", x, 490, "print")
    p.con("lb", 0, f"dl{k}", 0)
    p.con(f"dl{k}", 0, f"mg{k}", 0)
    p.con(f"dl{k}", 0, f"tg{k}", 0)
    p.con(f"tg{k}", 0, f"pt{k}", 0)

p.obj("dlq", 20, 560, "delay 14000")
p.msg("qt", 20, 590, "\\; pd quit")
p.con("lb", 0, "dlq", 0)
p.con("dlq", 0, "qt", 0)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pd", "_test_router06.pd")
p.write(os.path.abspath(out))
print("OK: pd/_test_router06.pd")
