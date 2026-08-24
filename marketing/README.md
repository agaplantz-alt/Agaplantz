# AgaPlantz Marketing Intelligence System

A standing system for running AgaPlantz paid acquisition on evidence rather than platform defaults.

**Built:** 2026-08-24 · **Data through:** 2026-08-24

## Start here
1. **[`02-account-state/audit-2026-08-24.md`](02-account-state/audit-2026-08-24.md)** — the full audit. Read this first.
2. **[`00-operating-system/operating-rules.md`](00-operating-system/operating-rules.md)** — decision hierarchy, evidence tiers, change discipline.
3. **[`04-experiments/experiment-log.md`](04-experiments/experiment-log.md)** — what to do, in order.

## The three things that matter right now
| | |
|---|---|
| 🔴 **Meta pixel has never fired** | Dataset created 2026-08-15, zero events browser and server. Meta advertising cannot work until fixed. |
| 🔴 **Checkout completion is 25.6%** | ~134 abandonments/month. Fixing it to 40% ≈ **+$5,500/month at zero extra ad spend** — the largest opportunity in the business. |
| 🔴 **Contribution margin is unknown** | No COGS anywhere. Every "is this ROAS good?" question is currently unanswerable. |

## Layout
```
00-operating-system/   How decisions get made
  operating-rules.md     Decision hierarchy · evidence tiers · scale rule
  hypothesis-system.md   Required fields before any change runs
  reporting-format.md    Action-first output format
  research-sops.md       Reusable procedures (audit, term mining, expert vetting)
  data-access.md         What we can and cannot see — including honest gaps

01-intelligence/       What we know about the market
  expert-panel.md          Practitioners + where their advice stops applying to us
  strategy-database.md     18 strategies, classified and scored
  rare-plant-psychology.md Buyer types, trust stack, customer vocabulary
  creative-library.md      6 concepts, Hook→Problem→Desire→Proof→Offer→CTA
  competitor-intel.md      Confirmed comparison set, from our own search terms

02-account-state/      What is true about the account
  audit-2026-08-24.md

03-playbook/           What we do
  tracking-spec.md         Fix-first checklist (8 defects)
  google-ads-playbook.md
  meta-ads-playbook.md     (blocked on pixel)
  cro-checkout.md          Highest-value work in the business

04-experiments/
  experiment-log.md        7 experiments, sequenced
```

## The rule that governs everything
> **AgaPlantz runs ~24 paid orders/month on ~$800/month spend, on a 4-month-old store.**
>
> Nearly every published expert framework assumes 20–500x that volume. Their *diagnostics* transfer almost perfectly. Their *structures* mostly do not.
>
> **Any strategy that divides ~24 monthly conversions into more than one optimisation bucket is presumed harmful until proven otherwise.**

## Honest limitations
- **No Apify access in this session** — expert research used web search/fetch, which reaches articles and podcast pages but not video transcripts at scale. This is the main gap vs. the original brief.
- **AdWhispr** free-tier calls were exhausted; competitor names came from our own search-term report instead (better evidence anyway).
- **No Merchant Center connector** — feed health, the biggest PMax lever, is unaudited.
- **No COGS** — the single most important missing input.
- Every claim is labelled Known fact / Inference / Hypothesis. Nothing is invented.
