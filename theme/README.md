# AgaPlantz theme — warm nursery homepage

Source of truth for the customisations applied to the Shopify draft theme
**"AgaPlantz 2026 (Claude draft)"** (unpublished, preview `/t/8`).

Base theme: Horizon 4.1.3 (duplicated from the live theme — not modified in place).
The live theme is untouched; publishing is a manual step in Shopify admin.

## Files

| File | Purpose |
| --- | --- |
| `config/settings_data.json` | Global design tokens — palette, typography, buttons, cards |
| `templates/index.json` | Homepage section layout |

Only these two files differ from the base theme. Everything else is stock Horizon.

## Design tokens

Direction: warm nursery / earthy.

| Token | Value | Role |
| --- | --- | --- |
| `background` | `#FBF8F2` | Warm cream page background |
| `foreground` | `#2F2A22` | Warm near-black text |
| `color1` | `#56503F` | Secondary text |
| `color3` | `#DED3C2` | Clay borders |
| `color4` | `#F2EBDE` | Sand surface (trust band) |
| `color7` | `#E8EDE1` | Sage tint (marquee, tissue-culture band) |
| — | `#5C6B4C` | Moss — primary buttons, icons |
| — | `#B4693C` | Terracotta — sale badges |

Type: Lora (headings/accent), Work Sans (body/subheading). H1 54px, body 16px,
page width `normal`, card + product radius 12px, `subtle-zoom` card hover.

## Homepage order

1. `hero_main` — full-bleed image, gradient overlay, CTA to ready-to-ship
2. `marquee_trust` — scrolling trust strip on sage
3. `collections_genus` — Philodendron / Alocasia / Monstera / Anthurium tiles
4. `products_rts` — Ready to ship (8 products)
5. `tissue_culture` — explainer + ready-to-ship vs pre-order cards
6. `products_acclimated` — Acclimated and established (8 products)
7. `why_agaplantz` — four icon/text columns on sand
8. `newsletter` — email signup

## Known store-data issue

`READY TO SHIP TISSUE CULTURE` (19 products) is almost entirely a subset of
`PRE-ORDER TISSUE CULTURE` (283 products) — the same products sit in both, and
their handles still end in `-pre-order`. A homepage row for each collection
therefore rendered 7 of 8 identical products.

Section 6 points at `acclimated-plants` instead to avoid the duplication. Fixing
the collection membership is a merchandising task, not a theme change.

## Applying changes

Both files are written to the draft theme via the Admin GraphQL
`themeFilesUpsert` mutation. Writes to the live/MAIN theme are blocked, so the
draft must be published manually once approved.
