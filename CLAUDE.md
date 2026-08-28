# Agaplantz — working notes for Claude

Read `brain/` before doing any work in this repo. It is the persistent memory
for this business: what we sell, who buys it, what we have already tried, and
what we decided and why.

## How to work here

- Start by reading `brain/README.md`, then the file relevant to the task.
- When a session establishes a durable fact (a price, a margin, a channel that
  worked, a decision), write it into the right `brain/` file and commit it.
  If it is not committed, the next session will not know it.
- Do not invent facts about the business. Anything marked `TODO` is genuinely
  unknown — ask, then fill it in.
- Keep entries short and dated. This is a reference, not an essay.

## Repo contents

- `brain/` — persistent business memory (see below).
- `docs/claude-ads-setup.md` — the Claude Ads plugin enabled for this repo.
- `.claude/settings.json` — plugin/marketplace configuration.
