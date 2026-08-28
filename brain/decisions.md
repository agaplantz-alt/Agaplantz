# Decision log

Newest first. Format: `## YYYY-MM-DD — decision` then one short paragraph of
reasoning.

## 2026-08-28 — Keep business memory in the repo, not in chat

Claude sessions start with no memory of previous conversations. Anything that
should survive gets written to `brain/` and committed, so every future session
loads it automatically via `CLAUDE.md`.

## 2026-08-28 — Store design: warm natural palette, serif headings, square corners

The live theme departs from stock Horizon in a consistent direction: cream
`#FBF8F2` instead of white, warm near-black `#2F2A22` instead of black, sage
`#5C6B4C` buttons instead of black, Lora serif headings over Work Sans body, and
square 2px corners instead of Horizon's 14px pill shapes. Headings are also
sized down (H1 42 vs 56). Full detail in `brain/shopify.md`.

## 2026-08-28 — Business is pre-order-first

283 of 301 products are tissue-culture pre-orders, with dedicated pre-order
page, collection and product templates. Ready-to-ship (36) and mature specimens
(7) are the minority. Marketing and site decisions should assume the buyer is
waiting for a plant, not receiving one immediately.
