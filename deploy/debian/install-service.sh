#!/usr/bin/env bash
# Installe le service systemd (lancement au boot, sans fenêtre).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MET_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
UNIT_IN="$SCRIPT_DIR/memoires-en-transit.service.in"
UNIT_DST="/etc/systemd/system/memoires-en-transit.service"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Relancer avec sudo: sudo bash deploy/debian/install-service.sh"
  exit 1
fi

if [[ ! -x "$SCRIPT_DIR/launch.sh" ]]; then
  echo "launch.sh n'est pas exécutable."
  exit 1
fi

sed "s|MET_ROOT_PLACEHOLDER|$MET_ROOT|g" "$UNIT_IN" > "$UNIT_DST"
# L'utilisateur qui possède le projet (souvent pi / loumana), pas root
OWNER="$(stat -c '%U' "$MET_ROOT" 2>/dev/null || echo pi)"
if id "$OWNER" >/dev/null 2>&1; then
  sed -i "/^\[Service\]/a User=$OWNER\nGroup=audio" "$UNIT_DST"
fi

systemctl daemon-reload
systemctl enable memoires-en-transit.service
echo "Service installé. Démarrer: sudo systemctl start memoires-en-transit"
echo "Logs: journalctl -u memoires-en-transit -f"
echo "Stop: sudo systemctl stop memoires-en-transit"
