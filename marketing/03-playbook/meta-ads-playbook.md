# Meta Ads Playbook — AgaPlantz

## 🔴 BLOCKED

**Do not spend on Meta until the pixel fires.** Dataset `4340434602872984` has received zero events, browser and server. See `tracking-spec.md` T-1/T-2. Spending now buys traffic no system can learn from — which is exactly how both existing campaigns ended up on a **Traffic** objective with $3.52 spent.

## Why build this channel at all

GA4, Jul 1–Aug 24: **Paid Social — 299 sessions → 5 purchases → $527.30 = 1.7% CVR, roughly double the 0.92% site average**, on essentially zero spend. Small sample, but the signal points the right way, and rare plants are a visually-driven, community-driven category that suits Meta.

## Launch sequence (only after tracking is green)

**Phase 0 — Preconditions**
- [ ] Pixel + CAPI firing, EMQ ≥ 6.0, deduplicated
- [ ] One ad account only (`1411593217321687`)
- [ ] Catalogue connected for retargeting
- [ ] COGS known → break-even ROAS set

**Phase 1 — One campaign, weeks 1–4**
```
Campaign: Sales objective (NEVER Traffic)     <- both current campaigns get this wrong
  Ad set: broad, Canada, no interest stacking
    Ads: C-01 (unboxing), C-03 (one plant one photo), C-05 (founder)
  Budget: $30–50/day
```
Broad targeting is a necessity, not a preference: with a cold pixel there is no signal to narrow on. Interest stacking on a zero-history pixel just shrinks the pool.

**Phase 2 — Retargeting, week 3+**
Only once site-visitor pools are large enough. Catalogue/DPA to viewers and cart abandoners. Given 74% checkout abandonment, **checkout abandoners are the highest-value pool in the account** — and they can't be reached at all until the pixel works.

**Phase 3 — Structured testing, month 2+**
Only when the account clears ~50 conversions/month. Until then, test inside the single campaign.

## Why we deviate from the panel here
Denney and Foxwell both recommend a dedicated creative-testing campaign alongside Advantage+. **We are not doing that at launch.** That structure needs enough conversions to read a test; we'll start at zero. Adopting it early would split a signal we don't have. Revisit at ~50 conv/month.

## Guardrails
- Sales objective only. Never Traffic. Never Engagement.
- One ad account.
- Minimum 4–5 days before judging an ad — Meta's learning phase is real.
- Kill early on 3-second hold rate and cost-per-ATC, not purchases (too little purchase volume for fast reads).
- Exclude existing customers from prospecting; build a separate winback.
- **Exclude the 71 free-kit claimers from lookalike seeds.**
