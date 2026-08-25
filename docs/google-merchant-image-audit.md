# Google Merchant Center — Product Image Audit

**Store:** AgaPlantz (Shopify) · **Audited:** 2026-08-25 · **Scope:** all 250 active products

Shopify is the source for the Merchant Center feed, so `image_link` and
`additional_image_link` come straight from each product's Shopify media. This audit reads
the live catalog and grades every image against Google's product image requirements.

Work list with every affected product: [`google-merchant-image-fix-list.csv`](./google-merchant-image-fix-list.csv)

## Headline

**95 of 250 active products (38%) need new photography.** Six of them are being dropped
from the feed entirely right now; the other 89 are in the feed but showing at a resolution
that guarantees they lose the click.

| Priority | Issue | Products | Merchant Center effect |
|---|---|---|---|
| P0 | No image at all | 6 | **Item disapproved.** `image_link` is required — these cannot serve. |
| P1 | Largest image 186–364 px | 87 | Serves, but far below the 800 px recommendation. Renders soft/pixelated in Shopping. |
| P2 | Largest image 1024 px | 2 | Serves fine. Below the 1200 px ideal for zoom and Performance Max crops. |

## What is *not* wrong

Worth stating plainly, because these are the usual disapproval causes and the catalog is clean on all of them:

- **No promotional overlays, watermarks, borders, or text.** Sampled the edited hero shots
  (e.g. Alocasia Bambino Aurea, Anthurium Wendlingeri) — plain product on white, which is
  exactly what Google wants. No policy risk here.
- **No placeholder or "image coming soon" graphics.**
- **File sizes and formats are fine.** The 2048×2048 PNGs run ~5 MB, well under the 16 MB
  cap, and nothing approaches the 64 MP ceiling.
- **Nothing is below the hard 100×100 px minimum**, so the low-res items are not
  *disapproved* for size — they simply perform badly.

The catalog splits cleanly into two populations: professionally edited 2048×2048 shots on
white, and a batch of small supplier thumbnails.

## P0 — Six products with no image (disapproved)

These have inventory and are ACTIVE, but carry zero media, so Merchant Center cannot build a
feed item for them:

| Product | Inventory |
|---|---|
| Alocasia Portei Aurea Variegated | 20 |
| Alocasia Macrorrhiza Albo Variegated | 20 |
| Alocasia Black Stem Variegated | 20 |
| Alocasia Brancifolia Aurea Variegated | 20 |
| Anthurium DocBlock Red Crystallinum Michelle F2 | 20 |
| Tissue Culture Starter Kit | −70 |

That is 100 units of sellable pre-order stock currently invisible to Shopping. Fixing these
six is the highest return-per-hour item in the whole audit.

Note: `Tissue Culture Starter Kit` also shows **−70** inventory. Negative stock will read as
out-of-stock in the feed regardless of imagery, so it needs an inventory correction too.

## P1 — 87 products on supplier thumbnails

These all trace to two bulk uploads (`1000XX-tc.jpg` / `1000XX-mature.jpg`, and the Anthurium
`1000XX_tc.jpg` set). They are 186–364 px — roughly a tenth the linear resolution of the
in-house shots, and about 1% of the pixel area.

They are also visibly different in kind, not just size. The `-tc` files are snapshots of a
hand holding a tissue-culture jar; the `-mature` files are plants photographed on concrete in
daylight. Next to a Shopping result set — where competitors show clean studio product shots —
these read as a lower-tier listing before anyone reads the price.

Two consequences worth separating:

1. **Performance.** Google serves the image at up to ~800 px in Shopping surfaces. A 219 px
   source gets upscaled and looks soft. This depresses CTR directly.
2. **Provenance.** These look like supplier catalog photos rather than AgaPlantz's own
   product. If they were supplied by a grower rather than shot in-house, confirm the usage
   rights — Google can pull listings on a rights complaint, and a supplier photo of a
   different specimen is also an accuracy risk for a product where the exact variegation
   pattern is the thing being bought.

The worst offenders (single image, under 200 px) are the place to start:

Alocasia Cucullata Albo · Alocasia Portora Albo · Alocasia Puber Aurea · Philodendron Yellow
Congo · Anthurium Bonplandii Narrow Mix · Anthurium SKG Red Crystallinum × Tezula

`Philodendron Lynamii` is the single weakest asset in the catalog: its "mature" image is
**140×186 px**, non-square, and shows one detached leaf rather than a plant.

## A quality note on the good images

The 2048×2048 in-house shots are policy-clean but leave a lot on the table. In the sampled
Alocasia Bambino Aurea hero, the plantlet occupies roughly 40% of the frame, off-centre, with
the tweezers cropped at the bottom edge. Google's guidance is that the product should fill
**75–90%** of the image.

At Shopping thumbnail size that difference is decisive: a plant filling 40% of a 250 px tile
is a small green smudge. Re-cropping the existing 2048 px files is cheap — no reshoot needed —
and applies to the whole edited library, not just the 95 products above.

## Image spec for replacements

Shoot and export to this, and both Merchant Center and the Shopify PDP are covered:

| Attribute | Target |
|---|---|
| Dimensions | 2000×2000 px square (minimum 1200×1200) |
| Format | JPEG, quality 85–90 (smaller than PNG at the same visual quality) |
| Background | Pure white `#FFFFFF`, seamless |
| Product fill | 75–90% of frame, centred, nothing cropped by the edge |
| Overlays | None — no text, logo, watermark, badge, border, or price |
| Staging | No tweezers, hands, jars, or concrete in the primary image |
| File size | Under 2 MB |
| Per product | 1 primary + 2–3 additional (leaf detail, whole plant, scale reference) |

For pre-order tissue-culture items, keep the convention of one plantlet shot and one mature
shot — but make the **mature plant the primary image**. It is what the buyer is purchasing
toward, and it photographs far better at thumbnail size than a plantlet in a jar.

## Suggested order of work

1. **Shoot the 6 P0 products.** Unblocks 100 units of stock from the feed. Half a day.
2. **Fix the `Tissue Culture Starter Kit` −70 inventory.** Minutes, unrelated to photography.
3. **Re-crop the existing 2048 px library to 75–90% fill.** No reshoot; batch operation.
4. **Reshoot the 87 P1 products**, cheapest-first by the single-image-under-200 px list above.
5. **Confirm image rights** on the supplier-sourced `1000XX` files before any of them stay in
   the feed long-term.

## How to re-run this audit

The data comes from the Shopify Admin GraphQL API — no Merchant Center access needed, since
the feed mirrors Shopify:

```graphql
query GetProductImages($after: String) {
  products(first: 50, after: $after, query: "status:active") {
    pageInfo { hasNextPage endCursor }
    nodes {
      id title handle totalInventory
      images(first: 12) { nodes { url width height altText } }
    }
  }
}
```

Flag any product where `images.nodes` is empty (P0) or where `max(width, height) < 800` (P1).
