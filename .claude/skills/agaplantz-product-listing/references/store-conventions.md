# Store conventions — agaplantz.com

Observed from the live catalogue on 8 Sept 2026. When a listing here and the live store disagree, the live store wins — check with `search_products` / `get-product`.

## Identity fields

| Field        | Convention                                   | Example                                        |
|--------------|----------------------------------------------|------------------------------------------------|
| Title        | `Genus Cultivar [Variegated]`, Title Case, no quotes around cultivar names | `Alocasia Melo Albo Variegated`   |
| Handle       | slug of the title + `-pre-order`             | `alocasia-melo-albo-variegated-pre-order`      |
| Product type | genus in UPPERCASE                           | `ALOCASIA`, `MONSTERA`, `PHILODENDRON`, `ANTHURIUM` |
| Vendor       | always `AgaPlantz`                           |                                                |

The `-pre-order` handle suffix is the norm even though the product also carries ready-to-ship and acclimated variants. A few early listings lack it (`alocasia-bambino-pink`); don't "fix" those — changing a handle breaks inbound links.

Slug rules (same as the `slugify` library Agam uses): lowercase, accents folded to ASCII, any run of non-alphanumerics becomes one hyphen, no leading/trailing hyphens. Cultivar quotes and apostrophes vanish: `Alocasia Cuprea 'Red Secret' Mint Variegated` → `alocasia-cuprea-red-secret-mint-variegated-pre-order`.

## Two listing formats

The catalogue has two families. Work out which one you're in before building variants — the difference is visible in the tags and variant titles of sibling listings.

**Single-plant listings** (the flagship aroid line: variegated Monsteras, Alocasias, Philodendrons; mostly ACTIVE):

| Variant title                   | SKU              | Price relationship                  | Typical inventory |
|---------------------------------|------------------|-------------------------------------|-------------------|
| `Tissue Culture (Pre-Order)`    | `PH-1xxxxx`      | base price, set by Agam             | ~100 (batch cap)  |
| `Acclimated Plant`              | `PH-1xxxxx-AC`   | no formula; 1.3× to 4× base         | usually 0         |
| `Tissue Culture (Ready to Ship)`| none             | ≈ base × 1.10, rounded up to dollar | 0–4 (what's in hand) |

Observed ready-to-ship ratios: 72→81, 54→60, 42→48, 84→96, 174→192, 30→33, 108→120, 60→66. The ×1.10 rule reproduces most of these; treat the script's figure as a suggestion and let Agam confirm. The Ready to Ship variant exists only on this family — it's a real "in the cupboard now" offer, so add it only when Agam has stock in hand or the sibling listings in that genus carry it.

**Pack listings** (green/non-variegated Alocasias, Warocqueanum, Thai Constellation, Frydek, Florida Beauty; many still DRAFT):

| Variant title                                  | SKU              | Notes                               |
|------------------------------------------------|------------------|-------------------------------------|
| `Tissue Culture (Pre-Order) - Pack of 5`  or  `Tissue Culture (Pre-Order) - 30 Plant Pack` | `PH-1xxxxx` | price is per pack. Some older pack listings keep the plain `Tissue Culture (Pre-Order)` title and rely on the tag + description |
| `Acclimated Plant`                             | `PH-1xxxxx-AC`   | single plant                        |

Two variants only — no Ready to Ship. Tags add `pack{N}` and usually `min-order-5` (a minimum line quantity at checkout); `moq{N}` is much larger (100–1000). The description carries a bold pack line (see `description-guide.md`). Match the variant-title style of the same pack size already on the store: `- Pack of 5` for fives, `- 30 Plant Pack` for thirties.

When Agam gives a price without saying pack or single, and the plant's siblings are packs, ask — a $52 5-pack and a $52 single are very different offers.

The `PH-` number is a six-digit catalogue code (`PH-100003` … `PH-100187`). It is **not** assigned in creation order, so never derive the next one — ask.

Inventory is tracked on all variants (`inventoryItem.tracked: true`).

## Tags

Eight tags, always present. Shopify stores them sorted case-insensitively, so order in the spec doesn't matter, but every one of these must be there because collections and filters key off them:

```
{Genus}
{Full title}
collector plant
moq{N}
Pre-Order
Rare {Genus}
rare houseplants Canada
Tissue culture
```

Optional extras seen in the catalogue:

- `pack{N}` — sold as a multi-pack (`pack5`, `pack10`, `pack30`)
- `min-order-5` — minimum quantity per line at checkout; goes with most `pack30` listings

`moq{N}` is the lab minimum order quantity for the batch (seen: 5, 10, 20, 50). It's a real operational number; leave the tag out rather than guess it.

## Description HTML

Plain `<p>` paragraphs only, no headings, no lists, no inline styles. Three body paragraphs then one bold disclaimer paragraph (plus a bold pack line on pack listings). Full guide and examples in `description-guide.md`.

**Placeholder descriptions.** A batch of DRAFT listings was created from a template and never written. They read like: *"[Name] is a compact, jewel-like Alocasia. Grown for its lush, healthy foliage and strong form. A sought-after collector's plant that…"* or *"…A clean, vigorous grower with handsome, glossy foliage. A genuinely uncommon find that…"* or *"…rare Alocasia offered as laboratory tissue culture…"*. Interchangeable sentences, nothing specific to the plant. When you touch one of these listings for any reason, say so and offer a real description — that's the store's biggest content gap, and Agam would rather hear it than not.

## SEO

Shopify's default SEO title is the product title; the store doesn't override it in the listings observed. When asked to write one:

- SEO title: `{Title} | Tissue Culture | AgaPlantz` (≤ 60 chars if possible; drop `| Tissue Culture` first)
- Meta description: ≤ 155 chars, plant name in the first clause, mention "tissue culture" and "Canada" — those are the queries the store ranks for.

## Images

Product images are PNGs on the Shopify CDN with empty alt text. When creating via the connector, images must already be public HTTPS URLs; pass `altText` as `{Title} tissue culture plant` so new listings are at least accessible.

## Collections

Collections are tag-driven (`Pre-Order`, genus tags). A product with the right tags lands in the right collections automatically, which is the main reason the tag set is non-negotiable.
