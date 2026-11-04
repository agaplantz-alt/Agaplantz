# Plant identity handoff — every plant gets its own page

For the two Claude sessions that fill the data behind the new product pages of
**AgaPlantz Inc.** (agaplantz.com, Shopify store `sk11xm-0b.myshopify.com`, Horizon theme).
Written 4 Nov 2026 by the theme session. Everything the theme reads is listed here; nothing
else needs to be written. The owner is non-technical and reads product pages on a phone.

Two jobs, two sessions, in this order:

| Session | Job | Fields it owns |
| --- | --- | --- |
| **A — batch & supplier session** | Decides, per plant, how likely the partner lab is to supply it in the next pre-order batch, from the batch payment / confirmation sheets. Re-runs after every supplier confirmation. | `availability_chance`, `last_batch_result`, `availability_note`, `availability_updated` |
| **B — plant identity session** | Gives every plant its own profile, A to Z: botanical facts, a summary, care lines, care levels, and checks the juvenile / mature photos. One pass over the whole catalogue, then upkeep when products are added. | the 18 profile fields below, plus a check of `young` / `big_one` |

Both write **product metafields in the `custom` namespace**. Definitions already exist in
admin (ids at the bottom); do not create new definitions or change types. All theme blocks
render nothing for a blank field, so a half-filled catalogue still looks finished.

---

## 0. The store, in one minute

- Rare aroids: Philodendron, Alocasia, Monstera, Anthurium, Begonia. ~600 active products.
- **Plant stage is a variant option (`Plant Stage`)**, not a product: a listing can carry
  `Tissue Culture (Pre-Order)`, `Tissue Culture (Ready to Ship)`, `Acclimated Plant`,
  `Mature Plant`. Most of the catalogue is tissue culture (lab-grown plantlets).
- Pre-orders are grown to order by a partner laboratory. After the batch cut-off the owner
  places the order; the lab confirms what it can supply; unavailable plants are refunded.
  That is what the availability chance is about.
- Two product templates: `product.tissue-culture.json` (most plants, tissue culture) and
  `product.json` (rooted / acclimated plants). Both show the same blocks.
- Variegated and green forms are **different products** with different care and rarity.

## 1. What the product page shows, and which field drives it

**Plant profile band** (below the buy box, one full-width band on the plant's own blurred photo):

| On the page | Field | Blank → |
| --- | --- | --- |
| Genus eyebrow ("Alocasia · Plant profile") | `product.type` (already set) | hidden |
| Italic botanical name | `botanical_name` | falls back to the product title |
| Pills | `rarity` (terracotta), `care_level` ("Moderate care"), `growth_habit`, `pet_safe` ("Not pet safe" / "Pet safe") | each pill hidden |
| Juvenile photo tile | `young` (image) | falls back to the product's first image |
| Mature photo tile + the blurred band background | `big_one` (image) | tile hidden; background uses the juvenile or first image |
| About this plant: summary | `plant_summary` | generic fallback sentence |
| Facts grid | `origin` (Native range), `growth_habit`, `mature_leaf_size` (Mature leaf), `variegation` | each fact hidden; grid hidden when all four are blank |
| What you'll receive tiles | `growth_stage`, `approximate_size`, `pot_size`, `root_condition` (already filled on most products; `NA` is treated as blank) | tile hidden |
| Care guide rows | `care_light`, `care_water`, `care_humidity`, `care_temperature`, `care_soil`, `care_fertilizer` | generic fallback line |
| Five-dot meters beside Light / Water / Humidity | `light_level`, `water_level`, `humidity_level` (1–5) | no dots |

**Availability chance card** (in the buy box, directly under the Plant Stage buttons; shown
for the pre-order stage only; an in-stock other stage shows "In stock, ready to ship"):

| On the page | Field |
| --- | --- |
| Pill + four-bar meter + coloured edge | `availability_chance` |
| "Last batch: …" line and the same line in the pop-up | `last_batch_result` |
| Extra line in the pop-up | `availability_note` |
| "Updated 4 November 2026" in the pop-up | `availability_updated` |

## 2. Field reference

All `ownerType: PRODUCT`, namespace `custom`. Types must be stated exactly; `choices` fields
reject any other spelling or case.

### Session B — identity (18)

| Key | Type | Rule | Write |
| --- | --- | --- | --- |
| `plant_summary` | `multi_line_text_field` | ≤ 400 chars | 1–2 sentences on what makes this plant special. No prices, no availability, no batch dates. |
| `botanical_name` | `single_line_text_field` | ≤ 80 | Genus + species; cultivar in single quotes; variegation in brackets. E.g. `Philodendron billietiae (variegated)`, `Alocasia reginula 'Black Velvet'`. Hybrids: `Philodendron 'Florida Beauty'`. |
| `origin` | `single_line_text_field` | ≤ 80 | Native range of the species. Hybrids / cultivars: `Hybrid (cultivated)` or `Borneo (species); variegation cultivated`. |
| `growth_habit` | `single_line_text_field` | choices: `Climbing` `Crawling` `Self-heading` `Trailing` `Rhizomatous` `Epiphytic` `Terrestrial` | One value. |
| `mature_leaf_size` | `single_line_text_field` | ≤ 60 | `Up to 60 cm (24 in)`. Indoor, realistic. |
| `variegation` | `single_line_text_field` | ≤ 80 | `Albo, sectoral, stable` / `Aurea, marbled, can revert` / `Pink, splashed, stable`. **Blank for green plants.** |
| `rarity` | `single_line_text_field` | choices: `Uncommon` `Rare` `Very rare` `Ultra rare` | |
| `care_level` | `single_line_text_field` | choices: `Easy` `Moderate` `Advanced` | |
| `pet_safe` | `boolean` | `"true"` / `"false"` | **`false` for every aroid** (calcium oxalate). Begonia: `false`. |
| `light_level` | `number_integer` | 1–5 | 1 low-light tolerant · 2 medium · 3 bright indirect · 4 very bright indirect · 5 some direct sun. |
| `water_level` | `number_integer` | 1–5 | 1 dry out fully · 2 top half dry · 3 top few cm dry · 4 barely dry · 5 evenly moist. |
| `humidity_level` | `number_integer` | 1–5 | 1 room air · 2 40–50% · 3 50–60% · 4 60–70% · 5 70%+ / cabinet. |
| `care_light` | `single_line_text_field` | ≤ 160 | One plant-specific sentence. |
| `care_water` | `single_line_text_field` | ≤ 160 | |
| `care_humidity` | `single_line_text_field` | ≤ 160 | |
| `care_temperature` | `single_line_text_field` | ≤ 160 | Celsius first, Fahrenheit in brackets: `18–27 °C (65–80 °F). …` |
| `care_soil` | `single_line_text_field` | ≤ 160 | Must match the shop's acclimation guide: **Monstera and Anthurium** → "our magic mix: 80% long-fibre sphagnum, 10% perlite, 10% Fluval Stratum"; **everything else** → "50/50 Fluval Stratum and perlite" (chunky aroid mix once established is fine to add). |
| `care_fertilizer` | `single_line_text_field` | ≤ 160 | Rendered under the label "Feeding". |

### Session A — availability (4)

| Key | Type | Rule | Write |
| --- | --- | --- | --- |
| `availability_chance` | `single_line_text_field` | choices: `Confirmed` `High` `Medium` `Low` `Not available` | The verdict for the **open** batch. Blank = card hidden. |
| `last_batch_result` | `single_line_text_field` | choices: `Available` `Partially available` `Not available` `Not ordered` | What happened in the most recent closed batch. |
| `availability_note` | `single_line_text_field` | ≤ 160 | Optional, customer-facing. No supplier names, no costs, no internal codes. |
| `availability_updated` | `date` | `YYYY-MM-DD` | The day the chance was last reviewed. |

Suggested rule for the chance: **Confirmed** = the lab's confirmation sheet lists it for the
open batch · **High** = shipped in the last two batches · **Medium** = shipped once, or
partial · **Low** = the last batch refunded it · **Not available** = the lab has said no for
this batch. Set `availability_updated` on every write. Re-run after each supplier message.

### Already filled, read by the theme, leave alone unless wrong

`growth_stage`, `approximate_size`, `pot_size`, `root_condition` (the "What you'll receive"
tiles; tissue-culture products say Juvenile / 2–4 inch / NA / Establishing, rooted products
say 4–6 inch / 2 inch / Well established) and the two images `young` / `big_one`. Session B
should **flag** products where `big_one` is missing or is not a mature plant, but not delete
media. `custom.ready_to_ship` exists on some products with no definition; ignore it.

## 3. Writing rules (both sessions)

- One sentence per care line, plain, no exclamation marks, no emoji, metric first.
- Never write a price, a discount, a batch date, a cut-off, or "in stock" into any field.
  Those live elsewhere and go stale.
- Do not edit product titles, descriptions, tags, prices, variants, media or collections.
  Metafields only.
- Do not create metafield definitions, pin or unpin them, or change the `choices` lists.
- A field you are not sure about stays **blank**; the theme hides it. Wrong is worse than empty.
- Variegated plants: say in `care_light` that the pale sectors need more light, set
  `light_level` one higher than the green form, and fill `variegation`.
- Keep the owner's voice: calm, specific, honest. The shop already says plants vary and that
  the mature photo is a reference, so the fields do not need to repeat that.

## 4. Per-genus defaults (start here, then adjust the exceptions)

| Genus | growth_habit | care_level | light | water | humidity | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Alocasia | Rhizomatous | Moderate (Advanced for jewel types: Cuprea, Dragon Scale, Black Velvet, Azlanii) | 3 | 2 | 4 | Dormancy below ~15 °C; corms; "let the top half dry" |
| Philodendron | Climbing (most) / Crawling (Gloriosum, Plowmanii, Mamei) / Self-heading (Birkin, Prince of Orange) | Easy–Moderate | 3 | 3 | 3 | Give a pole to climbers |
| Monstera | Climbing (Deliciosa, Thai, Albo) / Trailing (Adansonii, Obliqua, Siltepecana) | Moderate (Advanced for Obliqua) | 3 | 3 | 3 (4–5 Obliqua) | Magic mix |
| Anthurium | Epiphytic | Moderate–Advanced | 3 | 3 | 4 | Magic mix; velvet-leaf types want 70%+ |
| Begonia | Rhizomatous (most) / Climbing (scandent types) | Advanced | 2 | 3 | 4 | No misting on leaves; airflow matters |
| Scindapsus / Rhaphidophora / Epipremnum | Climbing | Easy | 3 | 2–3 | 2–3 | |

Rarity guide: common nursery plants → **Uncommon**; most tissue-culture collector plants →
**Rare**; variegated forms of rare species and the big names (Spiritus Sancti, Devil Monster,
Caramel Marble, Cuprea Red Secret, Obliqua Peru) → **Very rare**; one-off mature specimens and
plants the shop prices above ~$400 → **Ultra rare**. Ask the owner only if a plant is unknown.

## 5. How to find the products and write the fields

Use the Shopify Admin GraphQL API (2026-10). `bulkOperationRunMutation` is blocked in this
environment and `bulkOperationRunQuery` withholds its download URL, so page instead:

```graphql
{ products(first: 100, query: "status:active", after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes { id handle title productType tags templateSuffix
      metafields(first: 30, namespace: "custom") { nodes { key value } }
      variants(first: 5) { nodes { title availableForSale } } } } }
```

Write with `metafieldsSet` — **25 metafields per call**, so one product per call is simplest
(18 or 4 fields). Type must be in every entry:

```graphql
mutation { metafieldsSet(metafields: [
  { ownerId: "gid://shopify/Product/8897132953679", namespace: "custom", key: "rarity", type: "single_line_text_field", value: "Very rare" },
  { ownerId: "gid://shopify/Product/8897132953679", namespace: "custom", key: "light_level", type: "number_integer", value: "3" },
  { ownerId: "gid://shopify/Product/8897132953679", namespace: "custom", key: "pet_safe", type: "boolean", value: "false" },
  { ownerId: "gid://shopify/Product/8897132953679", namespace: "custom", key: "availability_updated", type: "date", value: "2026-11-04" }
]) { metafields { key value } userErrors { field message code } } }
```

Aliased mutations (several `metafieldsSet` calls in one request) work; keep a request under
~40 aliases. Check `userErrors` on every call; a `choices` violation fails only that entry.

The worked example, fully filled, is **Alocasia Black Velvet Pink Variegated**
(`alocasia-black-velvet-pink`, `gid://shopify/Product/8897132953679`). Read its metafields
first and match the tone.

## 6. A-to-Z plan for Session B

1. Page every active product; build a table of handle, title, type, templateSuffix, which
   `custom` keys are already set, and whether `young` / `big_one` exist.
2. Group by genus, then by species (the title before "Variegated", "Pink", "Albo"…). Write the
   species facts once and reuse them across forms; change `variegation`, `rarity`,
   `light_level` and `care_light` per form.
3. Write per product: the 18 fields. Skip accessories and services (product type `Pots`,
   `Service`, `Mystery`, the starter kit, the mystery box) — leave their metafields blank.
4. After each genus, spot-check three product pages on the phone-width preview and fix
   anything that reads wrong (long values wrap; `mature_leaf_size` and `origin` should stay
   short).
5. Report at the end: products written, products skipped and why, products with no
   `big_one` photo, products whose title does not say which genus they are, and any plant
   you could not identify.

## 7. Plan for Session A (each batch)

1. From the batch payment / confirmation sheet, list every pre-order product by handle and
   the lab's answer.
2. Map to `availability_chance` with the rule in §2; set `last_batch_result` from the
   previous closed batch; write a one-line `availability_note` only when it helps the
   customer ("Confirmed by the lab for the November batch").
3. `availability_updated` = today, on every product you touch, including unchanged ones.
4. Products the lab has never been asked for: leave `availability_chance` blank (the card
   stays hidden) rather than guessing.
5. Report: counts per level, and the list of `Not available` plants so the owner can decide
   whether to keep selling them.

## 8. Verification

Preview a product page with `?preview_theme_id=<draft id>` (or the live site once the owner
has published) and check: the band shows the botanical name and pills; the facts grid has the
four lines; the care rows read as full sentences; the dots match the levels; the availability
card appears under the Plant Stage buttons for the pre-order stage and changes on a stage tap.
A "Liquid error" anywhere on the page means a value broke the template; blank the field and
report it.

## 9. Definition ids (`gid://shopify/MetafieldDefinition/…`)

plant_summary 580330520655 · botanical_name 580330553423 · origin 580330586191 ·
growth_habit 580330618959 · mature_leaf_size 580330651727 · variegation 580330684495 ·
rarity 580330717263 · care_level 580330750031 · pet_safe 580330782799 ·
light_level 580330815567 · water_level 580330848335 · humidity_level 580330881103 ·
care_light 580330913871 · care_water 580330946639 · care_humidity 580330979407 ·
care_temperature 580331012175 · care_soil 580331044943 · care_fertilizer 580331077711 ·
availability_chance 580365647951 · last_batch_result 580365680719 ·
availability_note 580365713487 · availability_updated 580365746255.

Earlier, already-existing: growth_stage 211463929935 · approximate_size 211464028239 ·
pot_size 211464618063 · root_condition 211464650831 · young 196511432783 · big_one 196511563855.
