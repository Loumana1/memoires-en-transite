#!/bin/bash
# Lance le prototype 02 (2 sorties stereo) — Mémoires en transit
set -euo pipefail

MET_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PATCH="$MET_ROOT/pd/prototype_02_2out.pd"

if [[ ! -f "$PATCH" ]]; then
  echo "Patch introuvable: pd/prototype_02_2out.pd"
  exit 1
fi

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
