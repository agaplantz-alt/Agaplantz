# The brain

Persistent memory for Agaplantz. Claude loads `CLAUDE.md` automatically each
session, and `CLAUDE.md` points here.

## Files

| File | What belongs in it |
| --- | --- |
| `business.md` | What the business is, where it sells, economics, constraints |
| `products.md` | Plants and product lines, prices, margins, stock reality |
| `audience.md` | Who buys, why, objections, language they use |
| `shopify.md` | The store: live theme, design system, catalog, apps |
| `marketing.md` | Channels, budgets, what worked, what failed |
| `image-editing.md` | How images and creatives must be edited — the look, sizes, never-dos |
| `decisions.md` | Dated log of decisions and the reasoning behind them |

## Rules

1. **Facts only.** If it is a guess, mark it `(assumption)`.
2. **Date entries.** `2026-08-28 — ...` so stale information is visible.
3. **Delete what is wrong.** A brain full of outdated facts is worse than a
   small accurate one.
4. **Commit it.** Uncommitted knowledge does not survive the session.

## Adding to it during a session

Just say "remember this" and Claude writes it to the right file and commits.

## Automation

`.claude/hooks/brain-load.sh` (SessionStart) loads this index and the core
facts automatically. `.claude/hooks/brain-commit-check.sh` (Stop) blocks the
end of a session while brain changes are uncommitted or unpushed.
