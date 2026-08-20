#!/bin/bash
# Découpe les sources WAV longues en parties égales (mono 48 kHz).
# Sortie : SONS_PROTOTYPE/wav/parts/
# Idempotent : réécrit les fichiers à chaque exécution.
set -euo pipefail

MET_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WAV="$MET_ROOT/SONS_PROTOTYPE/wav"
OUTDIR="$MET_ROOT/SONS_PROTOTYPE/wav/parts"
FFMPEG="$(command -v ffmpeg)"

if [[ -z "$FFMPEG" ]]; then
  echo "ffmpeg introuvable"
  exit 1
fi

mkdir -p "$OUTDIR"

split_parts() {
  local src="$1" prefix="$2" count="$3"
  if [[ ! -f "$src" ]]; then
    echo "Ignoré (introuvable) : $src"
    return 0
  fi
  local dur part n start len out pad
  dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src")"
  part="$(echo "scale=6; $dur / $count" | bc)"

  echo "=== $(basename "$src") → ${count} parties (${dur}s total, ~${part}s/partie) ==="
  for ((n = 1; n <= count; n++)); do
    start="$(echo "scale=6; $part * ($n - 1)" | bc)"
    if [[ $n -eq $count ]]; then
      len="$(echo "scale=6; $dur - $start" | bc)"
    else
      len="$part"
    fi
    if [[ $count -ge 10 ]]; then
      pad="$(printf '%02d' "$n")"
    else
      pad="$n"
    fi
    out="$OUTDIR/${prefix}_part${pad}.wav"
    echo "  -> part${pad} (${start}s + ${len}s)"
    "$FFMPEG" -y -ss "$start" -i "$src" -t "$len" -ar 48000 -ac 1 "$out" -loglevel error
  done
}

split_parts "$WAV/Voix pour la danse fin.wav" "voix_danse" 3
split_parts "$WAV/cheick anta diop.wav" "cheick_diop" 3
split_parts "$WAV/radio campus rencontre.wav" "radio_campus" 10

echo ""
echo "Terminé. Fichiers dans $OUTDIR/"
