---
name: agaplantz-product-listing
description: Build and update Shopify product listings for AgaPlantz Inc. (agaplantz.com) — tissue-culture aroids sold as Pre-Order, Ready-to-Ship, and Acclimated variants. Produces the full listing spec (title, URL handle, product type, tags, single-plant or pack variants with SKUs and prices, HTML description, SEO title and meta) in the store's existing conventions, then creates or updates the product in Shopify as a DRAFT only after Agam confirms. Use this whenever Agam wants to add a new plant to the store, list a new batch or lab arrival, write or rewrite a product description, fix tags/handles/SKUs, or asks anything like "put this on the site", "make a listing for", "add the new Philodendron", "the description for X is weak", or pastes a plant name and a price — even if Shopify is not mentioned by name.
---

# AgaPlantz product listings

Turn a plant name and a price into a complete, store-consistent Shopify listing for agaplantz.com, and put it live in Shopify only when Agam says so.

**Why consistency matters here.** The store already has dozens of listings that share one shape: two listing formats (single plant, pack), one SKU scheme, one tag scheme, one description rhythm. Customers, Shopify collections (which are tag-driven), search, and Agam's own bookkeeping all depend on that shape. A listing that looks fine on its own but breaks the pattern creates cleanup work later, so match the pattern in `references/store-conventions.md` exactly and change it only when Agam asks.

---

## Workflow

### 1. Gather the inputs

You need, at minimum:

- **Plant name** as it will appear as the title (e.g. `Philodendron Gloriosum Variegated`)
- **Genus** — derive it from the first word of the title if not stated
- **Pre-order price** in CAD

Ask for, or mark `[TO CONFIRM]` if absent:

- **Ready-to-ship price** (single-plant listings only) — the script proposes pre-order × 1.10 rounded up to the dollar, which matches most of the catalogue, but Agam sets the real number
- **Acclimated plant price** — no formula in the store; always Agam's call
- **MOQ** (lab minimum order quantity for the batch) — sets the `moqN` tag
- **SKU number** — the six-digit code after `PH-` is a catalogue number, not sequential; never invent one
- **Image URLs** — must be public HTTPS; local files can't be uploaded through the connector
- **Whether the plant is variegated** — decides which disclaimer paragraph closes the description
- **Single plant or pack** — the store has two listing formats (see `references/store-conventions.md`); pack listings have different variants, tags, and an extra description line. If Agam's message doesn't say and the plant's siblings on the store are packs, ask

Don't block on the optional ones. Build the spec with placeholders, show it, and let Agam fill blanks in one pass.

### 2. Check the store first

Search Shopify (`search_products` with `title:` and `handle:` filters) for the plant before drafting. Three outcomes:

- **Exists** → this is an update, not a create. Pull it with `get-product`, keep its handle and SKUs (they're referenced by the lab order and existing links), and change only what Agam asked for. If the price Agam gave differs from the live one, say so plainly and ask before proposing the change — the live price is what customers have already paid. If the existing description is one of the placeholder templates described in the conventions file, offer a real one; otherwise leave the copy alone unless Agam asked for a rewrite.
- **Near-duplicate** (same plant under a slightly different name, e.g. "Albo" vs "Albo Variegated") → stop and ask which one is meant. Two listings for one plant splits inventory and confuses pre-order counts.
- **Not found** → proceed as a new listing.

### 3. Build the spec

Run the bundled script — it applies every convention deterministically so you spend your attention on the description, not on remembering tag order:

```bash
python scripts/build_listing.py "Philodendron Gloriosum Variegated" --preorder 84 --moq 10 --sku 100187 --variegated
python scripts/build_listing.py "Alocasia Tiny Dancers" --preorder 28 --moq 100 --sku 100752 --pack 5 --min-order 5
```

It prints a JSON spec (handle, product type, tags, variants, prices, SEO fields, and the pack line if any). Add `--rts` / `--acclimated` when Agam gave those prices. Run it with `--help` for the full list. The script always builds a *create*-shaped spec; on the update path, lift only the fields you're changing from it and keep the live product's status, variant titles, and SKUs as they are.

Then write the description following `references/description-guide.md`. That file has the paragraph structure, the voice, the two closing disclaimers, and real examples from the live store. Read it before writing — the store's descriptions have a specific rhythm (three short paragraphs, plant first, no marketing throat-clearing) and it's easy to drift into generic copy.

### 4. Present the spec before touching Shopify

Show Agam the complete listing as a readable block:

```
Title:        Philodendron Gloriosum Variegated
Handle:       philodendron-gloriosum-variegated-pre-order
Type:         PHILODENDRON        Vendor: AgaPlantz
Tags:         collector plant, moq10, Philodendron, Philodendron Gloriosum Variegated,
              Pre-Order, rare houseplants Canada, Rare Philodendron, Tissue culture

Variants
  Tissue Culture (Pre-Order)       PH-100187      $84.00
  Acclimated Plant                 PH-100187-AC   [TO CONFIRM]
  Tissue Culture (Ready to Ship)   (no SKU)       $93.00  ← suggested, confirm

Description
  <the HTML, rendered as plain paragraphs>

SEO title:  Philodendron Gloriosum Variegated | Tissue Culture | AgaPlantz
SEO meta:   <≤155 chars>

Open items: acclimated price, image URLs
```

Then stop and wait. Listings are customer-facing and pre-order counts feed the lab order, so Agam reviews every one before it exists in Shopify, even as a draft.

### 5. Create or update — DRAFT only

Once Agam confirms:

- **New product** → `create-product` with `status: "DRAFT"`, the spec's variants under a single option, `inventoryItem.tracked: true` on each variant, and the tags/type/vendor from the spec. The variant option name must match the store's existing products — check one with a `graphql_query` on `product.options { name }` before the first create in a session and reuse the name.
- **Existing product** → `update-product` with only the fields being changed. Don't resend variants that aren't changing.
- Leave `status` as DRAFT. Agam flips it to ACTIVE in the admin after checking images and collection placement. Never publish ACTIVE yourself, even if asked casually — say you've left it as a draft ready to publish and why.
- Report back with the product GID, the admin URL, and the remaining open items. The admin URL is `https://admin.shopify.com/store/<myshopify-handle>/products/<numeric id>`; `get-shop-info` returns the custom domain, not the handle, so fetch it once per session with `graphql_query` on `{ shop { myshopifyDomain } }` (the handle is the part before `.myshopify.com`). If that lookup isn't available, give the GID and skip the URL rather than guessing one.

---

## Hard limits

These exist because a listing is a promise to a customer and an input to a lab order.

- **Never guarantee variegation, colour, size, leaf count, or survival.** Variegation shifts with genetics and conditions; the store's published policy says so, and a description that overpromises turns into a refund request.
- **Never state a delivery or arrival date.** Pre-orders are described in terms of the batch, not a date. The current cut-off date lives in the support skill's facts file and goes stale; a product listing outlives it.
- **Never invent botanical facts.** If you're not sure whether a plant crawls or climbs, has velvet or gloss, or where it's from, leave it out or mark `[CHECK]`. A wrong fact on a $170 plant is worse than a shorter description.
- **Never invent a SKU number, MOQ, or acclimated price.** Placeholders are fine; guesses are not.
- **Never set a product ACTIVE, delete a product, or change the price of a live variant without Agam's explicit confirmation for that specific change.**
- **Canada only.** Don't mention US or international shipping in copy.
- Keep pesticide, fungicide, or dosage advice out of listings entirely.

---

## Reference files

- `references/store-conventions.md` — the observed catalogue shape: variants, SKUs, pricing relationships, tags, handles, product types. Read when building any spec by hand or when the script's output looks off.
- `references/description-guide.md` — paragraph structure, voice, disclaimers, and real examples. Read before writing every description.
- `scripts/build_listing.py` — deterministic spec builder. Run with `--help`.
