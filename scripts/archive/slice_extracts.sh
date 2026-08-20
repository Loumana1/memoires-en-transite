#!/bin/bash
# Découpe les 3 extraits réels MET en segments SONS/<ETAT>/<DUREE>/
# Format: mono 48 kHz (readsf~ / Pd)
set -euo pipefail

MET_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$MET_ROOT/SONS_PROTOTYPE/wav"
DST="$MET_ROOT/SONS"
FFMPEG="$(command -v ffmpeg)"

if [[ -z "$FFMPEG" ]]; then
  echo "ffmpeg introuvable"
  exit 1
fi

STATES=(CORTEX HIPPOCAMPE RECONSTRUCTION BOUCLE)
DURS=(COURT MOYEN LONG)
for e in "${STATES[@]}"; do
  for d in "${DURS[@]}"; do
    mkdir -p "$DST/$e/$d"
    rm -f "$DST/$e/$d"/*.wav
  done
done
mkdir -p "$DST/MEMOIRE_VIVANTE/COURT"
rm -f "$DST/MEMOIRE_VIVANTE/COURT"/*.wav

slice() {
  local out="$1" in="$2" start="$3" dur="$4"
  echo "  -> $out (${start}s + ${dur}s)"
  "$FFMPEG" -y -ss "$start" -i "$in" -t "$dur" -ar 48000 -ac 1 "$DST/$out" -loglevel error
}

echo "=== keren 5 bon.wav (voix intime — BOUCLE / HIPPOCAMPE) ==="
K="$SRC/keren 5 bon.wav"
slice "BOUCLE/COURT/keren_boucle_01.wav"      "$K" 0   8
slice "BOUCLE/COURT/keren_boucle_02.wav"      "$K" 12  9
slice "BOUCLE/MOYEN/keren_boucle_03.wav"      "$K" 22  25
slice "HIPPOCAMPE/COURT/keren_hippo_01.wav"   "$K" 5   10
slice "HIPPOCAMPE/MOYEN/keren_hippo_02.wav"   "$K" 30  35
slice "CORTEX/COURT/keren_cortex_01.wav"      "$K" 48  12

echo "=== Voix pour la danse fin.wav (corps / voix — RECONSTRUCTION / HIPPOCAMPE) ==="
V="$SRC/Voix pour la danse fin.wav"
slice "RECONSTRUCTION/LONG/voix_recon_01.wav"   "$V" 45   75
slice "RECONSTRUCTION/MOYEN/voix_recon_02.wav"  "$V" 180  40
slice "RECONSTRUCTION/MOYEN/voix_recon_03.wav"  "$V" 320  38
slice "RECONSTRUCTION/COURT/voix_recon_04.wav"  "$V" 400  12
slice "HIPPOCAMPE/LONG/voix_hippo_01.wav"     "$V" 90   70
slice "HIPPOCAMPE/MOYEN/voix_hippo_02.wav"    "$V" 250  35
slice "HIPPOCAMPE/COURT/voix_hippo_03.wav"    "$V" 10   11
slice "CORTEX/COURT/voix_cortex_01.wav"       "$V" 500  10
slice "BOUCLE/COURT/voix_boucle_01.wav"       "$V" 450  14

echo "=== radio campus rencontre.wav (dialogue / archive — CORTEX / HIPPOCAMPE) ==="
R="$SRC/radio campus rencontre.wav"
slice "CORTEX/MOYEN/radio_cortex_01.wav"        "$R" 60    45
slice "CORTEX/MOYEN/radio_cortex_02.wav"        "$R" 600   42
slice "CORTEX/COURT/radio_cortex_03.wav"        "$R" 5     11
slice "CORTEX/COURT/radio_cortex_04.wav"        "$R" 1200  12
slice "CORTEX/LONG/radio_cortex_05.wav"         "$R" 300   68
slice "HIPPOCAMPE/LONG/radio_hippo_01.wav"      "$R" 1800  80
slice "HIPPOCAMPE/MOYEN/radio_hippo_02.wav"     "$R" 500   40
slice "HIPPOCAMPE/MOYEN/radio_hippo_03.wav"     "$R" 2400  38
slice "HIPPOCAMPE/COURT/radio_hippo_04.wav"     "$R" 900   10
slice "RECONSTRUCTION/MOYEN/radio_recon_01.wav" "$R" 3600  42
slice "RECONSTRUCTION/COURT/radio_recon_02.wav" "$R" 1500  13
slice "BOUCLE/COURT/radio_boucle_01.wav"        "$R" 1505  11
slice "BOUCLE/COURT/radio_boucle_02.wav"        "$R" 4200  12

echo "=== Nouveaux extraits (archive / discours) ==="
M="$SRC/Martin Luther King.wav"
slice "CORTEX/COURT/mlk_cortex_01.wav"              "$M" 10  12
slice "CORTEX/MOYEN/mlk_cortex_02.wav"              "$M" 120 35
slice "HIPPOCAMPE/COURT/mlk_hippo_01.wav"           "$M" 45  11
slice "RECONSTRUCTION/MOYEN/mlk_recon_01.wav"       "$M" 180 32
slice "BOUCLE/COURT/mlk_boucle_01.wav"              "$M" 220 10

C="$SRC/cheick anta diop.wav"
slice "CORTEX/COURT/cheick_cortex_01.wav"           "$C" 15  10
slice "HIPPOCAMPE/MOYEN/cheick_hippo_01.wav"        "$C" 70  36
slice "HIPPOCAMPE/LONG/cheick_hippo_02.wav"         "$C" 150 65
slice "RECONSTRUCTION/COURT/cheick_recon_01.wav"    "$C" 240 12
slice "BOUCLE/MOYEN/cheick_boucle_01.wav"           "$C" 300 22

echo ""
echo "Terminé. $(find "$DST" -name '*.wav' | wc -l | tr -d ' ') fichiers dans SONS/"
python3 "$MET_ROOT/scripts/archive/build_sons_manifest.py"
