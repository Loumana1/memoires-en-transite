#!/usr/bin/env python3
"""Outil de test dev: pd/_test_chain06.pd — chaîne complète une couche.

noise~ -> fx_router_06 -> spatial_router_06 (mode 0 puis 1) -> decode_6hp_06.
Imprime toutes les 500 ms le niveau env~ (dB) des 5 canaux + bus W.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from proto06_lib.pdbuild import P

p = P(1000, 600)
p.obj("lb", 20, 20, "loadbang")
p.msg("dsp", 20, 50, "\\; pd dsp 1")
p.con("lb", 0, "dsp", 0)
p.obj("noise", 20, 100, "noise~")
p.obj("fx", 20, 130, "lib/fx_router_06 1")
p.obj("rt", 20, 160, "lib/spatial_router_06 1 60 1 5 4")
p.obj("dec", 20, 200, "lib/decode_6hp_06")
p.con("noise", 0, "fx", 0)
p.con("fx", 0, "rt", 0)
for c in range(3):
    p.con("rt", c, "dec", c)

p.obj("met", 700, 20, "metro 500")
p.msg("m1", 700, 50, "1")
p.con("lb", 0, "m1", 0)
p.con("m1", 0, "met", 0)

probes = [("dec", 0, "C1"), ("dec", 1, "C2"), ("dec", 2, "C4"),
          ("dec", 3, "C5"), ("dec", 4, "C6"), ("rt", 0, "W"), ("fx", 0, "FXOUT")]
for k, (src, o, nm) in enumerate(probes):
    x = 20 + k * 140
    p.obj(f"env{k}", x, 260, "env~ 16384")
    p.obj(f"f{k}", x, 290, "f")
    p.obj(f"i{k}", x, 320, "int")
    p.obj(f"pr{k}", x, 350, f"print {nm}")
    p.con(src, o, f"env{k}", 0)
    p.con(f"env{k}", 0, f"f{k}", 1)
    p.con("met", 0, f"f{k}", 0)
    p.con(f"f{k}", 0, f"i{k}", 0)
    p.con(f"i{k}", 0, f"pr{k}", 0)

seq = [
    (400, "\\; s6_l1_wet 0 \\; s6_l1_on 0 \\; s6_l1_rot 0.1 \\; s6_l1_sens 0 \\; s6_l1_mode 0", "MODE0"),
    (3000, "\\; s6_l1_mode 1", "MODE1"),
    (6000, "\\; s6_l1_wet 0.8 \\; s6_l1_del 700 \\; s6_l1_fb 0.6 \\; s6_l1_on 1", "ECHO_ON"),
]
for k, (ms, body, tag) in enumerate(seq):
    x = 20 + k * 300
    p.obj(f"dl{k}", x, 420, f"delay {ms}")
    p.msg(f"mg{k}", x, 450, body)
    p.msg(f"tg{k}", x, 480, f"MARK_{tag}")
    p.obj(f"pt{k}", x, 510, "print")
    p.con("lb", 0, f"dl{k}", 0)
    p.con(f"dl{k}", 0, f"mg{k}", 0)
    p.con(f"dl{k}", 0, f"tg{k}", 0)
    p.con(f"tg{k}", 0, f"pt{k}", 0)

p.obj("dlq", 620, 420, "delay 9000")
p.msg("qt", 620, 450, "\\; pd quit")
p.con("lb", 0, "dlq", 0)
p.con("dlq", 0, "qt", 0)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pd", "_test_chain06.pd")
p.write(os.path.abspath(out))
print("OK: pd/_test_chain06.pd")
