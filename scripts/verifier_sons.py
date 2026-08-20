#!/usr/bin/env python3
"""Vérifie que la matière sonore est jouable. À lancer avant chaque expo.

Le risque d'une installation, ce n'est pas le plantage — c'est le **silence que
personne ne remarque**. Un wav corrompu, vide ou muet ne fait pas planter Pd :
le lecteur l'ouvre, ne sort rien, et passe au suivant. Ça s'entend comme un trou
dans la pièce, et ça ne se voit dans aucun log.

Précédent : le calibrage du Proto 06 avait trouvé 8 segments morts, dont 14
secondes de silence pur dans `BOUCLE/COURT` (voir docs/archive/11_*).

Ce script contrôle trois choses :

  1. chaque wav de SONS_V3/ est lisible, mono 48 kHz, non vide, non muet,
     sans long trou interne ;
  2. chaque chemin cité par les playlists du Proto 07 existe vraiment ;
  3. le registre des ID et le disque disent la même chose.

`WIP/` (les masters) est ignoré : il n'est pas lu par le patch.

Usage:
  python3 scripts/verifier_sons.py
  python3 scripts/verifier_sons.py --verbose     # lister chaque fichier
  python3 scripts/verifier_sons.py --structure   # sans lire l'audio (rapide)

Sortie : code 1 s'il y a au moins une ERREUR, 0 sinon (avertissements tolérés).
"""
from __future__ import annotations

import argparse
import csv
import sys
import wave
from pathlib import Path

try:
    import numpy as np
except ImportError:
    sys.exit("pip3 install numpy")

ROOT = Path(__file__).resolve().parent.parent
SONS = ROOT / "SONS_V3"
PLAYLISTS = ROOT / "pd" / "lib" / "playlists07"
REGISTRE = ROOT / "docs" / "Matiere" / "registre_ids.csv"

RATE_ATTENDU = 48000
CANAUX_ATTENDUS = 1
OCTETS_ATTENDUS = 2

DUREE_MIN = 0.40          # sous ça, le fragment n'a pas de sens musical
PIC_MUET_DB = -60.0       # au-dessus de rien : fichier mort
PIC_FAIBLE_DB = -35.0     # audible mais suspect
TROU_SEUIL_DB = -50.0     # niveau sous lequel un bloc compte comme silence
TROU_MAX_S = 5.0          # trou interne toléré
BLOC_S = 0.05             # fenêtre d'analyse

PLEINE_ECHELLE = 32768.0


def db(x: float) -> float:
    return -200.0 if x <= 0 else 20.0 * float(np.log10(x))


class Rapport:
    def __init__(self) -> None:
        self.erreurs: list[str] = []
        self.avertissements: list[str] = []
        self.pics: list[float] = []

    def erreur(self, msg: str) -> None:
        self.erreurs.append(msg)

    def avertir(self, msg: str) -> None:
        self.avertissements.append(msg)

    @property
    def ok(self) -> bool:
        return not self.erreurs


def wavs_decoupes() -> list[Path]:
    return sorted(
        p for p in SONS.rglob("*.wav")
        if "WIP" not in p.parts and not p.name.startswith(".")
    )


def plus_long_trou(x: np.ndarray, rate: int) -> float:
    """Durée du plus long passage sous le seuil, en secondes."""
    n = max(1, int(rate * BLOC_S))
    reste = len(x) % n
    if reste:
        x = x[:-reste]
    if len(x) == 0:
        return 0.0
    blocs = x.reshape(-1, n).astype(np.float32) / PLEINE_ECHELLE
    rms = np.sqrt((blocs ** 2).mean(axis=1))
    muet = rms < (10.0 ** (TROU_SEUIL_DB / 20.0))
    if not muet.any():
        return 0.0
    best = courant = 0
    for m in muet:
        courant = courant + 1 if m else 0
        best = max(best, courant)
    return best * n / rate


def verifier_wav(path: Path, rap: Rapport, lire_audio: bool, verbose: bool) -> None:
    rel = path.relative_to(ROOT)
    try:
        with wave.open(str(path), "rb") as w:
            rate = w.getframerate()
            canaux = w.getnchannels()
            octets = w.getsampwidth()
            trames = w.getnframes()
            brut = w.readframes(trames) if lire_audio else b""
    except Exception as e:
        rap.erreur(f"{rel} — ILLISIBLE ({type(e).__name__}: {e})")
        return

    if trames == 0:
        rap.erreur(f"{rel} — 0 échantillon (fichier vide)")
        return
    duree = trames / float(rate or 1)
    if rate != RATE_ATTENDU:
        rap.erreur(f"{rel} — {rate} Hz au lieu de {RATE_ATTENDU}")
    if canaux != CANAUX_ATTENDUS:
        rap.erreur(f"{rel} — {canaux} canaux au lieu de {CANAUX_ATTENDUS}")
    if octets != OCTETS_ATTENDUS:
        rap.erreur(f"{rel} — {octets * 8} bits au lieu de {OCTETS_ATTENDUS * 8}")
    if duree < DUREE_MIN:
        rap.erreur(f"{rel} — {duree:.2f} s, sous le minimum de {DUREE_MIN:g} s")

    if not lire_audio:
        if verbose:
            print(f"  {rel}  {duree:6.2f}s  {rate} Hz  {canaux}ch")
        return

    if octets != 2:
        rap.avertir(f"{rel} — non analysé (largeur {octets * 8} bits)")
        return
    x = np.frombuffer(brut, dtype="<i2")
    if x.size == 0:
        rap.erreur(f"{rel} — aucune donnée lue")
        return

    pic = db(float(np.abs(x).max()) / PLEINE_ECHELLE)
    rms = db(float(np.sqrt((x.astype(np.float32) / PLEINE_ECHELLE) ** 2).mean()))
    trou = plus_long_trou(x, rate)
    rap.pics.append(pic)

    if pic <= PIC_MUET_DB:
        rap.erreur(f"{rel} — MUET ({duree:.1f} s, pic {pic:.0f} dBFS)")
    elif pic <= PIC_FAIBLE_DB:
        rap.avertir(f"{rel} — très bas (pic {pic:.0f} dBFS)")
    if trou >= TROU_MAX_S:
        part = 100.0 * trou / duree
        msg = f"{rel} — trou de {trou:.1f} s ({part:.0f} % du fichier)"
        (rap.erreur if part > 60 else rap.avertir)(msg)
    if np.abs(x).max() >= 32767 and (np.abs(x) >= 32767).sum() > rate * 0.001:
        rap.avertir(f"{rel} — saturation possible")

    if verbose:
        print(f"  {rel}  {duree:6.2f}s  pic {pic:6.1f}  rms {rms:6.1f}  trou {trou:4.1f}s")


def verifier_playlists(rap: Rapport) -> tuple[int, int]:
    """Chaque chemin cité par le patch doit exister. Sinon : lecteur muet."""
    if not PLAYLISTS.is_dir():
        rap.erreur(f"{PLAYLISTS.relative_to(ROOT)} introuvable — regénérer le patch")
        return 0, 0
    slots = sorted(PLAYLISTS.glob("slot_*.txt"))
    if not slots:
        rap.erreur(f"aucun slot_*.txt dans {PLAYLISTS.relative_to(ROOT)}")
        return 0, 0
    total = 0
    for slot in slots:
        lignes = [l.strip() for l in slot.read_text(encoding="utf-8").splitlines()]
        lignes = [l for l in lignes if l]
        if not lignes:
            rap.avertir(f"{slot.name} — playlist vide (lecteur muet)")
            continue
        for ligne in lignes:
            chemin = ligne.rstrip(";").split()[0]
            total += 1
            if not (ROOT / chemin).is_file():
                rap.erreur(f"{slot.name} — cité mais absent : {chemin}")
    return len(slots), total


def verifier_registre(disque: list[Path], rap: Rapport) -> None:
    if not REGISTRE.is_file():
        rap.avertir(f"{REGISTRE.relative_to(ROOT)} absent — ID non garantis stables")
        return
    with REGISTRE.open(newline="", encoding="utf-8") as f:
        ids = {r["id"] for r in csv.DictReader(f)}
    stems = {p.stem for p in disque}
    for manquant in sorted(ids - stems):
        rap.avertir(f"registre — {manquant} inscrit mais absent du disque")
    for inconnu in sorted(stems - ids):
        rap.avertir(f"registre — {inconnu} sur le disque mais pas au registre")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verbose", action="store_true", help="détailler chaque fichier")
    ap.add_argument("--structure", action="store_true",
                    help="ne pas lire l'audio (format et durées seulement)")
    args = ap.parse_args()

    if not SONS.is_dir():
        print(f"SONS_V3/ introuvable : {SONS}", file=sys.stderr)
        return 1

    rap = Rapport()
    fichiers = wavs_decoupes()
    if not fichiers:
        print("Aucun wav découpé dans SONS_V3/.", file=sys.stderr)
        return 1

    mode = "structure seule" if args.structure else "audio complet"
    octets = sum(p.stat().st_size for p in fichiers)
    print(f"SONS_V3/ — {len(fichiers)} wav, {octets / 1e6:.0f} Mo ({mode})")
    for p in fichiers:
        verifier_wav(p, rap, not args.structure, args.verbose)

    n_slots, n_cites = verifier_playlists(rap)
    print(f"Playlists 07 — {n_slots} slots, {n_cites} références")
    verifier_registre(fichiers, rap)

    if rap.pics:
        p = sorted(rap.pics)
        med = p[len(p) // 2]
        bas = sum(1 for v in p if v <= PIC_FAIBLE_DB)
        print(f"Niveaux — pic médian {med:.0f} dBFS, "
              f"étendue {p[0]:.0f} à {p[-1]:.0f} dBFS "
              f"({p[-1] - p[0]:.0f} dB d'écart), {bas} sous {PIC_FAIBLE_DB:.0f}")

    print()
    if rap.erreurs:
        print(f"ERREURS ({len(rap.erreurs)}) — à corriger avant l'expo :")
        for m in rap.erreurs:
            print(f"  ✗ {m}")
        print()
    if rap.avertissements:
        print(f"Avertissements ({len(rap.avertissements)}) — à écouter :")
        for m in rap.avertissements[:40]:
            print(f"  ! {m}")
        if len(rap.avertissements) > 40:
            print(f"  … et {len(rap.avertissements) - 40} autres")
        print()
    if rap.ok and not rap.avertissements:
        print("Tout est jouable. Aucune erreur, aucun avertissement.")
    elif rap.ok:
        print("Aucune erreur bloquante.")
    return 1 if rap.erreurs else 0


if __name__ == "__main__":
    raise SystemExit(main())
