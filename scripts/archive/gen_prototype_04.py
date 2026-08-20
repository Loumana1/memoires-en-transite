#!/usr/bin/env python3
"""Génère pd/prototype_04_effects.pd — Mémoires en transit.

Pourquoi un générateur : les indices des lignes `#X connect A out B in` sont
positionnels ; chaque insertion d'objet décale tout (cause n°1 de l'échec du
proto 03). Ici chaque objet a un NOM symbolique, les indices sont calculés.

Idempotent : régénère toujours le même fichier.
Validation obligatoire après chaque exécution :
    ./scripts/test_patch_console.sh pd/prototype_04_effects.pd
"""

import os

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "pd", "prototype_04_effects.pd")

objs = []            # lignes "#X ..." dans l'ordre
index = {}           # nom -> indice

def add(name, line):
    if name in index:
        raise SystemExit(f"objet duplique: {name}")
    index[name] = len(objs)
    objs.append(line)

def text(line):
    objs.append(line)  # les commentaires comptent dans l'indexation mais sans nom

conns = []

def con(src, outlet, dst, inlet):
    conns.append((src, outlet, dst, inlet))

# ---------------------------------------------------------------- panneaux UI
add("cnv_tr", "#X obj 40 40 cnv 15 220 120 empty empty TRANSPORT 10 14 0 13 #f0f0f0 #202020 0;")
add("cnv_sp", "#X obj 40 180 cnv 15 420 330 empty empty SPATIAL 10 14 0 13 #e8f4e8 #202020 0;")
add("cnv_fx", "#X obj 500 180 cnv 15 280 330 empty empty FLUID_FX 10 14 0 13 #e8eef8 #202020 0;")

# ---------------------------------------------------------------- transport
add("audio_on", "#X obj 60 85 tgl 19 1 empty empty AUDIO_ON 17 7 0 10 -262144 -1 -1 1 0;")
add("dsp_msg", "#X msg 60 118 \\; pd dsp \\$1;")
add("play", "#X obj 170 85 bng 19 250 50 0 empty empty PLAY_ALEATOIRE 17 7 0 10 -262144 -1 -1;")
text("#X text 60 140 dac~ 1-4 = carte 4 sorties (Pd: Audio Settings \\, output channels = 4);")

# ---------------------------------------------------------------- panneau SPAT
add("spat", "#X obj 60 230 hradio 18 1 1 3 empty empty SPAT 0 -8 0 10 -262144 -1 -1 0;")
text("#X text 130 232 0 manuel | 1 rotation | 2 saut;")
text("#X text 60 265 mode 0:;")
add("phi_num", "#X floatatom 60 290 5 0 360 0 phi - - 0;")
add("phi_sl", "#X obj 60 320 vsl 18 140 360 0 0 0 phi_manuel - - 0;")
text("#X text 190 265 mode 1:;")
add("rot_num", "#X floatatom 190 290 5 0 2 0 rot_speed - - 0;")
add("sens", "#X obj 190 330 tgl 18 1 empty empty SENS_antihoraire 21 8 0 10 -262144 -1 -1 0 0;")
text("#X text 310 265 mode 2:;")
add("jump_num", "#X floatatom 310 290 5 100 5000 0 jump_ms - - 0;")
add("xfade_num", "#X floatatom 310 340 5 0 500 0 jump_xfade - - 0;")
text("#X text 60 480 phi: 0=devant | 90=droite | 180=arriere | 270=gauche;")

# ---------------------------------------------------------------- panneau FLUID
add("fl_on", "#X obj 520 230 tgl 18 1 empty empty FLUID_FX 21 8 0 10 -262144 -1 -1 0 0;")
add("fl_wet", "#X floatatom 520 290 5 0 1 0 fluid_wet - - 0;")
add("fl_del", "#X floatatom 590 290 5 1 3900 0 fluid_delay - - 0;")
add("fl_fb", "#X floatatom 660 290 5 0 0.95 0 fluid_fb - - 0;")
add("fl_lfo", "#X floatatom 520 340 5 0 5 0 fluid_lfo - - 0;")
text("#X text 520 380 FX mono sur le bus lecteur (1 instance) \\, off = bypass sec;")

# ------------------------------------------------- logique SPAT (sous les panneaux)
add("eq0", "#X obj 60 560 == 0;")
add("eq1", "#X obj 60 590 == 1;")
add("eq2", "#X obj 60 620 == 2;")
add("spig0", "#X obj 160 560 spigot;")
add("spig1", "#X obj 160 590 spigot;")
add("phi_f", "#X obj 240 590 f;")
add("phi_s", "#X obj 240 622 s phi-azim;")

# rotation inline (pattern proto 01) : phasor~ -> *~360 -> snapshot~ <- metro
add("phasor", "#X obj 330 560 phasor~ 0.05;")
add("mul360", "#X obj 330 590 *~ 360;")
add("snap", "#X obj 330 620 snapshot~ 40;")
add("met40", "#X obj 410 590 metro 40;")

# vitesse signee : rot_speed * sens (1 ou -1) -> frequence phasor~
add("sensm2", "#X obj 190 660 * -2;")
add("sensp1", "#X obj 190 690 + 1;")
add("senst", "#X obj 190 720 t b f;")
add("rot_f", "#X obj 270 720 f;")
add("rot_mul", "#X obj 190 750 * 1;")

# commutation exclusive des gates audio (0/1 rampe 30 ms via line~)
add("gate_t", "#X obj 500 560 t f f;")
add("g_eq0", "#X obj 500 590 == 0;")
add("g_packa", "#X obj 500 620 pack 0 30;")
add("g_linea", "#X obj 500 650 line~;")
add("g_packj", "#X obj 590 590 pack 0 30;")
add("g_linej", "#X obj 590 620 line~;")

# ---------------------------------------------------------------- chaine audio
text("#X text 660 475 gates exclusifs: ambi (SPAT 0-1) / saut (SPAT 2);")
add("player", "#X obj 660 500 lib/player_folder;")
add("fx", "#X obj 660 532 lib/fx_fluid;")
add("gate_a", "#X obj 660 565 *~;")
add("enc", "#X obj 660 600 lib/encode_2d;")
add("dec", "#X obj 660 630 lib/decode_4hp;")
add("rphi", "#X obj 580 600 r phi-azim;")
add("gate_j", "#X obj 860 565 *~;")
add("jump", "#X obj 860 600 lib/spatial_jump;")
text("#X text 860 640 saut: 1 sortie de spatial_jump par HP;")
add("vol1", "#X obj 660 680 *~ 0.65;")
add("vol2", "#X obj 730 680 *~ 0.65;")
add("vol3", "#X obj 800 680 *~ 0.65;")
add("vol4", "#X obj 870 680 *~ 0.65;")
add("dac", "#X obj 660 715 dac~ 1 2 3 4;")
text("#X text 660 745 4 HP: HP1=5deg HP2=95 HP3=185 HP4=275 (decode_4hp);")

# ---------------------------------------------------------------- initialisation
add("lb", "#X obj 60 800 loadbang;")
add("msg005", "#X msg 130 800 0.05;")
add("msg800", "#X msg 180 800 800;")
add("msg20", "#X msg 230 800 20;")
add("del300", "#X obj 60 830 delay 300;")
add("msg90", "#X msg 60 860 90;")
add("del600", "#X obj 130 830 delay 600;")
add("playbang", "#X msg 130 860 bang;")
add("msgfx", "#X msg 280 800 0.5;")
add("msgfxd", "#X msg 330 800 300;")
add("msgfxb", "#X msg 380 800 0.4;")
add("msgfxl", "#X msg 430 800 0.15;")
# CRITIQUE (leçon proto 03) : initialiser SPAT au loadbang, sinon les spigots
# et les gates line~ restent a 0 -> silence total malgre DSP ON.
add("msgspat", "#X msg 480 800 0;")
text("#X text 250 830 init: phi=90 apres 300 ms \\, PLAY apres 600 ms \\, DSP via AUDIO_ON;")

# ================================================================ connexions
con("audio_on", 0, "dsp_msg", 0)
con("play", 0, "player", 0)

# SPAT -> comparateurs
con("spat", 0, "eq0", 0)
con("spat", 0, "eq1", 0)
con("spat", 0, "eq2", 0)

# mode 0 : phi manuel
con("phi_sl", 0, "phi_num", 0)
con("phi_num", 0, "spig0", 0)
con("eq0", 0, "spig0", 1)
con("spig0", 0, "phi_f", 0)

# mode 1 : rotation
con("eq1", 0, "spig1", 1)
con("eq1", 0, "met40", 0)
con("phasor", 0, "mul360", 0)
con("mul360", 0, "snap", 0)
con("met40", 0, "snap", 0)
con("snap", 0, "spig1", 0)
con("spig1", 0, "phi_f", 0)
con("phi_f", 0, "phi_s", 0)

# vitesse + sens -> phasor~
con("rot_num", 0, "rot_f", 1)
con("rot_num", 0, "rot_mul", 0)
con("sens", 0, "sensm2", 0)
con("sensm2", 0, "sensp1", 0)
con("sensp1", 0, "senst", 0)
con("senst", 1, "rot_mul", 1)
con("senst", 0, "rot_f", 0)
con("rot_f", 0, "rot_mul", 0)
con("rot_mul", 0, "phasor", 0)

# commutation exclusive ambi / saut
con("eq2", 0, "gate_t", 0)
con("gate_t", 1, "g_packj", 0)
con("g_packj", 0, "g_linej", 0)
con("g_linej", 0, "gate_j", 1)
con("gate_t", 0, "g_eq0", 0)
con("g_eq0", 0, "g_packa", 0)
con("g_packa", 0, "g_linea", 0)
con("g_linea", 0, "gate_a", 1)

# FX fluid : une instance sur le bus mono du lecteur, avant la commutation SPAT
con("player", 0, "fx", 0)
con("fl_wet", 0, "fx", 1)
con("fl_del", 0, "fx", 2)
con("fl_fb", 0, "fx", 3)
con("fl_lfo", 0, "fx", 4)
con("fl_on", 0, "fx", 5)

# chaine ambi (SPAT 0 et 1)
con("fx", 0, "gate_a", 0)
con("gate_a", 0, "enc", 1)
con("rphi", 0, "enc", 0)
con("enc", 0, "dec", 0)
con("enc", 1, "dec", 1)
con("enc", 2, "dec", 2)
con("dec", 0, "vol1", 0)
con("dec", 1, "vol2", 0)
con("dec", 2, "vol3", 0)
con("dec", 3, "vol4", 0)

# chaine saut (SPAT 2) — 1 sortie de spatial_jump par HP
con("fx", 0, "gate_j", 0)
con("gate_j", 0, "jump", 0)
con("jump_num", 0, "jump", 1)
con("xfade_num", 0, "jump", 2)
con("eq2", 0, "jump", 3)
con("jump", 0, "vol1", 0)
con("jump", 1, "vol2", 0)
con("jump", 2, "vol3", 0)
con("jump", 3, "vol4", 0)

# sortie
con("vol1", 0, "dac", 0)
con("vol2", 0, "dac", 1)
con("vol3", 0, "dac", 2)
con("vol4", 0, "dac", 3)

# init
con("lb", 0, "msgspat", 0)
con("msgspat", 0, "spat", 0)
con("lb", 0, "msg005", 0)
con("msg005", 0, "rot_num", 0)
con("lb", 0, "msgfx", 0)
con("msgfx", 0, "fl_wet", 0)
con("lb", 0, "msgfxd", 0)
con("msgfxd", 0, "fl_del", 0)
con("lb", 0, "msgfxb", 0)
con("msgfxb", 0, "fl_fb", 0)
con("lb", 0, "msgfxl", 0)
con("msgfxl", 0, "fl_lfo", 0)
con("lb", 0, "msg800", 0)
con("msg800", 0, "jump_num", 0)
con("lb", 0, "msg20", 0)
con("msg20", 0, "xfade_num", 0)
con("lb", 0, "del300", 0)
con("del300", 0, "msg90", 0)
con("msg90", 0, "phi_num", 0)
con("lb", 0, "del600", 0)
con("del600", 0, "playbang", 0)
con("playbang", 0, "player", 0)

# ================================================================ ecriture
lines = ["#N canvas 40 40 1020 920 10 MET_PROTOTYPE_04;",
         "#X declare -path .. -path . -path lib -path externals/iem_ambi-master"
         " -path externals/iemmatrix -lib iem_ambi -lib iemmatrix;"]
lines += objs
for s, o, d, i in conns:
    lines.append(f"#X connect {index[s]} {o} {index[d]} {i};")

with open(os.path.abspath(OUT), "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"OK: {os.path.abspath(OUT)} ({len(objs)} objets, {len(conns)} connexions)")
