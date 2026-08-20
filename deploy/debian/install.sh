#!/usr/bin/env bash
# Installe Pure Data + compile iem_ambi / iemmatrix pour Debian / Raspberry Pi.
# Idempotent. Mémoires en transit / Micro-opacités
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MET_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
IEM_AMBI="$MET_ROOT/pd/externals/iem_ambi-master"
IEM_MTX="$MET_ROOT/pd/externals/iemmatrix"

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "install.sh est pour Debian / Raspberry Pi (Linux)."
  exit 1
fi

if [[ ! -d "$IEM_AMBI" || ! -d "$IEM_MTX" ]]; then
  echo "Sources iem introuvables sous pd/externals/."
  exit 1
fi

SUDO=""
if [[ "$(id -u)" -ne 0 ]]; then
  if command -v sudo >/dev/null; then
    SUDO="sudo"
  else
    echo "Lancer en root ou installer sudo."
    exit 1
  fi
fi

echo "== paquets Debian =="
$SUDO apt-get update -y
$SUDO apt-get install -y \
  puredata puredata-dev python3 \
  build-essential pkg-config \
  libfftw3-dev \
  alsa-utils

PDINC=""
for d in /usr/include/pd /usr/include/puredata; do
  if [[ -f "$d/m_pd.h" ]]; then
    PDINC="$d"
    break
  fi
done
if [[ -z "$PDINC" ]]; then
  echo "m_pd.h introuvable. Paquet puredata-dev manquant ?"
  exit 1
fi
echo "PDINCLUDEDIR=$PDINC"

echo "== compile iem_ambi =="
make -C "$IEM_AMBI" PDINCLUDEDIR="$PDINC"

echo "== compile iemmatrix =="
make -C "$IEM_MTX" PDINCLUDEDIR="$PDINC"

USER_NAME="${SUDO_USER:-$USER}"
if [[ -n "$USER_NAME" && "$USER_NAME" != "root" ]]; then
  $SUDO usermod -aG audio "$USER_NAME" || true
  echo "Utilisateur $USER_NAME ajouté au groupe audio (se reconnecter)."
fi

echo
echo "OK. Lancer: bash deploy/debian/launch.sh"
echo "Expo sans écran: bash deploy/debian/launch.sh --nogui"
echo "Démarrage auto: sudo bash deploy/debian/install-service.sh"
