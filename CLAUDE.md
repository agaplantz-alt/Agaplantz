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

As of the last session: MAIN was `AgaPlantz 2026 (Claude) 0.1` = `149362769999`,
Horizon **4.1.4**. Verify, don't assume.

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
3. `collections_genus` — Philodendron / Alocasia / Monstera / Anthurium tiles
4. `tissue_culture` — explainer; intro on top, two cards side-by-side (also on mobile)
5. `products_tc` — Tissue culture pre-orders (`pre-order`, 283 products)
6. `products_sale` — Collector favourites on sale (`on-sale`), sand band
7. `products_rts` — Ready to ship (`ready-to-ship`)
8. `products_acclimated` — Mature specimens (`mature-specimens`), sand band
9. `why_agaplantz` — 4 icon/text cells, 2×2 on mobile, sage
10. `newsletter`

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

Consequence still unresolved: collection cards show a product's **first variant**, so
Mature Specimens shows tissue-culture prices. Fixes are reordering variants (puts a
cheap price on the product page) or splitting mature variants into own listings.
Not decided.

### Collections

| Handle | Title | Count |
| --- | --- | --- |
| `philodendron` / `alocasia` / `monstera` / `anthurium-1` | genus | 92 / 123 / 33 / 40 |
| `begonia` | BEGONIA | 10 (all DRAFT — not surfaced anywhere) |
| `pre-order` | TISSUE CULTURE — PRE-ORDER | 283 |
| `ready-to-ship-tissue-culture` | TISSUE CULTURE — READY TO SHIP | 19 |
| `ready-to-ship` | READY TO SHIP | 36 |
| `mature-specimens` | MATURE SPECIMENS | 7 |
| `on-sale` | ON SALE (rule: `IS_PRICE_REDUCED IS_SET`) | 62 |

`/collections` is a curated two-group page (`templates/list-collections.json`):
**Shop by plant** (four genus) and **Shop by stage** (RTS, RTS tissue culture,
mature, pre-order). Stock `main-collection-list` was replaced because the flat list
mixed genus and stage and served no browsing purpose.

`ACCLIMATED PLANTS` was deleted; `/collections/acclimated-plants` 301s to
`/collections/ready-to-ship`.

`catalog-backup/products-full.jsonl` is a full pre-deletion export of all 309 products
(descriptions, SEO, media, option value IDs, variants with SKU/price/compare-at/
inventory). Taken before any permanent delete — do the same before the next one.

## Horizon gotchas, learned the hard way

- **Product cards render nothing unless the gallery block is in `block_order`.** Type
  `_product-card-gallery`, name `t:names.product_card_media`, **not** `static: true`,
  and listed first. A declared-but-unordered block is silently ignored — this is why
  three product rows showed title+price with no photo. The Sale badge also lives
  inside this block.
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
- **A Horizon version upgrade re-seeds default sections into JSON templates.** The
  4.1.4 upgrade put a stock `main-collection-list` section back at the top of
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
`loox.avg_rating` for a true weighted average, then shows the first 5-star review
with a photo from each of six different products.

The aggregate is computed live, so it never goes stale, and it counts the low
ratings too (Gloriosum Variegated 1.0, Goeldii Mint 3.0, Tortum 3.5) — it reads
4.7, not 5.0. Do not hardcode it and do not exclude the low ones from the maths;
only the *featured cards* are filtered to 5-star.

**When new products get reviews, add their handles to the list**, or they are left
out of both the average and the cards.

A `skip_ids` list inside the block drops individual reviews from the *featured cards*
only — the average still counts them. Currently it skips one review whose text opens
"came slightly bent".

**Tissue-culture photos are wanted here, not filtered out.** Plantlets in prop boxes
and humidity domes are what most customers actually receive, and a real one arriving
healthy answers the objection that stops a first order. Do not "tidy" those photos
out of the section — the owner asked for them specifically.

## Open items

**Hidden from the Online Store** — 7 ACTIVE products with stock, published to Google/
Meta/TikTok/Microsoft but *not* the storefront, so ads point at unbuyable plants
(~157 units). Owner has not yet said whether to publish them:
Joepii (39), White Princess (20), Florida Ghost (20), Pink Princess (20), Birkin (20),
Pink Princess Marble Galaxy (19), Golden Dragon Variegated (19).
Philodendron Florida Beauty Variegated had the same problem and *was* published,
because it was breaking the Mature Specimens row.

- **Begonia** — 10 products, all DRAFT. Add to `/collections` once published.
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
| `theme/config/settings_data.json` | global design tokens |
| `theme/templates/index.json` | homepage |
| `theme/templates/list-collections.json` | curated /collections |
| `theme/sections/footer-group.json` | footer, all pages |
| `catalog-backup/` | pre-deletion product export |

Branch: `claude/shopify-theme-creation-ra78zf`. The local template is kept in sync
with whatever is live — pull the MAIN theme's file down after every publish so the
next session starts from the truth.
