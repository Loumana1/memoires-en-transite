"""Presets Proto 07 8HP — Q&A 16 août 2026.

Cycle AUTO: Cortex 40 s → Hippo 50 s → Recon 2 min.
9 couches: 8 fragments (HP1–8) + 1 ambiance (HP variable).
"""
ETAT_NOMS = ["CORTEX", "HIPPOCAMPE", "RECONSTRUCTION", "BOUCLE"]

# n = fragments actifs (ambiance = couche 9, gated à part).
# slot durée 0=COURT 1=MOYEN 2=LONG (ignoré en CORTEX exclusif)
FSM_N_8HP = {
    0: (6, 0, 0, 0, 0, 0, 0, 0, 0, 0),   # 6 frag = 3 baffles x 2
    1: (4, 1, 1, 1, 0, 0, 0, 0, 0, 0),   # 3 longs (≥8 s) + 1 court
    2: (2, 1, 0, 0, 0, 0, 0, 0, 0, 0),   # principal MOYEN + interrupt COURT
    3: (2, 0, 0, 0, 0, 0, 0, 0, 0, 0),   # réinjection courte
}
MAX_LAYERS_8HP = 9

CYCLE1_8HP = [(0, 40000), (1, 50000), (2, 120000)]
FREE_DUR_BASE = 40000
FREE_DUR_RAND = 50000
FREE_CORTEX_EVERY = 5
RESET_MS = 420000
BOUCLE_PROBA = 15          # % à une transition libre
BOUCLE_DUR_MS = 6000       # pique, pas un paysage

# Cortex: L1-L6 = 3 paires HP1-3 ; 5 nappes HP4-8 ; Hippo/Recon spatial 1:1.
ANCHORS_8HP = [
    (1, 0), (2, 45), (3, 90), (4, 135),
    (5, 180), (6, 225), (7, 270), (8, 315),
    (4, 135),
]
DECODE_8HP_AZ = [0, 45, 90, 135, 180, 225, 270, 315]

LAYER_DEFAULT = dict(mode=0, rot=0.02, sens=0, step=800, xfade=30,
                     wet=0, delay=200, fb=0, lfo=0, on=0,
                     sat=0, hpf=20, lpf=20000, flfo=0)


def L(**kw):
    d = dict(LAYER_DEFAULT)
    d.update(kw)
    return d


IDLE = L()

def _CX(**kw):
    # LPF 1500, bouge 500-2000 via cortex_ctrl (flfo 06 off pour pas doubler).
    d = dict(mode=0, on=1, sat=0.58, hpf=520, lpf=1500, flfo=0,
             wet=0.10, delay=180, fb=0.06, lfo=0.06)
    d.update(kw)
    return L(**d)


def _HP(**kw):
    # Voyageurs: peu d'FX. step = ms entre baffles. xfade court = saut sec.
    d = dict(mode=4, step=1400, xfade=35, on=0, sat=0.08, hpf=40,
             lpf=9000, wet=0.06, delay=80, fb=0.06, lfo=0.03)
    d.update(kw)
    return L(**d)


# Ambiance Cortex: sèche, ouverte, pas de reverb. Hippo: LPF 1000 Hz via ctrl.
_AM = L(mode=0, on=0, sat=0, hpf=30, lpf=18000, wet=0, delay=40, fb=0, flfo=0)

_RC0 = L(mode=1, rot=0.012, sens=0, sat=0, hpf=20, lpf=20000,
         wet=0.08, delay=100, fb=0.1, lfo=0.04, on=1)
_RC1 = L(mode=0, sat=0, hpf=25, lpf=18000, wet=0.05, delay=80, on=0)


def _nine(layers8, amb=_AM):
    ls = list(layers8) + [amb]
    while len(ls) < 9:
        ls.append(IDLE)
    return ls[:9]


PRESETS_8HP = {
    0: [
        # LPF 1500, sweep 500-2000 (oreille 18 aout).
        dict(ovl=45, play_reps=1, layers=_nine([
            _CX(sat=0.62, hpf=480),
            _CX(sat=0.55, hpf=560),
            _CX(sat=0.60, hpf=520),
            _CX(sat=0.52, hpf=600),
            _CX(sat=0.58, hpf=450),
            _CX(sat=0.54, hpf=580),
            IDLE, IDLE,
        ])),
        dict(ovl=80, play_reps=1, layers=_nine([
            _CX(sat=0.65, hpf=470),
            _CX(sat=0.56, hpf=570),
            _CX(sat=0.60, hpf=510),
            _CX(sat=0.52, hpf=610),
            _CX(sat=0.58, hpf=490),
            _CX(sat=0.50, hpf=630),
            IDLE, IDLE,
        ])),
        dict(ovl=50, play_reps=1, layers=_nine([
            _CX(sat=0.60, hpf=490),
            _CX(sat=0.54, hpf=545),
            _CX(sat=0.63, hpf=510),
            _CX(sat=0.50, hpf=615),
            _CX(sat=0.58, hpf=465),
            _CX(sat=0.52, hpf=590),
            IDLE, IDLE,
        ])),
    ],
    1: [
        dict(ovl=5, play_reps=1, layers=_nine([
            _HP(step=1100, sens=0, mode=4),
            _HP(step=1600, sens=1, mode=2),
            _HP(step=2200, sens=1, mode=4),
            _HP(step=1400, sens=0, mode=2),
            IDLE, IDLE, IDLE, IDLE,
        ])),
        dict(ovl=5, play_reps=1, layers=_nine([
            _HP(step=1300, mode=4),
            _HP(step=1900, sens=1, mode=2),
            _HP(step=1000, mode=4),
            _HP(step=2100, sens=1, mode=2),
            IDLE, IDLE, IDLE, IDLE,
        ])),
        dict(ovl=5, play_reps=1, layers=_nine([
            _HP(step=1700, mode=2),
            _HP(step=1200, sens=1, mode=4),
            _HP(step=2000, mode=2),
            _HP(step=1500, sens=1, mode=4),
            IDLE, IDLE, IDLE, IDLE,
        ])),
    ],
    2: [
        dict(ovl=5, play_reps=1, layers=_nine([
            _RC0, _RC1, IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ])),
        dict(ovl=5, play_reps=1, layers=_nine([
            L(mode=1, rot=0.01, sens=1, sat=0, lpf=20000, wet=0.1, delay=120, on=1),
            L(mode=3, step=2200, xfade=80, sat=0, wet=0.08, on=1),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ])),
        dict(ovl=5, play_reps=1, layers=_nine([
            L(mode=0, sat=0, lpf=20000),
            L(mode=1, rot=0.008, wet=0.06, delay=90, on=1, sat=0),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ])),
    ],
    3: [
        dict(ovl=5, play_reps=1, layers=_nine([
            L(mode=2, step=1800, xfade=40, wet=0.25, delay=400, fb=0.3, on=1, sat=0.2, lpf=6000),
            L(mode=0, wet=0.15, delay=300, on=1, sat=0.15),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ])),
        dict(ovl=5, play_reps=1, layers=_nine([
            L(mode=3, step=900, wet=0.2, delay=350, on=1, sat=0.18, lpf=7000),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ])),
        dict(ovl=5, play_reps=1, layers=_nine([
            L(mode=1, rot=0.04, wet=0.22, delay=280, on=1, sat=0.15),
            IDLE, IDLE, IDLE, IDLE, IDLE, IDLE, IDLE,
        ])),
    ],
}

LAYER_FIELDS = [("rot", "rot"), ("sens", "sens"), ("step", "step"),
                ("xfade", "xfade"), ("wet", "wet"), ("del", "delay"),
                ("fb", "fb"), ("lfo", "lfo"), ("on", "on"),
                ("sat", "sat"), ("hpf", "hpf"), ("lpf", "lpf"), ("flfo", "flfo"),
                ("mode", "mode")]
# Spat / filtre tout de suite. Delay/reverb 500 ms plus tard: la queue peut resonner.
LAYER_FIELDS_NOW = [("rot", "rot"), ("sens", "sens"), ("step", "step"),
                    ("xfade", "xfade"), ("sat", "sat"), ("hpf", "hpf"),
                    ("lpf", "lpf"), ("flfo", "flfo"), ("mode", "mode")]
LAYER_FIELDS_TAIL = [("wet", "wet"), ("del", "delay"), ("fb", "fb"),
                     ("lfo", "lfo"), ("on", "on")]

CONTRASTE_BAS = 0.35
PRESETS_V0 = [
    ("mode_presentation", 1, 1, 0),
    ("mode_edition_complete", 0, 0, 1),
    ("mode_automatique", 1, 1, 1),
    ("mode_danse", 1, 0, 1),
]


def fmt(v):
    return f"{v:g}"


def bank_msg_body(bank, fields=None):
    fields = fields or LAYER_FIELDS
    parts = []
    for i, lay in enumerate(bank["layers"], start=1):
        for send, field in fields:
            parts.append(f"s6_l{i}_{send} {fmt(lay[field])}")
    if fields is LAYER_FIELDS or fields is LAYER_FIELDS_NOW:
        parts.append(f"s6_cortex_ovl {fmt(bank['ovl'])}")
        parts.append(f"s6_play_reps {fmt(bank.get('play_reps', 1))}")
    return " \\; ".join(parts)


def fsm_n_padded(fsm_n, max_layers):
    out = {}
    for s, tup in fsm_n.items():
        n = tup[0]
        slots = list(tup[1:]) + [0] * max_layers
        out[s] = (n, *slots[:max_layers])
    return out
