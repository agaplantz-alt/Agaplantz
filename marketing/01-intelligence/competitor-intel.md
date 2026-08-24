# Competitor Intelligence

**Method note:** AdWhispr (live Meta/TikTok ad library research) is connected but its monthly free-tier calls were exhausted before returning results. So this file is built from a **better** source: our own Google Ads search-term report. Terms where a buyer typed a competitor's name *and clicked our ad* are Tier 1 evidence of who we're actually compared against — stronger than a scrape.

Public sources only. No attempts at private accounts or data (PART 19).

## Confirmed comparison set

Canadian plant retailers buyers searched for, then clicked AgaPlantz (90 days):

| Competitor | Clicks | Our spend | Conversions |
|---|---|---|---|
| Planteia | 9 | $21.00 | 0 |
| Plantsome | 4 | $2.79 | 0 |
| Floral Acres | 3 | $4.23 | 0 |
| GardenWorks | 3 | $1.92 | 0 |
| "toronto tropical plants" (generic local) | 4 | $4.13 | 0 |

**Read:** ~$34 spent on competitor-brand traffic, **zero conversions.** Someone searching a competitor by name is far along in their decision; intercepting them costs money and, at our scale, has returned nothing. **Action: exclude these as negatives** (EXP-006).

**Counter-read worth keeping:** the fact these searches happen at all tells us the comparison set is *mainstream Canadian plant retailers*, not rare-plant specialists. That is a positioning signal — AgaPlantz's rare/TC catalogue is differentiated against them, and competing on generic terms like `plants` or `monstera` (both zero-converting for us) means fighting on their ground.

## Positioning implication

Our defensible territory is where those competitors are weak:
- **Tissue culture** — `tissue culture plants canada` is our highest-volume search term. Mainstream retailers don't serve this.
- **Named rare cultivars** — `variegated billietiae` (157x ROAS), `monstera deliciosa aurea` (90x), `monstera bulbasaur` (9.4x). Specific, high-intent, low-competition.
- **Canadian domestic sourcing** — buyers append "canada" constantly, signalling real anxiety about cross-border plant purchases.

Where we should **not** compete: generic head terms (`plants`, `monstera`, `alocasia plant` — all zero conversions for us), and competitor brand names.

## What is still unknown
- Competitor **ad creative and offers** — needs an ad-library pull (AdWhispr quota, or manual Meta Ad Library check).
- Competitor **live-arrival guarantees and shipping thresholds** — directly relevant to our checkout problem. A manual review of 4 competitor shipping policies would be high-value and costs nothing.
- Competitor **pricing** on overlapping cultivars.

**Recommended next step:** manually review the shipping/guarantee policies of Planteia, Plantsome, Floral Acres and GardenWorks. If they offer live-arrival guarantees and we don't, that is a direct, testable explanation for our checkout abandonment.
