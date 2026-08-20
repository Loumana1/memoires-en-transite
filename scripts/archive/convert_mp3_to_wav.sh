#!/bin/bash
# Convertit les MP3 de SONS_PROTOTYPE/ vers wav/ (mono 48 kHz pour Pd)
# Chemins relatifs a MET_ROOT (racine du depot)
set -euo pipefail

MET_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$MET_ROOT/SONS_PROTOTYPE"
DST="$MET_ROOT/SONS_PROTOTYPE/wav"

mkdir -p "$DST"
shopt -s nullglob
for f in "$SRC"/*.mp3; do
  base="$(basename "${f%.mp3}")"
  echo "→ SONS_PROTOTYPE/wav/${base}.wav"
  ffmpeg -y -i "$f" -ar 48000 -ac 1 "$DST/${base}.wav" -loglevel error
done
echo "Terminé. $(ls "$DST"/*.wav 2>/dev/null | wc -l | tr -d ' ') fichiers dans SONS_PROTOTYPE/wav/"
