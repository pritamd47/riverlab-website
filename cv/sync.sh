#!/usr/bin/env bash
# Pull the latest CV source from its master copy (path configured under
# `cv:` in _config.yaml), and stage it for commit. Typesetting happens in
# CI (see .github/workflows/update-cv.yaml) once the change is pushed to main.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$DIR/.." && pwd)"
CONFIG="$ROOT/_config.yaml"

read_config() {
  python3 - "$CONFIG" "$1" <<'PY'
import sys
import yaml

config_path, key = sys.argv[1], sys.argv[2]
with open(config_path) as f:
    config = yaml.safe_load(f) or {}
print((config.get("cv") or {}).get(key, ""))
PY
}

SRC="$(read_config source)"
DEST_REL="$(read_config dest)"

if [[ -z "$SRC" ]]; then
  echo "error: 'cv.source' not set in _config.yaml" >&2
  exit 1
fi

if [[ -z "$DEST_REL" ]]; then
  echo "error: 'cv.dest' not set in _config.yaml" >&2
  exit 1
fi

if [[ ! -f "$SRC" ]]; then
  echo "error: source CV not found at: $SRC" >&2
  exit 1
fi

DEST="$ROOT/$DEST_REL"

if cmp -s "$SRC" "$DEST" 2>/dev/null; then
  echo "No changes — $DEST_REL already matches source."
  exit 0
fi

cp "$SRC" "$DEST"
git -C "$ROOT" add "$DEST_REL"
echo "Synced and staged: $DEST_REL"
echo "Review with 'git diff --cached $DEST_REL', then commit and push to typeset."
