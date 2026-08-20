#!/bin/bash
# Test console pd -nogui d'un patch MET — Mémoires en transit
# Usage: ./scripts/test_patch_console.sh pd/prototype_04_effects.pd
# Critère de succès: AUCUNE ligne filtrée (error / failed / ignored / signal->nonsignal)
set -uo pipefail

MET_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PD_BIN="/Applications/Pd-0.56-2.app/Contents/Resources/bin/pd"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <patch.pd>"
  exit 2
fi

PATCH="$1"
[[ "$PATCH" != /* ]] && PATCH="$MET_ROOT/$PATCH"

if [[ ! -f "$PATCH" ]]; then
  echo "Patch introuvable: $PATCH"
  exit 2
fi

if [[ ! -x "$PD_BIN" ]]; then
  echo "Binaire pd introuvable: $PD_BIN"
  exit 2
fi

# -noaudio : pas de prise du device (test structurel, erreurs de câblage
#            visibles quand même) ; -noprefs : environnement reproductible.
# _autoquit.pd quitte Pd 3 s après le chargement (laisse loadbang/delay agir).
LOG="$("$PD_BIN" -nogui -noaudio -noprefs -stderr \
  -path "$MET_ROOT" \
  -path "$MET_ROOT/pd" \
  -path "$MET_ROOT/pd/lib" \
  -path "$MET_ROOT/pd/externals/iem_ambi-master" \
  -path "$MET_ROOT/pd/externals/iemmatrix" \
  -lib iem_ambi -lib iemmatrix \
  "$PATCH" "$MET_ROOT/pd/_autoquit.pd" 2>&1)"

FILTERED="$(printf '%s\n' "$LOG" | grep -Ei 'error|failed|ignored|signal outlet connected to nonsignal inlet|couldn.t create|no method for' || true)"

if [[ -n "$FILTERED" ]]; then
  echo "ECHEC — lignes suspectes dans la console Pd:"
  printf '%s\n' "$FILTERED"
  exit 1
fi

echo "OK — console propre: $(basename "$PATCH")"
exit 0
