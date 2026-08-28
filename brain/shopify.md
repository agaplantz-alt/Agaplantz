# Shopify store

Everything below was read directly from the live store on **2026-08-28**, not
remembered. Re-verify before relying on numbers that move (counts, stock).

## Store

- **Store:** AgaPlantz Inc. — `agaplantz.com`
- **Plan:** Shopify | **Currency:** CAD | **Country:** Canada | **Timezone:** EDT
- **Products:** 301

## Live theme

- **Name:** `AgaPlantz 2026 (Claude) 0.1`
- **ID:** `gid://shopify/OnlineStoreTheme/149362769999`
- **Role:** MAIN (live) — published 2026-08-28 05:23 UTC
- **Base:** Horizon (theme store ID 2481)

### Theme lineage on the store

Ten themes exist, most unpublished. Working order, oldest first: `Horizon` ×2
(May 1) → `Tinker` (May 6, abandoned) → `Copy of Horizon` → `Updated copy of
Copy of Horizon` → two more `Updated copy of...` → `AgaPlantz 2026 (Claude
draft)` → `AgaPlantz 2026 (Claude)` → **`AgaPlantz 2026 (Claude) 0.1` (live)**.

Housekeeping note: the `Updated copy of Updated copy of Copy of Horizon` chain
is unreadable. Name future versions `AgaPlantz 2026 (Claude) 0.2`, `0.3`, and
delete dead drafts.

## Design system — live settings vs. the Horizon default

The right column is Horizon's stock preset, so every row is a deliberate
departure from it.

### Color palette

| Token | Live | Horizon default |
| --- | --- | --- |
| Background | `#FBF8F2` warm cream | `#ffffff` |
| Foreground (text) | `#2F2A22` warm near-black | `#000000` |
| color1 | `#56503F` | `#333333` |
| color3 | `#DED3C2` sand | — |
| color4 | `#F2EBDE` | — |
| color7 | `#E8EDE1` pale sage | — |
| Primary button bg | `#5C6B4C` sage green | foreground (black) |
| Primary button text | `#FBF8F2` cream | background |
| Sale badge | `#B4693C` terracotta / white text | background / foreground |

**The palette is warm and natural — cream, sage, sand, terracotta. No pure
white, no pure black anywhere.**

### Typography

| Role | Live | Horizon default |
| --- | --- | --- |
| Headings + accent | **Lora 400** (serif) | Inter 700 |
| Body | **Work Sans 400** | Inter 400 |
| Subheading | Work Sans 500 | Inter 500 |
| Paragraph | 15px, normal line height | 14px, loose |
| H1 / H2 / H3 / H4 / H5 | 42 / 30 / 22 / 18 / 13 | 56 / 48 / 32 / 24 / 14 |

**Serif headings over sans body, and headings are deliberately smaller and
calmer than stock Horizon.**

### Shape

Corners are squared off almost everywhere — buttons `2`, inputs `2`, badges `2`
(Horizon ships pill-shaped `100`), popovers `4`, product `2`, card `4`. Horizon
default is `14` on buttons. Secondary buttons are transparent with a 1px border.

### Layout & motion

- Page width `normal` (Horizon default: `narrow`)
- Page transitions **on**, transition-to-main-product **on** (both off in stock)
- Card hover: `subtle-zoom` (stock: none)
- Logo 42px desktop / 31px mobile (stock: 36 / 28)

### Cart

Drawer type, discount code field on, cart note off, price in secondary font.

## Custom templates

Beyond the stock set, this theme carries purpose-built templates:

- `product.tissue-culture.json` (27KB — the largest template in the theme)
- `page.pre-order.json` + `collection.pre-order.json`
- `page.acclamation-guide.json` — note the **misspelling** in the template file;
  the page itself is correctly titled "Acclimation guide"
- `page.faq.json`, `page.about-us.json`, `page.coming-soon-page.json`
- `templates/index.json` is 49KB — a heavily built custom homepage

## Catalog structure

| Collection | Products |
| --- | --- |
| TISSUE CULTURE — PRE-ORDER | 283 |
| ALOCASIA | 123 |
| PHILODENDRON | 92 |
| ON SALE | 62 |
| ANTHURIUM | 40 |
| READY TO SHIP | 36 |
| MONSTERA | 33 |
| TISSUE CULTURE — READY TO SHIP | 19 |
| BEGONIA | 10 |
| MATURE SPECIMENS | 7 |

The business is built around **tissue culture pre-orders** (283 of 301
products), with a much smaller ready-to-ship and mature-specimen offer.

## Pages

Contact, About us, FAQ, Payment Policy, Coming Soon, Pre Order, Acclimation
guide, Your Privacy Choices.

## Apps embedded in the theme

- Shopify Inbox (chat widget, bottom-right)
- Loox (reviews)
- Shopify Forms
- Koala Upsells & Gifts
- Google & YouTube channel widget

## Open questions

- Which of the settings above were changed in the 2026-08-28 session versus
  carried over from the earlier `Copy of Horizon` work? The API shows current
  state, not authorship. TODO — confirm.
- Was anything still unfinished when that session ended? TODO
