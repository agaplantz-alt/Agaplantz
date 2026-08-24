# Strategy Database — scored and classified

Every strategy is (a) **classified** by evidence type (PART 6), (b) **interrogated** for why it works and when it fails (PART 7), and (c) **scored** for AgaPlantz (PART 18).

**Scoring:** Evidence, Recency, Expert credibility, Relevance to AgaPlantz, Ease, Expected impact — each /10. **Risk /10 where 10 = riskiest.**
**Priority = (Evidence + Relevance + Impact) × 2 − Risk + Ease.** Max 71.

Classifications: **CONSENSUS** · **STRONG EVIDENCE** · **EXPERIMENTAL** · **OUTDATED** · **CONTRADICTORY**

---

## Priority ranking

| # | Strategy | Class | Ev | Rec | Cred | Rel | Risk | Ease | Impact | **Pri** |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fix the Meta pixel + CAPI | CONSENSUS | 10 | 10 | 10 | 10 | 1 | 7 | 9 | **64** |
| 2 | Stop counting $0 free-kit orders as purchase conversions | CONSENSUS | 9 | 10 | 9 | 10 | 2 | 7 | 8 | **59** |
| 3 | Real live-arrival guarantee, stated at checkout | STRONG EVIDENCE | 8 | 9 | 8 | 10 | 4 | 8 | 9 | **58** |
| 4 | Establish COGS → break-even ROAS | CONSENSUS | 10 | 10 | 10 | 10 | 1 | 5 | 8 | **60** |
| 5 | Keep PMax consolidated; do not segment | CONSENSUS | 9 | 10 | 9 | 10 | 1 | 10 | 7 | **61** |
| 6 | Fix GA4 e-commerce tagging | CONSENSUS | 9 | 9 | 9 | 8 | 2 | 6 | 6 | **50** |
| 7 | Negative-keyword the competitor brands + dead terms | CONSENSUS | 8 | 9 | 8 | 9 | 2 | 9 | 5 | **51** |
| 8 | Double down on the "tissue culture Canada" niche | STRONG EVIDENCE | 8 | 10 | 7 | 10 | 3 | 7 | 8 | **56** |
| 9 | Turn off the duplicate Standard Shopping campaigns | CONSENSUS | 8 | 9 | 8 | 9 | 2 | 10 | 4 | **50** |
| 10 | Cut the discount rate / stop rolling deadlines | STRONG EVIDENCE | 7 | 8 | 8 | 9 | 5 | 6 | 8 | **49** |
| 11 | Diagnose the email channel (25 checkouts → 0 purchases) | STRONG EVIDENCE | 8 | 9 | 7 | 9 | 2 | 6 | 7 | **52** |
| 12 | Feed optimisation in Merchant Center | CONSENSUS | 9 | 9 | 9 | 9 | 2 | 5 | 8 | **55** |
| 13 | Consolidate to ONE Meta ad account | CONSENSUS | 8 | 9 | 8 | 8 | 3 | 6 | 5 | **45** |
| 14 | Launch Meta with a Sales objective (never Traffic) | CONSENSUS | 9 | 10 | 9 | 9 | 3 | 8 | 7 | **55** |
| 15 | Exclude Search Partners / audit Aug-19 junk traffic | EXPERIMENTAL | 5 | 9 | 6 | 7 | 3 | 8 | 4 | **37** |
| 16 | Separate brand Search campaign | OUTDATED *(for us)* | 8 | 9 | 9 | 2 | 3 | 8 | 1 | **27** |
| 17 | Dedicated Meta creative-testing campaign | CONTRADICTORY | 7 | 9 | 9 | 2 | 6 | 5 | 2 | **21** |
| 18 | Segment PMax by margin tier | OUTDATED *(for us)* | 8 | 9 | 9 | 1 | 8 | 4 | 1 | **16** |

---

## The interrogation (PART 7) — top strategies

### 1. Fix the Meta pixel + CAPI — Priority 64
- **Problem solved:** dataset `4340434602872984` has `last_fired_time` at Unix epoch. Zero events, browser and server.
- **Why it works:** Meta's delivery system is a prediction engine. With no conversion events it has nothing to predict, so it optimises toward the cheapest available proxy — which is why both existing campaigns defaulted to Traffic.
- **Evidence:** Tier 1. Direct read from Meta's own dataset API.
- **Conditions:** none — this is a precondition, not a tactic.
- **When it fails:** it doesn't. Worst case, it's insufficient on its own.
- **Downside:** a few hours of setup.
- **Abandon if:** never.
- **Measure:** `last_fired_time` moves off epoch; Event Match Quality ≥ 6.0; server + browser both firing with deduplication.

### 4. Establish COGS → break-even ROAS — Priority 60
- **Problem solved:** every decision in this account is currently made on revenue ratios. MER 5.79x *looks* excellent, but with a 24.8% discount rate and shipping subsidy, the profit behind it is unknown.
- **Why it works:** break-even ROAS = 1 ÷ contribution margin. Without it, "is 3.2x good?" is unanswerable — and that question governs every budget decision.
- **Evidence:** Tier 1 reasoning; CONSENSUS across the panel (Common Thread Collective's central discipline).
- **When it fails:** if COGS varies wildly per SKU and gets averaged, tier it instead (TC vs acclimated vs premium variegated — these almost certainly have very different margins).
- **Downside:** none. Effort only.
- **Abandon if:** never.

### 5. Keep PMax consolidated — Priority 61
- **Problem solved:** the strongest temptation from expert content is to segment. At ~24 paid conversions/month, segmenting guarantees every campaign sits permanently in learning.
- **Why it works:** smart bidding needs a minimum conversion density per campaign. Below it, the model can't distinguish signal from noise.
- **Evidence:** CONSENSUS. Store Growers states it as an explicit rule (30–50 conv/mo → 1–2 campaigns); universally echoed.
- **Conditions:** holds until sustained ~$10k/month spend or 100+ monthly conversions.
- **When it fails:** at genuine scale, one ROAS target across 60%-margin and 10%-margin SKUs does become the constraint. Not our problem yet.
- **This is a "do nothing" strategy — its value is in preventing an expensive mistake.**

### 3. Real live-arrival guarantee — Priority 58
- **Problem solved:** 74.4% checkout abandonment.
- **Hypothesis (not fact):** buyers reach checkout, weigh a $200–500 living purchase against a policy that explicitly disclaims responsibility for transit damage, and stop.
- **Why it should work:** collector research is consistent that trust in the source is a gating condition for high-ticket purchases, and that ambiguity — not price — is what stalls them. A guarantee transfers transit risk from the buyer (who cannot control it) to the seller (who can, via packing and hold-for-weather).
- **Evidence:** Tier 2/3. The abandonment number is Tier 1; the *cause* is inference. **Must be tested, not assumed.**
- **When it fails:** if abandonment is actually driven by shipping cost or missing express wallets. Cheap to find out — run the checkout walkthrough first.
- **Downside:** real replacement cost. Cap exposure: 48-hour claim window with unboxing photo, DOA replacement or store credit, exclude heat/cold delays already disclosed.
- **Abandon if:** checkout completion doesn't move ≥5pp in 6 weeks, or claim rate exceeds ~3% of orders.

### 2. Stop counting $0 free-kit orders as conversions — Priority 59
- **Problem solved:** 42.5% of all orders are a free product; 28 came through `search`. They fire purchase events at ~$0.
- **Why it works:** value-based bidding partially absorbs $0 events, but the conversion *count* still drives learning-phase exit and audience expansion — and freebie-claimers enter the remarketing/Customer Match pools feeding PMax audience signals. The seed audience is being poisoned.
- **Evidence:** Tier 1 on the data; Tier 3 on the mechanism.
- **Fix:** separate the Starter Kit into its own conversion action marked **secondary** (observation only), keep the paid Purchase action primary. Do **not** delete the data — the kit may be a good acquisition tool; we just shouldn't bid on it.
- **When this reasoning fails:** if free-kit claimers convert to paying customers at a strong rate, they're a legitimate signal. **Unknown — measure it before deciding** (see experiment EXP-004).

### 8. Double down on "tissue culture Canada" — Priority 56
- **Evidence:** Tier 1. `tissue culture plants canada` is the account's highest-volume search term (63 clicks/90d); `tissue culture plants` returns 44x ROAS on small volume; the free Starter Kit and the pre-order model are already built around it.
- **Why it works:** it is a category most Canadian plant retailers don't serve, with genuine search demand and a natural pre-order/anticipation model. Defensible positioning beats competing on "monstera albo" against everyone.
- **When it fails:** if TC conversion economics are worse than acclimated (longer time-to-value, higher failure rate, more support). **Check margin by product type before scaling.**

### 16–18. Strategies we are explicitly NOT adopting

Recorded so they don't get re-proposed:

- **Brand Search campaign (Pri 27) — OUTDATED for us.** Correct advice, wrong preconditions. `aga plantz` = 3 clicks/90d. Nothing to defend. Revisit at ~100 brand impressions/month.
- **Dedicated creative-testing campaign (Pri 21) — CONTRADICTORY.** Denney and Foxwell both endorse it; both assume enough conversions to read a test. We'll have ~0 at Meta launch. Test inside one campaign first.
- **PMax margin-tier segmentation (Pri 16) — OUTDATED for us.** Needs ~$10k/mo. At $800/mo it splits 24 conversions into permanently-learning fragments. **Highest-risk "best practice" in this document.**

---

## Where the experts contradict each other, and why (PART 6)

| Disagreement | Camp A | Camp B | Root cause | Our call |
|---|---|---|---|---|
| PMax vs Standard Shopping | PMax with steering | Shopping for control | **Account size + feed quality.** Control matters more when you have enough volume to act on it. | PMax. We lack volume to steer Shopping manually, and PMax is producing 3.2x. |
| Broad vs segmented targeting (Meta) | Broad / Advantage+ | Structured audiences | **Pixel maturity.** Broad works when the pixel has signal. | Moot — our pixel has zero signal. Broad by necessity at launch. |
| Discounting | Drives volume & AOV thresholds | Destroys margin & trains waiting | **Margin structure and repeat rate.** | Our 24.8% rate with unknown COGS is unsafe. Reduce, and replace deadline-stacking with genuine scarcity (real batch limits). |
| Free lead-magnet products | Cheap list building | Attracts non-buyers | **Whether the freebie predicts purchase.** | **Genuinely unknown for us.** Measure (EXP-004) before judging. |
