"""Recettes spatiales Reconstruction V1 — modes Simon §14 (Q31)."""

from __future__ import annotations

# layer (1=L1 fil, 2=L2 court) -> spatial_router params
SPATIAL_RECIPES: list[dict[int, dict]] = [
    {  # 0 CONVERGENCE — fragments rapprochés
        1: {"mode": 3, "step": 1800, "sens": 0, "xfade": 80},
        2: {"mode": 3, "step": 1200, "sens": 1, "xfade": 60},
    },
    {  # 1 CONSTELLATION — dispersion puis points fixes
        1: {"mode": 3, "step": 2400, "sens": 0, "xfade": 80},
        2: {"mode": 2, "step": 1600, "sens": 1, "xfade": 60},
    },
    {  # 2 HALO — rotation lente fil + fixe interruptions
        1: {"mode": 1, "rot": 0.008, "sens": 0, "xfade": 80},
        2: {"mode": 0, "xfade": 40},
    },
    {  # 3 DISPERSION — sauts opposés
        1: {"mode": 2, "step": 2000, "sens": 0, "xfade": 70},
        2: {"mode": 3, "step": 900, "sens": 1, "xfade": 50},
    },
]

SPATIAL_NAMES = ("CONVERGENCE", "CONSTELLATION", "HALO", "DISPERSION")
