#!/usr/bin/env python3
"""Mesure la sonie de chaque fragment et calcule un gain de normalisation.

**Ne modifie aucun wav.** Le gain est inscrit dans le registre
(`docs/Matiere/registre_ids.csv`, colonnes `niveau_db` et `gain_db`), donc la
mesure est toujours refaite sur le fichier d'origine : relancer le script ne
peut pas cumuler deux normalisations. C'est réversible, et c'est auditable.

Pourquoi normaliser, et pourquoi ce n'est pas une question de volume :

  1. La saturation est **non linéaire**. Les couches du Cortex passent par
     `sat` 0,50 à 0,65 : un fragment à −14 dBFS attaque le saturateur, un
     fragment à −45 dBFS ne le touche pas. Le timbre de la zone dépend donc
     aujourd'hui du fichier tiré, ce qui contredit le principe « la zone
     impose son timbre, pas le fichier ».
  2. Les **plans de présence** (Q10) sont des écarts de 6 à 10 dB. Sur une
     matière qui varie de 47 dB, ils sont inaudibles comme intention.

On mesure la **sonie de la parole active**, pas le pic : le pic ne dit rien
d'utile sur de la parole. Méthode : RMS par blocs de 50 ms, on ne garde que
les blocs à moins de 30 dB sous le bloc le plus fort, et on moyenne.

Garde-fous :

  - **plafond de gain** (défaut +12 dB). Certaines tranches ne sont pas des
    voix faibles mais du fond de salle gardé par erreur par le détecteur de
    silence : `C002` est à −54,9 dBFS pour un fond à −57,7, soit moins de 3 dB
    d'écart. Les remonter de 33 dB ne produirait que du souffle. Le plafond
    les laisse en place et le rapport les signale.
  - **cible séparée pour les ambiances**, qui vivent 21 dB sous les paroles.
    Le but n'est pas d'aligner ambiances et paroles — c'est de rendre les
    ambiances cohérentes entre elles, pour que l'équilibre parole/ambiance
    devienne un réglage du moteur au lieu d'une propriété de la matière.

Usage:
  python3 scripts/normaliser_niveaux.py --rapport         # mesurer sans écrire
  python3 scripts/normaliser_niveaux.py
  python3 scripts/normaliser_niveaux.py --cible-parole -20 --plafond 15

Où le gain sera appliqué : chaque lecteur a déjà un `*~ 0.9` en sortie de
`readsf~` (`player_state_07`). C'est là que le gain par fragment doit entrer,
via un troisième mot dans les lignes des playlists. Câblage à faire dans le
Proto 08, avec les plans de présence.
"""
from __future__ import annotations

import argparse
import csv
import statistics as st
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "proto07"))
from sons_v3_paths import wav_path  # noqa: E402

try:
    import numpy as np
except ImportError:
    sys.exit("pip3 install numpy")

ROOT = Path(__file__).resolve().parent.parent
SONS = ROOT / "SONS_V3"
REGISTRE = ROOT / "docs" / "Matiere" / "registre_ids.csv"

PLEINE_ECHELLE = 32768.0
BLOC_S = 0.05
SEUIL_ACTIF_DB = 30.0      # un bloc compte s'il est à moins de 30 dB du plus fort
CIBLE_PAROLE = -23.0
CIBLE_AMBIANCE = -45.0
PLAFOND_GAIN = 12.0
SEUIL_SUSPECT = -45.0      # sous ça, ce n'est probablement pas de la matière


def db(x: float) -> float:
    return -200.0 if x <= 0 else float(20.0 * np.log10(x))


def mesurer(path: Path) -> tuple[float, float, float] | None:
    """(niveau actif, pic, plancher) en dBFS."""
    try:
        with wave.open(str(path), "rb") as w:
            rate = w.getframerate()
            x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
    except Exception:
        return None
    if x.size == 0 or rate <= 0:
        return None
    n = max(1, int(rate * BLOC_S))
    tronque = x[: len(x) - len(x) % n]
    if tronque.size == 0:
        return None
    blocs = tronque.reshape(-1, n).astype(np.float32) / PLEINE_ECHELLE
    rms = np.sqrt((blocs ** 2).mean(axis=1))
    fort = float(rms.max())
    if fort <= 0:
        return None
    actifs = rms[rms >= fort * 10.0 ** (-SEUIL_ACTIF_DB / 20.0)]
    niveau = db(float(np.sqrt((actifs ** 2).mean()))) if actifs.size else -200.0
    pic = db(float(np.abs(x).max()) / PLEINE_ECHELLE)
    plancher = db(float(np.percentile(rms, 10)))
    return niveau, pic, plancher


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cible-parole", type=float, default=CIBLE_PAROLE,
                    metavar="dBFS", help=f"défaut {CIBLE_PAROLE:g}")
    ap.add_argument("--cible-ambiance", type=float, default=CIBLE_AMBIANCE,
                    metavar="dBFS", help=f"défaut {CIBLE_AMBIANCE:g}")
    ap.add_argument("--plafond", type=float, default=PLAFOND_GAIN, metavar="dB",
                    help=f"gain positif maximal, défaut +{PLAFOND_GAIN:g}")
    ap.add_argument("--rapport", action="store_true",
                    help="mesurer et afficher sans rien écrire")
    args = ap.parse_args()

    if not REGISTRE.is_file():
        print(f"Registre introuvable : {REGISTRE}", file=sys.stderr)
        return 1
    with REGISTRE.open(newline="", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        entrees = [dict(r) for r in lecteur]
        colonnes = list(lecteur.fieldnames or [])

    absents, mesures = [], []
    for e in entrees:
        chemin = wav_path(e)
        m = mesurer(chemin) if chemin.is_file() else None
        if m is None:
            absents.append(e["id"])
            e["niveau_db"] = ""
            e["gain_db"] = ""
            continue
        niveau, pic, plancher = m
        cible = args.cible_ambiance if e["role"] == "AMBIANCE" else args.cible_parole
        gain = min(cible - niveau, args.plafond)
        e["niveau_db"] = f"{niveau:.1f}"
        e["gain_db"] = f"{gain:.1f}"
        mesures.append((e, niveau, pic, plancher, gain, cible))

    print(f"Cibles : paroles {args.cible_parole:+.0f} dBFS · "
          f"ambiances {args.cible_ambiance:+.0f} dBFS · plafond +{args.plafond:.0f} dB")
    print(f"Mesurés : {len(mesures)} fragments"
          + (f" · {len(absents)} illisibles ou absents" if absents else ""))

    for role, nom in (("TRACK", "paroles"), ("AMBIANCE", "ambiances")):
        sel = [m for m in mesures if m[0]["role"] == role]
        if not sel:
            continue
        niv = [m[1] for m in sel]
        gains = [m[4] for m in sel]
        print(f"\n{nom.upper()} (n={len(sel)})")
        print(f"  niveau avant : median {st.median(niv):6.1f}  "
              f"de {min(niv):.1f} à {max(niv):.1f}  → étendue {max(niv) - min(niv):.0f} dB")
        apres = [m[1] + m[4] for m in sel]
        print(f"  niveau après : median {st.median(apres):6.1f}  "
              f"de {min(apres):.1f} à {max(apres):.1f}  → étendue {max(apres) - min(apres):.0f} dB")
        print(f"  gain         : median {st.median(gains):+6.1f} dB  "
              f"de {min(gains):+.1f} à {max(gains):+.1f}")
        petits = sum(1 for g in gains if abs(g) <= 3)
        print(f"  {petits}/{len(sel)} ({100 * petits / len(sel):.0f} %) bougent de 3 dB ou moins")

    plafonnes = [m for m in mesures if m[4] >= args.plafond - 0.05]
    if plafonnes:
        print(f"\n⚠ {len(plafonnes)} fragments **plafonnés** : le gain n'a pas suffi à "
              f"atteindre la cible.")
        print("  Ce ne sont probablement pas des voix faibles mais des tranches "
              "quasi vides — à écouter, et sans doute à écarter des pools plutôt "
              "qu'à amplifier.")
        for e, niveau, pic, plancher, gain, cible in sorted(plafonnes, key=lambda m: m[1])[:15]:
            manque = cible - niveau - gain
            print(f"    {e['id']:30s} niveau {niveau:6.1f}  écart au fond "
                  f"{niveau - plancher:5.1f} dB  il manquerait {manque:+.0f} dB")
        if len(plafonnes) > 15:
            print(f"    … et {len(plafonnes) - 15} autres")

    suspects = [m for m in mesures if m[1] < SEUIL_SUSPECT]
    if suspects:
        par_master: dict[str, int] = {}
        for e, *_ in suspects:
            par_master[e["src"]] = par_master.get(e["src"], 0) + 1
        print(f"\n{len(suspects)} fragments sous {SEUIL_SUSPECT:.0f} dBFS, par master :")
        for src, n in sorted(par_master.items(), key=lambda kv: -kv[1]):
            debuts = sorted(float(e["start"]) for e, *_ in suspects if e["src"] == src)
            print(f"    {n:3d} × {src}")
            print(f"        positions {debuts[0]:.0f}s → {debuts[-1]:.0f}s")

    if args.rapport:
        print("\n--rapport : rien écrit.")
        return 0

    for c in ("niveau_db", "gain_db"):
        if c not in colonnes:
            colonnes.append(c)
    with REGISTRE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colonnes, restval="")
        w.writeheader()
        w.writerows(entrees)
    print(f"\nRegistre mis à jour : {REGISTRE.relative_to(ROOT)}")
    print("Colonnes ajoutées : niveau_db, gain_db. Aucun wav modifié.")
    print("Reste à câbler le gain dans le lecteur (Proto 08) — voir l'en-tête du script.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
