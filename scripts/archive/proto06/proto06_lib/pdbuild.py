"""Réexportation — le builder Pd vit maintenant dans `scripts/shared/pdbuild.py`.

Déplacé le 20 août 2026. Ce fichier existe pour que les générateurs et les
tests du Proto 06 (`from .pdbuild import P`) continuent de fonctionner sans
qu'il y ait deux copies du même code. Ne rien ajouter ici : toute
modification va dans `scripts/shared/pdbuild.py`.
"""
import os
import sys

_SCRIPTS = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
)
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

from shared.pdbuild import P  # noqa: E402,F401

__all__ = ["P"]
