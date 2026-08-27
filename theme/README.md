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
| `sections/footer-group.json` | Footer — shared by every page |

Only these three files differ from the base theme. Everything else is stock Horizon.

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

Type: Lora 400 (headings/accent), Work Sans (body/subheading). H1 42px, H2 30px,
H3 22px, body 15px, page width `normal`, `subtle-zoom` card hover.

Geometry is deliberately sharp — 2px on buttons, inputs, badges, product images and
panels, 4px on cards. Squared corners plus restrained type and generous vertical
padding (72–96px between sections) is what carries the luxury read; the earlier
pill buttons and 12px radii read casual-DTC.

## Homepage order

1. `hero_main` — full-bleed image, gradient overlay, CTA to ready-to-ship
2. `marquee_trust` — scrolling trust strip on sage
3. `collections_genus` — Philodendron / Alocasia / Monstera / Anthurium tiles
4. `products_rts` — Ready to ship (8 products)
5. `tissue_culture` — explainer + ready-to-ship vs pre-order cards
6. `products_acclimated` — Mature specimens (8 products, `acclimated-plants`)
7. `why_agaplantz` — four icon/text columns on sand
8. `newsletter` — email signup

## Footer

`sections/footer-group.json` carries two AI-generated blocks. The second
(`ai_gen_block_651bd33`) had `show_social_links: true` with every social URL blank,
so it rendered a second bare "Follow us on" heading under the real one in
`ai_gen_block_fa8568c`. Set to `false`.

Both blocks hardcode colours rather than reading the palette, so they were
retinted by hand (`#f5f5f5`→`#F2EBDE`, `#ffffff`→`#FBF8F2`, `#000000`→`#2F2A22`,
`#dfdfdf`→`#DED3C2`). Their `range` settings enforce step values — `icon_size`,
`icon_spacing`, `heading_spacing`, `padding_top`/`padding_bottom` are all step-5
and `heading_size` is step-2. Off-step values are rejected by `themeFilesUpsert`
with `FILE_VALIDATION_ERROR`.

## Known store-data issues

`READY TO SHIP TISSUE CULTURE` (19 products) is almost entirely a subset of
`PRE-ORDER TISSUE CULTURE` (283 products) — the same products sit in both, and
their handles still end in `-pre-order`. A homepage row for each collection
therefore rendered 7 of 8 identical products.

Section 6 points at `acclimated-plants` instead to avoid the duplication. Fixing
the collection membership is a merchandising task, not a theme change.

### Mature specimens are mostly unpublished or sold out

`ACCLIMATED PLANTS` (23 products) is the mature-specimen collection feeding the
"Mature specimens" row. Of those:

- **7 are DRAFT** and cannot render on the storefront at all — Caramel Marble,
  Micans Variegated, Atabapoense, Fire Tiger Variegated, El Choco Red, Orange
  Marmalade, Patriciae. Each has inventory 1–4, i.e. genuine single specimens.
- **10 of the 16 ACTIVE ones have 0 inventory**, including Monstera Devil Monster.
- `Tissue Culture Starter Kit` sits at **-70** (oversold).

So the row currently fills largely with sold-out plants. No theme change fixes
this: the products must be set ACTIVE and stocked in admin.

## Applying changes

Both files are written to the draft theme via the Admin GraphQL
`themeFilesUpsert` mutation. Writes to the live/MAIN theme are blocked, so the
draft must be published manually once approved.
