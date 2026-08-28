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

## Capture protocol — write it down as it happens

Do not wait to be asked. During any session, the moment one of these appears,
write it into the right `brain/` file and commit before the session ends:

- A **fact** about the business — a price, a margin, a lead time, a supplier.
- A **preference** — how something should look, sound, or be done.
- A **correction** — anything the user says is wrong. These matter most; a
  correction that is not written down gets repeated.
- A **decision** and its reasoning → `brain/decisions.md`, dated.
- A **result** — what a campaign, page, or change actually did.

Prefer verifying over remembering: the Shopify, Meta, and analytics accounts are
connected, so read the live state and record it with the date observed rather
than relying on recall. Mark anything unverified as `(assumption)`.

At the end of a working session, ask: *what did I learn here that the next
session would need?* Write that, then commit.

## Images

Before editing, generating, or resizing any image for Agaplantz, read
`brain/image-editing.md` and follow it. When the user corrects an edit, write
the correction into that file and commit it — a correction that is not written
down will be repeated.

## Automation

Two hooks in `.claude/settings.json` enforce the capture protocol, so it does
not depend on Claude remembering to follow it:

- **SessionStart** → `.claude/hooks/brain-load.sh` injects the brain index,
  `brain/README.md` and `brain/business.md` into context at session start.
- **Stop** → `.claude/hooks/brain-commit-check.sh` refuses to end the session
  while `brain/` or `CLAUDE.md` has uncommitted edits, or while commits sit
  unpushed. It blocks once, then lets the session end, so it can never loop.
