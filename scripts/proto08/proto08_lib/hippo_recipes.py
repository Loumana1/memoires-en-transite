"""5 recettes spatiales Hippocampe V1 — Q26."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Rotations mode 1 (phasor~ × rot → encode_2d — fluide ambisonique)
# Calibrer à l'oreille avec : ; s6_hippo_motion 0  (recette 0)
#                             ; s6_hippo_motion 4  (recette 4 / orbite)
# Ordre de grandeur : 0.18 Hz = 1 tour en ~5.5 s, perceptible en salle.
# ---------------------------------------------------------------------------
ROT_PAN_SLOW = 0.18   # recette 0 L1 — contre-rotation lente (était 0.04)
ROT_PAN_FAST = 0.32   # recette 0 L2 — contre-rotation rapide (était 0.07)
ROT_ORBIT    = 0.22   # recette 4 L2 — orbite (fixé + qui tourne) (était 0.03)

# layer -> params (spatial_router_06)
RECIPES: list[dict[int, dict]] = [
    {  # 0 — contre-rotation panoramique (fluide perceptible)
        1: {"mode": 1, "rot": ROT_PAN_SLOW, "sens": 0, "xfade": 35},
        2: {"mode": 1, "rot": ROT_PAN_FAST, "sens": 1, "xfade": 35},
    },
    {  # 1 — contre-rotation saut
        1: {"mode": 3, "step": 1400, "sens": 0, "xfade": 35},
        2: {"mode": 3, "step": 750, "sens": 1, "xfade": 35},
    },
    {  # 2 — local + saut (3 voyageurs)
        1: {"mode": 4, "step": 1100, "xfade": 35},
        2: {"mode": 2, "step": 1600, "xfade": 35},
        3: {"mode": 4, "step": 2200, "xfade": 35},
    },
    {  # 3 — opposition
        1: {"mode": 3, "step": 2000, "sens": 0, "xfade": 35},
        2: {"mode": 3, "step": 2000, "sens": 1, "xfade": 35},
    },
    {  # 4 — fixé + orbite (fluide perceptible)
        1: {"mode": 0, "xfade": 35},
        2: {"mode": 1, "rot": ROT_ORBIT, "xfade": 35},
    },
]

INIT_LAYERS = {
    1: {"mode": 4, "step": 1100, "sens": 0, "xfade": 35},
    2: {"mode": 4, "step": 1600, "sens": 1, "xfade": 35},
    3: {"mode": 2, "step": 1400, "sens": 0, "xfade": 35},
    4: {"mode": 2, "step": 1800, "sens": 1, "xfade": 35},
    13: {"mode": 4, "step": 1500, "xfade": 35},
}
