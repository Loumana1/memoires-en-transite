#!/bin/bash
# Raccourci → scripts/proto06/
set -euo pipefail
name="$(basename "$0")"
exec "$(cd "$(dirname "$0")" && pwd)/proto06/$name" "$@"
