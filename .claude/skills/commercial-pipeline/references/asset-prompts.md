# Stage 1 — asset image prompts

Reference images carry identity. The video prompt carries behaviour. Everything a reference gets wrong has to be fought in every segment afterwards, so the cheapest place to fix a film is here — and for plants, the reference is where the leaf count and the variegation get decided.

## House format

Plain text in one code block. Section labels in CAPS on their own line, prose underneath. No markdown, no bullets, no bold inside the prompt.

```
[one declarative opening line — what this image is]
BACKGROUND LOCK
SUBJECT
LEAF LOCK                      — every plant or plantlet asset
[MATERIAL or VESSEL LOCK]      — if the asset has a paired state
[SCALE LOCK]                   — if relative size is the point
LIGHTING
COMPOSITION
STYLE
NEGATIVE
ASPECT RATIO
```

Not every asset needs every section. Order does not vary.

## Before writing any prompt: what already exists

Check the listing photos and ask for phone shots. A real photo of the actual plant, cropped to a plain background, beats a generated hero on identity and needs no LEAF LOCK to be honest — it *is* the leaf lock. Use generated assets for what wasn't photographed: the location, the hands, the plantlet if no one shot it, a cleaner cutout when the real background is cluttered. When a real photo is the reference, still write its reference line in Stage 2 from what the photo shows, leaf by leaf.

## The five rules that matter

**1. Flat light on anything that travels.** Plants and hands appear under every lighting state in the film. Bake a dramatic key into the reference and the model fights it in every segment. Use the anti-studio block:

```
LIGHTING
This is not a studio photoshoot. No studio lights, no softboxes, no flash, no hard
directional key, no dramatic highlights. Plain ordinary soft ambient light wrapping
the subject evenly from all sides, gentle and uniform, no visible light direction,
no hotspots, no deep shadows. The only shadow in the image is a faint soft natural
contact shadow directly beneath the pot.
```

The location is the exception. It does not move through the film, so it is where the lighting design gets established, and it should be lit deliberately — usually one real window.

**2. Redundancy beats precision on backgrounds.** Models leak rooms into product shots. State the background four ways in one paragraph:

```
BACKGROUND LOCK
The entire background is seamless pure white: white behind the plant, white surface
beneath the pot, white to every edge of the frame. No room, no table, no walls, no
props, no other plants, no soil spill, no textures, no gradients, no colour anywhere
in the background — only the plant on infinite clean white, like a catalogue cutout.
```

**3. The leaf paragraph is the identity, and paired assets share it verbatim.** A plant's face is its leaves. Write one LEAF LOCK paragraph — count, shape, size relative to the pot, colour, sheen, and the variegation map in physical terms — and copy it word for word into every asset of the same plant (hero, plantlet, close-up). Two separately written descriptions of "mint variegation" produce two different plants, and the video model will pick a third.

```
LEAF LOCK
Exactly five leaves. Each leaf is a broad heart-shaped shield with a deeply
puckered, quilted surface, matte deep green with a metallic copper sheen across
the raised ridges and near-black in the valleys. Variegation is pale mint-green
sectors: one leaf carries a clean half-moon of mint on its left half, two leaves
carry narrow mint streaks along the midrib, two leaves are fully green. No white.
No pink. No yellow. The pattern is fixed: the same leaves carry the same sectors.
```

Physical terms, not adjectives: which leaf, which half, which colour, how many. "Beautiful mint variegation" gives the model permission to redraw it.

**4. Describe the variegation the store sells.** Pull the listing photos before writing the leaf paragraph. If the batch delivers plants with a few mint streaks, the reference has a few mint streaks — not a full half-moon on every leaf. The ad is a promise, and the refund policy already says variegation isn't guaranteed; don't make the gap bigger.

**5. Scale is a video-prompt problem.** Generate the plantlet at its real size in its real vessel. Trying to make it look substantial in the image distorts it. The contrast with the mature plant is stated in the reference line in Stage 2.

## By asset class

### Hero plant (acclimated, potted)

Pure white, catalogue cutout, flat light. Plain nursery pot in one stated colour (black or terracotta — the store's photos use both; pick one and lock it) with the soil surface visible and flat. No moss pole unless the plant is a climber sold with one. No water droplets — they become rain in the video.

LEAF LOCK is mandatory. State the plant's facing: which leaf is nearest camera, which way the newest leaf points. That facing is what the GEOMETRY LOCK will hold in Stage 2.

Aspect: 1:1 for anything that will pair with the plantlet; 4:5 if it's only ever a hero.

### Tissue-culture plantlet

What a pre-order buyer receives. Small — leaves a few centimetres — pale green, thin pale roots, often with a trace of clear gel at the base. Generate it two ways depending on the film:

- **In the vessel**: sealed clear culture jar or bag, the plantlet inside, agar visible as a pale layer at the bottom. VESSEL LOCK paragraph describes the container (shape, lid colour, label-free).
- **Out of the vessel**: on a clean white surface, roots exposed, a hand's-width of scale reference is allowed (a fingertip) but no full hand.

LEAF LOCK is the same paragraph as the hero, with the count and size adjusted honestly: *three leaves, each smaller than a thumbnail, same shield shape, mint sectors already visible on one leaf.* The variegation map is described in the same order and words so the two assets read as one variety.

No dressing up. If the plantlet looks like a seedling, that's correct.

### Vessel, dome or shipping box

Anything the plant goes into or comes out of and appears in more than one shot. Gets its own MATERIAL LOCK — the AgaPlantz box is plain kraft with the logo applied in the edit, not generated; the humidity dome is clear, unbranded, one stated shape. These are the objects most likely to drift between the before and the after.

Aspect: 1:1.

### Location

The one asset lit deliberately. For AgaPlantz that's usually one of three:

- **A Canadian apartment windowsill or plant shelf** — real daylight from one window, wood or white shelf, a few *other* plants allowed as background but the hero's spot left empty.
- **The Brampton grow bench** — white racks, grow-light bars, humidity, other plants in the depth.
- **A lab bench** — only for tissue-culture explainers; sterile, white, glassware.

Generate it **empty of the hero**. The playing area — the shelf spot, the bench square — must be clear. Every extra pot on the shelf is one more object the model has to keep still. Background plants are fine at a distance; give them the same LEAF-style discipline in one line ("background plants stay green, out of focus, and never change").

Aspect: match the film — 9:16 for a Reel, 16:9 for the site.

### Hands

A hands-only sheet: both hands, palms and backs, wrist to fingertip, on plain light grey, flat light. One or two identity anchors that survive: a plain ring, a sleeve cuff colour, short natural nails. No face, no arms above the elbow. Faces cost consistency and the ad doesn't need them; hands sell the plant and read as human.

Add a **performance lock** alongside the look: *calm, unhurried, never grabbing; lifts by the pot, never by the leaves.*

Check finger count in every generation. It's the plant-ad equivalent of the missing head on a character sheet.

### Logo

Never generate it. Use the file. A regenerated logo is wrong in a way Agam will notice instantly.

## Delivering a Stage 1 artifact

Name the model, say batch 4, then give three specific things to judge on — not "which looks best". Good judging criteria are binary and check the thing the prompt was fighting for: *does the leaf count match the lock, is the mint on the leaves the lock says and nowhere else, is the white truly white to every edge, are there exactly five fingers.*

Close with a one-line statement of assumptions, and name which paragraph is the shared one if the asset is half of a pair — for plants it's always the LEAF LOCK.
