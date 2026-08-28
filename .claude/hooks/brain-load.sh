#!/usr/bin/env bash
# SessionStart: put the brain's index and core facts into context automatically,
# so a new session never starts blank. Fails open — never blocks a session.
set -uo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[ -d "$repo/brain" ] || exit 0

{
  echo "# Agaplantz brain — loaded automatically at session start"
  echo
  echo "Files available in brain/ (read the one relevant to the task):"
  for f in "$repo"/brain/*.md; do
    [ -e "$f" ] || continue
    printf '  - brain/%s (%s lines)\n' "$(basename "$f")" "$(wc -l < "$f" | tr -d ' ')"
  done
  echo
  echo "===== brain/README.md ====="
  cat "$repo/brain/README.md" 2>/dev/null
  echo
  echo "===== brain/business.md ====="
  cat "$repo/brain/business.md" 2>/dev/null
  echo
  echo "===== Standing instruction ====="
  echo "Write every new fact, preference, correction, decision and result into the"
  echo "right brain/ file and commit it before this session ends. Prefer reading the"
  echo "live account (Shopify, Meta, analytics) over recalling; date what you record."
} | jq -Rs '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:.}}'
