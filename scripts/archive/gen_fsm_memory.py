#!/usr/bin/env python3
"""Génère pd/lib/fsm_memory.pd — version minimale vérifiée."""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "pd", "lib", "fsm_memory.pd")
PRESET = {0: (2, 0, 1, 0), 1: (3, 0, 1, 2), 2: (3, 1, 1, 2), 3: (1, 0, 0, 0)}
DELAY = {0: 45000, 1: 90000, 2: 180000, 3: 60000}

lines = ["#N canvas 0 0 520 400 10;"]
idx = {}
obj_i = 0
pending = []

def O(name, s):
    global obj_i
    idx[name] = obj_i
    obj_i += 1
    lines.append(s)

def C(a, ao, b, bi):
    pending.append((a, ao, b, bi))

O("in_au", "#X obj 40 40 inlet;")
O("in_fo", "#X obj 120 40 inlet;")
O("o_st", "#X obj 40 360 outlet;")
O("o_bg", "#X obj 120 360 outlet;")
O("o_n", "#X obj 200 360 outlet;")
O("o_d0", "#X obj 280 360 outlet;")
O("o_d1", "#X obj 360 360 outlet;")
O("o_d2", "#X obj 440 360 outlet;")
O("f_st", "#X obj 40 100 f 0;")
O("f_au", "#X obj 40 70 f 1;")
O("lb", "#X obj 40 130 loadbang;")
O("tfo", "#X obj 120 70 t f b;")
O("go", "#X obj 40 200 t b b b b b b;")
O("sel", "#X obj 200 200 select 0 1 2 3;")
O("delay", "#X obj 40 280 delay 60000;")
O("spig", "#X obj 40 250 spigot;")
O("rn4", "#X obj 120 280 random 4;")
O("msg0", "#X msg 40 160 0;")

for s in range(4):
    n, d0, d1, d2 = PRESET[s]
    O(f"pn{s}", f"#X msg 260 {170 + s * 22} {n};")
    O(f"p0{s}", f"#X msg 300 {170 + s * 22} {d0};")
    O(f"p1{s}", f"#X msg 340 {170 + s * 22} {d1};")
    O(f"p2{s}", f"#X msg 380 {170 + s * 22} {d2};")
    O(f"dl{s}", f"#X msg 420 {170 + s * 22} {DELAY[s]};")

C("in_au", 0, "f_au", 0)
C("in_fo", 0, "tfo", 0)
C("tfo", 0, "f_st", 0)
C("tfo", 1, "go", 0)
C("lb", 0, "msg0", 0)
C("msg0", 0, "f_st", 0)
C("go", 0, "o_bg", 0)
C("f_st", 0, "o_st", 0)
C("f_st", 0, "sel", 0)
for s in range(4):
    C("sel", s, f"pn{s}", 0)
    C("sel", s, f"p0{s}", 0)
    C("sel", s, f"p1{s}", 0)
    C("sel", s, f"p2{s}", 0)
    C("sel", s, f"dl{s}", 0)
    C(f"pn{s}", 0, "o_n", 0)
    C(f"p0{s}", 0, "o_d0", 0)
    C(f"p1{s}", 0, "o_d1", 0)
    C(f"p2{s}", 0, "o_d2", 0)
    C(f"dl{s}", 0, "delay", 0)
C("delay", 0, "spig", 0)
C("f_au", 0, "spig", 1)
C("spig", 0, "rn4", 0)
C("rn4", 0, "tfo", 0)

for a, ao, b, bi in pending:
    lines.append(f"#X connect {idx[a]} {ao} {idx[b]} {bi};")

with open(os.path.abspath(OUT), "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"OK: {OUT}")
