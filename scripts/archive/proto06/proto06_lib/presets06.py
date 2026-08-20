"""Données figées + calibrables Proto 06.

Sources: docs/archive/09_qa (legacy 4/6HP), docs/13_micro_opacites (cible artiste 8HP).

4HP / 6HP — dramaturgie historique (Q3):
  BOUCLE → HIPPO → RECON → CORTEX(clarté), ECHO off en CORTEX.

8HP — dramaturgie artiste (12 août 2026, docs/13):
  CORTEX(opaque) → HIPPO(mouvement) → RECON(lisible).
  CORTEX: 10 couches / 8 baffles (HP1–8 + 2e sur HP1/HP5), fragments exclusifs.
  BOUCLE hors cycle 1 (FORCE/debug).

Décisions figées communes:
- mapping fixe couches (N1), gain master 0.65 (L3)
- plafond ECHO: wet .85 / delay 800 / fb .70 / lfo .50
Les valeurs numériques fines restent à calibrer à l'oreille (§M).
"""

# --- FSM -------------------------------------------------------------------
# nb couches actives + slot durée par lecteur (0=COURT 1=MOYEN 2=LONG)
# Couche 1 = principal/fond: sample LONG (~20 s+, slot MOYEN);
# couches 2+ = interférences: samples COURTS par-dessus (retour 10 juil.).
# Tuple: (n, d0, d1, d2[, d3, d4, d5]) — slots absents = 0.
FSM_N = {
    0: (2, 1, 0, 0),  # CORTEX (4/6HP legacy): clarté + interférence
    1: (3, 1, 0, 0),  # HIPPOCAMPE: fond + 2 arrivées
    2: (2, 1, 0, 0),  # RECONSTRUCTION: superposition limitée
    3: (1, 1, 0, 0),  # BOUCLE: 1 lecteur strict
}

# 8HP — gradient artiste: CORTEX (profond/opaque) > HIPPO > RECON (clair)
# CORTEX: 10 couches — slots durée ignorés (engine → pools exclusifs 20..29)
FSM_N_8HP = {
    0: (10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # CORTEX: 10 × fragments exclusifs (8 HP)
    1: (4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),   # HIPPO: 4 — spread HP1–4 + motion
    2: (2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),   # RECON: 2
    3: (4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),   # BOUCLE: hors cycle 1
}

MAX_LAYERS = 3
MAX_LAYERS_8HP = 10

# Cycle 1 — 4/6HP legacy (Q3): BOUCLE → HIPPO → RECON → CORTEX(clarté)
CYCLE1 = [(3, 14000), (1, 7000), (2, 16000), (0, 13000)]
# Cycle 1 — 8HP artiste: CORTEX(opaque) → HIPPO → RECON
# CORTEX allongé pour laisser vivre les lits 13–30 s
CYCLE1_8HP = [(0, 28000), (1, 9000), (2, 16000)]
# Cycles 2+: durée aléatoire 15-35 s ; retour CORTEX 1 transition sur 5
# (8HP: retour = zone opaque, pas « atterrissage clarté »)
FREE_DUR_BASE = 15000
FREE_DUR_RAND = 20000
FREE_CORTEX_EVERY = 5
RESET_MS = 420000  # reset session 7 min -> cycle 1

# --- Ancres spatiales fixes (N1) --------------------------------------------
# (HP logique 1-based, azimut degrés) par couche.
ANCHORS_4HP = [(1, 5), (3, 185), (4, 275)]
ANCHORS_6HP = [(1, 60), (3, 240), (4, 300)]
# 8HP CORTEX: **8 baffles** exploités (octogone).
# L1–L8 → HP1–HP8 (1 fragment / baffle) ; L9–L10 → 2e fragment sur HP1 et HP5.
# (baffle 1-based, fragment 1|2) par couche — aligné ANCHORS_8HP / pools B1..B8
CORTEX_LAYER_MAP_8HP = [
    (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
    (1, 2), (5, 2),
]
ANCHORS_8HP = [
    (1, 0),      # L1  → HP1
    (2, 45),     # L2  → HP2
    (3, 90),     # L3  → HP3
    (4, 135),    # L4  → HP4
    (5, 180),    # L5  → HP5
    (6, 225),    # L6  → HP6
    (7, 270),    # L7  → HP7
    (8, 315),    # L8  → HP8
    (1, 0),      # L9  → HP1 (2e)
    (5, 180),    # L10 → HP5 (2e)
]

# Géométrie 6HP actée (§3.6): rectangle 4 coins + paire médiane du grand côté.
# Azimuts decode canaux carte 1/2/4/5/6: coins 60/120/240/300 + médiane 0.
DECODE_6HP_AZ = [60, 120, 240, 300, 0]

# Géométrie 8HP: octogone régulier, sorties carte 1..8.
DECODE_8HP_AZ = [0, 45, 90, 135, 180, 225, 270, 315]

# Noms UI des états FSM (visu historique).
ETAT_NOMS = ["CORTEX", "HIPPOCAMPE", "RECONSTRUCTION", "BOUCLE"]

# --- Presets par état x variante --------------------------------------------
# mode SPAT: 0=dry ancré, 1=rotation ambi, 2=saut HP, 3=séquence HP tous,
#            4=circulation locale 3–4 baffles voisins (HIPPO)
# sat 0-1 (drive/wet), hpf Hz, lpf Hz, flfo 0-1 (mod LPF)
LAYER_DEFAULT = dict(mode=0, rot=0.02, sens=0, step=800, xfade=30,
                     wet=0, delay=200, fb=0, lfo=0, on=0,
                     sat=0, hpf=20, lpf=20000, flfo=0)


def L(**kw):
    d = dict(LAYER_DEFAULT)
    d.update(kw)
    return d


IDLE = L()

PRESETS = {
    # CORTEX — clarté, ECHO off, superposition après délai (N6), 3 variantes
    0: [
        dict(ovl=3000, layers=[L(mode=0), L(mode=0), IDLE]),
        dict(ovl=5000, layers=[L(mode=1, rot=0.01), L(mode=1, rot=0.01), IDLE]),
        dict(ovl=8000, layers=[L(mode=0), L(mode=3, step=700, xfade=30), IDLE]),
    ],
    # HIPPOCAMPE — fond + arrivées, ECHO presque toujours mesuré (F4),
    # SPAT mixte autorisé (N3), sens configurable (N2)
    1: [
        dict(ovl=80, layers=[
            L(mode=1, rot=0.03, sens=0, wet=0.5, delay=400, fb=0.35, lfo=0.2, on=1),
            L(mode=3, step=900, xfade=40, sens=0, wet=0.3, delay=300, fb=0.25, lfo=0.15, on=1),
            L(mode=1, rot=0.05, sens=1),
        ]),
        dict(ovl=80, layers=[
            L(mode=0, wet=0.6, delay=500, fb=0.4, lfo=0.25, on=1),
            L(mode=3, step=600, xfade=30, sens=1),
            L(mode=1, rot=0.04, sens=0, wet=0.3, delay=250, fb=0.25, lfo=0.15, on=1),
        ]),
        dict(ovl=80, layers=[
            L(mode=1, rot=0.02, sens=0, wet=0.45, delay=350, fb=0.3, lfo=0.2, on=1),
            L(mode=2, step=1500, xfade=60),
            L(mode=3, step=800, xfade=40, sens=1, wet=0.3, delay=300, fb=0.25, on=1),
        ]),
    ],
    # RECONSTRUCTION — phi lent (G2/G3), wet/fb bas (G5)
    2: [
        dict(ovl=80, layers=[
            L(mode=1, rot=0.015, sens=0, wet=0.25, delay=300, fb=0.3, lfo=0.15, on=1),
            L(mode=0), IDLE,
        ]),
        dict(ovl=80, layers=[
            L(mode=0, wet=0.2, delay=200, fb=0.25, lfo=0.1, on=1),
            L(mode=1, rot=0.02, sens=1, wet=0.15, delay=150, fb=0.2, lfo=0.1, on=1),
            IDLE,
        ]),
        dict(ovl=80, layers=[
            L(mode=2, step=4000, xfade=100, wet=0.3, delay=350, fb=0.35, lfo=0.15, on=1),
            L(mode=1, rot=0.01, sens=0), IDLE,
        ]),
    ],
    # BOUCLE — 1 couche, ECHO plafond projet (H3), saut/seq 50/50 (H4),
    # variante clarté minoritaire (H5)
    3: [
        dict(ovl=80, layers=[
            L(mode=2, step=5000, xfade=60, wet=0.8, delay=750, fb=0.65, lfo=0.45, on=1),
            IDLE, IDLE,
        ]),
        dict(ovl=80, layers=[
            L(mode=3, step=2500, xfade=50, sens=0, wet=0.75, delay=700, fb=0.6, lfo=0.4, on=1),
            IDLE, IDLE,
        ]),
        dict(ovl=80, layers=[
            L(mode=1, rot=0.06, sens=1, wet=0.3, delay=600, fb=0.3, lfo=0.2, on=1),
            IDLE, IDLE,
        ]),
    ],
}

# 8HP — dramaturgie artiste (docs/13): CORTEX opaque → HIPPO → RECON
# CORTEX: 10× dry ancré (HP1–8 + 2e HP1/HP5) — fragments exclusifs, HPF 400–600
_CX = lambda **kw: L(mode=0, on=1, **kw)
PRESETS_8HP = {
    # CORTEX — densite 10 ; HPF LF 400–600 ; alts multi-samples / couche
    0: [
        dict(ovl=60, play_reps=1, layers=[
            _CX(wet=0.28, delay=280, fb=0.22, lfo=0.12, sat=0.5, hpf=420, lpf=2800, flfo=0.4),
            _CX(wet=0.22, delay=220, fb=0.18, lfo=0.1, sat=0.45, hpf=520, lpf=2400, flfo=0.35),
            _CX(wet=0.25, delay=250, fb=0.2, lfo=0.1, sat=0.5, hpf=480, lpf=3000, flfo=0.38),
            _CX(wet=0.2, delay=200, fb=0.15, lfo=0.08, sat=0.4, hpf=560, lpf=2600, flfo=0.32),
            _CX(wet=0.24, delay=240, fb=0.18, lfo=0.1, sat=0.45, hpf=400, lpf=2200, flfo=0.4),
            _CX(wet=0.18, delay=180, fb=0.14, lfo=0.08, sat=0.42, hpf=580, lpf=2500, flfo=0.35),
            _CX(wet=0.26, delay=260, fb=0.2, lfo=0.1, sat=0.48, hpf=450, lpf=2700, flfo=0.36),
            _CX(wet=0.19, delay=190, fb=0.15, lfo=0.08, sat=0.4, hpf=540, lpf=2300, flfo=0.33),
            _CX(wet=0.23, delay=230, fb=0.17, lfo=0.09, sat=0.46, hpf=500, lpf=2550, flfo=0.37),
            _CX(wet=0.17, delay=170, fb=0.13, lfo=0.07, sat=0.38, hpf=600, lpf=2100, flfo=0.34),
        ]),
        dict(ovl=80, play_reps=1, layers=[
            _CX(wet=0.3, delay=300, fb=0.25, lfo=0.12, sat=0.55, hpf=410, lpf=3200, flfo=0.45),
            _CX(wet=0.22, delay=210, fb=0.16, lfo=0.1, sat=0.48, hpf=530, lpf=2300, flfo=0.38),
            _CX(wet=0.26, delay=260, fb=0.2, lfo=0.1, sat=0.5, hpf=470, lpf=2700, flfo=0.4),
            _CX(wet=0.2, delay=190, fb=0.15, lfo=0.08, sat=0.42, hpf=570, lpf=2100, flfo=0.35),
            _CX(wet=0.24, delay=230, fb=0.18, lfo=0.1, sat=0.46, hpf=440, lpf=2900, flfo=0.42),
            _CX(wet=0.18, delay=170, fb=0.12, lfo=0.08, sat=0.4, hpf=590, lpf=2000, flfo=0.38),
            _CX(wet=0.27, delay=270, fb=0.21, lfo=0.11, sat=0.5, hpf=460, lpf=2800, flfo=0.4),
            _CX(wet=0.19, delay=185, fb=0.14, lfo=0.08, sat=0.41, hpf=510, lpf=2200, flfo=0.36),
            _CX(wet=0.23, delay=225, fb=0.17, lfo=0.09, sat=0.45, hpf=490, lpf=2500, flfo=0.39),
            _CX(wet=0.16, delay=160, fb=0.12, lfo=0.07, sat=0.38, hpf=550, lpf=1900, flfo=0.35),
        ]),
        dict(ovl=50, play_reps=1, layers=[
            _CX(wet=0.25, delay=240, fb=0.2, lfo=0.1, sat=0.48, hpf=430, lpf=2600, flfo=0.42),
            _CX(wet=0.2, delay=200, fb=0.15, lfo=0.08, sat=0.44, hpf=505, lpf=2200, flfo=0.36),
            _CX(wet=0.28, delay=270, fb=0.22, lfo=0.12, sat=0.52, hpf=465, lpf=3000, flfo=0.4),
            _CX(wet=0.18, delay=180, fb=0.14, lfo=0.08, sat=0.4, hpf=575, lpf=2400, flfo=0.34),
            _CX(wet=0.22, delay=220, fb=0.17, lfo=0.1, sat=0.46, hpf=415, lpf=2500, flfo=0.38),
            _CX(wet=0.16, delay=160, fb=0.12, lfo=0.06, sat=0.38, hpf=595, lpf=1900, flfo=0.4),
            _CX(wet=0.24, delay=235, fb=0.18, lfo=0.1, sat=0.47, hpf=445, lpf=2650, flfo=0.37),
            _CX(wet=0.19, delay=195, fb=0.15, lfo=0.08, sat=0.41, hpf=525, lpf=2150, flfo=0.35),
            _CX(wet=0.21, delay=215, fb=0.16, lfo=0.09, sat=0.43, hpf=485, lpf=2450, flfo=0.36),
            _CX(wet=0.15, delay=155, fb=0.11, lfo=0.06, sat=0.36, hpf=555, lpf=1850, flfo=0.38),
        ]),
    ],
    # HIPPO — densité 4 (HP1–4) + motion locale / sweep 1→8 (hippo_motion_06)
    # HPF ~400 sur certaines couches ; swap sample après 3 lectures
    1: [
        dict(ovl=80, play_reps=3, layers=[
            L(mode=4, step=480, xfade=35, sens=0, wet=0.35, delay=280, fb=0.28, lfo=0.15, on=1,
              sat=0.2, hpf=400, lpf=9000, flfo=0.1),
            L(mode=4, step=620, xfade=40, sens=1, wet=0.25, delay=200, fb=0.2, lfo=0.1, on=1,
              sat=0.25, hpf=70, lpf=8000, flfo=0.12),
            L(mode=1, rot=0.05, sens=1, wet=0.2, delay=180, fb=0.15, on=1,
              sat=0.15, hpf=400, lpf=10000, flfo=0.08),
            L(mode=4, step=550, xfade=35, sens=0, wet=0.22, delay=190, fb=0.16, on=1,
              sat=0.18, hpf=400, lpf=9500, flfo=0.1),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ]),
        dict(ovl=80, play_reps=3, layers=[
            L(mode=4, step=520, xfade=30, wet=0.3, delay=250, fb=0.25, lfo=0.12, on=1,
              sat=0.18, hpf=400, lpf=9500, flfo=0.1),
            L(mode=3, step=700, xfade=30, sens=1, wet=0.22, delay=180, fb=0.18, on=1,
              sat=0.22, hpf=400, lpf=8500, flfo=0.1),
            L(mode=4, step=580, xfade=35, sens=0, wet=0.2, delay=160, fb=0.15, on=1,
              sat=0.15, hpf=55, lpf=11000, flfo=0.08),
            L(mode=4, step=500, xfade=30, sens=1, wet=0.18, delay=170, fb=0.14, on=1,
              sat=0.16, hpf=400, lpf=9000, flfo=0.09),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ]),
        dict(ovl=80, play_reps=3, layers=[
            L(mode=4, step=450, xfade=30, sens=0, wet=0.32, delay=300, fb=0.25, lfo=0.15, on=1,
              sat=0.2, hpf=50, lpf=8800, flfo=0.12),
            L(mode=4, step=640, xfade=40, wet=0.2, delay=200, fb=0.18, on=1,
              sat=0.18, hpf=400, lpf=9200, flfo=0.1),
            L(mode=1, rot=0.04, sens=1, wet=0.18, delay=150, fb=0.15, on=1,
              sat=0.2, hpf=400, lpf=10500, flfo=0.08),
            L(mode=4, step=560, xfade=35, sens=0, wet=0.2, delay=175, fb=0.15, on=1,
              sat=0.17, hpf=400, lpf=9800, flfo=0.09),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ]),
    ],
    # RECON — zone haute: sat off, filtre ouvert, ECHO bas / dry
    2: [
        dict(ovl=80, play_reps=1, layers=[
            L(mode=0, sat=0, hpf=20, lpf=20000),
            L(mode=1, rot=0.015, sens=1, wet=0.12, delay=150, fb=0.15, lfo=0.08, on=1,
              sat=0.08, hpf=30, lpf=16000, flfo=0.05),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ]),
        dict(ovl=80, play_reps=1, layers=[
            L(mode=0, wet=0.1, delay=120, fb=0.12, lfo=0.05, on=1,
              sat=0, hpf=20, lpf=18000),
            L(mode=3, step=2500, xfade=80, wet=0.12, delay=140, fb=0.12, on=1,
              sat=0.1, hpf=35, lpf=15000, flfo=0.05),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ]),
        dict(ovl=80, play_reps=1, layers=[
            L(mode=1, rot=0.012, sens=0, wet=0.08, delay=100, fb=0.1, on=1,
              sat=0, hpf=20, lpf=20000),
            L(mode=0, sat=0, hpf=20, lpf=20000),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ]),
    ],
    # BOUCLE — hors cycle 1 artiste ; FORCE/debug uniquement
    3: [
        dict(ovl=80, play_reps=1, layers=[
            L(mode=2, step=5000, xfade=60, wet=0.7, delay=700, fb=0.55, lfo=0.4, on=1,
              sat=0.4, hpf=60, lpf=7000, flfo=0.15),
            L(mode=3, step=2800, xfade=50, sens=0, wet=0.35, delay=450, fb=0.3, on=1,
              sat=0.3, hpf=80, lpf=8000),
            L(mode=1, rot=0.04, sens=1, wet=0.3, delay=350, fb=0.25, on=1,
              sat=0.25, hpf=50, lpf=9000),
            L(mode=0, wet=0.25, delay=300, fb=0.2, on=1, sat=0.2, hpf=40, lpf=10000),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ]),
        dict(ovl=80, play_reps=1, layers=[
            L(mode=3, step=2500, xfade=50, sens=0, wet=0.65, delay=650, fb=0.5, lfo=0.35, on=1,
              sat=0.45, hpf=70, lpf=6500, flfo=0.2),
            L(mode=2, step=4000, xfade=60, wet=0.4, delay=500, fb=0.35, on=1,
              sat=0.3, hpf=90, lpf=7500),
            L(mode=1, rot=0.05, sens=0, wet=0.3, delay=380, fb=0.25, on=1,
              sat=0.25, hpf=55, lpf=8500),
            L(mode=0, wet=0.25, delay=280, fb=0.2, on=1, sat=0.2, hpf=45, lpf=9500),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ]),
        dict(ovl=80, play_reps=1, layers=[
            L(mode=1, rot=0.06, sens=1, wet=0.4, delay=550, fb=0.3, lfo=0.2, on=1,
              sat=0.35, hpf=65, lpf=7000, flfo=0.15),
            L(mode=2, step=3000, xfade=50, wet=0.45, delay=480, fb=0.35, on=1,
              sat=0.3, hpf=75, lpf=8000),
            L(mode=3, step=2200, xfade=45, sens=0, wet=0.35, delay=400, fb=0.3, on=1,
              sat=0.28, hpf=50, lpf=9000),
            L(mode=0, wet=0.25, delay=280, fb=0.2, on=1, sat=0.2, hpf=40, lpf=10000),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ]),
    ],
}

# Champs envoyés par bank (mode en dernier: les gates s'ouvrent params posés)
LAYER_FIELDS = [("rot", "rot"), ("sens", "sens"), ("step", "step"),
                ("xfade", "xfade"), ("wet", "wet"), ("del", "delay"),
                ("fb", "fb"), ("lfo", "lfo"), ("on", "on"),
                ("sat", "sat"), ("hpf", "hpf"), ("lpf", "lpf"), ("flfo", "flfo"),
                ("mode", "mode")]

# CONTRASTE (Q24): facteur appliqué à wet/fb/lfo — défaut HAUT (1.0)
CONTRASTE_BAS = 0.65

# Presets opératoires V0 FR (§3.7 / §7.2): (nom, FSM_AUTO, INSTALL_MODE, CONTRASTE)
PRESETS_V0 = [
    ("mode_presentation", 1, 1, 0),
    ("mode_edition_complete", 0, 0, 1),
    ("mode_automatique", 1, 1, 1),
    ("mode_danse", 1, 0, 1),
]


def fmt(v):
    return f"{v:g}"


def bank_msg_body(bank):
    """Corps d'un message multi-send Pd pour une variante (state x var)."""
    parts = []
    for i, lay in enumerate(bank["layers"], start=1):
        for send, field in LAYER_FIELDS:
            parts.append(f"s6_l{i}_{send} {fmt(lay[field])}")
    parts.append(f"s6_cortex_ovl {fmt(bank['ovl'])}")
    # nb de lectures d'un même sample avant swap (1 = à chaque EOF)
    parts.append(f"s6_play_reps {fmt(bank.get('play_reps', 1))}")
    return " \\; ".join(parts)


def fsm_n_padded(fsm_n, max_layers):
    """Normalise FSM_N en tuples (n, d0..d{max_layers-1})."""
    out = {}
    for s, tup in fsm_n.items():
        n = tup[0]
        slots = list(tup[1:]) + [0] * max_layers
        out[s] = (n, *slots[:max_layers])
    return out
