---
name: commercial-pipeline
description: End-to-end workflow for producing short AI video ads and brand films for AgaPlantz (agaplantz.com), a Canadian rare-plant and tissue-culture shop — planning the reference images, writing the image prompts that generate them, writing the multi-segment video prompt that assembles them for models like Seedance, Veo, Kling, Sora and Runway, and diagnosing what broke between generations. Use it whenever Agam is working toward any plant ad, Reel, TikTok, Meta video, product video, pre-order teaser, unboxing, launch spot, brand film or store header video, including when only one piece is asked for — a plant on white, a tissue-culture plantlet reference, a windowsill location plate, a hands sheet, a video prompt, a 9:16 cut of an existing prompt, or a fix like "the leaves keep changing between shots". Trigger even when nobody says "ad" or "commercial": "make a video for the Cuprea", "I need a reel for the pre-order", "the plant grew a leaf between cuts" and "give me a hero shot of the Albo" are all stages of this pipeline and the house rules apply.
---

# Commercial pipeline — AgaPlantz edition

A four-stage workflow for making short branded plant films with reference-driven video models. Every stage produces one artifact and names the next.

```
STAGE 0  BRIEF         platform, format, offer, hero plant, angle, one true claim
STAGE 1  ASSETS        image prompts → reference images, one per element
STAGE 2  VIDEO PROMPT  one long structured prompt that assembles them
STAGE 3  FIXES         diagnose a bad generation, rewrite only what broke
```

The pipeline exists because video models cannot hold identity, geography and continuity from prose alone. Identity is moved out of the video prompt and into images. What remains in the video prompt is behaviour, timing and rules. For plants that matters twice over: a plant's identity **is** its leaf count, leaf shape and variegation map, and video models redraw all three between cuts unless told, in absolutes, not to.

## Reading order

Read the reference file for the stage you are in. Do not read all of them.

| File | Read when |
|---|---|
| `references/plant-ad-formats.md` | Starting any ad (Stage 0): platform specs, durations, ad structures, plant buyer angles, and the AgaPlantz truth rules every ad must obey |
| `references/asset-prompts.md` | Writing any image prompt — plant, plantlet, vessel, packaging, location, hands, logo |
| `references/video-prompt.md` | Writing or rewriting the video prompt; contains the plant lock catalogue |
| `references/fix-playbook.md` | Agam reports a problem with a generation |
| `references/example-commercial.md` | Before writing a social plant ad from scratch — a 15-second 9:16 pre-order Reel in full |
| `references/example-pizza-30s.md` | Only for a long-form 16:9 film; the original the architecture was proven on |

## How to behave

**Produce first, ask second.** "A Monstera on white" wants the prompt, not a discovery call. Write it, state assumptions in one line at the end, and let Agam correct. Ask only when the answer changes the whole artifact and cannot be assumed — which plant, and pre-order or ready-to-ship, are the two that usually can't.

**Default to the social cut.** Unless told otherwise, the ad is 9:16, 15 seconds, sound-off-safe, for Meta Reels and TikTok. That is where the store's paid spend goes. Offer the 1:1 feed and 16:9 site versions as a follow-up, not as the first artifact.

**One artifact per turn.** Deliver the current stage, then name the next stage in one line. Do not run ahead into stages Agam has not reached.

**Every prompt goes in a single code block**, plain text, no markdown formatting inside it. Agam is pasting it into a generation tool. Commentary lives outside the block.

**Always name the model and always say batch 4.** Identical prompts diverge hard. One generation tells you nothing about whether the prompt is good.

**Always say what to judge the batch on** — three or four specific checks, in priority order, and for plant work the first one is nearly always *is it still the same plant in every shot*. Never "pick the one you like best".

**Check the store before writing about a plant.** If the Shopify connector is available, pull the live listing (`search_products`, `get-product`) so the variegation type, format (single or pack), and pre-order status in the ad match what's actually for sale. An ad for a plant the store sells as a 5-pack that shows one lush specimen is a refund request waiting to happen.

**Prompts stay in English.** Talk to Agam in whatever language he uses; the models are trained on English.

## Stage 0 — the brief

Ten lines, filled with defaults where Agam didn't say. Full guidance in `references/plant-ad-formats.md`.

```
Platform / placement:  Meta Reels + TikTok in-feed (default)
Aspect / length:       9:16 · 15.0s (default)   |  1:1 · 6–10s feed  |  16:9 · 30s site/YouTube
Hero plant:            exact store title, e.g. Alocasia Cuprea Red Secret Mint Variegated
Offer:                 pre-order (batch) | ready to ship | acclimated plant | pack of N
Angle:                 rarity | collector | value | new arrival | beginner | discovery
The one true claim:    e.g. "lab-grown, pest-free, ships across Canada"
Hook (0–2s):           the first frame and the on-screen line
CTA:                   Pre-order now | Shop now | See what's in stock
Assets on hand:        photos / logo file / nothing yet
Sound:                 SFX only (default) | music bed added in edit
```

The brief is what the rest of the pipeline is built from. If the offer is a pre-order, the ad shows a tissue-culture plantlet honestly at some point — that's what arrives in the box.

## Stage 1 — assets

Plan the full asset list before generating anything. A social plant ad needs three to six references:

- **Hero plant** — acclimated, potted, on pure white, flat light. The thing the buyer wants.
- **Tissue-culture plantlet** — what a pre-order customer actually receives: small, pale-rooted, in or just out of its sealed vessel. Honest scale, never dressed up.
- **Culture vessel or shipping box** — the container that carries the plantlet; gets its own lock if it appears in more than one shot.
- **Location** — a Canadian windowsill, plant shelf, or the Brampton grow bench, empty of the plant, lit the way the film will be lit.
- **Hands** — a hands-only sheet (no face) with one identity anchor: nail colour, a ring, a sleeve cuff. Faces cost consistency and the ad doesn't need them.
- **Logo** — never generate it. Use the file.

Each asset is a separate prompt and a separate batch. Full craft rules in `references/asset-prompts.md`. The rules that matter most:

- **References carry identity, prompts carry behaviour.** Flat ambient light on the plant and the hands so they survive every lighting state. The location is the exception and establishes the lighting design.
- **Paired assets share paragraphs verbatim.** Plantlet-in-vessel and plant-on-shelf must read as the same variety: the leaf paragraph (shape, colour, variegation map) is copied word for word between the two prompts.
- **Generate the variegation the store actually sells.** A reference with more white than the batch delivers is a customer-service problem, not a creative choice. Pull the listing photos and describe those.
- **Scale lives in the video prompt.** Generate the plantlet at its real size and state the contrast with the mature plant in the reference line later.

## Stage 2 — the video prompt

One long structured prompt in a fixed section order. Full architecture and the plant lock catalogue in `references/video-prompt.md`; worked example in `references/example-commercial.md`.

```
SCENE CONTEXT · ACTIVE REFERENCES · LOCATION MAP · LEAF LOCK · GEOMETRY LOCK
FIRST FRAME AND SPATIAL BLOCKING · FORMAT MODE · SAFE ZONE LOCK
OPTICS · LIGHTING PROGRESSION · CAMERA · ACTION TIMING
PHYSICS · AUDIO · TEXT RULE · POSITIVE LOCKS · global style tail
```

Spatial rules before camera style. Optics before aesthetic language. Lighting is a lock, not decoration. Everything critical appears twice — once where it applies, once in POSITIVE LOCKS.

**Assign the reference handles yourself.** Agam should never have to work out which reference belongs in which segment.

**Write the assets you actually have, not the ones you planned.** If the generated hero plant has five leaves, the reference line says five leaves. A reference line describing a half-moon leaf that didn't generate is worse than no reference line.

**Text stays out of the model.** Hooks, prices and CTAs are overlaid in the editor. The only text the model renders is the logo endcard, from the logo file. Say so in the TEXT RULE section or the model will write "PLANT" on the pot.

## Stage 3 — fixes

When Agam reports a problem: name the failure, apply the fix, rewrite **only** the affected sections, say what to re-batch. Never re-roll an unchanged prompt.

The master rule, and the highest-value lesson in the whole workflow:

> **If something keeps breaking between cuts, stop describing it better inside every shot. Give it its own lock.**

For plants the thing that keeps breaking is the plant itself — leaf count, leaf shape, the variegation pattern, the pot, which way the plant faces. Those get a LEAF LOCK and a GEOMETRY LOCK, stated in absolutes, restated in every segment. Adding "the same plant" inside each of eight segments does not work.

Full failure catalogue, with the plant-specific rows, in `references/fix-playbook.md`.

## The complexity budget

Every prompt has one. Once a prompt is generating clean results, one more brilliant idea often just gives the model one more thing to get wrong. For a 15-second plant Reel, expect six to eight generations, of which two or three are actual prompt changes. When a version is clean, stop and ship it. If a change made things worse, revert to the last clean version rather than trying to fix forward.

## Truth rules that override any brief

These come from the store's published policies and the support inbox. They apply to every frame and every overlay. The long form is in `references/plant-ad-formats.md`.

- Never promise variegation, size, leaf count or survival. Show representative plants and say so if the overlay makes a claim.
- Never show or state a delivery date. Pre-orders are described as a batch.
- Never invent scarcity. "Only 3 left" appears only when Shopify says so.
- Never show a tissue-culture pre-order as a mature plant without also showing the plantlet.
- Canada only. No US or international shipping language.
- No care how-to in the ad. The acclimation guide exists for that.
