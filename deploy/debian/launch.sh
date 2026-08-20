#!/usr/bin/env bash
# Lance Proto 07 sur Debian / Raspberry Pi (Pure Data du système).
# Mémoires en transit / Micro-opacités
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MET_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PATCH="$MET_ROOT/pd/prototype_07_fsm_8hp.pd"
IEM_AMBI="$MET_ROOT/pd/externals/iem_ambi-master"
IEM_MTX="$MET_ROOT/pd/externals/iemmatrix"

usage() {
  cat <<EOF
Usage: bash deploy/debian/launch.sh [options]

  --gui          fenêtre Pd (défaut si un écran est branché)
  --nogui        sans fenêtre (expo / SSH)
  --noaudio      test de chargement, pas de carte son
  --list         liste les périphériques ALSA puis quitte
  --device N     sortie Pd N (voir --list). Sans option: Scarlett / Focusrite
  --adc          ouvrir l'entrée ALSA (défaut: pas d'entrée, 8 HP seulement)
  --rate HZ      fréquence (défaut 48000)
  --channels N   sorties (défaut 8)
  -h, --help

Variables: MET_PD_DEVICE  MET_PD_RATE  MET_PD_CHANNELS  MET_PD_NOGUI=1
EOF
}

NOGUI=""
NOAUDIO=0
LIST=0
ADC=0
DEVICE="${MET_PD_DEVICE:-}"
RATE="${MET_PD_RATE:-48000}"
CHANNELS="${MET_PD_CHANNELS:-8}"

if [[ "${MET_PD_NOGUI:-}" == "1" ]]; then
  NOGUI="-nogui"
fi
if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
  NOGUI="-nogui"
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --gui) NOGUI="" ;;
    --nogui) NOGUI="-nogui" ;;
    --noaudio) NOAUDIO=1 ;;
    --list) LIST=1 ;;
    --device) DEVICE="$2"; shift ;;
    --adc) ADC=1 ;;
    --rate) RATE="$2"; shift ;;
    --channels) CHANNELS="$2"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Option inconnue: $1"; usage; exit 2 ;;
  esac
  shift
done

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "Ce script est pour Debian / Raspberry Pi."
  echo "Sur Mac: bash scripts/launch_prototype_07_8hp.sh"
  exit 1
fi

if [[ ! -f "$PATCH" ]]; then
  echo "Patch introuvable: $PATCH"
  echo "Sur la machine de dev: python3 scripts/gen_prototype_07_8hp.py"
  exit 1
fi

if [[ ! -d "$MET_ROOT/SONS_V3" ]]; then
  echo "SONS_V3/ introuvable. Copier le dossier sons avec le projet."
  exit 1
fi

has_iem() {
  local dir="$1" name="$2"
  local f
  for f in "$dir/$name.pd_linux" "$dir/$name.linux-arm64" "$dir/$name.linux-arm" \
           "$dir/$name.l_arm64" "$dir/$name.l_arm" "$dir/$name.linux-amd64"; do
    [[ -f "$f" ]] && return 0
  done
  return 1
}

if ! has_iem "$IEM_AMBI" iem_ambi || ! has_iem "$IEM_MTX" iemmatrix; then
  echo "Externals iem pas compilés pour Linux."
  echo "Lancer: bash deploy/debian/install.sh"
  exit 1
fi

PD_BIN="$(command -v pd || true)"
if [[ -z "$PD_BIN" ]]; then
  for cand in /usr/bin/pd /usr/local/bin/pd; do
    [[ -x "$cand" ]] && PD_BIN="$cand" && break
  done
fi
if [[ -z "$PD_BIN" ]]; then
  echo "Pure Data introuvable (paquet puredata)."
  echo "Lancer: bash deploy/debian/install.sh"
  exit 1
fi

# Au démarrage du Pi, l'énumération USB peut prendre plus de temps que le boot du
# service : sans réessai, on sort en erreur et l'expo est muette. D'où le retry.
LISTDEV_TIMEOUT=15
RETRY_DELAIS=(0 3 6 12)
LOG_CARTE="$MET_ROOT/deploy/debian/derniere_carte.log"

pd_listdev() {
  timeout "$LISTDEV_TIMEOUT" "$PD_BIN" -nogui -stderr -listdev -noloadbang 2>&1 || true
}

# Pd 0.55 numérote à partir de 0. 0–3 = HDMI Pi. Ne pas passer --device 1.
pd_parse_usb_out() {
  awk '
    /^audio output devices:/ { p=1; next }
    /^audio input devices:/ { p=0 }
    /^API / { p=0 }
    /^no MIDI/ { p=0 }
    !p { next }
    {
      n = $1; gsub(/\./, "", n)
      line = $0
      if (line !~ /Scarlett|Focusrite/) next
      if (line ~ /plug-in/) { print n; found=1; exit }
      if (hw == "") hw = n
    }
    END { if (!found && hw != "") print hw }
  '
}

alsa_voit_carte() {
  aplay -l 2>/dev/null | grep -qi 'scarlett\|focusrite'
}

if [[ "$LIST" -eq 1 ]]; then
  echo "=== ALSA (aplay -l) ==="
  aplay -l 2>/dev/null || true
  echo
  echo "=== Pd (0 = HDMI, Scarlett = souvent 4 hardware / 5 plug-in) ==="
  pd_listdev
  exit 0
fi

pd_pick_usb_out() {
  local n=${#RETRY_DELAIS[@]} i=0 delai sortie dev
  for delai in "${RETRY_DELAIS[@]}"; do
    i=$((i + 1))
    if [[ "$delai" -gt 0 ]]; then
      echo "Carte absente — nouvelle tentative dans ${delai}s ($i/$n)" >&2
      sleep "$delai"
    fi
    sortie="$(pd_listdev)"
    dev="$(printf '%s\n' "$sortie" | pd_parse_usb_out)"
    if [[ -n "$dev" ]]; then
      printf '%s\n' "$dev"
      return 0
    fi
    # Distinguer « pas branchée » de « Pd ne sait plus l'annoncer ».
    if alsa_voit_carte; then
      echo "ALSA voit la carte mais Pd ne la liste pas (tentative $i/$n)." >&2
      echo "Si ça persiste, le format de 'pd -listdev' a peut-être changé." >&2
    fi
  done
  # Trace pour autopsie : la sortie brute du dernier essai.
  {
    echo "=== $(date -Is) — échec détection après $n tentatives ==="
    echo "--- aplay -l ---"
    aplay -l 2>&1 || true
    echo "--- pd -listdev ---"
    printf '%s\n' "$sortie"
  } >"$LOG_CARTE" 2>&1 || true
  return 1
}

if [[ "$NOAUDIO" -eq 0 && -z "$DEVICE" ]]; then
  DEVICE="$(pd_pick_usb_out || true)"
  if [[ -z "$DEVICE" ]]; then
    echo "Pas de Scarlett/Focusrite dans Pd -listdev après ${#RETRY_DELAIS[@]} tentatives."
    echo "Sortie brute conservée dans: $LOG_CARTE"
    echo "Brancher la carte (USB, allumée) puis: bash deploy/debian/launch.sh --list"
    echo "Forcer: --device 5   (plug-in Scarlett, pas 0/1 = HDMI)"
    exit 1
  fi
  echo "Carte USB auto: Pd --device $DEVICE"
  # Trace du device retenu : c'est la première chose à regarder si le son sort
  # sur le HDMI au lieu de la Scarlett.
  echo "$(date -Is) device=$DEVICE" >"$LOG_CARTE" 2>/dev/null || true
fi

# -channels ouvre entrée+sortie. HDMI n'a pas de capture → "No such file".
# 8 HP: pas d'adc. presence_07 reste silencieux (piezo jamais vers dac~).
AUDIO_ARGS=(-alsa -r "$RATE" -outchannels "$CHANNELS" -audiobuf 40)
if [[ "$ADC" -eq 1 ]]; then
  AUDIO_ARGS=(-alsa -r "$RATE" -inchannels "$CHANNELS" -outchannels "$CHANNELS" -audiobuf 40)
else
  AUDIO_ARGS+=(-noadc)
fi
if [[ -n "$DEVICE" ]]; then
  AUDIO_ARGS+=(-audiooutdev "$DEVICE")
  if [[ "$ADC" -eq 1 ]]; then
    AUDIO_ARGS+=(-audioindev "$DEVICE")
  fi
fi
if [[ "$NOAUDIO" -eq 1 ]]; then
  AUDIO_ARGS=(-noaudio)
fi

cd "$MET_ROOT"
SEND_ARGS=()
if [[ "$NOAUDIO" -eq 0 ]]; then
  SEND_ARGS=(-send "r6_boot_expo 1")
fi
echo "MET_ROOT=$MET_ROOT"
echo "pd=$PD_BIN  $NOGUI  ${AUDIO_ARGS[*]}  ${SEND_ARGS[*]:-}"
exec "$PD_BIN" -stderr $NOGUI \
  "${AUDIO_ARGS[@]}" \
  "${SEND_ARGS[@]}" \
  -path "$MET_ROOT" -path "$MET_ROOT/pd" -path "$MET_ROOT/pd/lib" \
  -path "$IEM_AMBI" -path "$IEM_MTX" \
  -lib iem_ambi -lib iemmatrix \
  "$PATCH"
