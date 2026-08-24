# Experiment Log

Append-only. Every material change gets an entry before it runs. Status: `PROPOSED` → `RUNNING` → `KEPT` / `MODIFIED` / `REVERTED`.

**Sequencing rule:** EXP-001 and EXP-002 are preconditions. Nothing below them produces trustworthy results until they are done.

---

## EXP-001 — Restore Meta conversion tracking
**Status:** PROPOSED · **Priority:** CRITICAL
- **Problem:** Meta dataset `4340434602872984` has never fired an event. `last_fired_time` and `server_last_fired_time` both at Unix epoch.
- **Hypothesis:** Not a tactic — a broken precondition. The Shopify↔Meta integration was never completed after the dataset was created on 2026-08-15.
- **Change:** Bind the existing dataset via Shopify's Meta channel; enable CAPI; verify deduplication and match keys.
- **Expected:** Events flow browser + server; EMQ ≥ 6.0.
- **Measurement:** `last_fired_time` off epoch; Meta purchase count within ±10% of Shopify over 7 days.
- **Horizon:** 7 days post-implementation.
- **Decision rule:** KEEP on success. If EMQ < 6.0, add match keys and re-measure. **No Meta spend until this passes.**

## EXP-002 — Reclassify the free Starter Kit conversion
**Status:** PROPOSED · **Priority:** CRITICAL
- **Problem:** 71 free $0 orders = 42.5% of all orders; 28 arrived via `search` and fire purchase events into Google Ads.
- **Hypothesis:** Zero-value purchase events inflate the conversion count driving learning and audience expansion, and seed remarketing/Customer Match pools with people who take free things.
- **Change:** Separate conversion action for the kit, set to **Secondary (observation)**. Paid purchase stays Primary.
- **Expected:** Primary conversions fall to paid orders only (~24/mo). Reported ROAS may *rise* as the denominator cleans up.
- **Measurement:** Google primary conversion count vs Shopify paid orders.
- **Horizon:** 4 weeks.
- **Decision rule:** KEEP if primary conversions track Shopify paid orders within ±15%. REVERT only if EXP-004 shows kit claimers convert to paid at a strong rate.

## EXP-003 — Live-arrival guarantee at checkout
**Status:** PROPOSED · **Priority:** CRITICAL (largest revenue opportunity)
- **Problem:** checkout completion 25.6% (46 of 180). ~134 abandonments/month.
- **Hypothesis:** The homepage's soft "Live Plant Guarantee" is contradicted by a shipping policy that disclaims transit damage and offers no live-arrival guarantee. Buyers spending $200–500 on a living thing from a 4-month-old brand resolve that contradiction by leaving. *(Hypothesis — the number is Tier 1, the cause is inference.)*
- **Prerequisite:** manual checkout walkthrough first. If express wallets are missing or pre-order dates are unclear, fix that first and re-rank.
- **Change:** Publish a bounded live-arrival guarantee (48h claim, unboxing photo, DOA replacement or credit, weather holds excluded) and surface it **inside checkout**. One variable — do not also change shipping price.
- **Expected:** checkout completion 25.6% → ≥33% (conservative; +13 orders/mo ≈ +$2,750/mo at $212 AOV).
- **Measurement:** `sessions_that_completed_checkout / sessions_that_reached_checkout`. Baseline: 25.6% (Aug 2026). Secondary: claim rate, AOV, refunds.
- **Horizon:** 4 weeks (~180 checkouts/month — a shorter read cannot separate 5pp from noise).
- **Decision rule:** KEEP if completion ≥30% and claims <3% of orders. MODIFY if completion improves but claims 3–6%. REVERT if claims >6% or margin turns negative.

## EXP-004 — Does the free Starter Kit produce paying customers?
**Status:** PROPOSED · **Priority:** HIGH
- **Problem:** 71 free kits given away. Whether this is smart acquisition or pure cost is **unknown** — and it gates the EXP-002 decision.
- **Hypothesis:** TC kit claimers are propagator-type buyers who return for plants. Untested either way.
- **Change:** None. Pure measurement.
- **Measurement:** Of customers whose first order was the kit, what % placed a paid order within 60/90 days, and at what AOV? Compare with customers acquired via a paid first order.
- **Horizon:** Immediate cohort pull; re-read at 90 days.
- **Decision rule:** If ≥15% convert to paid → keep the kit as an acquisition tool and build an email sequence around it. If <5% → stop promoting it in paid channels.

## EXP-005 — Reduce discount depth
**Status:** PROPOSED · **Priority:** HIGH · **Blocked on COGS**
- **Problem:** August discounts 24.8% of gross ($3,106 of $12,533). Rolling deadlines ("Ends Aug 25", "Ends Aug 31") keep being replaced.
- **Hypothesis:** Perpetual deadline-stacking trains customers to wait and is unnecessary in a category where scarcity is structurally real.
- **Change:** Replace stacked percentage discounts with true batch scarcity ("this batch: 12 plants; next TC batch ~6 weeks"). Reduce blended discount to ≤15%.
- **Expected:** Order volume dips slightly; contribution margin per order rises materially.
- **Measurement:** Discount %, orders, contribution margin per order. **Cannot be judged without COGS — do not run before that exists.**
- **Horizon:** 4 weeks.
- **Decision rule:** KEEP if total contribution margin rises even with fewer orders. REVERT if orders fall >25%.

## EXP-006 — Google Ads waste cleanup
**Status:** PROPOSED · **Priority:** MEDIUM
- **Problem:** ~$93/90d on zero-converting terms incl. 4 competitor brands; two Standard Shopping campaigns re-enabled Aug 20–23 ($42.39, 0 conv) competing with PMax; Aug 19 junk-traffic spike (375 clicks, $0.35 CPC, 0 conv).
- **Change:** Pause the duplicate Shopping campaigns; add competitor-brand negatives; audit Aug 19 placements. Investigate `monstera albo` ($28.15, 0 conv) for landing-page mismatch **before** excluding — we do sell it.
- **Expected:** ~$40–60/month reclaimed. Small, but free.
- **Horizon:** 4 weeks.
- **Decision rule:** KEEP unless total conversions fall.

## EXP-007 — Diagnose the email channel
**Status:** PROPOSED · **Priority:** HIGH
- **Problem:** GA4 Jul 1–Aug 24: Email 310 sessions → 25 begin-checkouts → **0 purchases**.
- **Hypothesis:** Either an attribution/tracking break (likely, given GA4 captures only 61% of orders overall) or a genuine offer failure. **Cannot distinguish from available data.**
- **Change:** None yet — diagnose first. Requires email-platform access, which is not connected.
- **Decision rule:** If tracking artefact → fold into the GA4 rebuild. If real → treat as a channel rebuild, not an ads problem.
