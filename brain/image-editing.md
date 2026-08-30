# Image editing — how Agaplantz wants it done

House rules for editing plant photos and ad creatives. Claude follows this file
without being reminded. If an edit comes back wrong, fix the rule here, not just
the image.

## Status

The *intent* (the rules taught in an earlier session) is still missing. But the
*current practice* below was observed directly from live product images on
2026-08-30 — three files pulled from the Shopify CDN and inspected.

## Observed current practice (2026-08-30)

Every product photo is a **composite**: the plant is cut out of the original
shot and placed on a synthetic backdrop.

- **Format:** 2048 x 2048 PNG, square, no transparency
- **Filenames:** `edited-edited_-_<ISO timestamp>.png` — batch-exported from an
  editing tool, one per plant
- **Backdrop:** a studio scene with a visible wall/floor horizon line around
  62-65% down the frame
- **Light:** a diagonal shaft of window light across the wall, with a soft cast
  shadow falling to the lower left. Added, not from the original photo.
- **Pot:** the real nursery pot is kept — clear/frosted plastic, lava rock and
  perlite substrate, visible mineral crust. Never swapped for a decorative pot.
- **Plant position:** centred, occupying roughly the middle third, generous
  negative space all around
- **Support stakes** are kept in frame when present (see Gloriosum Variegated)

### Backdrops in use — not consistent

| Product | Backdrop |
| --- | --- |
| Monstera Bulbasaur (TC) | cold grey concrete/plaster |
| Philodendron Gloriosum Variegated (mature) | warm cream travertine |
| Philodendron Spiritus Sancti (ready to ship) | plain white seamless |

**Two problems this creates:**

1. **Backdrop colour is inconsistent across the catalogue.** A collection grid
   mixes cold grey, warm cream and white. The store palette is warm
   (`#FBF8F2` cream, `#F2EBDE` sand) — the cream travertine matches it, the
   cold grey concrete fights it.
2. **Scale is inconsistent.** The Spiritus Sancti (`IMG_0097.png` — the only
   file not named `edited-edited`) shows the plant tiny in the frame, maybe a
   tenth of the height the others occupy. Next to them in a grid it looks like
   a lesser plant, which for a Spiritus Sancti is the opposite of the truth.

## The look

- Background: TODO (keep original / remove / plain white / studio / lifestyle?)
- Lighting & color: TODO (brighter? warmer? true-to-leaf green, no oversaturation?)
- Crop & framing: TODO (how much space around the plant, is the pot included?)
- Pot / props: TODO (keep, swap, remove?)
- Retouching: TODO (remove damaged leaves? soil mess? labels? tags?)

## Text on image

- Do we add text at all: TODO
- Font: TODO
- Color: TODO
- Placement: TODO
- Plant name — Latin, common, or both: TODO

## Branding

- Logo: TODO (used? where? how big?)
- Watermark: TODO
- Brand colors (hex): TODO

## Sizes / aspect ratios

| Use | Ratio | Notes |
| --- | --- | --- |
| Instagram feed | TODO | |
| Instagram / TikTok story | TODO | |
| Meta ad | TODO | |
| Shopify product photo | TODO | |

## Never do this

TODO — the corrections matter most. Every "no, not like that" from a past
session belongs here as a line.

## Tools

- **Canva** (connected) — generate, edit, resize, export designs.
- **Meta Ads** (connected) — upload finished creatives to the ad account.
- Local editing via scripts (ImageMagick / Python) when a precise, repeatable
  transform is wanted.

Record which tool worked for which job here, so the next session starts with the
right one: TODO
