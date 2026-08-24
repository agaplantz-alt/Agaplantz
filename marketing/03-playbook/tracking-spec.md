# Tracking Specification — fix this before anything else

Decision hierarchy rule #1. Every number in this account is currently unreliable. No optimisation is legitimate until this file is fully green.

| # | Defect | Evidence | Status |
|---|---|---|---|
| T-1 | Meta pixel has never fired | `last_fired_time` = 1969-12-31 (epoch) | 🔴 |
| T-2 | Meta CAPI not sending | `server_last_fired_time` = epoch | 🔴 |
| T-3 | $0 free-kit orders counted as primary purchase conversions | 71 kit orders, 28 via `search` | 🔴 |
| T-4 | GA4 captures only 61% of orders / 66% of revenue | 74 vs 121 orders, Jul 1–Aug 24 | 🔴 |
| T-5 | GA4 `add_to_cart` over-fires | 30.6% of sessions vs Shopify ~6.6% | 🔴 |
| T-6 | GA4 `begin_checkout` under-fires | 91 vs expected ~585 | 🔴 |
| T-7 | PAGE_VIEW conversion actions carry revenue values | `all_conversions_value` = $444,422 | 🟠 |
| T-8 | Four Meta ad accounts fragment pixel data | 4 accounts, 1 business | 🟠 |

## T-1 / T-2 — Meta pixel + CAPI
1. Install the Meta sales channel on Shopify and bind dataset **`4340434602872984`** (do not create a new one — a new dataset restarts the learning history).
2. Enable **Conversions API** via the Shopify integration; confirm `server_last_fired_time` moves off epoch.
3. Verify event deduplication (`event_id` shared browser+server) — duplicated purchases are as damaging as none.
4. Target **Event Match Quality ≥ 6.0**. Pass email, phone, first/last name, city, postcode, `fbp`/`fbc`.
5. **Acceptance:** Purchase, InitiateCheckout, AddToCart, ViewContent all firing from both channels; Meta purchase count within ±10% of Shopify for a 7-day window.

## T-3 — De-weight the free Starter Kit
- Create a separate conversion action for the $0 Tissue Culture Starter Kit.
- Mark it **Secondary (observation only)**. Keep the paid purchase action Primary.
- Do **not** delete history — the kit may be a valid acquisition tool (EXP-004 decides).
- **Acceptance:** primary conversion count drops to paid orders only; verify against Shopify paid-order count.

## T-4 / T-5 / T-6 — GA4 rebuild
- Audit for duplicate tags: a theme-level `add_to_cart` plus an app-level one is the usual cause of 30% ATC.
- `begin_checkout` is almost certainly not firing on Shopify's checkout (a common gap on newer checkout extensibility). Wire it via a checkout UI extension or Customer Events.
- Reconcile `purchase` against Shopify weekly. Under-capture of 39% usually means checkout events aren't wired at all.
- **Acceptance:** GA4 purchases within ±5% of Shopify for 14 consecutive days.

## T-7 — Conversion action hygiene
Only `Google Shopping App Purchase` should be Primary and carry value. Every PAGE_VIEW / ADD_TO_CART / BEGIN_CHECKOUT action → Secondary, value removed. Report on `Conversions`, never `All conversions`.

## T-8 — Account consolidation
Standardise on **`1411593217321687` (Aga Plantz)** — the only account with campaign history and a payment method. Do not run spend from more than one.

## Definition of done
- [ ] Meta pixel + CAPI firing, EMQ ≥ 6.0, deduplicated
- [ ] Free kit reclassified as Secondary
- [ ] GA4 purchases within ±5% of Shopify for 14 days
- [ ] One Primary conversion action carrying value in Google Ads
- [ ] All ad spend running from one Meta account
- [ ] **COGS loaded** → break-even ROAS calculated (see below)

## The missing number
**Contribution margin is unknown.** Until it exists, "is 3.2x ROAS good?" cannot be answered.

```
Contribution margin % = (Price − COGS − Shipping cost − Payment fees − Discount) / Price
Break-even ROAS       = 1 / Contribution margin %
Target ROAS           = Break-even ROAS / (desired contribution ratio)
```

Tier COGS by **TC / acclimated / premium variegated** — these almost certainly have very different margins, and a blended average would hide it.
