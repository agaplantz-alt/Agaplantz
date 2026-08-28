#!/usr/bin/env bash
# Stop: refuse to end the session while the brain has knowledge that would be
# lost — uncommitted edits, or commits that were never pushed. The container is
# ephemeral, so unpushed work does not survive.
set -uo pipefail

input="$(cat)"
# Never loop: if this hook already blocked once this turn, let the session end.
[ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ] && exit 0

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo" || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

dirty="$(git status --porcelain -- brain CLAUDE.md 2>/dev/null)"
branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
unpushed=""
if git rev-parse --verify --quiet "origin/$branch" >/dev/null 2>&1; then
  unpushed="$(git log --oneline "origin/$branch..HEAD" 2>/dev/null)"
fi

[ -z "$dirty" ] && [ -z "$unpushed" ] && exit 0

reason="The brain has knowledge that will be lost if this session ends now."
[ -n "$dirty" ]    && reason="$reason"$'\n\nUncommitted changes:\n'"$dirty"
[ -n "$unpushed" ] && reason="$reason"$'\n\nCommits not pushed to origin/'"$branch"$':\n'"$unpushed"
reason="$reason"$'\n\nCommit and push before ending. Also check: did anything in this session establish a fact, preference, correction, decision or result that is not yet written into brain/? Write it now.'

jq -n --arg r "$reason" '{decision:"block", reason:$r}'
