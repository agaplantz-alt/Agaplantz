# Decision log

Newest first. Format: `## YYYY-MM-DD — decision` then one short paragraph of
reasoning.

## 2026-08-28 — Keep business memory in the repo, not in chat

Claude sessions start with no memory of previous conversations. Anything that
should survive gets written to `brain/` and committed, so every future session
loads it automatically via `CLAUDE.md`.
