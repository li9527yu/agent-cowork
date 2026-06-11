#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$(pwd)}"

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Target directory does not exist: $TARGET_DIR" >&2
  exit 1
fi

copy_file() {
  local src="$1"
  local dest="$2"
  mkdir -p "$(dirname "$dest")"
  if [[ -e "$dest" ]]; then
    if cmp -s "$src" "$dest"; then
      echo "unchanged $dest"
    else
      echo "exists    $dest"
    fi
  else
    cp "$src" "$dest"
    echo "created   $dest"
  fi
}

copy_tree_file() {
  local rel="$1"
  copy_file "$SOURCE_DIR/$rel" "$TARGET_DIR/$rel"
}

append_managed_block() {
  local file="$1"
  local title="$2"
  local body="$3"
  local begin="<!-- agent-collaboration:start -->"
  local end="<!-- agent-collaboration:end -->"

  mkdir -p "$(dirname "$file")"
  if [[ ! -e "$file" ]]; then
    {
      echo "# $title"
      echo
      echo "$begin"
      echo "$body"
      echo "$end"
    } > "$file"
    echo "created   $file"
    return
  fi

  if grep -q "$begin" "$file"; then
    echo "managed  $file"
    return
  fi

  {
    echo
    echo "$begin"
    echo "$body"
    echo "$end"
  } >> "$file"
  echo "updated   $file"
}

AGENTS_BLOCK='This repository uses Agent Collaboration Workflow.

Before substantial work, read `docs/ai-collaboration-sop.md` and the active task files under `docs/tasks/<task-id>/`.

Useful commands:

```bash
python3 tools/agent-context.py scaffold TASK-123 --title "Short title" --owner "Owner" --source "Issue or PR link"
python3 tools/agent-context.py check-all --strict
```'

CLAUDE_BLOCK='This repository uses Agent Collaboration Workflow.

Read `AGENTS.md`, `docs/ai-collaboration-sop.md`, and the active task files under `docs/tasks/<task-id>/` before substantial work. Update handoff before stopping and do not invent decisions or validation evidence.

```bash
python3 tools/agent-context.py check-all --strict
```'

append_managed_block "$TARGET_DIR/AGENTS.md" "Project Instructions" "$AGENTS_BLOCK"
append_managed_block "$TARGET_DIR/CLAUDE.md" "Claude Instructions" "$CLAUDE_BLOCK"

copy_tree_file ".cursor/rules/agent-collaboration.mdc"
copy_tree_file ".agents/skills/agent-collaboration/SKILL.md"
copy_tree_file ".agents/skills/agent-collaboration/agents/openai.yaml"
copy_tree_file "skills/agent-collaboration/SKILL.md"
copy_tree_file "docs/ai-collaboration-sop.md"
copy_tree_file "docs/templates/context-pack.md"
copy_tree_file "docs/templates/handoff.md"
copy_tree_file "docs/templates/pr-context-diff.md"
copy_tree_file "tools/agent-context.py"

chmod +x "$TARGET_DIR/tools/agent-context.py"

echo
echo "Agent Collaboration Workflow installed in: $TARGET_DIR"
echo "Next:"
echo "  python3 tools/agent-context.py scaffold TASK-123 --title \"Short title\" --owner \"Owner\" --source \"Issue or PR link\""
echo "  python3 tools/agent-context.py check-all --strict"
