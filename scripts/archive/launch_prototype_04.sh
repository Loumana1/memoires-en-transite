#!/bin/bash
# Lance le prototype 04 (effets spatiaux + fluid) — Mémoires en transit
set -euo pipefail

MET_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PATCH="$MET_ROOT/pd/prototype_04_effects.pd"

if [[ ! -f "$PATCH" ]]; then
  echo "Patch introuvable: pd/prototype_04_effects.pd"
  exit 1
fi

if [[ ! -f "$MET_ROOT/pd/externals/iem_ambi-master/iem_ambi.pd_darwin" ]]; then
  echo "iem_ambi non compile. Voir docs/archive/03_first_setup.md"
  exit 1
fi

# macOS : ouvrir via l'app Pd (GUI). Le declare du patch configure les paths.
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
  -path "$MET_ROOT/pd/lib" \
  -path "$MET_ROOT/pd/externals/iem_ambi-master" \
  -path "$MET_ROOT/pd/externals/iemmatrix" \
  -lib iem_ambi \
  -lib iemmatrix \
  "$PATCH"
