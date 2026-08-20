#!/usr/bin/env python3
"""Genere pd/lib/player_folder.pd a partir de SONS_PROTOTYPE/wav."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "SONS_PROTOTYPE" / "wav"
OUT = ROOT / "pd" / "lib" / "player_folder.pd"

files = sorted([p for p in SRC.glob("*.wav") if p.is_file()])
if not files:
    raise SystemExit("Aucun .wav trouve dans SONS_PROTOTYPE/wav")

lines = [
    "#N canvas 0 0 560 420 10;",
    "#X declare -path ../..;",
    "#X obj 40 40 inlet;",
    "#X obj 40 360 outlet~;",
    "#X obj 160 120 readsf~;",
    "#X obj 160 280 *~ 0.9;",
    "#X obj 40 80 t b;",
    f"#X obj 40 110 random {len(files)};",
    "#X obj 40 140 select " + " ".join(str(i) for i in range(len(files))) + ";",
]

for i, p in enumerate(files):
    esc = p.name.replace(" ", "\\ ")
    y = 160 + i * 20
    lines.append(f"#X msg 120 {y} open SONS_PROTOTYPE/wav/{esc};")

lines += [
    "#X obj 340 120 delay 150;",
    "#X msg 340 155 start;",
    "#X obj 380 60 loadbang;",
    "#X obj 380 90 delay 800;",
    f"#X text 20 10 bang = fichier aleatoire ({len(files)} pistes);",
    "#X text 20 26 declare -path ../.. = MET_ROOT (abstraction);",
]

# index helper (declare ne compte pas)
idx_readsf = 2
idx_gain = 3
idx_t = 4
idx_rand = 5
idx_sel = 6
idx_msg0 = 7
idx_delay = 7 + len(files)
idx_start = 8 + len(files)
idx_lb = 9 + len(files)
idx_lbdel = 10 + len(files)

conn = []
conn += [
    f"#X connect 0 0 {idx_t} 0;",
    f"#X connect {idx_readsf} 0 {idx_gain} 0;",
    f"#X connect {idx_gain} 0 1 0;",
    f"#X connect {idx_t} 0 {idx_rand} 0;",
    f"#X connect {idx_rand} 0 {idx_sel} 0;",
]
for i in range(len(files)):
    msg_idx = idx_msg0 + i
    conn.append(f"#X connect {idx_sel} {i} {msg_idx} 0;")
    conn.append(f"#X connect {msg_idx} 0 {idx_readsf} 0;")
    conn.append(f"#X connect {idx_sel} {i} {idx_delay} 0;")
conn += [
    f"#X connect {idx_delay} 0 {idx_start} 0;",
    f"#X connect {idx_start} 0 {idx_readsf} 0;",
    f"#X connect {idx_readsf} 1 {idx_t} 0;",
    f"#X connect {idx_lb} 0 {idx_lbdel} 0;",
    f"#X connect {idx_lbdel} 0 {idx_t} 0;",
]

lines.extend(conn)
OUT.write_text("\n".join(lines) + "\n")
print(f"OK: {OUT} ({len(files)} pistes)")
