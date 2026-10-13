#!/usr/bin/env bash
set -euo pipefail
office_root=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
cd "$office_root/app"
export XDG_CONFIG_HOME="$office_root/.local/state/config"
export DO_NOT_TRACK=1
exec node_modules/electron/dist/electron out/main/index.js "$@"
