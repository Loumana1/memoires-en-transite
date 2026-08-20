#!/bin/bash
# Lance le prototype 01 — Mémoires en transit
# MET_ROOT = racine du depot (dossier parent de scripts/)
set -euo pipefail

MET_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PATCH="$MET_ROOT/pd/prototype_01_4hp_ambi.pd"

if [[ ! -f "$PATCH" ]]; then
  echo "Patch introuvable: pd/prototype_01_4hp_ambi.pd"
  exit 1
fi

if [[ ! -f "$MET_ROOT/pd/externals/iem_ambi-master/iem_ambi.pd_darwin" ]]; then
  echo "iem_ambi non compile. Voir docs/archive/03_first_setup.md"
  exit 1
fi

# macOS : ouvrir via l'app Pd (GUI). Ne pas passer -path au launcher Tcl.
# Le patch declare ses paths/libs ; .. = MET_ROOT depuis pd/
if [[ "$(uname)" == "Darwin" ]]; then
  PD_APP=""
  for app in "/Applications/Pd-0.56-2.app" "/Applications/Pd.app"; do
    if [[ -d "$app" ]]; then
      PD_APP="$app"
      break
    fi
  done
  if [[ -z "$PD_APP" ]]; then
    echo "Pure Data introuvable dans /Applications/"
    exit 1
  fi
  exec open -a "$PD_APP" "$PATCH"
fi

# Linux / fallback : binaire pd en ligne de commande
PD="$(command -v pd || true)"
if [[ -z "$PD" ]]; then
  echo "Commande pd introuvable."
  exit 1
fi

exec "$PD" \
  -path "$MET_ROOT" \
  -path "$MET_ROOT/pd" \
  -path "$MET_ROOT/pd/externals/iem_ambi-master" \
  -path "$MET_ROOT/pd/externals/iemmatrix" \
  -lib iem_ambi \
  -lib iemmatrix \
  "$PATCH"
