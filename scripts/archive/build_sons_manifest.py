#!/usr/bin/env python3
"""Scanne SONS/ et génère pd/lib/player_state.pd."""
import glob
import os

MET_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
SONS = os.path.join(MET_ROOT, "SONS")
OUT = os.path.join(MET_ROOT, "pd", "lib", "player_state.pd")
STATES = ["CORTEX", "HIPPOCAMPE", "RECONSTRUCTION", "BOUCLE"]
DURS = ["COURT", "MOYEN", "LONG"]

lines = ["#N canvas 0 0 900 680 10;", "#X declare -path ../..;"]
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


folders = {}
for st in STATES:
    for du in DURS:
        key = f"{st}/{du}"
        files = sorted(glob.glob(os.path.join(SONS, st, du, "*.wav")))
        folders[key] = ["SONS/" + "/".join([st, du, os.path.basename(f)]) for f in files]

all_files = []
for st in STATES:
    for du in DURS:
        all_files.extend(folders[f"{st}/{du}"])
if not all_files:
    raise SystemExit("Aucun fichier wav dans SONS/")

O("in_bang", "#X obj 40 40 inlet;")
O("in_slot", "#X obj 120 40 inlet;")
O("out", "#X obj 40 600 outlet~;")
O("readsf", "#X obj 520 100 readsf~;")
O("gain", "#X obj 520 180 *~ 0.9;")
O("fslot", "#X obj 120 80 f;")
O("d0", "#X obj 40 110 delay 0;")
O("bout", "#X obj 280 95 t b;")
O("sel12", "#X obj 40 180 select 0 1 2 3 4 5 6 7 8 9 10 11;")
O("del150", "#X obj 640 140 del 150;")
O("start", "#X msg 640 175 start;")

C("in_slot", 0, "fslot", 0)
C("in_bang", 0, "d0", 0)
C("d0", 0, "bout", 0)
C("bout", 0, "fslot", 0)
C("fslot", 0, "sel12", 0)
C("del150", 0, "start", 0)
C("start", 0, "readsf", 0)
C("readsf", 0, "gain", 0)
C("gain", 0, "out", 0)

for fi in range(12):
    si, di = divmod(fi, 3)
    st, du = STATES[si], DURS[di]
    files = folders[f"{st}/{du}"]
    if not files:
        state_pool = []
        for d2 in DURS:
            state_pool.extend(folders[f"{st}/{d2}"])
        files = state_pool or all_files
    y = 220 + fi * 30
    rn, sn = f"rnd_{fi}", f"sel_{fi}"
    O(rn, f"#X obj 120 {y} random {len(files)};")
    O(sn, f"#X obj 220 {y} select {' '.join(str(k) for k in range(len(files)))};")
    C("sel12", fi, rn, 0)
    C("sel12", fi, "del150", 0)
    C(rn, 0, sn, 0)
    for j, path in enumerate(files):
        esc = path.replace(" ", "\\ ")
        mn = f"msg_{fi}_{j}"
        O(mn, f"#X msg 360 {y + j} open {esc};")
        C(sn, j, mn, 0)
        C(mn, 0, "readsf", 0)

for a, ao, b, bi in pending:
    lines.append(f"#X connect {idx[a]} {ao} {idx[b]} {bi};")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"OK: {OUT} ({sum(len(v) for v in folders.values())} fichiers)")
