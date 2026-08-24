# The Expert Panel

**Purpose:** a standing reference of practitioners whose published work informs AgaPlantz decisions — and, more importantly, *where each one's advice stops applying to us.*

**Honest scoping note.** This panel is built from published/searchable material (articles, podcasts, community posts, agency documentation). This session had **no Apify access** and no YouTube transcript pipeline, so per-video teardown extraction described in PART 2 was not possible. Nothing here is invented: where I could not verify a claim about a practitioner's results, the row says so. Reputation is not evidence — see `00-operating-system/evidence-tiers.md`.

---

## The filter that governs this whole document

> **AgaPlantz runs ~24 paid orders/month on ~$800/month ad spend, on a store that is 4 months old.**

Almost every practitioner below built their frameworks on accounts 20–500x larger. Their advice is not wrong; it is **calibrated to a different conversion volume.** The single most common way for AgaPlantz to waste money is to implement a correct strategy at the wrong scale — segmenting campaigns, building testing frameworks, or splitting budgets that starve every branch of data.

**Rule: any strategy that divides our ~24 monthly conversions into more than one optimisation bucket is presumed harmful until proven otherwise.**

---

## Google Ads

### Kasim Aslam / John Moran — Solutions 8
- **Focus:** Google Ads for e-commerce and lead gen; large-account management.
- **Signature ideas (as published):** hybrid PMax + Search rather than PMax-only; treating PMax as needing active "steering" via feed, search themes and exclusions rather than set-and-forget; separating brand into its own Search campaign so PMax cannot claim it.
- **Verification status:** widely-referenced practitioners with a long public track record and detailed teardown content. **I did not independently verify specific client result claims in this session.** Treat frameworks as Tier 3–4 (expert walkthrough / opinion), not Tier 1.
- **Relevance to AgaPlantz — MIXED.**
  - ✅ **Steer-don't-set-and-forget** applies fully. Adopted.
  - ❌ **Brand-separation Search campaign does not apply yet.** Their advice assumes brand search is being cannibalised. Ours isn't — `aga plantz` drew 3 clicks in 90 days. Building a brand campaign now would spend money defending demand that doesn't exist. **Revisit when brand search exceeds ~100 impressions/month.**
  - ⚠️ **Hybrid PMax + Search** is right *eventually*, wrong *now* — splitting 24 conversions across two campaigns starves both.

### Store Growers (Dennis Moons)
- **Focus:** Google Shopping and PMax for small-to-mid e-commerce. Notably writes *for small accounts*, which almost no one else does.
- **Signature ideas:** explicit spend-banded structure — under $1k/mo: skip PMax, use Standard Shopping + Search; $1k–3k/mo: one PMax across the full catalogue; segment only above ~$10k/mo. Feed-only PMax as the starting configuration. Don't create more campaigns than conversion volume supports (30–50 conv/mo → one or two campaigns). Allow 4–6 weeks and 30–50 conversions before judging.
- **Relevance to AgaPlantz — HIGHEST OF ANY SOURCE ON THIS PAGE.** This is the only widely-published framework whose *stated scale band matches ours.* At ~$800/mo we sit at the boundary of "skip PMax entirely." We are not going to skip it — it is working at 3.2x reported — but his volume discipline is adopted wholesale.
- **Direct consequences adopted:** one PMax campaign, no segmentation, feed-first, 4–6 week evaluation windows, no more campaigns than conversions support.

### Jyll Saskin Gales
- **Focus:** ex-Google; teaches the mechanics of how Google's systems actually decide, rather than tactics.
- **Value to us:** mechanism-level explanation (how signals feed bidding, what the platform can and cannot see). Useful for **PART 7 reverse-engineering** — understanding *why* a tactic works, which is what lets us judge whether it transfers to our scale.
- **Relevance:** HIGH as an explanatory source, LOW as a tactical source.

### Others tracked, not yet profiled
Ben Heath (Google + Meta), Surfside PPC, Loves Data, Ed Leake. Listed in the original brief; **I have not verified their work in depth in this session** and will not summarise frameworks I have not read. Adding a profile requires actually reading primary material — see the discovery SOP in `00-operating-system/research-sops.md`.

---

## Meta Ads

### Andrew Foxwell — Foxwell Digital / Foxwell Founders
- **Focus:** Meta buying; runs a large private practitioner community, which makes his read on "what is actually working now" unusually current — community-sourced rather than single-account.
- **Signature ideas (2026 material):** creative is the primary lever, not targeting; consolidation over fragmentation post-Andromeda; how to test creative when the platform increasingly refuses to give clean per-ad reads.
- **Relevance to AgaPlantz — HIGH, DEFERRED.** Creative-first is exactly right for us. But every Meta framework presupposes a working pixel. Ours has **never fired a single event.** All Meta strategy is blocked behind that fix.

### Dara Denney
- **Focus:** DTC creative strategy and performance creative; reports having managed $100M+ in spend.
- **Signature ideas:** a two-campaign core structure — one creative-testing campaign + one Advantage+ campaign; test into proven formats (UGC, before/after, reviews, tutorials) rather than inventing from scratch; creative auditing as a repeatable process.
- **Relevance to AgaPlantz — CONCEPT YES, STRUCTURE NO.**
  - ✅ The **format library** (UGC / before-after / review / tutorial) transfers directly and maps beautifully onto rare plants — see `creative-library.md`.
  - ❌ The **two-campaign split does not.** A dedicated testing campaign needs enough conversions to read results. We will have ~0 at launch. AgaPlantz tests creative *inside* one campaign until volume justifies splitting.

### Common Thread Collective
- **Focus:** DTC growth tied to financial forecasting; known for growth accounting and for insisting that media decisions be made against contribution margin, not platform ROAS.
- **Relevance to AgaPlantz — THE MOST IMPORTANT IDEA ON THIS PAGE, AND WE CANNOT YET USE IT.** Their central discipline — decide on contribution margin, not reported ROAS — is exactly the discipline this account is missing. **We do not have COGS.** That gap is now the #1 data blocker in the audit.

### Others tracked, not yet profiled
Nick Shackelford, Ralph Burns / Tier 11, Jon Loomer, Ben Heath. Same standard as above: **no profile without primary material read.**

---

## Cross-panel synthesis: what actually survives the scale filter

| Idea | Consensus among panel? | Survives AgaPlantz filter? |
|---|---|---|
| Tracking integrity precedes all optimisation | Universal | ✅ **Yes — and we fail it badly** |
| Decide on contribution margin, not platform ROAS | Strong (CTC especially) | ✅ Yes — blocked on COGS |
| Creative is the main Meta lever | Universal | ✅ Yes — blocked on pixel |
| Feed quality is the main PMax lever | Strong | ✅ Yes |
| Consolidate; don't fragment low volume | Strong (Store Growers explicit) | ✅ **Yes — most load-bearing rule we have** |
| Separate brand into its own Search campaign | Strong | ❌ **No — we have no brand demand to protect** |
| Dedicated creative-testing campaign | Strong (Denney, Foxwell) | ❌ **No — not enough conversions to read a test** |
| Segment PMax by margin tier | Strong | ❌ **No — needs ~$10k/mo spend** |
| Advantage+ / broad targeting | Strong | ⏸️ Deferred until pixel fires |

**The pattern:** panel *diagnostics* transfer to AgaPlantz almost perfectly. Panel *structures* mostly do not, because structure is a function of conversion volume and ours is 20–500x smaller. Take their reasoning; leave their org charts.
