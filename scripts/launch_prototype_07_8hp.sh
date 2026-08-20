#!/bin/bash
# Raccourci → scripts/proto07/
set -euo pipefail
exec "$(cd "$(dirname "$0")" && pwd)/proto07/launch_prototype_07_8hp.sh" "$@"
