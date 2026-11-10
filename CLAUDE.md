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

**As of 10 Nov 2026: MAIN is `AgaPlantz 2026 — cart add-ons restored (from live)` =
`190324277327`** — the owner published it (*"Cart restored is live"*) and it became MAIN **in
place** (same id). Post-publish check the same hour: `cart-summary.liquid`, `index.json`,
`header-group.json` and the three re-seed-prone templates all match the repo by checksum, and
the **live** cart with a pre-order in it renders the substrate offer, the heat-pack offer and
the guarantee line (drawer DOM carries the same three). The next change starts with a fresh
`themeDuplicate` of `190324277327`.

**Earlier, 9 Nov 2026: MAIN was `AgaPlantz 2026 — crochet line` = `190192943183`** — the owner
published the crochet draft on 7 Nov at 20:34Z and it became MAIN **in place** (same id, no
"Updated copy of"). Merge check on 9 Nov: every file we wrote matches the repo by checksum
(index, header-group, crochet-feature, tc-stages, why-agaplantz, the three re-seed-prone
templates); `product.json`, `product.tissue-culture.json`, `product.crochet.json`,
`footer-group.json`, `page.faq.json` and `settings_data.json` differ only by re-serialisation
(all stamped 06 Nov 18:55Z, the duplicate's creation). **The cart add-ons were gone on live** —
the owner's screenshot of the drawer on 9 Nov (*"it does not show add-ups"*): no guarantee line,
no heat-pack offer, no substrate offer. Cause: `snippets/cart-summary.liquid` is stock Horizon
on every theme since 1 Nov (see the 5 Nov note below), and it is the **only** file that renders
`acclimation-guarantee-badge` in cart context (the drawer and `blocks/_cart-summary.liquid`
both render `cart-summary`). The 5 Nov claim that the cart line "survived" was wrong — rendered
with an item in the cart, both `190146576463` and the live theme show zero `.hp-addon` and no
guarantee line. Fix: draft **`AgaPlantz 2026 — cart add-ons restored (from live)` =
`190324277327`** (duplicated from MAIN), with the live stock `cart-summary.liquid` plus the one
render block after `.cart__ctas` (checksum `0b41a1877f7f779e4221902ea92f0645`); the repo copy is
now that file, so it is no longer stale. Verified on the preview with a pre-order in the cart:
substrate offer, heat-pack offer with Add, and "Covered by our 30-Day Plant Guarantee" all render
on `/cart`, and the drawer's DOM carries the same three. The owner publishes it.

**Earlier, 5 Nov 2026, 20:21Z: MAIN was `AgaPlantz 2026 — guide pages repaired (from live)` =
`190146576463`** — the owner published the repair draft and it became MAIN **in place** (same
id, no "Updated copy of"), so nothing was re-seeded this time. Full sweep the same hour: all 31
repo-tracked files compared (Liquid by checksum, JSON parsed), 23 live pages rendered with no
Liquid error, all 15 FAQ questions, both guide pages' 8 chapters, `/collections` curated, the
cart showing the guarantee line and the heat-pack offer. **One real loss, found in the sweep and
not yet fixed: the `Save X%` badge is gone.** Since the 1 Nov publish, `snippets/price.liquid`,
`snippets/cart-summary.liquid`, `sections/main-collection.liquid` and
`sections/product-list.liquid` on every theme in the line are **stock Horizon** (newer, with
`<bdi>` wrappers) — our patches were overwritten. The price one is the visible loss: Devil Monster
shows its struck-through compare-at but no badge. The in-stock-first sorts are no-ops now
(collections exclude sold-out plants). The cart guarantee line survived because another session
rebuilt `snippets/acclimation-guarantee-badge.liquid` as a wrapper around
`snippets/acclimation-guarantee-badge-core.liquid` that also renders `tc-kit-addon` and
`heat-pack-addon`, and the cart renders it from somewhere other than `cart-summary.liquid`.
**The repo copies of those five files are stale** — pull the live ones before editing any of them.

**Earlier on 5 Nov: MAIN was `Updated copy of AgaPlantz 2026 — plant profile …` =
`190114758735`**, created by Shopify at 06:15:49Z when the owner published the plant-profile
draft `190043619407`. **It re-seeded exactly the same three templates as on 1 Nov**:
`page.pre-order.json` and `page.tissue-culture.json` came back as the bare 823-byte `main-page`
template (identical checksums) and `list-collections.json` got `collection_list_Wfgh3m` back at
the top. The owner noticed from their phone ("what happened to the pre-order page?") about
14 hours later. Everything else (index, header, all four product templates, FAQ, guarantee,
default page) parsed identical to the repo. Repair draft: **`AgaPlantz 2026 — guide pages
repaired (from live)` = `190146576463`**, MAIN plus the three repo templates (3 of 3 written,
checksums match); verified on the preview: both guide pages render their 8 chapters, `Order by
30 November` is on the Pre Order page, `/collections` starts with Shop by plant, no Liquid
errors. **So this is not a one-off: when publishing produces an "Updated copy of" theme, these
three templates are reset every time.** After every publish, check those three files on the
new MAIN first.

**Before that, 4 Nov 2026: MAIN was `AgaPlantz 2026 — November ladder 20/15/10 (from live)` =
`189923491919`** — the owner published it; the re-seeded pages are repaired live. The draft waiting
for them is the plant-profile theme `190043619407` (see that section).

**Before that, 1 Nov 2026 22:30Z: MAIN was `Updated copy of AgaPlantz 2026 — what is tissue…` =
`189909401679`**, created by Shopify at 16:48:43Z — 68 seconds after `189688381519` became MAIN —
when the owner published again. **That copy re-seeded three JSON templates**: `page.pre-order.json`
and `page.tissue-culture.json` came back as a bare `main-page` template (identical checksums, two
blocks, the thread gone — both pages showed only their one-line body for six hours) and
`list-collections.json` got `collection_list_Wfgh3m` back at the top. Everything else
(index, header, product templates, FAQ, settings) was byte-different but semantically identical —
copies re-serialise JSON, so **compare parsed JSON, not checksums, after any publish**, and render
the TC page, the Pre Order page and `/collections` every time. The fix plus the 20/15/10 ladder and
the shipping copy is draft **`AgaPlantz 2026 — November ladder 20/15/10 (from live)` =
`189923491919`**, duplicated from `189909401679`; `189923459151` is a dead duplicate of the
superseded theme, made a minute too early — ignore it (deleting is the owner's call).

**Before that, 16:47Z: MAIN was `AgaPlantz 2026 — what is tissue culture page` =
`189688381519`** — the long-lived "clean post-Halloween draft" the owner finally published,
carrying the November promo ladder, the 30 Nov cut-off, the 3D logo and favicon, the magic-mix
guide and the 48-hour cancellation answers. The Halloween line (`189887840335` and its
ancestors) is retired. **It is MAIN now, so the API can no longer write to it** — the next change
starts with a fresh `themeDuplicate` of it. Post-publish check the same hour: all ten key pages
rendered with no Liquid error, `templates/list-collections.json` kept its three curated sections
(no re-seeded `main-collection-list` this time), the homepage section order was intact and the
`/collections/halloween-spooky-plants` page shows no badge.

As of 27 Oct 2026: MAIN was `AgaPlantz 2026 — product pages: Loox only` = `189569040463`
(the owner published the 25 Oct draft, so the reviews-wall removal and the acclimation-add-on
pause are live); the draft waiting for them is `AgaPlantz 2026 — what is tissue culture
page` = `189688381519`. As of 16 Oct: MAIN was `AgaPlantz 2026 — ladder hides past tiers` = `188747120719`,
published by the owner on 6 Oct, so the self-trimming ladder is live and did its job on the
16th with no edit. Before that (6 Oct): MAIN was `AgaPlantz 2026 — mystery box call-out` =
`188663136335` — the owner published our 4 Oct draft as-is, so the mystery-box band, its
cut-outs and the scroll motion are live. Before that (4 Oct): MAIN was `AgaPlantz 2026 — subscription page` = `188662284367`, Horizon
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
   added to this batch", "Pre-orders are open again" and now "New batch now open", so re-read it whenever
   the deadline moves or it will state something that is no longer true. It hides itself
   once the timer expires. The deadline is a hardcoded ISO string carrying the Toronto offset
   (`assign deadline = '2026-11-30T23:59:59-05:00'`) — one of the six places the cut-off
   date lives, and the only one that also needs the *time*. Classes are `aga-batch__*`;
   when the timer hits zero the JS rewrites the headline, the line and the CTA in place
   and hides the digits **and the discount ladder**, so an expired batch never reads as a
   live one. The **discount ladder lives inside this same section** — see below.
4. `collections_genus` — Philodendron / Alocasia / Monstera / Anthurium / **Begonia**
   tiles. `max_collections` was `4` and silently drops the fifth handle — it is now 5,
   and `columns` went 4 → 5 so the row stays one line instead of 4 plus an orphan.
4b. `tc_learn_more` — slim sage strip, "What is a tissue culture plant? → Learn more",
   linking to `/pages/tissue-culture`. See the education-page section below.
5. `tissue_culture` — **rebuilt 7 Nov 2026 as `sections/tc-stages.liquid`**, same key in
   `order`, now a **sand** band (`#F2EBDE`). Three passes in one night. The owner, on a phone
   screenshot of the old group/text version: *"We need to rebuild this one. It's not looking
   good anymore."* Pass one was photo-led cards with moss buttons and a boxed guarantee strip;
   the owner: *"Every other part of homepage I'm loving it, but this part I'm still not able to
   love it… smaller or maybe like it should look luxurious, but it should not complicate
   things."* So now: heading, one line and "Read the full guide →" on the left; on the right one
   **slim hairline-ruled row per `stage` block** — a 96px square photo (76px on a phone), a
   terracotta small-caps line (`tag`), a Lora title, one line and a moss outline arrow; the whole
   row is the link, no buttons, no pills, no boxes. The photo is the block's `image`, else the
   collection image, else the first product photo in that collection. Under the rows, the
   30-Day Plant Guarantee as one line (moss shield disc, bold title, short copy, "How it works →",
   `show_guarantee`). Two columns from 990px, stacked below. Padding 48/48. Then the owner:
   *"I think the background color is what we need to change"* — sage → sand. The old group/text
   block tree is gone from `index.json` (git history has it).
5. `spotlight_plant` — **one plant, shown big**, sand band. A `spotlight-plant` section;
   see below. Sits between the genus tiles and the tissue-culture explainer.
6. `subscription_box` — the mystery-box call-out, **moss band**. A `subscription-callout`
   section; see below. Deliberately directly under the spotlight: a visitor who has just
   scrolled past two expensive named plants is the one still undecided.
7. `tissue_culture` — the explainer (numbering above is off by one from here down)
8. `products_popular` — **the only product row on the homepage**, cream band. A
   `stage-products` section on the automated `popular` collection, sorted BEST_SELLING.
9. `crochet_feature` — the crochet band, see **Crochet line**. Light pink.
9b. `why_agaplantz` — **rebuilt 7 Nov 2026 as `sections/why-agaplantz.liquid`**, same key,
   **moved below the crochet band** on the owner's say-so (*"why people choose … should be
   below CROKET"*), now a **sand** band with a plant photo. Same three passes as the explainer:
   numbered cream cards with moss icon discs were rejected as not luxurious; it is now a
   two-column layout — **a mature plant photo on the left** (4:5, 4px radius, a small cream
   caption chip bottom-left, the whole photo a link) and on the right a small eyebrow, the Lora
   heading and **one hairline-ruled row** of `reason` blocks: thin-line moss icon, Lora title,
   one line, vertical rules between items, 2×2 with rules on a phone (the photo goes on top at
   16:10, focal point shifted to 62% so the pot stays in frame). No cards, no fills, no numbers
   (`show_numbers` is kept in the schema but unused). Photo settings: `image` (image_picker),
   `product` (fallback photo and link), `image_link`, `image_caption`, `image_position`. The
   owner then pointed at three products — *"we can use these one or more like these"*:
   Anthurium warocqueanum, **Monstera White Lava Ghost**, Alocasia Nobilis Pink K — and the
   White Lava Ghost's second photo (`edited-edited20.png`, beige pot in warm light, 2048²) is
   the one in use, referenced as `shopify://shop_images/edited-edited20.png`, linked to
   `/products/monstera-white-lava-ghost-pre-order`, caption "Monstera White Lava Ghost". The
   Gloriosum mature photo (`edited-edited_-_2026-08-25T221144.243.png`, warm beige concrete)
   was the first pick and is the best alternative; the other mature-specimen shots are on cool
   grey concrete and fight the sand band. **The two-column grid must live on an inner wrapper
   (`.agwy__grid`), not on the `.section` element** — Horizon's `.section` is already a grid
   and placing columns on it stacked the photo and the copy in one column. The four reasons
   and their lines are the old copy, with "local pickup available" now "local pickup in
   Brampton". Bands now run: popular (cream) → crochet (pink) → why (sand) → Loox (cream).
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

**Every plant collection sorts by BEST_SELLING since 10 Nov 2026.** Karan (the ads agency, in
the "Aga Plantz X NOIR" WhatsApp group): *"keep all the bestsellers on the top of collection
pages … based on the sales data"*; the owner: *"Can you do it for me"*. `pre-order`, `monstera`,
`alocasia`, `philodendron` and `anthurium-1` were `MOST_RELEVANT` and were switched with
`collectionUpdate(collection: {id, sortOrder: BEST_SELLING})` (the `input:` argument is
deprecated in 2026-10; `Collection.ruleSet` is too — it is `sources` now). Begonia, RTS,
on-sale, acclimated, popular and the crochet collections were already BEST_SELLING;
`mature-specimens` is `PRICE_DESC` (3 products, dearest first — left alone) and
`crochet-gifts-under-25` is `PRICE_ASC` (left alone). Live immediately — it is data, not theme.
Verified: `/collections/monstera` now leads Bulbasaur, Devil Monster, White Monster, Creme
Brulee, the same order as the ShopifyQL ranking. Shopify's ranking is its own rolling window;
nothing to maintain.

**"BEST SELLERS" in the menu, 10 Nov 2026.** The owner read Karan's ask again — *"one more bar
at the top, like after all collections, best sellings"* — so the live menu `main-menu-crochet`
(`gid://shopify/Menu/275458555983`, `menuUpdate`, whole tree resent with every `id`) now has a
**BEST SELLERS** item in the Plants collections submenu directly after "All collections",
pointing at the `popular` collection (`491313004623`), which was **retitled "BEST SELLERS"**
(handle still `popular`; the homepage row heading is the section's own "Popular right now"
string, so it did not change). Its first render led with the $3.50 heat-pack add-on, and the
old `TITLE NOT_CONTAINS "Starter Kit"` rule no longer catches the substrate kit (its title is
"Tissue Culture Substrate" now), so both are **excluded by product selection** on the
collection's conditions source (`sourcesToUpdate` → `exclusion.selectionsToAdd`; the source is
`gid://shopify/CollectionConditionsSource/53987278927`). The 2026-10 schema replaced
`ruleSet` with `sources` and `collectionUpdate(input:)` with `collectionUpdate(collection:)`.
The 15 crochet products are still in it and sit at the bottom until they sell; the pot
accessory too. Verified live: the page is titled BEST SELLERS and opens Bulbasaur, Devil
Monster, White Monster, Bambino Pink.

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

**A tier disappears the day after it ends (6 Oct).** The owner crossed out the expired
Oct 1–5 card on a screenshot — a discount you can no longer use reads as a loss, not an
incentive. Each card is wrapped in `{% if day_now <= <last day> %}`, `tier_count` is
computed alongside `day_now` and written to the `<ol>` as `--tiers`, and the grid takes
`repeat(var(--tiers), …)` so three cards fill the row instead of leaving a gap. On a
phone an odd last card spans both columns (`:last-child:nth-child(odd)`). Once only
"Regular" is left (day 21 on) the whole ladder is skipped — one lonely "full price" card
with a Now pill is worse than nothing. The expiry script guards its `.aga-batch__tiers`
lookup for the same reason. So the ladder is 3 cards from 6 Oct, 2 from 16 Oct, gone from
21 Oct, with no edit needed.

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

### The discounts themselves

**The 15% tier exists as of 6 Oct** — the owner created it in admin:
`15% OFF SALE - orders $100+` (`gid://shopify/DiscountAutomaticNode/1531118911567`),
automatic, 15%, minimum subtotal $100 CAD, `2026-10-06T04:00Z` → `2026-10-16T03:59Z`
(Oct 6 00:00 → Oct 15 23:59 Toronto, exactly the card), one-time purchases only (the
mystery box is excluded, correctly), scoped to the PRE-ORDER, READY TO SHIP and
ACCLIMATED PLANTS collections — mature specimens are outside it.

**Two things about it were flagged, not changed** — it is the owner's discount:
`combinesWith.orderDiscounts: true`, and every active code in the shop is an ORDER-class
code that also allows combining (`WELCOME10` 10%, `NEWPLANTLOVE` 10%, nine Loox review
codes at 10–20%), so a customer can stack a code on top and take 25–35% off. Setting the
automatic discount's `orderDiscounts` to `false` blocks all of them at once. And
`shippingDiscounts: false` is harmless — free shipping over $180 is a shipping *rate*, not
a discount (no active automatic free-shipping discount exists).

**The 10% tier exists as of 16 Oct** — created from here on the owner's say-so
(*"go create the 10% or change the discount name to 10% now"*): `10% OFF SALE - orders $100+`
(`gid://shopify/DiscountAutomaticNode/1533887348815`), `2026-10-16T04:00Z` →
`2026-10-21T03:59Z` (Oct 16 00:00 → Oct 20 23:59 Toronto), a **new** discount rather than
the 15% one edited, so the 15% keeps its own reporting line. Every other setting mirrors
the 15% exactly, stacking included — the stacking question above was raised twice and never
answered, so it was left as the owner set it, not decided for them. The 15% expired on
schedule at 03:59Z on the 16th; the 20% never existed and is moot.

**Its scope is two collections, not three.** By 16 Oct the 15% listed only PRE-ORDER and
READY TO SHIP — ACCLIMATED PLANTS had dropped off it, most likely because the owner deleted
or rebuilt that collection (it has been deleted and recreated before; see **Collections**).
The 10% mirrors the two that were there. If acclimated plants are meant to be in the
promotion, that collection has to exist and be added to the discount.

**Verified on the live homepage the same morning:** the ladder rendered `--tiers: 2` (Oct
16–20 *Now*, Oct 21–31 Regular) and the string `15%` appeared nowhere on the page, so
"remove the 15% from the website" needed no theme change at all.

The original finding, kept for the pattern: at build time (2 Oct) **every automatic
discount in the shop was EXPIRED.** The only ACTIVE ones were Loox review codes and
`WELCOME10`, all code-based. So the ladder as first published advertised money off that
checkout would not give.

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

## Plant profile — the product-page "About this plant" / "Care guide" (4 Nov 2026)

The owner, looking at a product page: *"we need to upgrade this section now … make it more
premium. And meta fields also need to be upgraded … create those first"* — another Claude
will fill the values. The old pair was `ai_gen_block_b7314fa_8XqVwX` in the `_blocks` section
`177813606948323435` on both `product.json` and `product.tissue-culture.json`: an AI block with
16px radii and off-palette greens, whose About card read four `custom.*` metafields that say
the same thing on nearly every product (Juvenile / 2–4 inch / NA / Establishing) and whose
six care lines were **one hardcoded string each, shared by all 600 products** — an Alocasia
and a Monstera gave identical watering advice.

**Now:** `blocks/plant-profile.liquid` (+ `snippets/plant-profile-dots.liquid`), a theme block
added as `plant_profile_main` on both templates. **Second pass the same night:** the owner
wanted the "What This Plant Can Become" block (`ai_gen_block_d0d88e1_RyQrMA`, juvenile →
mature photos from `custom.young` / `custom.big_one`) *integrated* into it, and a background
"like the countdown, blurry kind of … expensive". So it is now **one full-bleed band**: the
host `_blocks` section `177813606948323435` is `section_width: full-width` and the block caps
its own content at `var(--page-width)` / `var(--page-margin)`; behind everything sits the
plant's own mature photo (then juvenile, then first image; an `image_picker` override exists)
at `blur(40px)`, scaled 1.3, at 55% over a sand base with a cream gradient, and the two cards
are translucent (`#FBF8F2C7` / `#E8EDE1D1`, `alpha: true` colour settings) with
`backdrop-filter: blur(14px)`, so each product page gets its own colour wash. Top row on
desktop: photos left (two square tiles, moss arrow disc between, Lora captions), names and
pills plus "What this plant becomes" + note on the right; on a phone it is names, photos,
text. Both AI blocks (`d0d88e1` and `b7314fa`) are `disabled: true`, settings intact, so they
can come back. Design system, not AI defaults: sand About card, sage Care card, clay borders,
4px radius, Lora titles, moss icon discs. Header: genus eyebrow (from `product.type`),
botanical name in italic Lora (falls back to the product title), pills (rarity in terracotta,
"<level> care", growth habit, pet safe).
About card: summary, a 2-column facts list (native range / growth habit / mature leaf /
variegation), "What you'll receive" tiles from the four old fields (`NA`-style values are
hidden), the variation note. Care card: six rows, with a five-dot meter beside Light, Water
and Humidity when the 1–5 level is set; each line falls back to a block setting when the
product's metafield is blank, so nothing breaks before the fill. 18 definitions were created
with `metafieldDefinitionCreate` (ids and the fill plan in **`docs/plant-profile-metafields.md`**
— that file is the brief for the Claude doing the values). `custom` pins are at Shopify's cap of
20, which is why four of the 18 are unpinned. One product is filled as the worked example:
Alocasia Black Velvet Pink Variegated. Theme **`AgaPlantz 2026 — plant profile (metafields)` =
`190043619407`** (from MAIN `189923491919`, which the owner published on 1 Nov with the
November ladder). Verified: all four files match the repo by checksum, both templates render
with no Liquid error, screenshots at 390 and 1280. Screenshots at 390 and 1280 again after the merge; the
band is `x: 0`, full viewport width. The block sits in a `_blocks` section, not in
`main`, so it does **not** re-render on variant change — the "What you'll receive" tiles are
per product, not per stage (see the plan file for how the two templates split that).

## Availability chance — the buy-box badge (4 Nov 2026)

The owner, same evening: orders are taken and *"most of the time those plants are not
available at the lab and we have to refund it… we cannot stop taking orders"*, so a per-plant
**availability chance** goes in the two places they marked on a screenshot — under the price,
and under "More payment options" — set by *another* Claude session that runs the batch
payments and supplier confirmations. *"It should not look like it stayed out of the TikTok
shop"*; a small (?) opens a pop-up explaining what the chance is and how the last batch went.

`blocks/availability-chance.liquid`, a theme block inside `main` → `product-details` on both
product templates. It was first placed twice (under the price and under the buy buttons);
the owner then said *"we only want to make at one spot… above description"*, then, seeing it there,
*"move this section above, so when person is clicking a different variance, it's changing…
change the background color, because this one is just mixing up with everything… that
question mark is not looking good."* So it is **one block, `availability_bottom` (layout
`card`, four-bar meter, last-batch line), directly after `variant_picker_R3rGDr`**, where a
stage tap visibly changes it; sage `#E8EDE1` (a `card_bg` setting) with a 4px left bar in the
level's colour so it no longer blends with the sand guarantee card; and the trigger is an
info icon plus "How it's decided" (`help_label`), not a circled "?". The `inline`
layout still exists in the schema if a one-liner is ever wanted under the price. **It follows the selected variant, and that needed its own
listener.** The owner: *"when I go from tissue culture pre-order to ready to ship, it does not
change for me."* **Horizon does not re-render `product-information` on a variant change** —
`variant-picker` fetches `?variant=…&section_id=…`, parses it, and dispatches a bubbling
`ProductSelectEvent` (`StandardEvents.productSelect` from the `@shopify/events` import map,
name `<prefix>product:select`) whose `event.promise` resolves to `{ detail: { html, resource } }`;
then **each component morphs only its own piece** (`product-price`, `product-form-component`,
`product-inventory`…). A theme block that merely reads the variant in Liquid stays stale. So
the block always renders a `[data-agav-host="{{ block.id }}"]` wrapper (empty when there is
nothing to show) and a `<script type="module">` imports `StandardEvents` and, on
`productSelect` (capture, on `document`, guarded by `window.__agavInit`), replaces every host
with its counterpart from `detail.html`. Verified in a real browser by checking the stage
radios: Pre-Order → "High" card, Ready to Ship → "In stock, ready to ship", Acclimated (sold
out) → empty, back to Pre-Order → the card again. The `?variant=` URL test used before only
proved the server render. **The same applies to `blocks/acclimation-guarantee.liquid`** —
the note under 30-Day Plant Guarantee that Horizon "re-renders the product-information
section on variant change" is wrong for theme blocks; the guarantee tier on Devil Monster
very likely does not switch between $150 and $240 on a tap either. Not fixed; flagged to the
owner. Levels: High (moss dot, 3 bars) · Medium (amber) · Low (terracotta) · Not available
(grey); the `Confirmed` choice still exists on the definition but **renders as "High" with a
full meter** — the owner (5 Nov): *"Don't you think this line gives too much surety that it
will be confirmed for this batch? We should say like high and it was confirmed last batch"*,
and *"the November batch has to still go through the lab at the end of this batch close"*, so
nothing is confirmed while a batch is open. The last-batch line reads `last_batch_result`:
`Available` → "Last batch: confirmed by the lab and every order shipped.", `Partially
available` / `Not available` → their lines, **`Not ordered` → no line at all** (a plant that
was not in the last batch must not read as unavailable). The same evening the batch
session's first pass was corrected in the data: 117 products carrying `Confirmed` plus the
note "Confirmed by the lab for the November batch." were set to `High`,
`availability_updated` `2026-11-05`, note deleted (`metafieldsSet` ×2 per product and
`metafieldsDelete`, 30 products per call; `metafieldsDelete`'s `userErrors` is a plain
`UserError` with no `code` field). Notes must never be forward-looking — the rule is in the
handoff.

**Removed from the page an hour later (5 Nov).** The owner, seeing the card on the preview: *"I
would say just remove this section. It's making things ugly."* So `availability_bottom` is
`disabled: true` on both `product.json` and `product.tissue-culture.json` — settings intact,
still in `block_order`, the block file and the four metafield definitions untouched, and the
batch session keeps filling the values. Bringing it back is one flag. The owner was not shown
a variant without the last-batch line first; if it ever returns, try the `inline` layout
(one line under the price, no card) before the card. The (?) is a native `<details>`; the pop-up
is absolutely positioned under the row and a document-level listener (guarded by
`window.__agavInit`) closes it on outside click or Escape. **Nothing renders while
`custom.availability_chance` is blank**, so the catalogue is unchanged until the batch session
fills it. Four definitions were created; the field table, ids and a suggested rule for setting
the level are in `docs/plant-identity-handoff.md` (the file the owner hands to the batch
session and then to the A-to-Z identity session). Example values are on Black Velvet Pink.
Same draft theme `190043619407`.

## Crochet line (6 Nov 2026) — storefront only, nothing live yet

A second product session created 15 **DRAFT** crochet products (type `Crochet`, option
`Colour`, no photos yet, $12.99–$79.99) and six **unpublished** automatic collections:
`crochet` (all, tag `Crochet`), `crochet-flowers`, `crochet-bags`, `crochet-charms-keychains`,
`crochet-hangings-wreaths`, `crochet-gifts-under-25` (tag `Under 25`). Rules from the brief:
everything stays under the AgaPlantz name; say *"hand-crocheted by our artisan partner"*, never
"handmade by us" or "made in Canada"; **crochet is excluded from every discount**, so no sale
badges, no "% off" copy, never in the ON SALE row; products and collections stay unpublished
until Agam says the line is live; **crochet must not sync to Etsy** (DPL Etsy Integration app,
not the theme).

Draft theme **`AgaPlantz 2026 — crochet line` = `190192943183`** (from MAIN `190146576463`):

- **Menu.** `menuUpdate` is live-immediate and the collections 404 until published, so the live
  `main-menu` was **not** touched. A copy, **`main-menu-crochet`** (`gid://shopify/Menu/275458555983`,
  made with `menuCreate`), is the live menu plus a **Crochet** item after Accessories with the
  five sub-links (Flowers / Bags / Charms & Keychains / Hangings & Wreaths / Gifts Under $25).
  `sections/header-group.json` → `header-menu.menu` points at it on the draft, so publishing the
  theme switches the menu. **Anything Agam adds to `main-menu` in the meantime has to be copied
  to `main-menu-crochet` by hand.**
- **Homepage.** `sections/crochet-feature.liquid` as `crochet_feature` in `templates/index.json`,
  after `why_agaplantz` (sage) and before the Loox carousel — sand band. Eyebrow / heading
  "Flowers that never wilt" / one line / moss "Shop crochet" button; a product row from `crochet`
  (first available variant, **no compare-at, no badge**, hidden by itself while the collection is
  empty); up to four `tile` blocks (collection, title, line, image with fallback to the
  collection image, then a sage glyph — the crochet collections have **no images yet**, so the
  glyph shows); a moss "Gifts under $25" strip; and a note "Every piece is hand-crocheted by our
  artisan partner. Crochet is not included in plant discounts." All links are set explicitly in
  the template (`cta_url`, `gift_url`, each tile's `link`) because an unpublished collection
  resolves to blank in Liquid and the button and strip vanished on the first preview.
- **Product template `product.crochet`** (`templates/product.crochet.json`), from `product.json`
  minus the pre-order/ready-to-ship card (`ai_gen_block_910fa12`), the guarantee block, the
  price-lock note, the disabled availability card and the whole plant-profile `_blocks` section;
  plus a centred trust line under the price ("Hand-crocheted · Never needs water · Ships from
  Brampton", a `text` block) and a **"Complete the gift"** `stage-products` row on
  `crochet-gifts-under-25` (blank `stage_match`, `allow_fallback`) before "You may also like".
  Gallery, Colour picker, price, quantity, buy buttons, description and both Loox sections kept.
  The heat-pack and substrate offers are cart-only (rendered from the guarantee snippet in cart
  context), so nothing else was needed. **The product session assigns the suffix `crochet`** to
  the 15 products. Verified with `?view=crochet` on the self-watering pot: no guarantee, no
  price lock, no plant profile, trust line and gift row present, no Liquid error. Shopify
  re-serialises this template on upload (13.5 KB stored vs 22.6 KB sent) — compare parsed JSON,
  not checksums.
- **Not done / cannot be done yet:** the six collection pages **404 on the preview** until the
  collections are published (check them at 390px then; the standard `collection.json` is used,
  filters today are Availability + Price + sort — a Colour filter is a Search & Discovery app
  setting, not theme work); search for "crochet"/"rose"/"bag" only works once the products are
  active; **all 15 crochet products already sit in `popular`** (its rules admit anything in
  stock that is not a Service), so they will join the homepage "Popular right now" row the day
  they go active unless a `TYPE != Crochet` condition is added — Agam's call, not made.
- **Drawer accordion + yarn-styled Crochet item (same evening).** The owner, seeing the drawer:
  *"make a crochet with a crochet string so it looks different and eye-catching… a drop-down
  menu will be great, because right now it's like automatically opening."* So `header-menu`
  has `drawer_accordion: true` (every parent collapses to a +/− row; Plants collections too),
  and a **`custom-liquid` section `crochet_menu_style` sits first in `header-group.json`**
  carrying only a `<style>`. First pass: the Crochet label turned terracotta with a yarn-ball
  icon and a chain-stitch underline. The owner: *"Use a pink crochet string. Write that crochet
  with the pink string, not like under it."* So now the label (desktop `.menu-list__link-title`,
  drawer `#HeaderDrawer-crochet > .menu-drawer__menu-item-text`, matched by the
  `/collections/crochet` href) is replaced by a **wordmark**: the word "Crochet" set in Pacifico,
  converted to a path with fontTools and filled with a diagonal two-pink stripe pattern
  (`#E8A3BE` / `#CF6F96`, edge `#B8577D`) so it reads as twisted yarn, with a ball of yarn at
  the start, a thread running into the C and a loose tail after the t. It is one inline SVG
  data URI (~5 KB) used as the span's background; the text stays in the DOM (transparent,
  indented away) for screen readers. 1.5em tall in the desktop bar, 1.3em in the drawer. The
  SVG is also in `brand/crochet-yarn-wordmark.svg`; the generator was fontTools + Pacifico from
  Google Fonts, not kept. The section's
  own wrapper is hidden by id (`[id$="__crochet_menu_style"]`; in a section group the DOM id is
  `shopify-section-sections--<group>__<key>`, not `shopify-section-<key>`). Verified in a
  browser at 390 and 1280.
- **Homepage band in the same pink (same evening).** The owner, on the band's screenshot:
  *"Change it now"* — so `crochet-feature.liquid` now shows the same yarn "Crochet" wordmark
  above the heading (`show_yarn` setting, the SVG data URI repeated in the section's
  stylesheet) and each tile's fallback icon is a pink crochet drawing instead of the grey
  sun: a `glyph` select per tile (yarn / flower / bag / charm / gift), drawn once in `<defs>`
  and `<use>`d three times — dark outer stroke, light inner stroke, dashed mid stroke — so
  the line reads as twisted yarn; the icon panel is blush `#F6E7EE`. Tiles still prefer a real
  image when one is set. The owner also asked *"do you have product reviews as well"* — yes,
  `product.crochet.json` keeps both Loox blocks.
- **Band trimmed on the owner's marks (6 Nov, later):** the moss "Gifts under $25" strip is
  off (`show_gift: false`, the setting and markup stay), the tiles are the new `tile_size:
  compact` mode (one 52px row each: icon, title, arrow, no line) and the band background is
  light pink `#FBEEF3` — *"make them small and change the background into a light pink color
  so it looks pretty."* The owner then circled the compact rows: *"It's not giving what it's
  need to give."* So the tiles are now **`tile_size: photo`** (the default): three small photo
  squares side by side, name underneath, no line and no arrow; 3 across at every width (4 tiles
  go 2×2 on a phone). The photo is the tile's `image` setting, else the collection image, else
  **the first product photo in that collection** (`for tp in t_coll.products limit: 12`) — the
  crochet collections still have no images of their own, so today every tile shows a product
  shot. The pink glyph only appears when a collection has no photographed products at all.
  `regular` and `compact` tile modes still exist in the editor.
- **Products and collections went live on 6 Nov 21:00Z, on the owner's say-so** (*"publish all
  the products, so we see like what's going on and how things are looking"*): all 15 products
  set ACTIVE with `templateSuffix: crochet` (`productUpdate`, aliased ×15) and published to the
  **Online Store only** (`publishablePublish`, publication `164313432143`; not Shop / TikTok /
  Meta / Google / Microsoft), and the six crochet collections published to the Online Store the
  same way. By then the product session had attached photos to most products (Daisy Granny Bag
  still had none). **What this exposes on the live site while the theme is still a draft:** the
  product and collection URLs work for anyone who has them, store search will find them once
  indexed, and they are eligible for the `popular` collection (none in the live "Popular right
  now" row yet — BEST_SELLING puts unsold items last). The live menu, homepage and
  `/collections` page do not link them. **Etsy still has to be excluded in the DPL app** before
  this is announced. Verified on the preview after publishing: band shows the product row,
  `/collections/crochet` renders the cards with Filter + Price/Availability, the Rose Pot
  product page uses `product.crochet` (trust line, Colour buttons, gift row, no guarantee).
- Also on this draft: the announcement bar flipped for 6 Nov (`announcement_sale` disabled,
  `announcement_sale15` enabled) — the 20% slide was still live a day after the discount ended.

## Reviews on product pages — Loox only, since 25 Oct 2026

**The native "What collectors say about AgaPlantz" wall (`store_reviews`) is gone from the
product pages.** The owner asked for it on 21 Oct: *"we only gonna keep the one division
which automatically updates each review"* — the Loox widget. By then they had switched
Loox from `product_reviews_only` to showing the whole store's reviews ("64 Reviews", every
plant), so the two walls sat one above the other saying the same thing and ours needed its
handle list maintained by hand. Removed from both `templates/product.json` and
`templates/product.tissue-culture.json` (`product.subscription.json` never had it); the
section file itself is untouched and the homepage no longer used it either, so the block
is now unreferenced — delete it from admin if a cleanup pass ever happens.

**There are three product templates now**: `product.json`, `product.tissue-culture.json`
(most of the catalogue) and `product.subscription.json` (the mystery box). Check all three
before assuming a product-page change has landed; a fourth can appear at any time, so run
`files(filenames: ["templates/product.*"])`.

How it was verified: both templates re-read from the draft matched the local md5s (**two
of two returned** — the lie to watch for is a file silently dropped, see below), and three
preview product pages — one per template — rendered with no Liquid error and no trace of
the wall, while the live page still carried it.

The repo copies of these two templates were stale before this (the owner had edited them
in the theme editor); both are now the live file minus the section, header comment
stripped, so the next edit can start from the repo again.

## "What is tissue culture?" — the education page (27 Oct 2026)

The owner circled the gap between the genus tiles and the plant spotlight and asked for a
*"what is tissue culture, learn more"* entry there, leading to *"a page where we are
explaining TC from start to end, from policy links to anything that will educate people
about our business and TC."*

**The page** is `/pages/tissue-culture` (`gid://shopify/Page/167359774799`, title "What is
tissue culture?", template suffix `tissue-culture`), rendered by `sections/tc-guide.liquid`
through `templates/page.tissue-culture.json`. The split is deliberate: the **opening prose is
the Shopify page body**, so the owner edits it in admin on a phone, and **everything
structured is a block** in the theme editor — six block types, rendered in order, with
consecutive blocks of one kind wrapped as a group:

| Block | Renders as | Used for |
| --- | --- | --- |
| `chapter` | numbered node on the thread + eyebrow + h2 + one line | the eight section headings |
| `step` | numbered circle + title + text; a run becomes an `<ol>` | how TC is made (4), the pre-order journey (5) |
| `card` | bordered card, `featured` fills it moss | pre-order / ready to ship / mature; guide + free kit; guarantee |
| `faq` | native `<details>` accordion | the honest small print (7) |
| `link` | link card with an arrow; a run becomes a grid | the eight policy and guide links |
| `cta` (limit 1) | sand band, two buttons | shop ready to ship / browse pre-orders |

| `stat` | sand tile with a big Lora number and a label; a run becomes a row | the four guarantee numbers |
| `tile` | icon in a sage circle, title, one line; a run becomes a row | the five acclimation stages, the shipping facts |

The grouping is done in Liquid by watching the block type change (`open` tracks the current
run and closes it before a different kind starts), so the owner can reorder or add items
freely and the markup stays valid.

**Visuals, first pass (same day).** The owner saw the first preview and said it was *"just a
read"*, so every `step` got an `icon` from a 22-icon inline SVG set (keyed by name inside
`icon_paths`, no asset upload), `stat` and `tile` blocks carry the numbers and the process, and
three mystery-box cut-outs were placed beside chapters.

**Built to be skimmed, not read (second pass, same day).** The owner called those chapter
pictures *"plant picture for no reason"* and asked instead for motion that connects everything
as you scroll, with copy short enough that nobody has to read it all. So: the chapter images are
gone (the `chapter` block has no `image` setting any more), every block's text is one or two
short sentences, the Shopify page body is a single sentence, and the page is **one thread**. A
2px clay line runs down the left of the body (`.agtc__spine`; gutter `--agtc-g` is 72px on
desktop, 56px on a phone) and fills moss as the reading line, 62% down the viewport, passes —
a 30-line script writes `--p` to `.agtc__body` on each frame. Every chapter is a numbered node
on the thread and every step's icon sits on it; each mark gets `is-lit` (moss, one-shot pulse
ring) once the line passes it. Everything else is `[data-reveal]`: hidden until an
`IntersectionObserver` sees it, then rises in, staggered by `--i` within its group. `stat`
values count up from zero (`data-count`; the number is parsed out of the string, so `$14.99`
and `30 days` both work). The hero plantlet floats and parallaxes; it is the one picture left
because it *is* the subject — clear `hero_image` for a text-only hero. The CTA band spans the
full column and caps the thread. Without JavaScript, or under `prefers-reduced-motion`, nothing
is hidden, the thread is fully drawn and the marks are lit; the script adds `agtc--js` only when
it will animate, so a theme-editor re-render (which does not re-run inline scripts) simply shows
everything. Verified at 390px by scrolling a local render and reading `--p`, the lit-mark count
and the revealed count back at five positions; desktop checked at a 7000px-tall viewport. Five
icon tiles fit one desktop row at `minmax(min(118px,100%),1fr)`; 130px wrapped the fifth onto
its own line.

**Shopify caps a section at 50 blocks**, and the first visual pass hit 52. Two were folded away:
"Free over $180" became the second line of the Canada-wide tile, and the local-pickup
question was dropped (it is on the FAQ page, which the links grid points at). 50 blocks as
shipped — **the page is full**. Adding anything means removing something, or a second
section on the template.

**Every fact on it was lifted from pages the owner already published** — FAQ, Pre Order,
30-Day Plant Guarantee, About, the shipping and refund policies, the Acclimation Guide — so
nothing new was asserted about the business. Two places were deliberately vague where the
site contradicts itself: dispatch days ("early in the week, never over a weekend" — the
shipping policy says Mon–Wed, the product-page card says Mon–Thu) and the kit's name (the
product `tissue-culture-starter-kit` is titled "Tissue Culture Substrate"; the page calls it
the starter kit, as the product card does). The TC process steps are general horticulture,
phrased around "our laboratory partners" as the Pre Order page does — never "our lab".

**The page went live the moment it was created** (`pageCreate`, published) — it is not in
any menu, and until the draft theme is published the live theme has no
`page.tissue-culture.json`, so it falls back to `page.json` and shows only the prose. That
is a readable page, not a broken one, which is why the body carries real copy rather than a
placeholder. Not added to the main menu: `menuUpdate` is live-immediate and the owner was
not asked yet.

**The homepage entry** is `sections/tc-learn-more.liquid` as `tc_learn_more` in
`templates/index.json`, directly after `collections_genus` — a slim sage strip (eyebrow,
one heading, one line, "Learn more →", moss leaf icon), all settings. Sage between the cream
genus row and the sand spotlight keeps the bands alternating. It is a single `<a>`, so the
whole strip is the tap target on a phone.

## Pre Order page: same thread, same day (27 Oct 2026)

*"Let's redesign pre order detail as well."* `/pages/pre-order` (`gid://shopify/Page/115038879823`,
suffix `pre-order`) was five AI-generated blocks of long paragraphs plus the pricing-policy text
block. `templates/page.pre-order.json` is now a single `tc-guide` section — the section was
renamed **"Guide page (thread)"** in its schema because it serves two pages now; the file is
still `sections/tc-guide.liquid`. 40 blocks: why-early tiles, the cut-off chapter with four
stats (2–3 weeks · 2 days · 100% refund · Locked), the five-step journey, pricing tiles (locked
at checkout · re-set each batch · nearly 200 plants cheaper), why-a-lab-batch tiles, five
questions, three cards (TC page · Acclimation Guide · guarantee), five policy links, CTA to the
pre-order collection. Every fact came off the old blocks; the only new line is "next batch opens
15–30 days after a cut-off", which the announcement bar already says. The page body (was empty)
is one sentence, set with `pageUpdate`. **No hero picture** — it was the pink plantlet, the owner saw it live and said *"just remove
it"*, so `hero_image` is blank (the TC page keeps its green plantlet; nobody objected to that one). **The cut-off date now lives in `ch_cutoff.heading`** ("Order by 31
October") — the six-places table is updated; it is still one place on this page, deliberately
not repeated in a stat.

**Desktop Safari did not move (same day).** The owner's screenshot: thread filled a few pixels,
every mark unlit, cards visible. Cause: Horizon does not scroll the window on desktop — `body`
is `overflow: hidden` and `.page-wrapper` is the scroller — so `window.addEventListener('scroll')`
never fired, while the `IntersectionObserver` reveals (viewport-relative) kept working. Phones
scroll the window, which is why it worked there. Fix, three layers in the section script: a
capture-phase `scroll` listener on `document` (scroll events don't bubble but do capture, so
this hears any element), a second `IntersectionObserver` on the marks with
`rootMargin: 0 0 -38%` that lights them as they cross the reading line, and a per-frame
`getBoundingClientRect().top` check on the body that runs `frame()` only when the body has
moved. Reproduced in the local harness, which has the same inner scroller when Horizon's JS is
blocked: before the fix `--p` stayed at 0.0048 after scrolling `.page-wrapper`; after, it read
0.46 and 0.98 with 9 then 13 lit marks. **Any scroll-linked effect in this theme must not
assume the window scrolls.**

## Halloween sale theme (27 Oct 2026) — temporary, gone when the next theme is published

A separate draft, **`AgaPlantz 2026 — Halloween sale` = `189700112463`**, duplicated from MAIN
`189569040463` on 27 Oct and carrying **only** the Halloween changes. **The owner published it
the same evening (it became MAIN in place — same id, role flipped).** Today's page work (TC
page, Pre Order page, Safari fix) was deliberately left off it, on draft `189688381519` —
and the owner immediately noticed the pages were "missing" and wanted them live too. So a
third theme, **`AgaPlantz 2026 — Halloween + tissue culture pages` = `189701881935`**, is the
Halloween MAIN plus `tc-guide.liquid`, `tc-learn-more.liquid`, both page templates and the
`tc_learn_more` strip inserted after `collections_genus` (`merged/index.json` in the repo is
that homepage: Halloween section *and* the strip). The owner publishes that one. **They did, within the hour** — then asked for the
Pre Order hero photo to go, which made a fourth theme, `AgaPlantz 2026 — Halloween + pages, no
pre-order photo` = `189702373455` (MAIN minus that one picture). The same template went onto
the clean draft `189688381519` so the post-Halloween publish carries it too. The owner then
published the *clean* draft by mistake ("Now Halloween is gone"), re-published
`189702373455`, and asked for a better pumpkin — fifth theme, `AgaPlantz 2026 — Halloween,
drawn pumpkin` = `189703094351`, MAIN plus the new `stage-products.liquid`. Then, on 28 Oct, the
cancellation FAQ rewrite made a sixth, `AgaPlantz 2026 — Halloween, 48-hour cancellation FAQ`
= `189743595599` (MAIN plus the three page templates); the same three went onto the clean
draft `189688381519`. **Each ask has
meant a new duplicate because the owner publishes within minutes and the API cannot write to
MAIN**; check `roles: [MAIN]` before every upload.

**Take-down after 1 Nov:** done on 1 Nov, see **20% off everything** below — the owner
publishes `189688381519`. Draft `189688381519` (copied from MAIN *before* Halloween, with
the pages) is still the clean post-Halloween theme — publishing it removes the slide and the
section in one step: *"I want just Halloween to be gone."* The badge expires on its own
either way. The `announcement_halloween` slide says "Ends Sunday Nov 1" and has no expiry —
stale from 2 Nov until the clean draft is published. Anything the owner edits in the theme editor between now and then lives only on
the Halloween theme and would need carrying across; compare md5s first, as always.

**Scope was cut on the owner's say-so the same evening.** A first pass followed the handoff
doc fully (Halloween hero with the Devil Monster photo, two buttons, a row directly under the
hero, a line on the Devil Monster spotlight). The owner: *"Do not change the home page, only
put a section down it."* So the hero, spotlight and every other homepage section are
byte-for-byte the live ones, and the homepage differs from live in **one** added section.

The brief came from a Claude Docs handoff ("Halloween Sale — Homepage Handoff"): 49
spooky-named plants in `halloween-spooky-plants` (`gid://shopify/Collection/493327056975`,
manual sort, in-stock first), 20% automatic discount `Halloween Sale — 20% off Spooky Plants`
(`gid://shopify/DiscountAutomaticNode/1536364445775`), scheduled Oct 28 04:00Z → Nov 2
04:59Z, stacks with order codes. **The owner said they would move the discount start to
today (27 Oct) themselves** — the badge below already assumes that. If the start is not
moved, the storefront promises 20% that checkout will not give until Wednesday: the same
trap as the ladder.

Files are kept in **`halloween/`** in the repo, mirroring theme paths, so they never touch
`theme/`:

| File | Change |
| --- | --- |
| `sections/header-group.json` | `announcement_halloween` first in the bar, linked to the collection; `announcement_early` ("Order Early, Pay Less") set `disabled: true` — its ladder ended 20 Oct, so it was promising a discount that no longer exists |
| `templates/index.json` | the live file plus one section: `products_halloween`, a `stage-products` row on the collection, **after `custom_liquid_KL8FyB`** (the countdown) and before the genus tiles. Background warm charcoal `#3B342C` with `halloween_decor: true` — near-black `#1f1a14` was "too dark", sage was then too light: *"Black is fine but not dark and add lil Halloween decoration."* The decoration is a checkbox setting added to `stage-products.liquid` **on this theme only**: four small inline-SVG bats drifting in the corners (two hidden on phones), a shaded pumpkin illustration (gradient lobes, stem, leaf, tendril; ids suffixed with `section.id`) before the heading — the first outline icon "looked fake", "20% off" and the View-all link in pumpkin `#F0A04B`; `prefers-reduced-motion` stops the bats, heading "Spooky plants, extra 20% off" (the owner: some plants already carry a compare-at, so plain "20% off" read as the sale they already had — every Halloween string says **extra**), link "Shop all 49 · ends Sunday", 8 cards, `allow_fallback` |
| `snippets/halloween-sale-badge.liquid` | new. Renders only for products in the collection and only between `2026-10-27T04:00:00Z` and `2026-11-02T04:59:59Z`, so it switches itself off. `context: 'card'` is a dark pill top-left of the photo; `'product'` is a dark bar on the product page |
| `blocks/acclimation-guarantee.liquid` | one `render` line above the guarantee div (product pages) |
| `snippets/product-card.liquid` | core Horizon; one `render` line above `{{ children }}` (collection pages) |
| `sections/stage-products.liquid` | one `render` line after the Sale badge (homepage rows — these use their own cards, not `product-card`) |

Verified on the preview: six of six checksums, no Liquid errors, the hero is the live one,
the homepage carries the slide and the section; `/collections/halloween-spooky-plants`
renders 24 card badges; the Devil Monster page carries the product badge and Bambino Pink
(outside the collection) carries none. Two sale plants have no photo at all (Alocasia Aranea,
Philodendron Black Billietiae) and show the placeholder.

## 20% off everything, 1–5 Nov 2026 — and the Halloween take-down

The owner, 1 Nov morning: *"The prices has changed. Please look at the prices of the plant
and change as required on homepage. And let's issue a 20% discount on all plants. Today and
remove the Halloween one. The discount will be 20% until November 5."*

**Prices.** They had repriced the catalogue at 01:24 Toronto that morning — 467 active
variants touched in one pass, mostly the pre-order TC variants, and only 20 of those still
carry a compare-at (45 active variants shop-wide now have a compare-at above price, so the
`Save X%` badges and the `on-sale` collection have mostly emptied). **Nothing on the
homepage hardcodes a price**: the spotlight, the stage-product rows and the mystery-box tiers
all read live variants, so the page followed the repricing by itself. The one price *claim*
on the homepage, the "Nearly 200 Plants Now Cheaper" announcement slide (and the same tile on
the Pre Order page), was re-measured against `catalog-backup/products-full.jsonl` the way the
Batch pricing notice describes: **192 cheaper (median −31%), 268 unchanged, 43 higher** across
503 matched active variants (the first 1000 of 1083 variants; the last page is Begonias and
ready-to-ship stock with no baseline). Still true, left alone. Devil Monster's spotlight line
"On sale while this batch is open" also still holds — its $306 compare-at survived.
`bulkOperationRunQuery` runs but the connector withholds the download URL, so the variants
were paged with `productVariants(first: 250)` instead (five pages).

**The discount.** `20% Off All Plants — Nov 1 to 5` (`gid://shopify/DiscountAutomaticNode/
1537379106895`), automatic, 20% off all items, `2026-11-01T04:00Z` → `2026-11-06T04:59:59Z`
(Nov 1 00:00 → Nov 5 23:59 Toronto, EST), one-time purchases only so the mystery-box
subscription is excluded, `combinesWith` order **false** / product **false** / shipping
**true** — the Labour Day settings, so `WELCOME10` and the Loox codes cannot stack on top
(the owner's own Halloween discount *did* allow stacking; flagged, not decided for them). The
Halloween discount `1536364445775` was **deactivated** at 15:55Z the same morning (it would
have run to Nov 2 05:00Z) — *"remove the Halloween one"*.

**The theme.** The clean post-Halloween draft `189688381519` is the take-down theme, as
planned: a full file-list comparison against the Halloween MAIN (`189887840335`, the 30 Nov
theme the owner published within the hour) showed the two differ in exactly the six Halloween
files plus **one template the owner had created in the editor on the live line on 31 Oct,
`templates/product.accessory.json`** (used by `self-watering-pot-humidity-dome`, product type
Pots, four pack-size variants — a Horizon product-information template with the Subscriptions
app block and two Loox sections). It was carried onto the clean draft — `themeFilesCopy` is
refused when the *source* is the live theme, so it was re-typed into the repo with the editor
header stripped and uploaded; the product page renders on the preview with no Liquid error.
The sale slide `announcement_sale` ("20% Off All Plants — Applied Automatically at Checkout •
Ends Thursday, November 5", link `/collections/all`) is **first** in the clean draft's bar,
cloned from `announcement_labour_day`; it has no expiry, so **disable it on 6 Nov** — the
same trap as every slide before it. Publishing `189688381519` removes the Halloween slide,
row, badge and pumpkin in one step and carries everything else (pages, logo, favicon,
magic-mix guide, 30 Nov cut-off, 48-hour cancellation answers). Verified on the preview: sale
slide present, zero matches for "Halloween" or "Spooky", deadline `2026-11-30T23:59:59-05:00`,
no Liquid errors. The storefront rate-limits preview fetches (HTTP 429 after ~15 in a few
minutes) — space them out.

## November 2026 promo calendar (set 1 Nov) — four discounts, one theme, nothing to flip but slides

The owner pasted a table the same morning: **Nov 1–5** 20% off all plants, stacks with codes ·
**Nov 6 – Nov 26 7:59 pm** 15% off all plants, stacks with codes — **revised that evening to
Nov 6–15 at 15% and Nov 16 – Nov 26 7:59 pm at 10%** (*"from 1 to 5 20%, then 5 to 10 15%,
then 5 to 15 15%, then 15 to 26 10%"* — read as 6–15 / 16–26, the October shape) · **Nov 26 8 pm – Nov 30
11:59 pm, Black Friday** ready-to-ship 40%, acclimated 30%, pre-orders under $150 20%,
pre-orders $150+ 10%, free mystery ready-to-ship plant on a $150+ pre-order, no code stacking
(shipping only) · **Nov 30 midnight** batch closes. "All plants (pre-order, RTS, acclimated)"
was first taken literally (the three stage collections); the owner then widened the 20% to every
plant — see the row. The 15% was widened the same way so the ladder card can say "all plants". All times
Toronto, EST. **Both the 20% and the 15% need a $100 subtotal** — the owner added that
after seeing the cards (*"and order above 100 only will get the discounts"*), the same
`DiscountMinimumSubtotal` the October ladder used; the Black Friday tiers carry no minimum
(the free plant has its own $150 rule) — nobody asked for one there. The cards and the two
slides say "Orders $100+".

| # | Discount | Window (UTC) | Scope | Stacks |
| --- | --- | --- | --- | --- |
| `1537379106895` | 20% Off All Plants — Nov 1 to 5 | 11-01 04:00 → 11-06 04:59:59 | **all items** (one-time purchases) — it was scoped to the three stage collections for an hour, then the owner: *"Just make a one discount. We are giving 20% discount from 1 to 5 on each plant… on each genus, like acclimated or tissue culture or whatever, pre-order"*, so every stage and the mature specimens are in; the pot accessory rides along, the mystery box is out by being a subscription | order codes **yes** (changed from the Labour Day setting on the owner's say-so) |
| `1537384513615` | 15% Off All Plants — Nov 6 to 15 | 11-06 05:00 → 11-16 04:59:59 | **all items**, $100 min | order codes yes |
| `1537439006799` | 10% Off All Plants — Nov 16 to 26 | 11-16 05:00 → 11-27 00:59:59 | **all items**, $100 min | order codes yes |
| `1537385168975` | BF — Ready-to-Ship 40% | 11-27 01:00 → 12-01 04:59:59 | **73 variants** | other BF tiers only |
| `1537385201743` | BF — Acclimated 30% | same | **15 variants** | same |
| `1537385234511` | BF — Pre-Orders $150+ 10% | same | **81 variants** | same |
| `1537386053711` `…184783` `…217551` `…414159` `…446927` | BF — Pre-Orders Under $150 20% (1–5 of 5) | same | **492 variants in five discounts** | same |
| `1537386152015` | BF — Free Mystery Ready-to-Ship Plant With $150+ Pre-Order (BXGY) | same | buys ≥ $150 from collection `pre-order`; gets 1 × product below at 100% off, one per order | same |

**Why Black Friday is variant lists, not collections.** Stage is a variant and the collections
hold products: Devil Monster sits in both `pre-order` and `ready-to-ship-tissue-culture`, so
collection-scoped 40% and 20% discounts that combine would both land on its pre-order line
(52% off), and ones that don't combine would let only one discount apply to the whole order,
so a mixed cart loses a tier. `productVariantsToAdd` targets the variant itself; the four
buckets (`Ready to Ship` / `Acclimated` / `Pre-Order` < $150 / ≥ $150 in the variant title and
price) are disjoint, so they are all `productDiscounts: true` and combine with each other, and
every active code in the shop is ORDER-class (checked: 40 of 40), so `orderDiscounts: false`
is what makes "no code stacking" hold. **Shopify caps a discount at 100 hand-picked variants**
("You've selected 250 variants, but the limit is 100") — hence five discounts for the 492
cheap pre-orders. Lists were built from the 1 Nov prices with RTS and acclimated limited to
in-stock variants; they are in `catalog-backup/black-friday-2026-variant-lists.json` with the
discount ids. **Rebuild them on 26 Nov** (a pre-order repriced across $150, or a ready-to-ship
restock, is in the wrong tier or no tier until then): `productVariants(first: 250)` paged five
times, bucket, then `discountAutomaticBasicUpdate` with `productVariantsToAdd/Remove`.
`bulkOperationRunQuery` runs but the connector withholds the download URL.

**The free plant is the one soft spot.** A BXGY "buys" list has the same 100 cap, so it uses
the `pre-order` *collection* — product-level — which means $150 of ready-to-ship variants of
pre-order products also earns the gift. Flagged to the owner, not fixed; RTS stock is 73 units
across 61 products. The gift is a new product, **`mystery-ready-to-ship-plant`**
(`gid://shopify/Product/15506497208399`, $39, type Mystery, **DRAFT**, no photo) — Shopify
BXGY does not add the gift to the cart, the customer adds it and checkout zeroes it, so **the
owner must set it ACTIVE (and give it a photo) before 8 pm on 26 Nov** or nobody can claim it.
Whether the $150 is judged before or after the 20%/10% line discounts was not verified — test
a cart on the 26th. The pre-order page body / tc-guide do not mention the gift.

**Theme.** All on the clean draft `189688381519`, which is now also the take-down theme (see
the 20% section above). Announcement bar (the slides duplicate the ladder; keep them anyway, the bar is on every
page and the ladder only on the homepage), in order: `announcement_sale` (20%, live),
`announcement_sale15` (**disabled — enable 6 Nov, disable the 20% one**), `announcement_sale10`
(**disabled — enable 16 Nov, disable the 15% one**), `announcement_bf` (**disabled — enable
26 Nov 8 pm, disable the 10% one**), then the old slides. Slides take no
Liquid, so those flips are by hand in the theme editor. The **countdown eyebrow, by contrast,
switches itself**: `custom_liquid_KL8FyB` compares `now_s` against three EST boundaries
(`2026-11-05T23:59:59-05:00`, `2026-11-26T19:59:59-05:00`, `2026-11-30T23:59:59-05:00`) and
printed the current offer — for about an hour. Then the owner, looking at the countdown
on their phone: *"last time we advertised our discounts here, so we need to do that again
here"* — they wanted the **ladder cards** back under the digits, so the eyebrow went back to
"New batch now open" and the ladder was rebuilt for November. **It is clock-gated, not
day-counted**: `batch_start`/`day_now` are gone; each card compares `now_s` with an EST
boundary (`sale20_end`, `sale15_end`, `bf_start`, `bf_end`). Cards: **Nov 1–5 · 20% off ·
Orders $100+** (Now until the 5th, then gone), **Nov 6–15 · 15% off · Orders $100+** (Now from
the 6th, gone after the 15th), **Nov 16–26 · 10% off · Orders $100+** (Now from the 16th, gone
after 7:59 pm on the 26th), and **Nov 26–30 · Black Friday · Up to 40% off ·
Ready to ship 40% · Acclimated 30% · Pre-orders 10–20%**, which **does not render before 8 pm
on the 26th** — the owner wanted Black Friday unannounced. `tier_count` drives `--tiers` as
before; the `<ol>` is skipped at zero. A lone card is allowed now (the old "one lonely
Regular card" rule is gone, because a lone *live* card is an offer), and the grid's
`max-width` became `max(300px, …)` so the single Black Friday card has room for its line.
Verified on the preview on 1 Nov: `--tiers: 2`, one `is-now`, no Liquid error. Both the 20% and the 15% are `allItems` discounts with a $100 minimum, which is what the cards say.
Same change is **not** on the Halloween line (`merged/index.json`) — that line is finished.

## Shipping is province-based since 1 Nov 2026

The owner rewrote the **Shipping policy** (22:30Z) and the delivery profile to match: flat rates
by province, **free standard shipping from $200 in Ontario, $225 Quebec, $250 Prairies and
Atlantic, $275 BC, none in the territories**; express $35–$59.99 and "Arrives Before Pre-Order"
$30–$59.99 by zone; **dispatch Monday–Wednesday only**, handling 1–3 business days, transit 1–5,
2–8 door to door; live-arrival coverage only when transit is ≤ 5 business days (so a far address
needs express); no P.O. boxes; free pickup in Brampton; replacement shipping still a flat $14.99.
*"You don't have to update the shipping policy. You just have to update like the FAQs and stuff
like that. And announcement bar."* So the theme copy was brought in line, nothing else:

| Where | Was | Now |
| --- | --- | --- |
| `header-group.json` → `announcement_HUGfag` | "Free shipping on orders over $180" | "Free Standard Shipping From $200 in Ontario • Flat Province Rates Shown at Checkout", linked to `/policies/shipping-policy` |
| `page.tissue-culture.json` → `tl_s1` | "Standard $14.99, free over $180. Express $25." | "Flat rate by province, from $14.99. Free standard shipping from $200 in Ontario." |
| `page.tissue-culture.json` → `tl_s3` | "Never over a weekend." | "Monday to Wednesday only, never over a weekend." |
| `page.faq.json` → `faq_1_answer`, `faq_2_answer` | one line each | the province thresholds, no P.O. boxes, pickup; Mon–Wed dispatch, 1–3 handling, 1–5 transit, the 5-business-day coverage rule, link to the policy |
| `product.tissue-culture.json` (4 strings), `product.json` (1) | "Monday–Thursday" | "Monday–Wednesday" — the product-page card had disagreed with the policy since September |

Not touched: the guarantee's $14.99 replacement shipping (still true), the Pre Order page
("early in the week"), the homepage marquee ("Canada-wide shipping"), the winter heat-pack lines.
The `$180` string now appears nowhere in `theme/`.

## The 3D glass logo (31 Oct 2026)

The owner designed a glass/3D version of the logo on a Claude Design canvas ("AgaPlantz Liquid
Logo", `https://claude.ai/artifact/NVZAQr4PEAJq9WTtFNu9Yy`: wordmark on white, wordmark on
dark, leaf icon) and said *"update logos"*. The artboards are SVG (Poppins 600 wordmark + two
leaf paths with blur-mask shading), so they were rendered with headless Chromium — Poppins
fetched from Google Fonts first, since the renders must not depend on a network call — trimmed
to the opaque bounding box with 4–6% padding, and uploaded to **Files** with `fileCreate`:

| File | What | Used for |
| --- | --- | --- |
| `agaplantz-logo-3d.png` (2310×1083, transparent) | wordmark + leaves | **theme setting `logo`** |
| `agaplantz-favicon-3d-leaf.png` (1024², leaves only, transparent, filling ~90% of the frame) | leaf icon | **theme setting `favicon`** — the owner saw the white-tile version in Safari's address pill and said *"we need lil zoom in and background removed"* |
| `agaplantz-favicon-3d.png` (1024², white rounded tile, radius 224) | leaf icon on a tile | spare — app-icon style |
| `agaplantz-leaf-3d.png` (777×825, transparent) | leaves only | spare — profile pictures, badges |
| `agaplantz-logo-3d-dark.jpg` (2400×1200) | wordmark on dark green | spare — dark backgrounds, social |

Copies live in **`brand/`** in the repo. `config/settings_data.json`: `logo` and `favicon`
repointed, `logo_height` 38 → **48** and `logo_height_mobile` 31 → **40**, because the new mark
is squarer than the old PNG (about 2.1:1 against the old 2.6:1) and read too small at 38px. The
header renders it 102×48. Theme **`AgaPlantz 2026 — Halloween, 3D logo` = `189874307151`**
(duplicated from MAIN `189703094351`), published by the owner within minutes; the favicon swap
then made **`AgaPlantz 2026 — Halloween, leaf favicon` = `189875224655`**. Each settings file
also went onto the clean post-Halloween draft `189688381519`. Note **Shopify re-serialises `config/settings_data.json` on upload**, so
its `checksumMd5` does *not* match the local md5 even for a file we wrote — verify this one by
re-reading the keys (or the preview's `<img>` for the logo), not by checksum. The old header logo
`067AE3BF-9F4E-45C4-BC71-F9D0E5F961F1.png` and favicon `edited-edited_60_…png` are still in
Files, untouched, so reverting is two settings.

## Acclimation Service: paused 24 Oct 2026

The paid add-on `Acclimation Service (Add-On)` (`gid://shopify/Product/8916960084047`,
handle `acclimation-service`, three price tiers $12 / $18 / $28, type `Service`) was set to
**DRAFT** by the owner on 24 Oct and is published nowhere. On the 25th they asked for the
website to match (*"we have currently stopped acclimation service, so please add it on the
website as well"*).

**The one selling surface was `ai_gen_block_8ec2c32_DTK4mA`** — an "Add acclimation
service" card, first in `main`'s `block_order` on `templates/product.tissue-culture.json`
(`product.json` and `product.subscription.json` never had it). Its block file
`blocks/ai_gen_block_8ec2c32.liquid` links to a `product` setting; **when that product is a
draft, Liquid resolves the setting to blank and the block falls through to its editor
placeholder** — a greyed card reading *"Next, select your acclimation service product"* —
so for a day every tissue-culture page carried that broken card at the top of the buy box.
Drafting a product does not hide the blocks that point at it. The block is now
`disabled: true`, settings intact and still in `block_order`, so bringing the service back
is: set the product ACTIVE, flip the block on. Same recipe as the pre-order pause.

Checked and clean, nothing to change: the "Acclimation dome" card (`ai_gen_block_c6aca6a`)
talks about the guide and the free kit, not the service; the FAQ, Pre Order page, guarantee
page, cart, about, contact and all three policies carry no mention; the main menu has no
link to it. The only other place the string appears is inside Shopify's analytics JSON on
the pre-order page, which is not copy. Product descriptions were not swept (standing rule),
but two sampled pages had no mention outside the block.

## Cancellations: a 48-hour window since 28 Oct 2026

The owner rewrote the cancellation rules (*"I have updated a cancellation policy"*): both the
**Refund policy** ("Order Cancellations" / "Pre-Order Cancellations") and a new
**`SUBSCRIPTION_POLICY` titled "Cancellations"** (`/policies/subscription-policy`) now say
ready-to-ship orders can be cancelled **within 48 hours of ordering, as long as they haven't
shipped**, and **pre-orders within 48 hours of ordering** — after that the order has gone to
the partner lab. Mixed orders: each item follows its own rule. Email `info@agaplantz.com`
(or +1 647 621-3033) with the order number; approved cancellations are refunded in full in
5–10 business days. Subscriptions: cancel any time, at least 48 hours before the next billing
date. **Before this the site said pre-orders could never be cancelled**, in three places, all
rewritten to the 48-hour rule: `page.faq.json` → `faq_14_answer` ("Can I cancel my order?"),
`page.pre-order.json` → `fq_cancel`, `page.tissue-culture.json` → `fq_cancel`. The TC page's
"If a plant doesn't pull through" and the Pre Order page's "Lab confirms" step are about
*availability*, not cancellation, and were left alone.

**Two things the owner has to fix by hand** (policies are read-only from here): the Refund
policy's cancellation section ends with a stray author's note — *"I used 48 hours from
checkout for 'two days' so it's clear-cut, rather than 2 business days. For a mixed order…"* —
that reads as the shop talking to itself; the first sentence should go (the second is the
mixed-order rule and belongs). And Terms of Service §3 still says AgaPlantz *"may be unable
to accommodate cancellation requests after an order is accepted"* — not wrong, but vaguer
than the 48-hour rule; worth a one-line pointer to the Refund policy.

The FAQ template is editor-written JSON, so it was re-written from the live body with the
header stripped and verified semantically: the only key that moved is `faq_14_answer`.

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
hand-entered strings, not one setting. The current batch closes **30 Nov 2026, 23:59
Toronto** (`-05:00`, EST). The owner's whole message was *"new batch date is 30 nov"* —
date only, end of day assumed, as for the 31 Oct batch. Set on 1 Nov 2026, about ten
minutes after the October batch had closed (the countdown had already flipped to "This
batch has closed"), as theme **`AgaPlantz 2026 — Halloween, batch closes 30 Nov` =
`189887840335`** (from MAIN `189881450575`, the magic-mix theme the owner had published
within the hour) plus the same four files on the clean draft `189688381519`. The countdown
eyebrow now reads "New batch now open". **The discount ladder stays hidden**: `batch_start`
is still `2026-10-01`, so `day_now` is past 20 and the whole `<ol>` is skipped — verified
on both previews. No November discounts exist, so this is correct; if the owner wants a
November ladder it needs new tier dates, a new `batch_start`, *and* the automatic discounts.
**Found while doing this: the 28 Oct cancellation rewrite was never live.** The Halloween
line was duplicated from the drawn-pumpkin theme, not from `189743595599`, so MAIN's
`page.faq.json`, `page.pre-order.json` and `page.tissue-culture.json` still said pre-orders
could never be cancelled. The three repo templates went onto `189887840335` as well (MAIN's
copies differed from the repo only in those two answers — checked by eye on all three
bodies). The clean draft already had them. Also `announcement_early` ("Order Early, Pay
Less") was still enabled on the clean draft's bar — it had been disabled on the Halloween
line on 27 Oct — so it is now disabled there too.

| File | Field | Now says |
| --- | --- | --- |
| `sections/header-group.json` | `announcement_jeGMHt.text` | `Tissue Culture Pre-Orders Close November 30 • …` |
| `templates/index.json` | `custom_liquid_KL8FyB` → `assign deadline` | `2026-11-30T23:59:59-05:00` |
| `templates/page.pre-order.json` | `main` → `ch_cutoff.heading` | `Order by 30 November` (a `chapter` heading on the thread section — since 27 Oct; the old `ai_gen_block_41bf156_tpPC39.cutoff_date` block is gone) |
| `templates/product.tissue-culture.json` | `ai_gen_block_c6aca6a_HjQ7Ph.preorder_date` | `30 NOVEMBER` |
| `templates/product.tissue-culture.json` | `ai_gen_block_675aea4_RGqfCa.preorder_text` | `Order by [30 NOVEMBER]…` (hidden block) |
| `templates/product.tissue-culture.json` | `ai_gen_block_44763e7_iKDBHj.preorder_text` | `Order by [30 NOVEMBER]…` (hidden block) |

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

Growing medium as of 31 Oct: **the "magic mix" for Monstera and Anthurium — 80% long-fiber
sphagnum moss, 10% perlite, 10% Fluval Stratum** (the owner: *"it will provide best mineral
for plants it's our magic mix"*); still 50/50 Fluval Stratum and perlite for Philodendron,
Alocasia and other aroids. The owner said "for monstera"; the mix was applied to the existing
"For Monstera and Anthurium" subsection, since Anthurium shares it — split the subsection if
Anthurium should stay on plain moss. Changed in all four places (both "What You'll Need"
lists, both copies of Step 2); the Step 10 transplant mix ("a small amount of sphagnum moss")
is a different recipe and was left alone, as were the product-page kit cards ("Perlite and
stratum mix or sphagnum moss"), which are still true. Theme **`AgaPlantz 2026 — Halloween,
magic mix guide` = `189881450575`** (from MAIN `189875224655`); the same block went onto the
clean draft `189688381519`. **The moisture rule flipped the same night (1 Nov):** the old
text said squeeze the moss until "only a drop or two" comes out; the owner corrected it —
*"moss should be saturated with water nicely not dry, when squeezed it should drip water,
make sure you don't squeeze much so it loses its water"*. Step 2 now says soak until
saturated, keep it wet not just damp, water should drip when a handful is squeezed, and don't
wring it dry. Both drafts were overwritten in place (same theme ids). The other-aroids mix
still says "damp but never waterlogged" — the owner did not mention it. Before this, as of 7 Sep: plain sphagnum moss for Monstera and
Anthurium. "Ready-to-use" was dropped from the Betadine line — it now just reads "Diluted
Betadine solution". Note the duplicate reports `schema_version: 4.2.0`, not 4.1.4 — Horizon
has been upgraded under the Halloween chain at some point; nothing on this page was affected.

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
| `theme/snippets/cart-summary.liquid` | core Horizon (live stock copy as of 9 Nov), patched with the one cart render block — re-apply after every upgrade or stock overwrite |
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
| `theme/sections/tc-guide.liquid` | the "What is tissue culture?" page, six block types |
| `theme/sections/tc-learn-more.liquid` | homepage strip linking to it |
| `theme/sections/tc-stages.liquid` | homepage "New to tissue culture?" — slim photo rows + guarantee line (7 Nov) |
| `theme/sections/why-agaplantz.liquid` | homepage "Why collectors choose AgaPlantz" — plant photo + hairline reasons row (7 Nov) |
| `theme/templates/page.tissue-culture.json` | the page's blocks — all its structured copy |
| `theme/templates/page.pre-order.json` | the Pre Order page, same section, 40 blocks |
| `theme/templates/product.accessory.json` | owner-made template for the self-watering pot (editor header stripped) |
| `theme/blocks/plant-profile.liquid` / `theme/snippets/plant-profile-dots.liquid` | product-page About / Care cards, metafield-driven |
| `theme/templates/product.json` / `product.tissue-culture.json` | product templates (plant profile block, hidden old AI block) |
| `theme/blocks/availability-chance.liquid` | buy-box availability chance badge + pop-up, variant-aware |
| `docs/plant-identity-handoff.md` | **the handoff** for the two filling sessions: what the page shows, all 22 fields, per-genus defaults, writing rules, API recipe, A–Z plan, verification |
| `docs/plant-profile-metafields.md` | earlier, shorter brief (superseded by the handoff; kept for the definition history) |
| `brand/` | the 3D logo renders uploaded to Files (header logo, favicon, leaf, dark) |
| `halloween/` | the Halloween sale theme files (temporary, see that section) |
| `merged/index.json` | homepage of the Halloween + pages theme: live Halloween file plus the `tc_learn_more` strip |
| `catalog-backup/` | pre-deletion product export; `black-friday-2026-variant-lists.json` — the BF discount ids and variant lists |

Branch: `claude/shopify-theme-creation-ra78zf`. The local template is kept in sync
with whatever is live — pull the MAIN theme's file down after every publish so the
next session starts from the truth.
