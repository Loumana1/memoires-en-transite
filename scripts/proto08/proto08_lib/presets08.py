"""Presets Proto 08 8HP — 6 baffles × 2 voix + 2 ambiances globales.

Cycle AUTO: Cortex 40 s → Hippo 50 s → Recon 2 min.
[Q10] deux plans : PREMIER_PLAN + ARRIERE_PLAN (INTERMEDIAIRE abandonné).
"""
from . import layout08 as LAY

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
# Seul le baffle est choisi ici : l'azimut vient du layout, il n'est plus
# recopié à la main à côté du numéro.
LAYER_HP_8HP = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 4]
ANCHORS_8HP = LAY.anchors(LAYER_HP_8HP)
DECODE_8HP_AZ = LAY.azimuths()

# Baffles ambiance Cortex — musicale HP7, texture HP8 (oreille Loumana 24 août).
# [Q25] préférait non-adjacent ; HP7/HP8 voisins — choix assumé pour libérer HP5.
AMBI_MUSICAL_HP = 7
AMBI_TEXTURE_HP = 8

LAYER_DEFAULT = dict(mode=0, rot=0.02, sens=0, step=800, xfade=30,
                     wet=0, delay=200, fb=0, lfo=0, on=0,
                     sat=0, hpf=20, lpf=20000, flfo=0)

# Gain nappes Cortex — spec §7 : 0,25 · paroles un peu plus basses pour laisser respirer
# Les nappes sont normalisées à -45 dB RMS par normaliser_niveaux.py, contre
# -23 pour les fragments : 22 dB d'écart que le mixage du patch doit rendre,
# c'était le pari de CIBLE_AMBIANCE. À 0.42 il n'en rendait que 6,5, et avec
# 12 fragments contre 2 nappes celles-ci jouaient ~23 dB sous la masse du
# Cortex — inaudibles. À 2.0 elles passent ~10 dB dessous ; +3 dB à l'écoute
# Loumana (22 août) → 2.825 ; +2 dB (24 août) → 3.556. Puis écart musicale/texture :
CORTEX_AMB_GAIN = 3.556  # référence (couche 13 Hippo/Recon si utilisée)
CORTEX_AMB_GAIN_MUSICAL = 3.556 * (10 ** (4 / 20))   # HP7 · +4 dB vs 3.556 → ~5.638
CORTEX_AMB_GAIN_TEXTURE = 3.556 * (10 ** (-2 / 20))  # HP8 · −2 dB vs 3.556 → ~2.826
# Bleed musicale → HP1–6 (couches voix) : présence dans le champ ; HP7 un peu baissé.
CORTEX_AMB_MUSICAL_BLEED = 0.14       # ~−17 dB par baffle voix
CORTEX_AMB_MUSICAL_HP7_SCALE = 0.794  # ~−2 dB sur la source dédiée HP7

# HPF momentané voix HP1–6 (paroles seulement — pas bleed / nappes).
CORTEX_VOIX_HPF_HZ = 400
CORTEX_VOIX_HPF_ATTACK_MS = 600
CORTEX_VOIX_HPF_HOLD_MS = 2800
CORTEX_VOIX_HPF_RELEASE_MS = 2000
# 1× auto par passage Cortex (sans piezo), tiré entre 8 et 33 s après l'entrée.
CORTEX_VOIX_HPF_CYCLE_DELAY_MIN = 8000
CORTEX_VOIX_HPF_CYCLE_DELAY_RAND = 25000
CORTEX_LAYER_GAIN = 0.20
# Gains plans présence §5 bis (linéaire)
GAIN_PREMIER_PLAN = 1.0
GAIN_ARRIERE_PLAN = 0.79

# Voyage spatial Cortex : la voix d'arrière-plan quitte son baffle, parcourt un
# demi-tour (phi) et revient. Une seule fois par passage, sur 2 baffles tirés.
# Le décodage ordre 1 donne +6 dB sur le HP d'axe : TRAVEL_GAIN compense.
CORTEX_TRAVEL_GAIN = 0.45
CORTEX_TRAVEL_MS = 15000
CORTEX_TRAVEL_ARC = 180
CORTEX_TRAVEL_XFADE = 500
CORTEX_TRAVEL_DELAY_MIN = 5000
CORTEX_TRAVEL_DELAY_RAND = 10000

# Plages du balayage LPF « underwater » — c'est ce qui sépare les deux plans à
# l'oreille : l'avant est ouvert, l'arrière est sourd (§5 bis).
CORTEX_LPF_AVANT = (800, 2000)
CORTEX_LPF_ARRIERE = (500, 1000)

# Échange avant / arrière : la voix d'arrière-plan passe devant, celle de
# devant recule. Gains et plages de filtre glissent ensemble. Quelques
# rendez-vous par passage, sur une paire tirée à chaque fois.
CORTEX_SWAP_COUNT = 4
CORTEX_SWAP_MS = 7000
CORTEX_SWAP_RISE = 2500        # montée et descente ; le reste est tenu
CORTEX_SWAP_FIRST = 3000       # premier rendez-vous après l'entrée en Cortex
CORTEX_SWAP_EVERY = 8000       # écart nominal entre deux rendez-vous
CORTEX_SWAP_JITTER = 2500      # tiré en plus, pour ne pas être métronomique
# Gains des deux plans pendant l'échange (voir GAIN_PREMIER/ARRIERE_PLAN).
CORTEX_SWAP_DELTA = GAIN_PREMIER_PLAN - GAIN_ARRIERE_PLAN
# Volet spatial : la voix qui remonte devant se décale aussi en azimut. Bien
# plus court que l'arc du voyage (CORTEX_TRAVEL_ARC) — ici on veut un
# déhanchement, pas un déplacement. Une paire ne fait jamais les deux à la
# fois : chaque paire n'a qu'un encodeur, et deux gestes ne peuvent pas écrire
# le même azimut.
CORTEX_SWAP_ARC = 60
CORTEX_SWAP_ENC = 0.4          # part envoyée à l'encodeur pendant l'échange

CORTEX_SPECTRAL_RECIPES = [
    "MUR_TREMBLE", "RIPPLE", "DOMINO_OUVERTURE", "CLUSTER_BREATHE",
]

CORTEX_SPECTRAL_PROBA = 0.65          # probabilité d'un geste par passage Cortex
CORTEX_SPECTRAL_T0_MIN = 8000         # ms avant 1er déclenchement (éviter le boot)
CORTEX_SPECTRAL_T0_RAND = 12000       # jitter additionnel

# Par recette
CORTEX_SPECTRAL_MUR_FACTOR = 3.0
CORTEX_SPECTRAL_MUR_MS = 4000

CORTEX_SPECTRAL_RIPPLE_MS = 3200
CORTEX_SPECTRAL_RIPPLE_NEIGH_DELAY = 90   # ms
CORTEX_SPECTRAL_RIPPLE_NEIGH_AMP = 0.6

CORTEX_SPECTRAL_DOMINO_MS = 4000
CORTEX_SPECTRAL_DOMINO_STEP_MS = 80
CORTEX_SPECTRAL_DOMINO_LPF = (800, 1600, 800)

CORTEX_SPECTRAL_CLUSTER_MS = 6000
CORTEX_SPECTRAL_CLUSTER_LFO = 0.6         # Hz
CORTEX_SPECTRAL_CLUSTER_LPF = (450, 1100)


def layers_for_hp(hp: int) -> list[int]:
    """Indices 1-based des couches L sur ce baffle parole."""
    return [i + 1 for i, h in enumerate(LAYER_HP_8HP[:12]) if h == hp]


def L(**kw):
    d = dict(LAYER_DEFAULT)
    d.update(kw)
    return d


IDLE = L()

# [Q10] defaults §5 bis Cortex.md — premier = plus ouvert, arrière = pièce voisine (delay+fb)
PLAN_PREMIER = dict(mode=0, on=1, sat=0.48, hpf=300, lpf=1400, flfo=0,
                    wet=0.05, delay=110, fb=0.05, lfo=0.04)
PLAN_ARRIERE = dict(mode=0, on=1, sat=0.52, hpf=60, lpf=750, flfo=0,
                    wet=0.28, delay=260, fb=0.30, lfo=0.025)

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
