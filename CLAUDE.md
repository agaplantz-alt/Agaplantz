# AgaPlantz — working notes

Context for anyone (human or Claude) picking this up cold. Read the **Workflow rule**
first; it is the one thing that will bite you.

## The business

AgaPlantz Inc. — Canadian rare-aroid nursery, agaplantz.com (`sk11xm-0b.myshopify.com`).
Sells collector aroids: Philodendron, Alocasia, Monstera, Anthurium, plus Begonia.
Most of the catalogue is **tissue culture** — lab-propagated plantlets, sold either as
pre-order (next lab batch, cheaper) or ready-to-ship (already rooted and acclimated).
A small number of **mature specimens** are one-off plants.

Owner is non-technical and works mostly from a phone. Judge every change on a
390px screen, not just desktop.

## Workflow rule — read this before touching the theme

**The Admin API refuses writes to the live/MAIN theme.** So:

1. `themes(first: 15)` → find the current `MAIN`. **Do not trust a theme ID written
   down anywhere, including this file.** Publishing creates a *new* theme rather than
   promoting the draft, and Horizon version upgrades create another one. The ID has
   already changed three times.
2. `themeDuplicate` the current MAIN (payload field is `newTheme`, not `theme`).
3. Edit the duplicate, verify it, hand over the preview link:
   `https://agaplantz.com/?preview_theme_id=<id>`
4. The owner publishes from Shopify admin.

Duplicate **at the moment a change is requested**, not in advance. A draft made early
goes stale the moment they touch the theme editor — that already caused one lost-edit
scare (their hero CTA edit `"Shop ready to ship"` → `"Shop"` lived only on the
published theme while our work sat in an unrelated draft).

They edit in the theme editor freely. Always re-pull live before editing, and treat
their version as the base to merge onto.

As of 4 Oct 2026: MAIN was `AgaPlantz 2026 — subscription page` = `188662284367`, Horizon
**4.1.4** — the owner now publishes their own drafts too, so MAIN may be a theme they named
themselves rather than an "Updated copy of" one. It carried every one of our files unchanged
(`templates/index.json`, `sections/header-group.json`, `spotlight-plant.liquid`,
`stage-products.liquid`, `batch-discounts.liquid` all matched the repo md5 for md5), so the
ladder and the announcement slide are live. **Compare md5s against the repo before editing** —
that one query is the whole merge check. Verify, don't assume. Note the name: Shopify prefixes **"Updated copy of"**
automatically when the owner publishes a draft, so a theme called that is *our* work that
they published, not something they hand-wrote.

### Uploading a large template

`templates/index.json` is ~90 KB — too big to paste into a mutation. Use staged upload:

```
stagedUploadsCreate(resource: FILE, mimeType: "application/json", httpMethod: POST)
  → curl -F each returned parameter -F "file=@<path>" <url>     # expect HTTP 201
  → themeFilesUpsert(files: [{ body: { type: URL, value: <resourceUrl> } }])
```

`upsertedThemeFiles` comes back empty even on success — verify by re-reading the file.

### Verifying a preview

The preview **requires a cookie jar**, or you silently get the live theme:

```
curl -s -c cj -b cj -L "https://agaplantz.com/?preview_theme_id=<id>" -o page.html
```

Then grep for `Liquid error`, the section IDs, and whatever you changed.

## Homepage — current section order

`templates/index.json`, section IDs as they appear in `order`:

1. `hero_main` — full-bleed image, gradient overlay, CTA "Shop" → ready-to-ship
2. `marquee_trust` — scrolling trust strip, sage
3. `custom_liquid_KL8FyB` — batch countdown, sand band. A `custom-liquid` section, not a
   block: a terracotta eyebrow ("Pre-orders are open again"), headline "This batch
   closes in", four Lora digits, the repricing line, a moss CTA. **The eyebrow is a
   hand-written string** — it has no logic behind it. It has said "3 more days
   added to this batch" and now says "Pre-orders are open again", so re-read it whenever
   the deadline moves or it will state something that is no longer true. It hides itself
   once the timer expires. The deadline is a hardcoded ISO string carrying the Toronto offset
   (`assign deadline = '2026-10-31T23:59:59-04:00'`) — one of the six places the cut-off
   date lives, and the only one that also needs the *time*. Classes are `aga-batch__*`;
   when the timer hits zero the JS rewrites the headline, the line and the CTA in place
   and hides the digits **and the discount ladder**, so an expired batch never reads as a
   live one. The **discount ladder lives inside this same section** — see below.
4. `collections_genus` — Philodendron / Alocasia / Monstera / Anthurium / **Begonia**
   tiles. `max_collections` was `4` and silently drops the fifth handle — it is now 5,
   and `columns` went 4 → 5 so the row stays one line instead of 4 plus an orphan.
5. `tissue_culture` — explainer; intro on top, two cards side-by-side (also on mobile),
   then `tc_guarantee`, a full-width strip carrying the 30-Day Plant Guarantee. It sits
   *below* the two stage cards deliberately: the reassurance lands after the customer has
   picked a stage, and the explainer and both CTAs are kept rather than replaced.
5. `spotlight_plant` — **one plant, shown big**, sand band. A `spotlight-plant` section;
   see below. Sits between the genus tiles and the tissue-culture explainer.
6. `subscription_box` — the mystery-box call-out, **moss band**. A `subscription-callout`
   section; see below. Deliberately directly under the spotlight: a visitor who has just
   scrolled past two expensive named plants is the one still undecided.
7. `tissue_culture` — the explainer (numbering above is off by one from here down)
8. `products_popular` — **the only product row on the homepage**, cream band. A
   `stage-products` section on the automated `popular` collection, sorted BEST_SELLING.
9. `why_agaplantz` — 4 icon/text cells, 2×2 on mobile, sage
10. Loox `loox-dynamic-carousel` app block — added by the owner in the theme editor

**Disabled, still in `order` so they can come back:** `products_tc` (pre-order),
`products_sale` (on-sale), `products_rts` (ready-to-ship), `products_acclimated`
(mature-specimens). See **One featured row** below for why.

There is **no `newsletter` section on the homepage**: it duplicated the email signup
that Horizon's footer already renders on every page, so the homepage one was removed
and the footer default kept. Both were identical `email-signup` blocks posting to
`/contact`; neither was broken.

The owner replaced the native `reviews` wall here with the Loox carousel. That block
renders **nothing server-side** — an empty container filled by a ~74 KB script — so it
is invisible to Google and shifts layout as it loads. The native wall still runs on
product pages (`store_reviews`), where it renders in the HTML.

Bands alternate sage / default / sand so no two same-coloured sections touch.

## Design system

`config/settings_data.json`. Direction: **warm nursery / earthy**.

| Token | Value | Role |
| --- | --- | --- |
| `background` | `#FBF8F2` | warm cream page |
| `foreground` | `#2F2A22` | warm near-black |
| `color1` | `#56503F` | secondary text |
| `color3` | `#DED3C2` | clay borders |
| `color4` | `#F2EBDE` | sand band |
| `color7` | `#E8EDE1` | sage band |
| — | `#5C6B4C` | moss — primary buttons, icons |
| — | `#B4693C` | terracotta — sale badges |

Lora 400 headings/accent, Work Sans body/subheading. H1 42 / H2 30 / H3 22 / body 15.
Corners deliberately sharp — 2px buttons, inputs, badges, product images; 4px cards.
Sharp corners + restrained type + 56–96px section padding is what reads as luxury;
the pill buttons and 12px radii it replaced read casual-DTC.

All five app embed blocks (Inbox, Loox, Forms, Koala, Google/YouTube) must be
preserved on every settings write. Conversion tracking was verified identical
between live and draft across 12 signals.

## Catalogue architecture

**The central fact: plant stage is a variant option (`Plant Stage`), not a product.**
Shopify collections hold products, not variants, so stage can never be cleanly split by
collection. This is why the homepage originally "didn't differentiate the stage".

**Merge rule, set by the owner:** one listing per plant, stages as variants.
*Black Velvet Pink* pre-order TC and acclimated belong on one page — but **variegated
is a different plant from green** and keeps its own listing. They corrected an early
mistake here (Tortum green $18 vs Tortum Variegated $130), so treat any variegation
marker as disqualifying for a merge. Applying this strictly cut 10 candidate pairs to
2 real duplicates.

**Exception, settled 4 Sep: mature specimens are their own listings.** The merge rule
could not survive contact with the homepage — a card shows one photo and one price per
product, so a merged listing could not show a plantlet in the pre-order row and a mature
plant in the Mature specimens row, and Mature specimens was quoting tissue-culture prices
(Gloriosum Variegated at $84 rather than $350). The six merged mature variants were moved
to their own products; see **Mature specimen listings** below.

### Collections

Counts as of 1 Oct 2026 — they move a lot, re-read rather than trusting these:

| Handle | Title | Count |
| --- | --- | --- |
| `philodendron` / `alocasia` / `monstera` / `anthurium-1` | genus, rule `TITLE CONTAINS <genus>` | 186 / 236 / 48 / 72 |
| `begonia` | BEGONIA | 29 — **a fifth genus since 1 Oct**, see below |
| `pre-order` | TISSUE CULTURE — PRE-ORDER | 552 |
| `ready-to-ship-tissue-culture` | TISSUE CULTURE — READY TO SHIP | 12 |
| `mature-specimens` | MATURE SPECIMENS | 4 |
| `acclimated-plants` | ACCLIMATED PLANTS | 13 |
| `on-sale` | ON SALE (rule: `IS_PRICE_REDUCED IS_SET`) | 31 |
| `popular` | POPULAR — automated, `sortOrder: BEST_SELLING`, drives the homepage row | ~all in stock |
| `featured` | FEATURED — manual. **Built 1 Oct, rejected the same day, now unused.** Safe to delete | 8 |

**`ready-to-ship` no longer exists.** The owner deleted it some time before 1 Oct, and
`collectionByHandle(handle: "ready-to-ship")` now returns `null`. It had been wired into
two places and both broke silently: the homepage `products_rts` row rendered a heading
with **zero cards**, and the first tile of `shop_by_stage` on `/collections` pointed at a
dead handle. Both are fixed. **A deleted collection does not announce itself** — if a row
or a tile goes empty, check the collection still exists before debugging the theme.

`/collections` is a curated three-section page (`templates/list-collections.json`), in
this order, set by the owner on 1 Oct:

1. `shop_by_plant` — the five genus tiles, Begonia included (cream band, `columns: 5`)
2. `shop_by_stage` — RTS tissue culture, acclimated, mature, pre-order (sand band).
   The `ready-to-ship` tile was dropped on 1 Oct: that collection no longer exists.
3. `shop_by_sale` — **a product row, not tiles.** It is a `stage-products` section (the
   same one the homepage rows use) pointed at `on-sale` with `sale_only: true` and a
   blank `stage_match`, so each card shows the discounted variant's own photo and price.
   A single ON SALE tile would have been one lonely square; a row of eight real plants
   is worth the space.

Stock `main-collection-list` is deliberately **not** in `order` — it mixes genus and
stage alphabetically and drags in the draft Begonias and the orphan `home-page`
collection. Publishing re-seeds it; see the Horizon gotchas.

`ACCLIMATED PLANTS` was deleted; `/collections/acclimated-plants` 301s to
`/collections/ready-to-ship`.

`catalog-backup/products-full.jsonl` is a full pre-deletion export of all 309 products
(descriptions, SEO, media, option value IDs, variants with SKU/price/compare-at/
inventory). Taken before any permanent delete — do the same before the next one.

## Begonia — the fifth genus (1 Oct 2026)

The owner added Begonia as a genus alongside Philodendron, Alocasia, Monstera and
Anthurium. It is wired in three places: the homepage `collections_genus` row, the
`shop_by_plant` row on `/collections`, and a `BEGONIA` item in the main menu's **Plants
collections** submenu (alphabetical, after ANTHURIUM; `gid://shopify/Collection/317272391759`).

The products are **real and live** — 29 in the collection, all ACTIVE, 100 units each,
collection rule `TITLE CONTAINS Begonia` + `VARIANT_INVENTORY > 0` like the other genus.
The old note that they were 10 DRAFT products is out of date.

**But there is not a single Begonia photograph in the store.** Checked on 1 Oct:

- all 29 products have `mediaCount: 0` — not one image between them
- the `begonia` collection's own `image` is `null`
- `files(query: "begonia")` returns **nothing**, so there is nothing to attach either

So the genus tile falls back to Shopify's grey placeholder, and
`/collections/begonia` renders 28 product cards with zero real images and 40
placeholder references. Adding one collection image fixes the *tile* in both rows
immediately — that is the cheapest single win and it needs no code. The collection page
stays a wall of placeholders until the products themselves get photos.

**Also publication-starved:** the `begonia` collection is published to **2** channels
(Online Store, TikTok) where `philodendron` is on **7**. So Begonia is invisible to the
Google, Meta and Microsoft feeds. `publishablePublish` fixes it; nobody has asked yet.

## The homepage: popular, and one plant shown big (1 Oct 2026)

Two passes on the same day. **Pass one** replaced four product rows with one hand-picked
`featured` row. The owner rejected it — *"I don't like the feature plan. Maybe we should
do the popular plants, and line them by how much they sold… we're not gonna show how
much they sold, but we can use that number."* They also asked for one famous plant shown
**in a big chunk**, an idea borrowed from another nursery's homepage, and said the genus
tiles are fine as they are.

### Why four rows had to go (the measurement, worth keeping)

Four rows, 20 cards rendered, and only **one** plant literally repeated. The sameness was
not duplication: the rows were **four filters over one pool**, so 15 of the 20 cards were
`-pre-order` handles with the same plantlet-on-white photo. Ready to ship rendered
**zero** cards (its collection had been deleted) and Mature specimens was down to 4.

### `products_popular`

A `stage-products` row on **`popular`** (`gid://shopify/Collection/491313004623`),
automated, `sortOrder: BEST_SELLING`, published to Online Store + Shop. Rules:
`VARIANT_INVENTORY > 0` + `TYPE != Service` + `TITLE NOT_CONTAINS "Starter Kit"` — the
last two matter because the free Starter Kit (79 units) and the Acclimation Service
add-on (37) outsell every plant and would otherwise lead the row.

**BEST_SELLING was chosen over a manually ordered list so it never goes stale** — and
`stage-products.liquid` does `paginate coll.products` / `for product in coll.products`,
so it inherits the collection's sort. **No sales numbers are shown anywhere**, as asked;
the ranking is the only thing that surfaces.

Sanity check against ShopifyQL (`FROM sales SHOW net_items_sold GROUP BY product_title
SINCE -90d`): the rendered order was Bulbasaur, Devil Monster, White Monster, Cuprea Red
Secret, Bambino Pink, Creme Brulee, Billietiae, Nobilis Pink K against a 90-day ranking of
Bulbasaur 45, White Monster 24, Spiritus Sancti 22, Devil Monster 20, Creme Brulee 18,
Cuprea 16, Bambino Pink 16, Billietiae 13. Near-identical; Shopify's window is its own.
Spiritus Sancti is absent only because it is out of stock, which is correct.

### `sections/spotlight-plant.liquid` — plants shown big, one per slide

Big photo one side, name / price / one line / moss CTA the other; stacks with the photo
first on mobile. **Each slide is a block**, so the owner adds, removes and reorders
plants in the theme editor. Block settings: `product`, `eyebrow`, `heading` (blank = the
plant's own name), `text`, `cta_label`. Section settings: `image_position`, `autoplay`
(on, 6s), background and paddings. `max_blocks: 6`.

The track is CSS scroll-snap with arrows and dots; autoplay pauses on hover and on
focus, and does nothing under `prefers-reduced-motion`. With a single block the controls
are not rendered at all, so it degrades to the plain feature it started as.

**It reads a variant, not the product**, for the same reason `stage-products` does:
`product.price` is the cheapest stage and would under-quote what is in stock. It takes
the first available variant, **preferring one that is on sale**, shows the compare-at
struck through with a terracotta `Save X%` badge, names the stage, and the CTA carries
`?variant=` so the product page opens on it. If nothing is available it prints "Sold out
for this batch" instead of a button.

Two slides as of 1 Oct:

1. **Monstera Devil Monster Premium Variegated** — 20 sold in 90 days and the **highest
   revenue plant in the shop** ($4,013), 197 units in stock. The owner raised Premium
   from $204 to **$240** against the same $306 compare-at, so the badge moved 33% → 22%
   on its own: **the section reads live variant data and never needs touching after a
   price change.**
2. **Alocasia Cuprea Red Secret Variegated Super Pink** — $162, 93 in stock, **no
   compare-at**, so that slide renders with no strikethrough and no badge. Worth knowing
   the sale treatment is conditional, not assumed.

Monstera Bulbasaur outsells both on units (45) but had **one unit left**, so a spotlight
would have sold it out immediately — check stock before spotlighting a bestseller.

## Monthly Mystery Plant Box (4 Oct 2026)

The owner built the box themselves — product `monthly-mystery-plant-box`
(`gid://shopify/Product/15404945670223`), template suffix `subscription`, one `Tier` option
with `$50 / $100 / $150 / $200 Box`, one selling plan ("Deliver every month", no discount),
and the Shopify Subscriptions app block on `templates/product.subscription.json`. They asked
for a call-out on the homepage *underneath* the spotlight slider: *"not sure what to buy? Get
a plant subscription monthly."*

`sections/subscription-callout.liquid` — photo one side, pitch and CTA the other, stacking
with the photo first on mobile. All copy is a section setting, so the owner edits it in the
theme editor. **The tier chips are read from the product's own variants**, each linking with
`?variant=`, so renaming a tier or changing a price in admin moves the homepage with no theme
edit; an unavailable tier simply is not rendered. Settings: `product`, `eyebrow`, `heading`
(blank = the product's name), `text`, `show_tiers`, `cta_label`, `note`, `image_position`, and
four colours — `background_color` (moss `#5C6B4C`), `text_color`, `button_background`,
`button_text`, defaulting to a **dark moss band with an inverted cream button**. That band
colour is doing real work: it is the one dark section between the hero and the footer, so it
reads as a feature rather than another row, and it keeps the sand spotlight above and the sage
explainer below from touching.

### The picture side is five cut-outs, not one photo

The owner rejected the product's own square photo (*"not giving premium energy"*) and sent
five individual plant shots on white. They were cut out with `rembg` (`isnet-general-use`,
alpha matting on — the clear nursery cups kept their translucency and the gaps between roots
and tweezers survived) and uploaded to **Files** as `aga-box-*.png`, trimmed to 1200px:

| Slot | File | What it is |
| --- | --- | --- |
| `plant_1` top left | `aga-box-plantlet-green.png` | green plantlet in tweezers |
| `plant_2` top middle | `aga-box-plantlet-pink.png` | pink variegated plantlet in tweezers |
| `plant_3` top right | `aga-box-monstera-variegated.png` | variegated Monstera in tweezers |
| `plant_4` bottom left | `aga-box-alocasia-dark-cup.png` | rooted Alocasia in a clear cup |
| `plant_5` bottom right | `aga-box-alocasia-pink-cup.png` | rooted pink Alocasia in a clear cup |

The section arranges them **three over two** in a square "stage": lab plantlets on top,
rooted plants on the floor — the story of what a box contains. Each slot is an
`image_picker`, so the owner can swap a photo; leave all five empty and it falls back to the
product's featured image. **The tweezer ends fade out** with a `mask-image` gradient per
slot, because the originals are hard-cropped where the tweezers leave the frame and a
floating rectangle edge looked wrong. The arrangement is percentages of the square, so it
scales; on a phone the stage caps at 420px wide. Each plant floats on a 6.5–9s CSS loop
(plantlets ±10px with 0.8° of rotation, rooted plants ±4px with none), all under
`prefers-reduced-motion`. Two earlier compositions were rejected by eye before this one: a
free scatter read as clutter, with two tweezers crossing. **"Organized" was the brief.**

**Scroll-linked motion (4 Oct).** The owner asked for the thing premium sites do where
*"when you're scrolling down, all the subjects are moving pretty quickly … zoom in and circle
around"* — on this band only. A 30-line script in the section writes two numbers to the
stage on every frame: `--q`, where the stage is in the viewport (`1` entering at the
bottom, `0` centred, `-1` leaving at the top) and `--aq`, its magnitude. The CSS does the
choreography from those: each plant has a spread vector (`--sx/--sy`, by `--aq`, so they
sit apart and at 70% size while off-centre and converge to the layout as it centres), a
drift vector (`--px/--py`, by `--q`, different per row so the rows separate in depth — the
top row travels faster), and a turn (`--r`, by `--q`, so they rotate one way coming in and
the other going out). `--k` scales the amplitudes to 0.6 on phones. The scroll transform
sits on the wrapper `<span>` and the slow float on the `<img>`, so the two never fight.
`.agmb` is `overflow: hidden` because the spread pushes plants past the stage. Everything
is transform-only and rAF-throttled; `prefers-reduced-motion` turns both layers off.

Verified by scrolling a local render at 390px and reading `--q` back at four positions.
**The desktop harness cannot scroll** — with Horizon's scripts blocked the body stays
`overflow: hidden` at 100dvh — so desktop was checked by setting `--q` by hand; the maths
is the same. Nothing about this is Horizon-specific; it survives upgrades as long as the
section file does.

**No shadows, no glow.** The first version had a CSS `drop-shadow` on each cut-out, a floor
ellipse under the cups and a radial lift behind the stage; the owner read all three as a
halo (*"there is shadow I don't like behind them"*) and they were removed. The PNGs
themselves are clean — the alpha channel was checked at 6× gain — so if a halo ever
reappears it is CSS, not the files. Keep the plants flat on the moss.

Slot order is positional — a tall rooted plant dropped into slot 1 gets a tweezer-fade mask
it does not need. Keep plantlets in 1–3 and rooted plants in 4–5.

Source photos are not in the repo; the cut-outs live only in Files. If they ever need
redoing, `rembg` is in pip and the model is ~180 MB.

**Inventory is not tracked on this product** (`inventoryItem.tracked: false`), so all four
variants showing `inventoryQuantity: 0` is harmless — they stay buyable. Do not "fix" it by
setting stock.

Two things to re-check if the box changes: the small print says *"Manage or cancel it any time
from your account"*, which holds because the shop runs **new customer accounts** and the
Subscriptions app gives subscribers a portal — if customer accounts are ever switched off, that
line stops being true. And the product is published to **5** channels (Online Store, Shop,
TikTok, Meta AI, Microsoft Copilot) where the plants are on 7; nobody has asked about Google or
Meta feeds for it.

## Batch discount ladder (2 Oct 2026)

The owner's scheme: the discount falls as the batch fills, so ordering early is worth
money.

| Dates | Discount |
| --- | --- |
| Oct 1–5 | 20% off orders $100+ |
| Oct 6–15 | 15% off orders $100+ |
| Oct 16–20 | 10% off orders $100+ |
| Oct 21–31 | Regular, full price |

**It lives inside `custom_liquid_KL8FyB`, the countdown section** — four compact cards
between the digits and the "repriced to supply and demand" line, with the current one
filled moss and carrying a terracotta **Now** pill. Four across on desktop, 2×2 under
560px.

It was first built as its own section, `sections/batch-discounts.liquid`, with a second
countdown of its own ticking down to the next discount drop. The owner wanted the
compact card row but **not** a second timer: *"keep the original batch timeline, don't
change it by a discount change, just keep that same. And everything just add that
discounts down there."* So the one timer still counts to the batch close
(`2026-10-31T23:59:59-04:00`) and the ladder sits under it. **Do not retarget that timer
at a tier boundary.** `sections/batch-discounts.liquid` is still in the theme, unused —
it is a working standalone section if a ladder is ever wanted on another page.

**Which tier is "now" is computed in Liquid, not JavaScript**, so it renders server-side —
no flash of the wrong tier, and Google sees it:

```liquid
{% assign batch_start = '2026-10-01T00:00:00-04:00' %}
assign day_now = 'now' | date: '%s' | minus: start_s | divided_by: 86400 | floor | plus: 1
```

**`batch_start` must carry the Toronto offset.** Without it the date parses as UTC, the
day boundary moves four hours, and between 8pm and midnight Toronto the card would claim
a tier checkout does not honour. Switch to `-05:00` after 1 November, same as `deadline`.

The tier dates and percentages are **hand-written strings in the custom Liquid**, like
everything else in this section. When the batch moves, they move with the deadline and
the `batch_start` — add them to the cut-off checklist.

**Day 1 = 1 Oct 2026 is an inference, not something the owner stated.** It fits:
pre-orders resumed 1 Oct, the ladder is 30 days, the cut-off is 31 Oct.

### The discounts themselves did not exist

Checked at build time: **every automatic discount in the shop is EXPIRED.** The only
ACTIVE ones are Loox review codes and `WELCOME10`, all code-based. So the ladder as
published advertises money off that checkout would not give.

This is the same class of trap as the "An automatic discount does not change the price on
the storefront" note under **Running a sale**, but worse — there the price simply did not
move; here the shop would promise a discount and deliver none. **Never publish this
without four matching automatic discounts in place.** They need
`discountAutomaticBasicCreate`, each with its own `startsAt`/`endsAt` window and a
`DiscountMinimumSubtotal` of $100, and `combinesWith` product discounts **false** so a
tier cannot stack on top of the existing compare-at sales.

## Horizon gotchas, learned the hard way

- **Product cards render nothing unless the gallery block is in `block_order`.** Type
  `_product-card-gallery`, name `t:names.product_card_media`, **not** `static: true`,
  and listed first. A declared-but-unordered block is silently ignored — this is why
  three product rows showed title+price with no photo. The Sale badge also lives
  inside this block.
- **`.section` does not consume `--padding-block-start` / `--padding-block-end`.** Setting
  them inline on a custom section's wrapper — the pattern every section here uses — computes
  to `padding: 0` at every width; what looks like section padding on `spotlight-plant` and
  `stage-products` is just their tall content. On a light band nobody notices; on a dark one
  the content sits flush against the neighbouring section and reads as a bug.
  `subscription-callout.liquid` therefore applies the padding itself:
  `padding-block-start: var(--padding-block-start, 56px)`. Measure the computed padding
  rather than trusting the setting.
- **The type scale is fixed rem with no `clamp()`** — `--font-size--h1: 2.625rem` on a
  phone and a desktop alike. Responsive type therefore needs CSS. The hero accepts
  `@theme` blocks, so a `custom-liquid` block carrying a `<style>` works: override the
  inline `--font-size` with `!important`, scope with `#Hero-{{ section.id }}` plus
  `[class*="__hero_heading"]` (the block-key suffix is stable, the hash prefix is not),
  and hide the block's own wrapper with `div:has(> style) { display: none }` so it adds
  no flex gap.
- **Group blocks give responsive grids**: `content_direction: row` +
  `vertical_on_mobile: false` stays horizontal on phones. Nest two such pairs inside an
  outer row group with `vertical_on_mobile: true` → 4-across desktop, 2×2 mobile.
- **Check enums against the schema before writing.** `card_hover_effect` is
  `subtle-zoom` (not `zoom`); `type_line_height_paragraph` is `body-normal` (not
  `normal`); button `width` is only `fit-content` or `custom` (no `fill`); text block
  `width` is `fit-content` or `100%`.
- **`range` settings enforce `step`.** Off-step values → `FILE_VALIDATION_ERROR`. The
  AI footer blocks are step-5 and step-2.
- **Shopify never upscales images.** Asking for `width=3840` from a 2096px source
  returns 2096px and the browser stretches it — that was the blurry hero. Source must
  be at least as wide as the largest srcset entry (3840).
- **Publishing a theme re-seeds default sections into JSON templates — not just a
  version upgrade.** It happened again on 29 Sep when the owner simply published a
  draft: `main-collection-list` reappeared as `collection_list_Wfgh3m`, **first** in
  `templates/list-collections.json`'s `order`, listing every collection alphabetically —
  which quietly put `TISSUE CULTURE — PRE-ORDER` back on `/collections` a few hours
  after it had been deliberately removed, along with the draft Begonias and the orphan
  `IN STOCK ACCLIMATED PLANT`. The curated `shop_by_plant` / `shop_by_stage` sections
  survived untouched underneath, settings intact. **Re-check `list-collections.json`
  after every publish, not just after upgrades.** The original case: the 4.1.4 upgrade
  put the same stock `main-collection-list` section back at the top of
  `templates/list-collections.json`, above the curated `shop_by_plant` /
  `shop_by_stage` sections, which survived untouched underneath. It renders every
  collection alphabetically — including `home-page` and image-less ones like Begonia,
  which fall back to Shopify's t-shirt placeholder. `templates/index.json` was not
  touched. **After every version upgrade, re-check each customised template for
  re-seeded default sections**, not just the homepage.
- Raw `collectionCreate` does **not** publish; `resourcePublications` comes back empty.
  Follow with `publishablePublish` to Online Store + Shop.
- `bulkOperationRunMutation` is blocked; batched aliased mutations work fine.
  `collectionDelete` and `productDeleteMedia` were blocked at one point and succeeded
  on a later retry — worth retrying before reporting a block.
- `productVariantsBulkReorder` uses `position`, not `newPosition`.

## Homepage reviews section

`sections.reviews` renders customer reviews natively in Liquid rather than through
Loox's JavaScript widget. Loox writes per-product metafields and `loox.review_feed`
is type **json**, so `product.metafields.loox.review_feed.value.reviews` is a real
array in Liquid — no JSON parsing needed, and the section renders server-side.

The block loops an explicit handle list (`all_products` is capped at **20 distinct
handles per page**, so the list must stay under that), sums `loox.num_reviews` and
`loox.avg_rating` for a true weighted average, then fills cards with 5-star reviews
that carry a photo and more than 25 characters of text.

Selection is **round-robin**: each pass takes at most one review per plant, so the
strongest photo from every plant lands before any plant gets a second card.
Spiritus Sancti alone has eight qualifying reviews and would otherwise swamp the
row. Card order follows the handle list, so reordering handles reorders the wall —
that is how the labelled-bag photo is held at position 2.

Tunables at the top of the block: `max_cards` (11), `per_product` (4, a ceiling that
rarely binds now), `min_rating` (4 — admits one genuine 4-star review whose photo is
among the best and whose text is positive). Asking for more cards than the pool
supports simply renders fewer; it never pads or repeats.

**Judge the photo, not just the rating.** Several 5-star reviews have pictures shot
through a fogged prop-box lid or into packing wool, where the plant is invisible.
Those are in `skip_ids`. What sells here is a plant you can actually see, a big
well-rooted one, or the sealed bag with the lab label on it — that last one is proof
the tissue culture is properly sourced and the owner asked for it specifically.

The aggregate is computed live, so it never goes stale, and it counts the low
ratings too (Gloriosum Variegated 1.0, Goeldii Mint 3.0, Tortum 3.5) — it reads
4.7, not 5.0. Do not hardcode it and do not exclude the low ones from the maths;
only the *featured cards* are filtered to 5-star.

**When new products get reviews, add their handles to the list**, or they are left
out of both the average and the cards.

A `skip_ids` list inside the block drops individual reviews from the *featured cards*
only — the average still counts them. Currently it skips one review whose text opens
"came slightly bent".

**Tissue-culture plantlets are wanted here** — that is what customers actually
receive, and proof one arrived healthy answers the objection that stops a first
order. What the owner rejected twice is not the subject but the *shot*: photos taken
through a fogged prop-box lid, where condensation hides the plant. A plantlet in a
cup or tray in daylight is exactly right; a murky one behind plastic is not. When
skipping one, check the next review in that product's feed — the replacement is
often another photo of the same kind.

## Reviews on product pages

Every plant page carries the same reviews wall, so a product with no reviews of its
own is not left with an empty page. `templates/product.json` and
`templates/product.tissue-culture.json` each get a `store_reviews` section, inserted
after the two Loox app-block sections.

**There are two product templates.** `product.tissue-culture.json` serves most of the
catalogue. Adding a section to `templates/product.json` alone reaches only a handful
of plants — check both, and check whether a third has appeared, with
`files(filenames: ["templates/*"])`.

The section reuses the homepage block with three changes: 6 cards instead of 11, the
heading names the shop ("What collectors say about AgaPlantz"), and the loop skips
`product.handle` so a plant's own reviews are not repeated below Loox's widget.

Both Loox app blocks are set to `reviews_to_display: product_reviews_only`, which is
why they render nothing on an unreviewed plant. That setting is a dropdown on the
block in the theme editor; switching it is the native alternative to this section, but
its enum values are not readable from the theme files, so it was not changed by API.

## Pre-orders: paused 29 Sep, resumed 1 Oct 2026

Pre-orders were switched off for two days and are **back on**, with a **31 Oct 2026**
cut-off. Everything the pause touched has been reversed; this section is kept because
the pause will happen again between batches and the list is the recipe.

**How the pause was done, and how to redo it.** Every item is a `disabled: true` flag, a
blanked setting or a list entry — nothing was deleted, and every id stayed in its
`order` / `block_order` list:

| File / place | What to switch off | Back on |
| --- | --- | --- |
| `templates/index.json` | `custom_liquid_KL8FyB` — the batch countdown | drop `disabled`, set the new deadline, re-read the eyebrow |
| `templates/index.json` | `products_tc` — the "Tissue culture pre-orders" row | drop `disabled` |
| `templates/index.json` | `tissue_culture` → `tc_cards` → `tc_pre` — the Pre-order card | drop `disabled` |
| `sections/header-group.json` | `announcement_jeGMHt` (cut-off slide), `announcement_pricing` (batch pricing) | drop `disabled`, set the date first |
| `templates/list-collections.json` | the `pre-order` entry in `shop_by_stage.collection_list` | append it back |
| `templates/product.tissue-culture.json` | `ai_gen_block_c6aca6a_HjQ7Ph`'s four pre-order strings | restore them with the new date |
| main menu (live data) | the `TISSUE CULTURE — PRE-ORDER` item | re-add with `resourceId: gid://shopify/Collection/314417578063` |

The line the owner drew, in their words: *"we are just hiding the main main parts, we are
not completely cutting the pre-orders off — people that have ordered, if they need our
information they can go look it up. Right now we are not selling it, so we just want to
remove it from the place where we sell."* So: **selling surfaces go, information surfaces
stay.** `/pages/pre-order` stayed published and stayed linked from the main menu and the
footer throughout. Do not unpublish that page or drop those two links when pausing.

### The product-page card cannot simply be hidden

`blocks/ai_gen_block_c6aca6a.liquid` renders three cards — acclimation dome, pre-order,
shipping — and the middle `<article>` has **no `{% if %}` guard**. Blanking its settings
leaves an empty white card with an empty green date chip, and disabling the whole block
would take the free-kit and acclimation-guide links with it. So during the pause its four
strings were rewritten in place ("Pre-orders are paused" / "PAUSED" / …) rather than
hidden, and restored on resume. If it should ever vanish outright, the block file needs
one `{% if block.settings.preorder_title != blank %}` around that `<article>` and its grid
changed from `repeat(3,…)` to `repeat(auto-fit, minmax(240px,1fr))`.

### What a pause does *not* do

**A pre-order stays buyable.** Pausing only changes what the storefront *says*. Every
plant keeps its in-stock, selectable `Tissue Culture (Pre-Order)` variant, and the
`pre-order` collection keeps ~310 products at `/collections/pre-order` — unlinked during
the pause, but reachable and indexed. Nothing advertises pre-orders, nothing blocks a
checkout. Actually closing that gap means zeroing those variants' inventory (a
~300-product data change — take a `catalog-backup/` export first) or unpublishing the
collection. The owner has not asked for either, and "we are just hiding the main main
parts" reads as deliberately not going that far.

Also never touched: ~300 product descriptions open with "Available as a tissue-culture
pre-order plantlet or as a rooted, acclimated plant ready to ship" (standing rule: no
description rewrites without approval), and the shipping line mentions the *Arrives
Before Pre-Order* checkout option, which mixed orders still use.

**The menu is the one thing that cannot go on a draft.** `menuUpdate` writes to the live
store immediately, and it replaces the whole menu — read every item's `id`, `type` and
`resourceId` first and send them all back, or items silently change type or disappear.
Adding an item back is the same call with one entry that has no `id`.

Worth knowing: the homepage product rows were checked variant by variant during the
pause and **none surfaced a pre-order variant**. `on-sale` and `ready-to-ship` are both
scoped by `VARIANT_INVENTORY > 0` per variant, and `stage-products.liquid` picks the
row's own variant, so the sale row links Ready-to-Ship and Acclimated variants even on
products whose *handle* still ends `-pre-order`. Those handles are legacy names;
customers never see them and renaming them would break links and SEO.

## The batch cut-off date lives in six places

When the pre-order cut-off changes, all of these need updating — they are separate
hand-entered strings, not one setting. The current batch closes **31 Oct 2026, 23:59
Toronto**. The owner gave the date only, not a time; end of day was assumed, unlike the
28 Sep batch where they said 11:30 pm explicitly. 31 Oct is still **EDT (`-04:00`)** —
Toronto flips to EST at 02:00 on 1 Nov, one day later.

| File | Field | Now says |
| --- | --- | --- |
| `sections/header-group.json` | `announcement_jeGMHt.text` | `Tissue Culture Pre-Orders Close October 31 • …` |
| `templates/index.json` | `custom_liquid_KL8FyB` → `assign deadline` | `2026-10-31T23:59:59-04:00` |
| `templates/page.pre-order.json` | `ai_gen_block_41bf156_tpPC39.cutoff_date` | `31 OCT 2026` (`date_label` back to `Cut-off Date:`) |
| `templates/product.tissue-culture.json` | `ai_gen_block_c6aca6a_HjQ7Ph.preorder_date` | `31 OCTOBER` |
| `templates/product.tissue-culture.json` | `ai_gen_block_675aea4_RGqfCa.preorder_text` | `Order by [31 OCTOBER]…` (hidden block) |
| `templates/product.tissue-culture.json` | `ai_gen_block_44763e7_iKDBHj.preorder_text` | `Order by [31 OCTOBER]…` (hidden block) |

Two of the six are visible: the Pre Order Details page card and the product-page card.
The other four sit on disabled blocks and are changed anyway, because the owner reads
them in the theme editor and a stale date there looks like a live one.

**Do the countdown first.** The other five are static strings that go stale quietly; the
countdown flips itself to "This batch has closed" the second the deadline passes, so a
missed date change is visible on the homepage within a minute. Its offset is `-04:00`
through early November and `-05:00` after — the shop is `America/Toronto`, so always
convert rather than writing a bare local time.

The last two sit on `disabled: true` blocks, so customers do not see them — but they
are kept in sync so re-enabling one never publishes a stale date. One of them shipped
with the literal placeholder `[cutoff date]` still in it.

`templates/product.json` carries no date (its pre-order block just links to the Pre
Order page), and no date appears in product descriptions, collection descriptions or
Shopify page bodies — checked. Searching the storefront HTML for `August` also matches
Loox **review dates**, which are not ours to change.

## Batch pricing notice

Prices are locked at checkout until dispatch, and re-set at the start of each batch.
The message lives in three places, all native `text` blocks (no custom Liquid), so the
owner can edit them in the theme editor:

| File | Block | What it says |
| --- | --- | --- |
| `templates/product.json` | `main` → `product-details` → `text_price_lock` | short price-lock note, sage, below the description |
| `templates/product.tissue-culture.json` | same path | identical block |
| `templates/page.pre-order.json` | `17824073197e77fd90` → `text_pricing_policy` | "How our pricing works", three points, sand card |
| `sections/header-group.json` | `announcement_pricing` | headline slide, links to `/pages/pre-order` |

The Horizon `text` block takes `type_preset: "custom"` plus `font_size`, `background`,
`background_color`, `corner_radius` and the four paddings — enough to build a tinted
callout without a `custom-liquid` block. Its `text` setting is a **richtext** field, so
only `<p> <strong> <em> <ul> <li> <h1>–<h6> <a> <br>` survive; no `<div>`, no inline
`style`.

**Do not write "prices are much cheaper" site-wide.** Measured like-for-like against
`catalog-backup/products-full.jsonl` (588 variants matched on handle + variant name):
**188 cheaper** (median −24%, 117 of them by ≥20%), **344 unchanged**, **56 higher** —
some steeply (Gigas TC 30-pack $95→$414, Anthurium Crystallinum × Dorayaki +156%,
Black Velvet +144%). Collectors track individual plants, so the copy says "nearly 200
plants now cheaper", which is true and checkable. Re-measure before changing that
number; the bulk query is
`{ products { edges { node { id handle title variants { edges { node { id title price compareAtPrice } } } } } } }`
(both `node` levels need `id` or the bulk operation is rejected).

## Announcement bar

`sections/header-group.json` → `header_announcements_ELa3gw` is the live bar; a second
section `header_announcements_9jGBFp` is **disabled** and contradicts it ("Free delivery
over $120" vs the live "Free shipping over $180"). Slides are hand-written strings with
no expiry, so they go stale silently — `announcement_JRWntd`
("Acclimated plants — 20% off, no minimum. Ends Aug 31") was still running on 2 Sep and
was set `disabled: true` rather than deleted, so it can be brought back. **Check this bar
for expired dates whenever the cut-off date changes.**

`announcement_early` was added 2 Oct, **first** in `block_order`, linking to
`/collections/pre-order`:

> Order Early, Pay Less — The Pre-Order Discount Drops As This Batch Fills • Orders $100+

**It deliberately names no percentage.** These blocks take plain text with no Liquid, so
"20% off" written here would be wrong on 6 Oct, again on 16 Oct and again on 21 Oct — and
this bar has already shipped two slides that went stale unnoticed. The wording above is
true for the whole batch and needs changing only when the ladder itself changes. If a
number is ever wanted here, it is three diary entries, not one edit.

It carries the same caveat as the homepage ladder: **it promises a discount checkout does
not give until the four automatic discounts exist.**

### Mature specimen listings

Six mature variants were split out of their merged pre-order listings on 4 Sep. Each new
product keeps the option name **`Plant Stage`** and variant titles starting
**`Mature Plant`**, which is what the `mature-specimens` and `ready-to-ship` collection
rules match on — rename either and the product silently leaves both collections.

| New listing | Was on | Variants |
| --- | --- | --- |
| `monstera-devil-monster-premium-variegated-mature-specimen` | Devil Monster pre-order | $2580 |
| `philodendron-caramel-marble-variegated-mature-specimen` | Caramel Marble pre-order | $450 / $350 |
| `philodendron-gloriosum-variegated-mature-specimen` | Gloriosum Var. pre-order | $350 |
| `philodendron-billietiae-variegated-mature-specimen` | Billietiae Var. pre-order | $250 / $450 |
| `monstera-bulbasaur-mature-specimen` | Bulbasaur pre-order | $250 |
| `philodendron-florida-beauty-variegated-mature-specimen` | Florida Beauty Var. | $150 |

`philodendron-florida-beauty-x-tortum` was already mature-only and was left alone.

Descriptions are written fresh rather than copied, to avoid duplicate content, and each
links back to its tissue-culture listing. Tags drop `Pre-Order` and `Tissue culture` and
gain `Mature Specimen`. All six are published to the same seven channels as the originals.

**Florida Beauty Variegated's mature photo is confirmed:** the plant on the concrete plinth
(`edited-edited_-_2026-08-25T213155.131…`), identified by the owner on 4 Sep. Its listing
now carries that one photo only; the other two candidates were detached. Note the pre-order
listing still has no tissue-culture plantlet photo — its card is a styled windowsill shot.

**Media created from an existing CDN URL is shared between products.** `productSet` with
`files: [{ originalSource: <cdn url> }]` reuses the same `MediaImage` id rather than making
a copy, so the mature listings and their pre-order listings reference identical media ids.
`productDeleteMedia` still only detaches from the product you name — verified by checking
the other product afterwards — but check both before deleting anything.

After the split, Devil Monster and Caramel Marble no longer needed a mature photo first,
so their media were reordered to lead with the tissue-culture plantlet. Removing the mature
variants also drops Billietiae Variegated and Florida Beauty Variegated out of
`ready-to-ship`, correctly — they have no ready-to-ship stock.

`catalog-backup/products-full-2026-09-04.jsonl` is the pre-split export (descriptions, SEO,
options, media, variants with price/SKU/inventory). Take one before the next structural
change too.

## Product photos: what drives the card, and the conflict it causes

**A collection card shows `product.featured_media` — the product's first photo.** Not the
variant image. `snippets/card-gallery.liquid` assigns `featured_media` directly, so
setting a variant image changes the *product page* gallery and nothing else. This is why
assigning mature photos to mature variants did not change the Mature specimens row.

**Photo order convention: #1 is the tissue culture, #2 is the mature plant.** Verified by
eye across ~40 products. The TC shot is either a plantlet held in tweezers on white, or
the plants inside the lab jar/bag; both count. Exceptions found: Devil Monster and
Caramel Marble have a mature photo at #1, and Florida Beauty x Tortum is mature-only
(correctly).

**The conflict this caused, now resolved:** all 7 products in `mature-specimens` were also
in `pre-order`, because stage is a variant. One product has one featured photo, so it was
impossible to show a plantlet in the pre-order row *and* a mature plant in the mature row —
and the mature row quoted tissue-culture prices. Fixed by splitting; see **Mature specimen
listings** above. The same trap returns the moment a mature variant is added back to a
merged listing.

**A card's price is `selected_or_first_available_variant.price`** (`snippets/price.liquid`),
so it follows *variant order*, not the row the card appears in. A merged listing therefore
quotes the same price in every row: Devil Monster reads $204 (its pre-order Premium) in the
Ready to ship row, where the actual ready-to-ship price is $382. No variant ordering fixes
both rows at once — the choice is a "From $X" range in the price snippet, or splitting, as
was done for mature specimens. Left as-is for now.

### Variant image convention

Every "Tissue Culture" variant (pre-order and ready-to-ship) points at the product's
first photo that is not already claimed by a Mature variant. Acclimated variants carry
no photo, deliberately — there are no acclimated photos. Mature variants keep whatever
the owner set. Counts after the September pass: TC pre-order 219/266, TC ready-to-ship
20/20, acclimated 0/273, mature 8/9. The 47 TC variants with no photo belong to the 48
active products that have no media at all.

`productVariantsBulkUpdate` takes `mediaId` (a MediaImage gid, not a ProductImage gid —
`variant.image.id` returns the latter, so match media by URL filename, not by id).
`bulkOperationRunMutation` is blocked; 40 aliased mutations per call works fine.

## Stage product rows (the homepage product rows)

`sections/stage-products.liquid` replaced Horizon's stock `product-list` on all four
homepage rows. Stock cards read `product.featured_media` and
`product.selected_or_first_available_variant.price` — both properties of the *product*.
Because plant stage is a variant, one listing sits in several rows and every row was
forced to show the same photo and the same price. Ready to ship quoted Devil Monster at
$204, its pre-order price, next to a mature plant photo.

This section picks the variant that belongs to the row and builds the card from it: that
variant's photo, price and compare-at price, plus a link carrying `?variant=<id>` so the
product page opens already on that stage.

| Section id | Collection | `stage_match` | Notes |
| --- | --- | --- | --- |
| `products_tc` | `pre-order` | `Tissue Culture (Pre-Order)` | |
| `products_sale` | `on-sale` | *(blank)* | `sale_only: true` — only variants with a compare-at price |
| `products_rts` | `ready-to-ship` | `Tissue Culture (Ready to Ship), Mature Plant` | `allow_fallback: true` |
| `products_acclimated` | `mature-specimens` | `Mature Plant` | |

**`allow_fallback`** exists for one-off plants sold as a single item, whose variant carries
no stage in its name (Spiritus Sancti, Tortum, Atabapoense…). It falls back to the first
available variant *only when the product has no stage-named variant at all*, so a merged
listing never falls back onto the wrong stage's price.

Only in-stock variants are shown, so the sold-out sorting in `product-list.liquid` no
longer applies to the homepage — sold-out plants are simply absent from these rows. That
file still carries the fix for any product row added from the theme editor.

The heading reuses Horizon's `h3` preset class and the link its `button-unstyled` class,
so both match the rest of the page without restating the type scale. Desktop is a grid of
`columns`; mobile is a scroll-snap carousel with moss arrow buttons.

### Uploading a section file

**A template is validated against the section schema already on the theme, not against
the one in the same call.** Sending `sections/spotlight-plant.liquid` (newly gaining
`blocks`) and `templates/index.json` (newly using those blocks) in **one**
`themeFilesUpsert` wrote the section and **silently dropped the template** —
`userErrors: []`, checksum unchanged. Re-sending the template on its own, once the
section was in place, worked first time. **Upload the section first, then the template,
in two calls.**

`themeFilesUpsert` with `body: { type: URL }` **swallows validation errors** — it returns
`userErrors: []` and simply does not write the file. Four silent no-ops here were one
schema mistake (`"default": ""` is rejected: a setting's default can't be blank). When an
upsert appears to succeed but the checksum does not change, re-send it with
`body: { type: TEXT }`, which reports the real `FILE_VALIDATION_ERROR`. Always verify by
comparing `checksumMd5` against the local file.

## Running a sale

**An automatic discount does not change the price on the storefront.** Shopify applies it
to cart line items, so product pages, cards, the `Save X%` badge and the `on-sale`
collection all still show the undiscounted price. Confirmed against Shopify's own docs;
do not promise the merchant a strikethrough from an automatic discount.

The two mechanisms, and what each buys:

| | Automatic discount | Compare-at prices |
| --- | --- | --- |
| Where it shows | cart and checkout only | strikethrough + `Save X%` badge everywhere, joins `on-sale` |
| Start / stop | dated, turns itself off | manual, someone must change ~700 variants back |
| Risk | none, no product data touched | a missed revert leaves the sale running |

**Labour Day 2026** (6–7 Sep) ran as an automatic discount: 20% off all items,
`combinesWith` order and product discounts **false** so it cannot stack with the existing
compare-at sales, shipping discounts **true** so free shipping over $180 still applies.
It ends 2026-09-08T03:59:59Z, which is Monday 23:59 Toronto — the shop is
`America/Toronto`, so always convert; September is UTC-4.

`sections/header-group.json` carries `announcement_labour_day`, first in `block_order`.
It says the discount is applied at checkout, because the prices on the page will not move.
The slide has no expiry, so it kept promising 20% off for four hours after the discount
expired; it was set `disabled: true` on 8 Sep and left in `block_order` so it can be
brought back. **Disable the slide in the same breath as ending a sale** — same trap as the
"Ends Aug 31" slide before it.

**What it earned.** 12 orders used the discount: $1,971 net, $2,433 gross, $461.80 given
away. Against the Aug 23 – Sep 5 baseline of $489/day and 2.9 orders/day, the two sale days
ran $1,077/day and 6.5 orders/day — roughly 2.2× on both, about $1,180 of extra revenue.

Two things worth remembering next time. **The deadline did the work, not the 20%:** the
final 7 hours produced $958, 49% of the whole sale, including the two largest orders. And
**basket size did not move** — net AOV was $164 against a $167 baseline, so the entire gain
was more people ordering, not bigger carts. The gross basket was bigger ($203) and the
discount ate exactly that difference.

The owner declined to extend it by a day on 8 Sep. Worth raising if a next sale comes up
soon: there has been a 20%-ish promo running almost continuously since May (BUY2ORMORE,
MIDSUMMER, GROW75/150/250, LAST3DAY20/30, ACCLIMATED SALE for a full month, three FOR WAIT
BATCH discounts, Labour Day), so a collector has had little reason to ever pay list price.
The 25 Sep batch cutoff is a real deadline that costs nothing.

## Sale savings badge

`snippets/price.liquid` renders a terracotta **Save X%** badge beside the price when the
selected variant has a compare-at price above its price. The percentage is worked out in
Liquid from that variant, before the prices are formatted into strings, so it follows the
plant stage the customer has selected — Devil Monster reads *Save 58%* on its pre-order
variant and *Save 22%* on ready-to-ship, off the same $490 compare-at.

It renders in two places, both wanted: the main price block and the sticky add-to-cart
bar.

**Scope it by handle, not by `is_product_card`.** That variable is derived from
`template.name`, so it is false for *every* price on a product page — including the
recommendation cards underneath, which each grew a badge on the first attempt. The guard
is `product.handle == product_resource.handle`, which is nil-safe on collection pages.

Styles are inline: a snippet cannot carry a `{% stylesheet %}` block. Collection and
homepage cards deliberately keep their plain "Sale" badge — a card's percentage would
have to come from product-level min/max prices, which on a merged listing is not the
same variant and would print a wrong number.

There is no campaign-name setting ("Labour Day Sale"). Adding one means editing
`config/settings_schema.json` (50 KB) and leaves stale text on 300 product pages when the
sale ends; the announcement bar already carries campaign names and the owner edits it
themselves.

## Collections never show a plant you cannot buy

**Shopify evaluates variant-scoped collection conditions per variant.** A rule set of
`variant_title contains "Acclimated"` **and** `variant_inventory > 0` matches only
products where *the same variant* satisfies both — so "the acclimated one is in stock"
is expressible natively, in the collection, with correct counts and pagination. This was
not obvious and is the key to the whole thing; prefer it over theme filtering.

Every all-conditions collection now carries `VARIANT_INVENTORY > 0`:

| Collection | Rules |
| --- | --- |
| `pre-order` | variant title contains `Tissue Culture (Pre-Order)` + stock > 0 |
| `ready-to-ship-tissue-culture` | variant title contains `Tissue Culture (Ready to Ship)` + stock > 0 |
| `acclimated-plants` | variant title contains `Acclimated` + stock > 0 |
| `mature-specimens` | variant title contains `Mature Plant` + stock > 0 |
| `on-sale` | `IS_PRICE_REDUCED IS_SET` + stock > 0 — the same variant must be both discounted and in stock |
| genus + `begonia` | title contains `<genus>` + stock > 0 |
| `ready-to-ship` | three OR'd rules, so **no** AND condition is possible — the theme filter below is the only mechanism for this one |

`ACCLIMATED PLANTS` (`acclimated-plants`) was created 4 Sep. The old one lived at the
Shopify default **Home page** collection (`/collections/home-page`, id 314086195279),
renamed to "IN STOCK ACCLIMATED PLANT" and hand-picked, so it listed mature specimens
too. **That collection is invisible to the Admin API** — `collectionByHandle`, `node`
and `collections` all return nothing for it, though the storefront renders it — so it
cannot be edited or deleted from here. The main menu item was repointed to the new
collection via `menuUpdate`; the old one is orphaned and the owner has to delete it in
admin.

The `/collections/acclimated-plants` → `/collections/ready-to-ship` redirect was deleted
to free the handle.

### No theme filter any more

There *was* one — `sections/main-collection.liquid` read a `custom.stage_match` collection
metafield and hid products whose stage variant was out of stock. It was removed on 6 Sep,
along with the metafield definition, because the collection rules now do the same job
natively and the two started to disagree.

The owner rewrote `ready-to-ship` themselves to `variant title NOT CONTAINS "Pre-Order"` +
`stock > 0` + `type NOT_EQUALS "Service"` — better than the OR'd rules it replaced, because
it also admits a plant whose only in-stock non-pre-order variant is Acclimated. The theme
filter, still looking only for `Tissue Culture (Ready to Ship)` or `Mature Plant`, would
have hidden exactly those plants: Bambino Pink, Nobilis Pink K, Micans, three Dragon
Scales, Polly Pink, Joepii.

**The rule is: stock and stage filtering belongs in the collection, not the theme.** The
owner asked for this explicitly, and it survives Horizon upgrades, keeps counts and
pagination honest, and shows in admin where they can see it.

`sections/main-collection.liquid` is back to the version that only sorts in-stock first —
now a no-op, since no collection contains a sold-out plant.

## Sold-out products

Shopify has no "in stock first" collection sort, and every collection here is rule-based,
so manual sorting is unavailable too. It is done in the theme instead:

| File | What it does |
| --- | --- |
| `sections/product-list.liquid` | any product row added from the theme editor — paginate widened to 50, in-stock first, then trimmed to `max_products`. The homepage no longer uses this section |
| `sections/main-collection.liquid` | collection pages — now *hides* what you cannot buy; see the section above |
| `snippets/cart-summary.liquid` | carries the 30-Day Plant Guarantee line; see that section |

Both are `where: 'available', true` + `reject: 'available', true` + `concat`. Liquid only
sees the current page, so collection pages sort per page, not across the whole collection;
with 17 fully sold-out products that reads correctly nearly everywhere.

**These are core Horizon files — a theme version upgrade overwrites them.** Re-apply the
two edits after every upgrade, alongside the re-seeded-sections check above.

## Acclimation guide page

`/pages/acclimation-guide`. The Shopify page body is **empty** — the whole guide is
hardcoded HTML inside `blocks/ai_gen_block_7be2211.liquid` (38 KB), referenced from
`templates/page.acclamation-guide.json` as block `ai_gen_block_7be2211_7RazQm`. Note the
misspelled template filename (`acclamation`), which is what the page's `template_suffix`
points at. None of the guide's wording is exposed as a block setting, so **any copy change
means rewriting the whole file** — the owner cannot edit this text in the theme editor.

The file says the same things twice: once in the "What You'll Need" list and again inside
the numbered steps, plus a third time in the `{% doc %} @prompt` comment at the top. Change
all three or the page contradicts itself.

Growing medium as of 7 Sep: sphagnum moss for **Monstera and Anthurium**; 50/50 Fluval
Stratum and perlite for Philodendron, Alocasia and other aroids. "Ready-to-use" was dropped
from the Betadine line — it now just reads "Diluted Betadine solution".

Rebuilding the file by hand is error-prone. Verify it by reverse-applying the intended
edits with `sed` and checking the result's md5 against the file you fetched — if it matches,
nothing else drifted.

## 30-Day Plant Guarantee

Launched 11 Sep. **Named "Acclimation Guarantee" for about an hour, then renamed** — it
collided with the Acclimation Guide and the paid Acclimation Service, so customers could read
it as something they had to buy. The internal filenames still say `acclimation-guarantee`;
only the customer-facing wording changed. Every plant is covered for **30 days from the delivery scan**: under $200 a
free replacement, $200 and over a replacement at **50% of what the customer paid** (not list
price — they buy on sale often). Customer pays a flat **$14.99** replacement shipping, charged
per parcel not per plant. One replacement per plant; store credit if the variety has sold out.
Conditions: **an arrival photo taken the day it is delivered** (hard gate — no photo, no
claim; it is the only way to tell a plant that arrived weak from one that was mistreated),
photos of the problem, and that they followed the Acclimation Guide. Claims go to
`info@agaplantz.com`. The photo rule applies only to orders delivered after launch — nobody
in transit beforehand was told to take one; drop that sentence around mid-October.

**DOA is deliberately kept separate.** The 24-hour dead-on-arrival claim can end in a full
refund with no shipping charge, which is *better* for the customer than the guarantee. The
guarantee covers day two to day 30. Never let a DOA case get routed into the guarantee.

**All guarantee copy lives in `snippets/acclimation-guarantee-badge.liquid`** — the product
block and the cart both render it, so wording changes happen there and nowhere else. Snippets
cannot carry `{% stylesheet %}`, so its styles are inline, like `snippets/price.liquid`.

| File | Role |
| --- | --- |
| `snippets/acclimation-guarantee-badge.liquid` | the copy and markup; `context: 'product'` or `'cart'` |
| `blocks/acclimation-guarantee.liquid` | product block — reads the variant, exposes settings, renders the snippet |
| `templates/page.plant-guarantee.json` | the page, native `text`/`group` blocks so the owner can edit it |

**The tier must follow the variant, never `product.price`.** `product.price` is the product's
*minimum* variant price and stage is a variant here, so a listing with a $150 Grade B and a
$204 Premium would advertise the free tier on both. The block reads
`closest.product.selected_or_first_available_variant.price`; Horizon re-renders the
`product-information` section on variant change, which is what keeps it in step — the same
mechanism the `Save X%` badge relies on. Devil Monster pre-order is the **only** in-stock
listing whose variants straddle $200, so it is the regression test: `?variant=45989665603663`
($150) must read "Free replacement", `?variant=45988645666895` (**$240** since 1 Oct, was
$204) must read "50%".

**`snippets/cart-summary.liquid` now carries the cart line and is a core Horizon file** — add
it to the list of files to re-apply after every theme upgrade, alongside
`sections/product-list.liquid` and `sections/main-collection.liquid`. One insertion covers both
the cart page and the drawer: the drawer renders this snippet directly, bypassing
`blocks/_cart-summary.liquid`.

The footer block `ai_gen_block_651bd33.liquid` gained a sixth policy slot
(`policy_link_6_text` / `_url`) because all five were used.

### What the API would not let me do

- **Policies are read-only from here.** `shopPolicyUpdate` returns *"Access denied … Required
  access: `write_legal_policies`"*. The app does not hold that scope, so Refund / Shipping /
  Terms edits must be pasted by the owner in Settings → Policies, or the scope granted.
- `bulkOperationRunMutation` is **still** blocked ("can execute arbitrary mutations"), so there
  is no way to push large bodies from a staged file. Anything the API takes as a full body has
  to be sent inline.
- `themeFilesDelete` and `themePublish` are blocked by the connector's safety policy, so an
  orphaned template can only be removed in admin, and the owner always publishes.
- `pageCreate` / `pageUpdate` / `menuUpdate` / `urlRedirectCreate` all work fine.

### Two ways a theme upload lies to you

**1. Verify that every file you asked for came back, not that the ones that came back match.**
`themeFilesUpsert` with a URL body returns `userErrors: []` on a *rejected* file, and a
follow-up `files(filenames: [...])` query simply omits it. Comparing the checksums that come
back looks like a pass. A whole template was reported as written this way when it had never
been created — the page silently fell back to `templates/page.json` for hours. Always assert
`len(returned) == len(requested)` and name the missing ones.

**2. An inline `style=` attribute inside a `text` block's richtext setting rejects the whole
file.** It does not get stripped on render — the upload is refused outright, silently. One
`<p style="margin-top:12px">` in a 48 KB page template was enough. Use the block's own
`padding-block-start` setting instead. Same allowed-tag list as the batch pricing notice
above: `<p> <strong> <em> <ul> <li> <h1>–<h6> <a> <br>` and nothing else.

**Template suffixes are fine starting with a digit** — `page.30-day-plant-guarantee.json` was
wrongly blamed for this before the real cause was found. The page's suffix is now
`plant-guarantee`, which is what `templates/page.plant-guarantee.json` serves; the page
*handle* is `30-day-plant-guarantee` and is unrelated.

### The FAQ accordion existed twice

`templates/page.json` — the **default** page template — carried its own full copy of the
15-question FAQ accordion (`ai_gen_block_138208e_JAjVmB`), on top of the one in
`page.faq.json`. Every page without its own template therefore ended in a generic shipping
FAQ: Payment Policy, Your Privacy Choices, and the guarantee page while it was falling back.
Removed on 11 Sep — `templates/page.json` is now just `main`. The FAQ lives on `/pages/faq`
only. If a page ever sprouts an FAQ nobody put there, this is why.

### JSON checksums do not round-trip

For a `.json` theme file **last written by the theme editor**, the API returns a
pretty-printed body with an auto-generated `/* ... */` header, while `size` and `checksumMd5`
describe a different stored form — strip the header and you still will not match, and it is
not plain minification either. So the reverse-apply-and-compare-md5 trick only works on files
*you* last wrote. For editor-written JSON, verify **semantically**: parse before and after and
assert only the intended keys moved. Files you upload are stored as your exact bytes, so the
checksum always matches on the way back.

## Open items

**Hidden from the Online Store** — 7 ACTIVE products with stock, published to Google/
Meta/TikTok/Microsoft but *not* the storefront, so ads point at unbuyable plants
(~157 units). Owner has not yet said whether to publish them:
Joepii (39), White Princess (20), Florida Ghost (20), Pink Princess (20), Birkin (20),
Pink Princess Marble Galaxy (19), Golden Dragon Variegated (19).
Philodendron Florida Beauty Variegated had the same problem and *was* published,
because it was breaking the Mature Specimens row.

- **Begonia has no photographs at all** — see the section below. This is the one thing
  holding the new genus back.
- **Four naming near-matches** never eyeballed: Obliqua Peru vs Peruvian · Nairobi
  Nights Variegated vs A Grade · Dragon Scale Albo vs Albo Ultra · Thai Constellation
  vs Pro.
- **Mature row shows first-variant prices** (see Catalogue architecture).
- **Mobile hero art direction** — hero has a separate mobile image slot
  (`custom_mobile_media`). A 4:5 or 9:16 crop would beat centre-cropping the wide shot.
- **Theme cleanup** — ~10 themes exist, including five stale Horizon copies from
  May–July and superseded `AgaPlantz 2026 (Claude*)` versions. Never delete without
  explicit say-so.
- **`agaplantz-hero-2026.jpg`** in Files is an interim upscale, now unreferenced.

## Things already fixed (don't re-litigate)

Duplicate "Follow us on" in the footer · 10 compare-at prices set *below* price
(Devil Monster mature showed ~~$490~~ $2,580) · mature photos buried at gallery
position 4+ behind bare-root plantlets · 7 spellings of the ready-to-ship variant
normalised (25 values, 20 products) · 6 duplicate listings merged without
double-counting stock · Florida Beauty price inversion · Jose Buono, which looked like
a duplicate but was a wrong title on a real product.

## Repo layout

Only the files that differ from stock Horizon are tracked:

| Path | Purpose |
| --- | --- |
| `theme/blocks/ai_gen_block_7be2211.liquid` | acclimation guide (all copy hardcoded) |
| `theme/blocks/ai_gen_block_651bd33.liquid` | footer block (policy + quick links, email) |
| `theme/blocks/acclimation-guarantee.liquid` | guarantee product block |
| `theme/snippets/acclimation-guarantee-badge.liquid` | all guarantee copy |
| `theme/snippets/cart-summary.liquid` | core Horizon, patched for the cart line |
| `theme/snippets/price.liquid` | Save X% badge |
| `theme/templates/page.plant-guarantee.json` | the guarantee page (suffix `plant-guarantee`) |
| `theme/templates/page.json` | default page template — FAQ accordion removed |
| `theme/templates/page.faq.json` / `page.contact.json` | FAQ answers, contact email |
| `theme/config/settings_data.json` | global design tokens |
| `theme/templates/index.json` | homepage |
| `theme/templates/list-collections.json` | curated /collections |
| `theme/sections/footer-group.json` | footer, all pages |
| `theme/sections/stage-products.liquid` | variant-aware product row (homepage + /collections) |
| `theme/sections/spotlight-plant.liquid` | plants shown big, one per slide |
| `theme/sections/subscription-callout.liquid` | mystery-box band, five floating cut-outs, tiers read from the product |
| `theme/sections/batch-discounts.liquid` | standalone discount ladder — **unused**, the ladder lives in the countdown |
| `catalog-backup/` | pre-deletion product export |

Branch: `claude/shopify-theme-creation-ra78zf`. The local template is kept in sync
with whatever is live — pull the MAIN theme's file down after every publish so the
next session starts from the truth.
