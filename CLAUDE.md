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
10. Loox `loox-dynamic-carousel` app block — added by the owner in the theme editor

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

| Handle | Title | Count |
| --- | --- | --- |
| `philodendron` / `alocasia` / `monstera` / `anthurium-1` | genus, rule `TITLE CONTAINS <genus>` | 63 / 123 / 36 / 38 live |
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

## The batch cut-off date lives in five places

When the pre-order cut-off changes, all of these need updating — they are separate
hand-entered strings, not one setting:

| File | Field | Format |
| --- | --- | --- |
| `sections/header-group.json` | `announcement_jeGMHt.text` | `Close September 25` |
| `templates/page.pre-order.json` | `ai_gen_block_41bf156_tpPC39.cutoff_date` | `25 SEP 2026` |
| `templates/product.tissue-culture.json` | `ai_gen_block_c6aca6a_HjQ7Ph.preorder_date` | `25 SEPTEMBER` |
| `templates/product.tissue-culture.json` | `ai_gen_block_675aea4_RGqfCa.preorder_text` | hidden block |
| `templates/product.tissue-culture.json` | `ai_gen_block_44763e7_iKDBHj.preorder_text` | hidden block |

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

`themeFilesUpsert` with `body: { type: URL }` **swallows validation errors** — it returns
`userErrors: []` and simply does not write the file. Four silent no-ops here were one
schema mistake (`"default": ""` is rejected: a setting's default can't be blank). When an
upsert appears to succeed but the checksum does not change, re-send it with
`body: { type: TEXT }`, which reports the real `FILE_VALIDATION_ERROR`. Always verify by
comparing `checksumMd5` against the local file.

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

### The theme filter (still needed)

Set 4 Sep. Hiding fully sold-out products is not enough, because plant stage is a
variant: Monstera Bulbasaur has pre-order stock and no ready-to-ship stock, so it
belongs in the pre-order collection but not in `ready-to-ship-tissue-culture`, where it
was sitting first in the row.

`sections/main-collection.liquid` reads a collection metafield and shows a product only
when *that collection's* variant is in stock:

| Collection | `custom.stage_match` |
| --- | --- |
| `pre-order` | `Tissue Culture (Pre-Order)` |
| `ready-to-ship-tissue-culture` | `Tissue Culture (Ready to Ship)` |
| `ready-to-ship` | `Tissue Culture (Ready to Ship), Mature Plant` |
| `mature-specimens` | `Mature Plant` |
| everything else | *(blank)* — hides only what is completely sold out |

A product whose variants carry no stage at all — a one-off specimen like Spiritus
Sancti — is shown whenever anything on it is in stock, so those never vanish. With the
metafield blank the same rule reduces to "hide anything sold out", which is why the
genus collections need no setting.

**The metafield definition must have `access: { storefront: PUBLIC_READ }`.** Created
through `metafieldDefinitionCreate` it defaults to `storefront: NONE`, and Liquid then
reads it as nil — the filter silently degrades to "hide sold out" with no error. That
cost a debugging round; the symptom is a collection showing its full unfiltered count.

Products are hidden *after* Shopify has paged them, so a page can hold fewer than 24
cards. At current stock that is 15 of 19 on RTS tissue culture and 19 of 24 on
Philodendron — acceptable; the alternative is per-collection inventory rules, which
Shopify cannot express for `ready-to-ship` because its rules are OR-joined.

**Collection descriptions were stored HTML-escaped** (`&lt;p&gt;…`) on five collections
and rendered as literal `<p>` tags to customers. Fixed by re-setting `descriptionHtml`.
Check any new collection description on the storefront, not just in admin.

## Sold-out products

Shopify has no "in stock first" collection sort, and every collection here is rule-based,
so manual sorting is unavailable too. It is done in the theme instead:

| File | What it does |
| --- | --- |
| `sections/product-list.liquid` | any product row added from the theme editor — paginate widened to 50, in-stock first, then trimmed to `max_products`. The homepage no longer uses this section |
| `sections/main-collection.liquid` | collection pages — now *hides* what you cannot buy; see the section above |

Both are `where: 'available', true` + `reject: 'available', true` + `concat`. Liquid only
sees the current page, so collection pages sort per page, not across the whole collection;
with 17 fully sold-out products that reads correctly nearly everywhere.

**These are core Horizon files — a theme version upgrade overwrites them.** Re-apply the
two edits after every upgrade, alongside the re-seeded-sections check above.

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
