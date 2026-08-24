# Google Ads Playbook — AgaPlantz

**Governing constraint: ~24 paid conversions/month, ~$800/month spend.** Everything below is calibrated to that. Re-derive when spend passes $3k/month.

## Account architecture (current state is close to correct)

```
ONE PMax campaign — "Sales-Performance max"        <- keep, do not split
  └─ feed: full catalogue
  └─ audience signal: customer match (paying customers only)
NO brand Search campaign                            <- no brand demand exists yet
NO Standard Shopping                                <- competes with PMax on the same feed
```

**Rules:**
1. **Never create more campaigns than conversion volume supports.** Below 30 conv/mo: one campaign. Panel-consensus, Store Growers explicit.
2. **No margin-tier segmentation until ~$10k/month spend.**
3. **No brand campaign until brand search exceeds ~100 impressions/month.** Currently 3 clicks/90 days.
4. **Evaluate on 4–6 week windows**, never daily. Daily reads at 0.8 conversions/day are noise.

## Immediate housekeeping
- **Pause** `Sales Shopping` and `Sales-Shopping` (re-enabled Aug 20–23, $42.39, 0 conversions). PMax takes priority on the same feed; these only bid against it.
- **Add negative keywords** — competitor brands, zero-converting terms:
  `planteia`, `plantsome`, `floral acres`, `gardenworks`, `toronto tropical plants`, `white princess tricolor`
- **Investigate `monstera albo`** — 29 clicks, $28.15, 0 conversions in 90 days. Our Monstera Albo sells (7 orders, $334) so the term isn't inherently bad; likely a price or landing-page mismatch. Check before excluding.
- **Investigate Aug 19** — $132.18, 375 clicks, 0 conversions, CPC $0.35 vs ~$0.90 norm. Check placement report for Display/Search Partners junk; exclude if confirmed.

## Feed optimisation (highest-leverage unmeasured lever)
Panel consensus: in PMax the feed *is* the campaign. We have no Merchant Center connector, so this is unaudited.

Title formula, derived from our own Tier 1 search data:
```
[Cultivar Name] + [Variegation/Form] + [TC or Acclimated] + "Canada"
e.g. "Monstera Bulbasaur Variegated — Acclimated Plant | Canada"
```
Justification: customers search cultivar names and append "canada" constantly. `tissue culture plants canada` is our highest-volume term.

Also: real per-plant photography (variegation is unique — stock images read as a red flag), `google_product_category`, GTIN/MPN where possible, accurate availability for pre-orders.

## Bidding
- Stay on value-based bidding.
- **Do not set a tROAS target until COGS exists.** A target picked without break-even is a guess with a decimal point.
- Once break-even ROAS is known, set tROAS ~20% above it and move in ≤15% steps, no more than every 2 weeks.

## Budget
Current ~$55/day. Scale rules:
- **Raise 20% only when** trailing 28-day ROAS is above target *and* tracking is green.
- **Never raise more than 20% in a 7-day period** — resets learning.
- **Do not scale on a week with fewer than 15 conversions** — insufficient signal.

## Audience signals
Once T-3 is fixed: Customer Match list of **paying customers only** (exclude the 71 free-kit claimers — they are the wrong seed). Panel consensus: one genuine customer list beats a dozen broad audiences.

## Watchlist
| Metric | Now | Watch for |
|---|---|---|
| Reported vs GA4 ROAS gap | 1.53x | Widening = more over-attribution |
| Shopping share of PMax spend | Unknown | Below ~60% = drifting to Display |
| Conversions/month | ~24 paid | Below 15 = can't optimise |
| CPC | ~$0.90 | Sudden drop = junk traffic |
