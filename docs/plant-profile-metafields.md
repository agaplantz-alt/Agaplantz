# Plant profile metafields — the fill plan

Created 4 Nov 2026. The product page's "About this plant" / "Care guide" pair is now
`blocks/plant-profile.liquid`, which reads these product metafields (namespace `custom`).
The block falls back to one generic line per care row until a product has its own value,
so a half-filled catalogue still renders cleanly. **Every field is optional**; a blank
field simply does not print.

Reference product, fully filled as the worked example:
**Alocasia Black Velvet Pink Variegated** (`alocasia-black-velvet-pink`,
`gid://shopify/Product/8897132953679`).

## New definitions (18)

| Key | Name | Type | Rule | What to write |
| --- | --- | --- | --- | --- |
| `plant_summary` | Plant summary | multi_line_text_field | ≤ 400 chars | 1–2 sentences on what makes the plant special. Opens the About card. |
| `botanical_name` | Botanical name | single_line_text_field | ≤ 80 | Genus + species, cultivar in quotes. Shown in italic Lora above the cards. |
| `origin` | Native range | single_line_text_field | ≤ 80 | Where the species grows wild. Hybrids: "Hybrid (cultivated)". |
| `growth_habit` | Growth habit | single_line_text_field | choices: Climbing · Crawling · Self-heading · Trailing · Rhizomatous · Epiphytic · Terrestrial | Exact spelling; also shown as a pill. |
| `mature_leaf_size` | Mature leaf size | single_line_text_field | ≤ 60 | "Up to 60 cm (24 in)". |
| `variegation` | Variegation | single_line_text_field | ≤ 80 | Type + stability, e.g. "Albo, sectoral, stable". **Blank for green plants.** |
| `rarity` | Rarity | single_line_text_field | choices: Uncommon · Rare · Very rare · Ultra rare | Terracotta pill. |
| `care_level` | Care level | single_line_text_field | choices: Easy · Moderate · Advanced | Pill reads "<value> care". |
| `pet_safe` | Pet safe | boolean | | `false` for every aroid (calcium oxalate). Pill "Not pet safe" / "Pet safe". Unset = no pill. |
| `light_level` | Light level | number_integer | 1–5 | 1 low-light tolerant · 3 bright indirect · 5 very bright. Five dots beside "Light". |
| `water_level` | Water level | number_integer | 1–5 | 1 dry out fully · 3 top few cm dry · 5 evenly moist. |
| `humidity_level` | Humidity level | number_integer | 1–5 | 1 room air · 3 50–60% · 5 70%+ / cabinet. |
| `care_light` | Care: light | single_line_text_field | ≤ 160 | One plant-specific sentence. |
| `care_water` | Care: water | single_line_text_field | ≤ 160 | |
| `care_humidity` | Care: humidity | single_line_text_field | ≤ 160 | |
| `care_temperature` | Care: temperature | single_line_text_field | ≤ 160 | "18–27 °C (65–80 °F)…" |
| `care_soil` | Care: soil | single_line_text_field | ≤ 160 | Match the acclimation guide: Monstera/Anthurium magic mix (80% sphagnum, 10% perlite, 10% Stratum); other aroids 50/50 Stratum and perlite. |
| `care_fertilizer` | Care: fertilizer | single_line_text_field | ≤ 160 | Rendered under the label "Feeding". |

## Existing definitions the block also reads (unchanged)

`growth_stage`, `approximate_size`, `pot_size`, `root_condition` — the "What you'll receive"
tiles. They are **product-level**, so on a listing with both a pre-order and an acclimated
variant they describe the stage the template is for: tissue-culture products
(`product.tissue-culture.json`) carry the plantlet (Juvenile / 2–4 inch / pot NA /
Establishing), default-template products carry the rooted plant (4–6 inch / 2 inch pot /
Well established). `NA`, `N/A`, `-` and `none` are treated as blank and never print.

`young` / `big_one` (file references) are the juvenile and mature photos at the top of the band
(juvenile falls back to the product's first image; with neither set the photo row is skipped). The
mature photo, blurred, is also the band's background, so a good `big_one` matters twice.

## Filling guidance

- Write with `metafieldsSet` (25 metafields per call max; batch by product). Types must be
  stated exactly as in the table; `choices` validation rejects any other spelling.
- Per-genus defaults make this fast: Alocasia (rhizomatous, water 2, humidity 4, dormancy
  line), Philodendron (climbing or crawling, water 3, humidity 3), Monstera (climbing,
  water 3, humidity 3, magic mix), Anthurium (epiphytic, water 3, humidity 4, magic mix),
  Begonia (rhizomatous, water 3, humidity 4, Advanced). Then adjust the few that differ.
- Variegated plants: say in `care_light` that the pale sectors need more light and will
  bleach or revert otherwise; set `light_level` one higher than the green form.
- Keep every line one sentence, plain, no exclamation marks, metric first with imperial
  in brackets. The owner reads these on a phone.
- Do not write prices, batch dates or availability into any of these fields — those live
  elsewhere and go stale.
- The Shopify standard taxonomy fields (`shopify.sunlight`, `shopify.watering-needs`,
  `shopify.preferred-soil-type`, `shopify.plant-care-difficulty`…) are metaobject lists used
  by the Shop and Google feeds. They were left alone; they do not drive the theme.
- The undefined `custom.ready_to_ship` metafield seen on some products has no definition
  and is not read by the theme; leave it.

## Example payload (the reference product)

```graphql
mutation { metafieldsSet(metafields: [
 { ownerId: "gid://shopify/Product/8897132953679", namespace: "custom", key: "plant_summary", type: "multi_line_text_field", value: "Velvet-black leaves with silver veins, splashed pink. One of the few Alocasia that stays small enough for a cabinet or a windowsill, and the pink holds as the leaves mature." },
 { ownerId: "...", namespace: "custom", key: "botanical_name", type: "single_line_text_field", value: "Alocasia reginula 'Black Velvet' (pink variegated)" },
 { ownerId: "...", namespace: "custom", key: "origin", type: "single_line_text_field", value: "Borneo (species); variegation cultivated" },
 { ownerId: "...", namespace: "custom", key: "growth_habit", type: "single_line_text_field", value: "Rhizomatous" },
 { ownerId: "...", namespace: "custom", key: "mature_leaf_size", type: "single_line_text_field", value: "Up to 15 cm (6 in)" },
 { ownerId: "...", namespace: "custom", key: "variegation", type: "single_line_text_field", value: "Pink, sectoral, stable" },
 { ownerId: "...", namespace: "custom", key: "rarity", type: "single_line_text_field", value: "Very rare" },
 { ownerId: "...", namespace: "custom", key: "care_level", type: "single_line_text_field", value: "Moderate" },
 { ownerId: "...", namespace: "custom", key: "pet_safe", type: "boolean", value: "false" },
 { ownerId: "...", namespace: "custom", key: "light_level", type: "number_integer", value: "3" },
 { ownerId: "...", namespace: "custom", key: "water_level", type: "number_integer", value: "2" },
 { ownerId: "...", namespace: "custom", key: "humidity_level", type: "number_integer", value: "4" },
 { ownerId: "...", namespace: "custom", key: "care_light", type: "single_line_text_field", value: "Bright, indirect light keeps the leaves black; direct sun bleaches the pink." },
 { ownerId: "...", namespace: "custom", key: "care_water", type: "single_line_text_field", value: "Let the top half of the mix dry out, then water well. Soggy roots are the usual cause of loss." },
 { ownerId: "...", namespace: "custom", key: "care_humidity", type: "single_line_text_field", value: "60–80%. A cabinet or a humidity dome for the first weeks after acclimation." },
 { ownerId: "...", namespace: "custom", key: "care_temperature", type: "single_line_text_field", value: "20–28 °C (68–82 °F). Below 15 °C it may go dormant." },
 { ownerId: "...", namespace: "custom", key: "care_soil", type: "single_line_text_field", value: "50/50 Fluval Stratum and perlite, as in our acclimation guide." },
 { ownerId: "...", namespace: "custom", key: "care_fertilizer", type: "single_line_text_field", value: "Quarter-strength liquid feed every two weeks while it is putting out leaves." }
]) { metafields { key } userErrors { field message code } } }
```

Definition ids: plant_summary 580330520655 · botanical_name 580330553423 · origin 580330586191 ·
growth_habit 580330618959 · mature_leaf_size 580330651727 · variegation 580330684495 ·
rarity 580330717263 · care_level 580330750031 · pet_safe 580330782799 · light_level 580330815567 ·
water_level 580330848335 · humidity_level 580330881103 · care_light 580330913871 ·
care_water 580330946639 · care_humidity 580330979407 · care_temperature 580331012175 ·
care_soil 580331044943 · care_fertilizer 580331077711 (all `gid://shopify/MetafieldDefinition/…`).

## Availability chance (added 4 Nov 2026, evening) — filled by the batch/supplier session

`blocks/availability-chance.liquid` sits twice in the buy box of both product templates
(`availability_top`, one line under the price; `availability_bottom`, a card with a four-bar
meter under the buy buttons). It renders **only for the Tissue Culture (Pre-Order) variant**
and only when `availability_chance` is set; on an in-stock ready-to-ship / acclimated / mature
variant it prints "In stock, ready to ship" instead; on a sold-out variant, nothing. The (?)
opens a pop-up: the general explanation (a block setting) plus this plant's last-batch line,
note and date.

| Key | Name | Type | Rule | What to write |
| --- | --- | --- | --- | --- |
| `availability_chance` | Availability chance | single_line_text_field | choices: Confirmed · High · Medium · Low · Not available | The verdict. Confirmed = the lab has confirmed it for the open batch (filled moss pill). Not available = we will take the order but expect to refund. Blank hides both blocks. |
| `last_batch_result` | Last batch result | single_line_text_field | choices: Available · Partially available · Not available · Not ordered | What happened last time. Rendered as a sentence ("Last batch: not available at the lab, orders were refunded."). |
| `availability_note` | Availability note | single_line_text_field | ≤ 160 | Optional, customer-facing, one line. No supplier names, no costs. |
| `availability_updated` | Availability updated | date | `YYYY-MM-DD` | When the chance was last reviewed. Shown as "Updated 4 November 2026". |

Definition ids: availability_chance 580365647951 · last_batch_result 580365680719 ·
availability_note 580365713487 · availability_updated 580365746255.

Suggested rule for the batch session: **Confirmed** once the lab's confirmation sheet lists
the plant for the open batch; **High** if it shipped in the last two batches; **Medium** if it
shipped once or was partial; **Low** if the last batch refunded it; **Not available** if the
lab has said no for this batch. Re-run after every supplier confirmation and set the date.
Example product: Alocasia Black Velvet Pink Variegated (High / Available / 2026-11-04).
