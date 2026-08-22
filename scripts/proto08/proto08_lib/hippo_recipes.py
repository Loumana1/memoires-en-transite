"""5 recettes spatiales Hippocampe V1 — Q26."""

from __future__ import annotations

# layer -> params (spatial_router_06)
RECIPES: list[dict[int, dict]] = [
    {  # 0 — contre-rotation panoramique
        1: {"mode": 1, "rot": 0.04, "sens": 0, "xfade": 35},
        2: {"mode": 1, "rot": 0.07, "sens": 1, "xfade": 35},
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
    {  # 4 — fixe + orbite
        1: {"mode": 0, "xfade": 35},
        2: {"mode": 1, "rot": 0.03, "xfade": 35},
    },
]

INIT_LAYERS = {
    1: {"mode": 4, "step": 1100, "sens": 0, "xfade": 35},
    2: {"mode": 4, "step": 1600, "sens": 1, "xfade": 35},
    3: {"mode": 2, "step": 1400, "sens": 0, "xfade": 35},
    4: {"mode": 2, "step": 1800, "sens": 1, "xfade": 35},
    13: {"mode": 4, "step": 1500, "xfade": 35},
}
