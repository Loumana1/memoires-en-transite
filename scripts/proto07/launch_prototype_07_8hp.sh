#!/bin/bash
# Lance le prototype 07 — variante 8HP (SONS_V3, cycle 40/50/120 s)
# Mémoires en transit / Micro-opacités
set -euo pipefail

MET_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PATCH="$MET_ROOT/pd/prototype_07_fsm_8hp.pd"

if [[ ! -f "$PATCH" ]]; then
  echo "Patch introuvable. Lancer: python3 scripts/gen_prototype_07_8hp.py"
  exit 1
fi

if [[ ! -f "$MET_ROOT/pd/externals/iem_ambi-master/iem_ambi.pd_darwin" ]]; then
  echo "iem_ambi non compile. Voir docs/archive/03_first_setup.md"
  exit 1
fi

if [[ "$(uname)" == "Darwin" ]]; then
  PD_BIN=""
  for app in "/Applications/Pd-0.56-2.app" "/Applications/Pd.app"; do
    cand="$app/Contents/Resources/bin/pd"
    [[ -x "$cand" ]] && PD_BIN="$cand" && break
  done
  [[ -z "$PD_BIN" ]] && echo "Pure Data introuvable." && exit 1
  cd "$MET_ROOT"
  exec "$PD_BIN" -stderr \
    -path "$MET_ROOT" -path "$MET_ROOT/pd" -path "$MET_ROOT/pd/lib" \
    -path "$MET_ROOT/pd/externals/iem_ambi-master" -path "$MET_ROOT/pd/externals/iemmatrix" \
    -lib iem_ambi -lib iemmatrix "$PATCH"
fi

PD="$(command -v pd || true)"
[[ -z "$PD" ]] && echo "pd introuvable." && exit 1
cd "$MET_ROOT"
exec "$PD" -path "$MET_ROOT" -path "$MET_ROOT/pd" -path "$MET_ROOT/pd/lib" \
  -path "$MET_ROOT/pd/externals/iem_ambi-master" -path "$MET_ROOT/pd/externals/iemmatrix" \
  -lib iem_ambi -lib iemmatrix "$PATCH"
