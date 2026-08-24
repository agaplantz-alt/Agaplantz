# Data Access — what this system can and cannot see

Honest inventory as of 2026-08-24. Update when connectors change.

## Connected and working
| System | Identifier | Access |
|---|---|---|
| Shopify Admin | `agaplantz.com` / `sk11xm-0b.myshopify.com` | Read + write; ShopifyQL analytics |
| Google Ads | `877-370-0048` (AgaPlantz) | Read via Windsor.ai; write actions available |
| GA4 | `544946327` (Agaplantz) | Read via Windsor.ai |
| Meta Ads | 4 accounts; primary `1411593217321687` | Read + write via `metah` |
| Meta dataset/pixel | `4340434602872984` | Health/quality reads |
| Supermetrics | 150+ sources | Available, not yet used |
| Web research | WebSearch / WebFetch | Live |
| Canva, Gmail, Drive | — | Available for creative/reporting workflows |

## NOT available (stated plainly)
- **Apify — not connected.** The brief assumed Apify access for YouTube scraping and transcript mining. It is not in this session. Expert research was done via WebSearch/WebFetch instead, which reaches articles and podcast pages but **not video transcripts at scale.** This is the main gap between the brief and what was delivered.
- **AdWhispr competitor research** — connected but monthly free-tier calls exhausted before returning results. Competitor names in this system came from our own Google Ads search-term report instead (Planteia, Plantsome, Floral Acres, GardenWorks — Tier 1, better evidence than a scrape anyway).
- **Google Merchant Center** — no direct connector. Feed health is unaudited and is the largest unmeasured lever in PMax.
- **Email platform (Klaviyo etc.)** — not connected. Email shows 25 checkouts → 0 purchases in GA4 and cannot be diagnosed from here.
- **COGS / margin data** — exists nowhere in any connected system. **The single most important missing input.**

## Standing rule
When a question cannot be answered from the systems above, say so. Do not estimate campaign performance, competitor spend, or customer behaviour from general knowledge and present it as analysis.
