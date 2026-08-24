# Research SOPs

Reusable procedures. These are the *operating procedures* PART 3 asked for — converted from how experienced practitioners work, not summaries of their content.

## SOP-1 — Monthly account audit
1. Pull Shopify: monthly orders / gross / discounts / total_sales / AOV; sessions funnel; product mix; new vs returning.
2. Pull Google Ads: campaign performance, conversion actions, search terms (`clicks > 2`), daily spend for anomalies.
3. Pull GA4: channel group × sessions / ATC / checkouts / purchases / revenue.
4. Pull Meta: campaigns, dataset `last_fired_time`, EMQ.
5. **Triangulate revenue three ways** (platform / GA4 / Shopify). Divergence >20% is a tracking defect, not an attribution nuance.
6. Recompute blended MER and, once COGS exists, contribution margin.
7. Walk the decision hierarchy top-down. Stop at the first red layer.

## SOP-2 — Search term mining (Tier 1 customer language)
Monthly, `clicks > 2`, 90-day window. Sort three ways:
- **Zero-conversion spend** → negative keyword candidates (check for landing-page mismatch first — a term that should convert but doesn't is a page problem, not a keyword problem).
- **High ROAS, low volume** → feed title and ad copy language.
- **Competitor brand names** → exclude, and log as competitor intelligence.
Feed the vocabulary into `rare-plant-psychology.md`. **Customers' own words beat invented copy.**

## SOP-3 — Anomaly detection
Scan daily spend for: click count >2x the trailing median with CPC <60% of median (junk traffic signature — this is how Aug 19 was caught); spend days with zero conversions exceeding two consecutive; conversion value diverging from Shopify by >30% week-on-week.

## SOP-4 — Adding an expert to the panel
1. Find primary material — an actual walkthrough, case study or account teardown, not a summary.
2. Extract the *mechanism*: what problem, why it should work, under what conditions.
3. Assign an evidence tier. Reputation alone is Tier 4.
4. **Apply the scale filter:** what conversion volume does this assume? If >5x ours, mark structure as non-transferable and keep only the diagnostic.
5. Score into `strategy-database.md`. **No profile without primary material read.**

## SOP-5 — Before implementing any expert tactic
Ask, in order: What problem does this solve? Do we have that problem? What conversion volume does it assume? What breaks if we're wrong? How would we detect that? What's the revert path?
**If "do we have that problem" is no, stop.** This is what disqualified brand-Search separation and PMax margin segmentation for AgaPlantz.

## SOP-6 — Competitor intelligence (ethical bounds)
Public sources only: ad libraries, storefronts, pricing, reviews, policies. Never attempt access to private accounts or data. Our own search-term report is the highest-quality competitor signal we have — it shows who buyers actually compare us against.
