"""Presets Proto 08 8HP — 6 baffles × 2 voix + 2 ambiances globales.

Cycle AUTO: Cortex 40 s → Hippo 50 s → Recon 2 min.
[Q10] deux plans : PREMIER_PLAN + ARRIERE_PLAN (INTERMEDIAIRE abandonné).
"""
ETAT_NOMS = ["CORTEX", "HIPPOCAMPE", "RECONSTRUCTION", "BOUCLE"]

# 12 paroles Cortex + 1 nappe Hippo/Recon (couche 13).
MAX_LAYERS_8HP = 13

FSM_N_8HP = {
    0: (12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),   # 12 voix Cortex
    1: (4, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),    # 2 longs + 2 courts Hippo V1
    2: (2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    3: (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
}

CYCLE1_8HP = [(0, 40000), (1, 50000), (2, 120000)]
FREE_DUR_BASE = 40000
FREE_DUR_RAND = 50000
FREE_CORTEX_EVERY = 5
RESET_MS = 420000
BOUCLE_PROBA = 15
BOUCLE_DUR_MS = 6000

# L1–L12 → cortex_pair_08 (HP1–6). L13 = nappe mobile Hippo.
ANCHORS_8HP = [
    (1, 0), (1, 0), (2, 45), (2, 45), (3, 90), (3, 90),
    (4, 135), (4, 135), (5, 180), (5, 180), (6, 225), (6, 225),
    (4, 135),
]
DECODE_8HP_AZ = [0, 45, 90, 135, 180, 225, 270, 315]

# Baffles ambiance Cortex fixés — non adjacents ([Q25]).
AMBI_MUSICAL_HP = 7   # 1-indexed HP7
AMBI_TEXTURE_HP = 5   # HP5 (écart avec HP7)

LAYER_DEFAULT = dict(mode=0, rot=0.02, sens=0, step=800, xfade=30,
                     wet=0, delay=200, fb=0, lfo=0, on=0,
                     sat=0, hpf=20, lpf=20000, flfo=0)

# Gain nappes Cortex — spec §7 : 0,25 · paroles un peu plus basses pour laisser respirer
CORTEX_AMB_GAIN = 0.25
CORTEX_LAYER_GAIN = 0.20
# Gains plans présence §5 bis (linéaire)
GAIN_PREMIER_PLAN = 1.0
GAIN_ARRIERE_PLAN = 0.79


def L(**kw):
    d = dict(LAYER_DEFAULT)
    d.update(kw)
    return d


IDLE = L()

# [Q10] defaults §5 bis Cortex.md — premier = plus ouvert, arrière = pièce voisine (delay+fb)
PLAN_PREMIER = dict(mode=0, on=1, sat=0.48, hpf=300, lpf=1400, flfo=0,
                    wet=0.05, delay=110, fb=0.05, lfo=0.04)
PLAN_ARRIERE = dict(mode=0, on=1, sat=0.52, hpf=60, lpf=750, flfo=0,
                    wet=0.20, delay=260, fb=0.22, lfo=0.025)

# Nappes : sèches en Cortex (§7) — pas de wet/delay audibles
AMB_MUSICALE_FX = dict(mode=0, on=1, sat=0, hpf=30, lpf=18000, flfo=0,
                       wet=0, delay=40, fb=0, lfo=0)
AMB_TEXTURE_FX = dict(mode=0, on=1, sat=0, hpf=40, lpf=16000, flfo=0,
                      wet=0, delay=40, fb=0, lfo=0)


def _CX_PREMIER(**kw):
    d = dict(PLAN_PREMIER)
    d.update(kw)
    return L(**d)


def _CX_ARRIERE(**kw):
    d = dict(PLAN_ARRIERE)
    d.update(kw)
    return L(**d)


def _cortex_twelve_parole():
    """Alternance premier / arrière par paire (L1+L2, …)."""
    out = []
    for i in range(12):
        if i % 2 == 0:
            out.append(_CX_PREMIER(hpf=300 + (i % 4) * 15, lpf=1350 + i * 5))
        else:
            out.append(_CX_ARRIERE(hpf=55 + i * 3, lpf=720 + i * 8,
                                   wet=0.18 + (i % 3) * 0.02))
    return out


def _HP(**kw):
    d = dict(mode=4, step=1400, xfade=35, on=1, sat=0.06, hpf=40,
             lpf=9000, wet=0.10, delay=140, fb=0.08, lfo=0.02)
    d.update(kw)
    return L(**d)


_AM = L(mode=0, on=0, sat=0, hpf=30, lpf=18000, wet=0, delay=40, fb=0, flfo=0)


# Champs lus par fx_router_06 (pas mode/rot/step — gérés par spatial_router ailleurs).
FX_ROUTER_FIELDS = [("wet", "wet"), ("del", "delay"), ("fb", "fb"), ("lfo", "lfo"),
                    ("on", "on"), ("sat", "sat"), ("hpf", "hpf"), ("lpf", "lpf"),
                    ("flfo", "flfo")]


def amb_fx_msg(layer_idx: int, spec: dict) -> str:
    """Message Pd pour fx_router (couches 15 = musicale, 16 = texture)."""
    parts = []
    for send, field in FX_ROUTER_FIELDS:
        if field in spec:
            parts.append(f"s6_l{layer_idx}_{send} {fmt(spec[field])}")
    return " \\; ".join(parts)
_RC0 = L(mode=1, rot=0.012, sens=0, sat=0, hpf=20, lpf=20000,
         wet=0.06, delay=100, fb=0.08, lfo=0.03, on=1)
_RC1 = L(mode=0, sat=0.08, hpf=25, lpf=12000, wet=0.14, delay=180, fb=0.12, on=1)


def _layers13(parole12, amb=_AM):
    ls = list(parole12) + [amb]
    while len(ls) < MAX_LAYERS_8HP:
        ls.append(IDLE)
    return ls[:MAX_LAYERS_8HP]


PRESETS_8HP = {
    0: [
        dict(ovl=70, play_reps=1, layers=_layers13(_cortex_twelve_parole())),
        dict(ovl=95, play_reps=1, layers=_layers13(_cortex_twelve_parole())),
        dict(ovl=80, play_reps=1, layers=_layers13(_cortex_twelve_parole())),
    ],
    1: [
        dict(ovl=5, play_reps=1, layers=_layers13([
            _HP(step=1100, sens=0, mode=4),
            _HP(step=1600, sens=1, mode=2),
            _HP(step=2200, sens=1, mode=4),
            _HP(step=1400, sens=0, mode=2),
        ] + [IDLE] * 8)),
        dict(ovl=5, play_reps=1, layers=_layers13([
            _HP(step=1300, mode=4),
            _HP(step=1900, sens=1, mode=2),
            _HP(step=1000, mode=4),
            _HP(step=2100, sens=1, mode=2),
        ] + [IDLE] * 8)),
        dict(ovl=5, play_reps=1, layers=_layers13([
            _HP(step=1700, mode=2),
            _HP(step=1200, sens=1, mode=4),
            _HP(step=2000, mode=2),
            _HP(step=1500, sens=1, mode=4),
        ] + [IDLE] * 8)),
    ],
    2: [
        dict(ovl=5, play_reps=1, layers=_layers13([_RC0, _RC1] + [IDLE] * 10)),
        dict(ovl=5, play_reps=1, layers=_layers13([
            L(mode=1, rot=0.01, sens=1, sat=0, lpf=20000, wet=0.1, delay=120, on=1),
            L(mode=3, step=2200, xfade=80, sat=0, wet=0.08, on=1),
        ] + [IDLE] * 10)),
        dict(ovl=5, play_reps=1, layers=_layers13([
            L(mode=0, sat=0, lpf=20000),
            L(mode=1, rot=0.008, wet=0.06, delay=90, on=1, sat=0),
        ] + [IDLE] * 10)),
    ],
    3: [
        dict(ovl=5, play_reps=1, layers=_layers13([
            L(mode=2, step=1800, xfade=40, wet=0.25, delay=400, fb=0.3, on=1, sat=0.2, lpf=6000),
            L(mode=0, wet=0.18, delay=260, fb=0.22, on=1, sat=0.12, lpf=5500),
        ] + [IDLE] * 10)),
        dict(ovl=5, play_reps=1, layers=_layers13([
            L(mode=3, step=900, wet=0.2, delay=350, on=1, sat=0.18, lpf=7000),
        ] + [IDLE] * 11)),
        dict(ovl=5, play_reps=1, layers=_layers13([
            L(mode=1, rot=0.04, wet=0.22, delay=280, on=1, sat=0.15),
        ] + [IDLE] * 11)),
    ],
}

LAYER_FIELDS = [("rot", "rot"), ("sens", "sens"), ("step", "step"),
                ("xfade", "xfade"), ("wet", "wet"), ("del", "delay"),
                ("fb", "fb"), ("lfo", "lfo"), ("on", "on"),
                ("sat", "sat"), ("hpf", "hpf"), ("lpf", "lpf"), ("flfo", "flfo"),
                ("mode", "mode")]
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
