#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"

"$ROOT/install.sh" "$TMP_DIR" >/dev/null

cd "$TMP_DIR"
python3 tools/agent-context.py --help >/dev/null
python3 tools/agent-context.py scaffold TASK-123 --title "Smoke test" --owner test --source local >/dev/null
python3 tools/agent-context.py check TASK-123 >/dev/null

if python3 tools/agent-context.py check TASK-123 --strict >/dev/null 2>&1; then
  echo "Expected strict check to fail while scaffolded TODO placeholders remain" >&2
  exit 1
fi

echo "Smoke test passed"
