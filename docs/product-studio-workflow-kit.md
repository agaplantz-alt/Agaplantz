# Product Studio — Prep Kit for the Plant Photo Workflow

Companion to [`google-merchant-image-audit.md`](./google-merchant-image-audit.md). The audit says
*which* 95 products need images. This says, for each one, **what raw reference already exists on
the site** and **what to type into Product Studio** — so those calls are made before you sit down
in the tool rather than during.

Readiness data: [`product-studio-reference-readiness.csv`](./product-studio-reference-readiness.csv)

## 1. Where the raw references already are

Step 1 of the workflow says check the AgaPlantz site first. Good news: for most products the site
already holds **both** raw shots you need.

The two bulk uploads flagged as P1 in the audit are named by role —
`1000XX-tc.jpg` is the tissue-culture shot, `1000XX-mature.jpg` is the mature plant. They are too
small to ship (186–364 px), but they are perfectly good **references to paste into Product
Studio**. That is exactly the input the workflow wants.

| Reference status | Products | What it means at the tool |
|---|---|---|
| Both TC and mature on-site | 69 | No Google Search needed. Screenshot both from the product page. |
| One on-site, one missing | 20 | One screenshot, one Google Search. |
| Neither (the P0 six) | 6 | Both from Google Search — no on-site asset exists. |

**32 Google searches total across all 95 products**, not 190. Roughly a sixth of what the workflow
would cost if you sourced every reference externally.

The 20 half-covered products are listed in the CSV with which half is missing, so you know before
opening each one whether to expect a search.

### The six with no on-site reference

These are the P0 products from the audit — no media at all in Shopify, so both references must come
from Google Search, and the cultivar check in step 5.4 matters most here:

- Alocasia Portei Aurea Variegated
- Alocasia Macrorrhiza Albo Variegated
- Alocasia Black Stem Variegated
- Alocasia Brancifolia Aurea Variegated
- Anthurium DocBlock Red Crystallinum Michelle F2
- Tissue Culture Starter Kit — *not a plant; needs a product shot of the kit itself, not this workflow*

## 2. Background and pot, by foliage type

Step 6 says don't force the same background on every plant, and step 7 says fix cheap pots. Rather
than deciding per plant at the tool, decide by **foliage type** — the choice is really driven by
contrast, and there are only a few cases.

| Foliage | Background | Pot | Why |
|---|---|---|---|
| Dark / velvet — Black Velvet, Infernalis, Anthurium Black Velvet, Nairobi Nights | Warm pale plaster or light natural stone | Matte cream or bone ceramic | Dark leaves vanish on a dark ground; the leaf edge needs a light field behind it |
| Silver / pale / crystalline — Silver Dragon, Crystallinum, Clarinervium, Anthurium Luxurians | Charcoal concrete or dark slate | Matte black or graphite stone | Reverse case — silver veining only reads against a dark ground |
| Pink / aurea variegated — Bambino Pink, Polly Aurea, Pink Princess | Clean neutral warm white, minimal | Simple off-white ceramic, low gloss | Variegation is the product; anything in the background competes with it |
| Large architectural — Macrorrhiza, Portei, Calidora, Regal Shields | Modern interior floor, soft daylight from one side | Large floor planter, neutral stone or concrete | These read as furniture-scale; a tabletop pot makes them look small |
| Compact jewel — Bambino, Polly, Melo, Nebula | Close tabletop, shallow depth of field | Small footed ceramic, matte | Scale cue matters; a big pot swallows them |
| Trailing / vining — Scindapsus, Micans, Vittarifolium | Simple ledge or shelf edge, plain wall behind | Straight-sided cylinder, neutral | Needs vertical room below for the trail to fall |

Pebbles and stone props only when the plant is small enough that the frame looks empty without
them. On a large plant they just add AI-artifact surface.

## 3. Prompt templates

### Tissue culture

⚠️ **Replace this with your own TC command.** The one you referenced is from an earlier session and
isn't available here — paste it and this section gets swapped for it. Until then, this draft encodes
the mandatory realism points from step 3 of the workflow:

```
Professional product photograph of a single tissue-culture plantlet of {PLANT NAME},
held by stainless steel laboratory tweezers gripping the base of the stem.
Clean seamless white laboratory background, soft even diffused lighting from above
and slightly to the left, with a soft contact shadow beneath.
The roots are short, pale, fine tissue-culture roots emerging directly from the stem
base, clearly attached, resting naturally — not floating, not suspended.
The tweezer tips make firm visible contact with the stem. Every leaf attaches to a
visible petiole. Botanically accurate leaf shape and variegation for {PLANT NAME}.
Shot on a macro lens, shallow but sufficient depth of field, sharp focus on the plant.
Realistic photograph, not an illustration or render.
No hands, no jars, no containers, no extra stems, no duplicated leaves.
```

### Mature plant

```
Professional product photograph of a mature {PLANT NAME} in a {POT}, placed in a
{BACKGROUND}. Soft natural directional daylight from one side, realistic contact
shadows where the pot meets the surface. The plant keeps the exact leaf shape,
venation, and variegation pattern of the reference image. Sharp focus on the
foliage, background slightly soft. Realistic photograph, not a render.
No extra plants, no text, no duplicated leaves, no floating elements.
```

Fill `{POT}` and `{BACKGROUND}` from the table in section 2.

## 4. Condensed QC pass

Run this on every generated set before upscaling. Any single failure means regenerate rather than
accept — per the core rule, realism beats aesthetics.

**Reject immediately if:**
- Roots float, or emerge from nothing
- Tweezers don't visibly contact the stem, or pass through it
- A leaf attaches to no petiole, or a petiole leads nowhere
- The plant is the wrong cultivar for the name
- Shadow direction disagrees with the light source
- Any hand, jar, or stray container appears
- The pot is disproportionate to the plant

**Then, only after it passes:** upscale → download → next plant.

## 5. Two things to decide before starting

1. **Rights on the `1000XX` files.** They appear to be grower catalog photos. Using them as a
   private Product Studio *reference* is a much weaker claim than publishing them, but if the
   generated output closely traces the source it inherits the problem. Worth confirming before
   running 87 of them.

2. **Whether generated imagery is right for the primary image.** For a plant sold on its exact
   variegation pattern, a generated photo shows a plant that doesn't exist — the buyer receives a
   different specimen. Consider generated images for the *mature* reference shot, where the
   customer understands they're seeing the plant's potential, and a real photograph for the
   plantlet they actually receive. Google's policy prohibits images that misrepresent the product.
