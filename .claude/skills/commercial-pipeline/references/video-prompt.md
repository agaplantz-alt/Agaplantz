# Stage 2 — video prompt architecture

One long structured prompt. For a social plant ad read `example-commercial.md` before writing from scratch; for a long-form 16:9 film read `example-pizza-30s.md` for density.

## Section order

```
SCENE CONTEXT
ACTIVE REFERENCES
LOCATION MAP
LEAF LOCK
GEOMETRY LOCK
FIRST FRAME AND SPATIAL BLOCKING
FORMAT MODE
SAFE ZONE LOCK                  (9:16 and 4:5 only)
[EDIT ACCELERATION LOCK]        (30s films)
OPTICS
LIGHTING PROGRESSION
CAMERA
ACTION TIMING
PHYSICS
AUDIO
TEXT RULE
POSITIVE LOCKS
[global style tail]
```

Spatial rules before camera style. Optics before aesthetic language. Locks before the segments they govern, so the segments can reference them by name. Sections in brackets are conditional — include them when the film has the problem they solve.

## Reference handles

Handles are `<<<image_1>>>` … `<<<image_N>>>`, numbered in the order images are attached. Not `@tags`.

Every reference gets one line: identity anchors only, then the fidelity phrase.

```
<<<image_1>>>: Alocasia Cuprea Red Secret Mint Variegated, acclimated plant in a plain
black nursery pot, five quilted shield leaves with a metallic copper sheen, one leaf
carrying a mint half-moon on its left half, two with mint midrib streaks, two fully
green. 100% matches the reference.
```

`100% matches the reference.` closes every line. Anchors only — the image already carries the leaves, and prose piled on top competes with it.

**Describe what generated, not what was planned.** If the hero came back with six leaves, the line says six leaves, and so does the LEAF LOCK. A reference line that contradicts its own image is worse than no reference line.

Two things ride on reference lines that people usually put elsewhere:

- **The scale contrast** between plantlet and plant goes on the plantlet's line: *in this film the plantlet is small enough to sit inside a closed hand; its largest leaf is smaller than a thumbnail.*
- **The logo's permitted placements** are declared on its reference line, then repeated in POSITIVE LOCKS. For AgaPlantz that's the endcard, and at most one diegetic surface (the shipping box), never on the pot.

## What each section does

**SCENE CONTEXT** — one paragraph, the whole ad start to finish, in plain language. Concept, not craft. Name the offer: *a pre-order teaser for…*

**LOCATION MAP** — the location reference converted into geography: the window and which side it's on, the shelf or bench, what's along the depth, where the empty playing spot is. Name the zones in caps (`THE SHELF SPOT`, `THE BENCH SQUARE`) so segments can reference them. Include the living background in one line — *two other plants sit out of focus at the far end of the shelf and never change* — because a dead shelf reads as a render.

**LEAF LOCK** — see the catalogue below. Mandatory in every plant film.

**GEOMETRY LOCK** — for the pot, the vessel, the dome: anything that must hold position across cuts. Catalogue below.

**FIRST FRAME AND SPATIAL BLOCKING** — what is on screen at frame one, stated as an image, plus `No empty establishing frame.` For a Reel the first frame is the hook: the leaf trait already filling the frame, or the box already half-open. Nothing before the interesting thing.

**FORMAT MODE** — aspect, segment count, runtime, cut types, and a ban on everything else: *9:16 vertical, eight scripted segments across 15.0 seconds, HARD CUTS only, every cut hidden in motion. No fades, no dissolves, no unscripted cuts.*

**SAFE ZONE LOCK** — the UI band rule from `plant-ad-formats.md`. The hero and hands live in the central 66% of frame height.

**OPTICS** — one `LENS LOCK` line per segment, in **degrees of diagonal field of view**, never millimetres. Close with `No lens drift mid-segment.`

Rough map: 8° super-telephoto · 18° macro insert · 29° short telephoto and product macro · 47° standard normal · 84° classic wide · 107° wide rectilinear.

For plant macro blocks give each shot its own camera distance and angle. Leaves are the product block of a plant ad; without per-shot distances, four leaf macros collapse into the same shot four times.

**CAMERA** — operator behaviour plus any global movement law. *Every shot moves from its first frame*, with named exceptions. Plant ads want slow: a slow push, a slow arc, a slow tilt. Whip pans and crash zooms belong to the pizza film, not to a windowsill.

**ACTION TIMING** — the body of the prompt. Every segment gets a range, an ID, a lighting tag, its anchor names, and an explicit cut marker. Timings run to one decimal and every gap is filled. Write hand mechanics the way a director would: *the right hand takes the pot by its rim, thumb outside, lifts it ten centimetres, sets it down on THE SHELF SPOT — never touching a leaf.*

**PHYSICS** — leaves have weight and spring: they sway once when the pot is set down and settle within a second, they do not flutter without wind, they do not unfurl. Soil stays in the pot. Gel is viscous and slow. Condensation on a dome forms as a haze, not as drops that run. Steam never rises from a plant.

**AUDIO** — a sound-design pass in film order, not a list: the papery slide of a box lid, the soft click of a dome, a pot set down on wood, room tone with a distant street. SFX only unless asked.

**TEXT RULE** — *The model renders no text of any kind: no words on the pot, no label on the vessel, no writing on the box, no captions, no watermark. The only text in the film is the logo endcard from* `<<<image_N>>>` *at the scripted time.* Hooks and CTAs are overlaid in the edit.

**POSITIVE LOCKS** — every non-negotiable restated as a hard rule in plain declarative sentences. Everything here is also written inside the segment where it applies. Saying it twice is the point.

**Global style tail** — an unlabelled closing paragraph: aspect, grain, bokeh behaviour, framing law, cut law, absolutes. End on the hard ones — `NO CGI. NO TEXT. NON-IP.`

## The plant lock catalogue

Locks are how a rule survives a cut. Each one is a named section or a named line, stated in absolutes, and restated in POSITIVE LOCKS.

### LEAF LOCK

The single most valuable section in a plant film. Video models redraw foliage between cuts the way they redraw faces, and a plant with a new leaf in shot four is a different plant.

```
LEAF LOCK — THE PLANT
"The plant" means <<<image_1>>>. There is only ever ONE of it in the film.
LEAF COUNT: exactly five leaves in every segment where the plant appears. No leaf
appears, unfurls, opens, grows, drops, or is hidden and replaced. Five in S2, five
in S5, five in S6, five in S7, five in S8.
LEAF MAP: leaf one, nearest camera and lowest, carries the mint half-moon on its
left half. Leaves two and three, mid-height, carry a single mint streak along the
midrib. Leaves four and five, highest and newest, are fully green. The same leaves
carry the same sectors in every shot. Variegation does not move between leaves,
does not spread, does not fade, does not change colour. No white, no pink, no
yellow, no cream anywhere on the plant.
LEAF FORM: broad shield-shaped, deeply quilted, metallic copper sheen on the
ridges, near-black in the valleys. Leaves do not change shape, size, or texture
between cuts.
RESTATEMENT: every segment that shows the plant names THE PLANT and its leaf
count.
```

Four clauses earn their place:

- **A definition clause** — only ONE plant exists. Without it a second pot appears at the end of the shelf.
- **Explicit negation of every drift mode** — appears, unfurls, grows, drops. Listing the failure modes works; asserting "stays the same" doesn't.
- **A leaf map in physical terms** — which leaf, which half, which colour. This is what stops the variegation wandering.
- **A restatement requirement** — the count is named in every segment, not inherited.

The plantlet gets its own LEAF LOCK with its own honest count, linked to the plant's by the same map language: *the mint half-moon that will be leaf one is already visible as a mint edge on the plantlet's largest leaf.*

### GEOMETRY LOCK

For the pot, vessel, dome or box. Anchor to a **world landmark**, never to screen coordinates.

```
SHELF ANCHOR — governs S5 to S8
Position: on the wooden shelf, one hand's width in from the window-side end,
directly below the window's centre mullion.
Orientation: leaf one faces CAMERA. The pot does not rotate.
THE POT NEVER MOVES OR TURNS ON THE SHELF.
It does not slide. It does not rotate to show a better leaf. It does not shift
toward the window. It does not get re-centred. The anchor is a place ON THE SHELF,
not a place in the frame. When the camera moves, the pot does not.
```

If the pot legitimately moves once — lifted out of a box, set down on the shelf — give it a second anchor and **show the transit on screen**. An unshown move reads as a teleport.

If the film has a hidden swap — plantlet under the dome becomes the acclimated plant when the dome lifts — the swap inherits the anchor and says so: *the object changes, the position does not.* Never both in frame.

### HANDS LOCK

```
HANDS LOCK: <<<image_4>>> are the only hands in the film. Two hands, five fingers
each, short natural nails, plain silver ring on the right hand. Hands hold the pot
by its rim or base and never touch a leaf. Hands never obscure leaf one. No face,
no forearm above the elbow, no second person's hands.
```

### DOME / VESSEL LOCK

```
DOME LOCK: one clear unbranded dome, the same dome in every shot it appears in.
Condensation reads as an even soft haze on the inside, never as running drops. The
dome never changes shape, tint or size. It lifts once, in S5, straight up.
```

### LIGHTING PROGRESSION

Lighting written as prose is decoration and gets ignored. Written as named states and tagged per segment, it becomes a rule. A 15-second plant ad needs two or three:

```
LIGHT STATE A — WINDOW, S1 to S4. Soft daylight from the single window camera-left,
overcast, no direct sun. Even on the leaves, a faint cool rim on the far edges.
LIGHT STATE B — SUN, S5 to S8. Triggered as the dome lifts: a low warm shaft of
direct sun crosses the shelf from camera-left, raking across the leaf ridges so the
copper sheen catches. Strictly realistic — no glow, no bloom, no god rays.
```

Bind the transition to a frame: *STATE A cuts to STATE B as the dome clears the leaves, not after.*

### PRODUCT VARIETY LOCK

For any block of consecutive leaf shots:

```
LEAF VARIETY LOCK: S6, S7 and S8 are THREE different shots of THE PLANT. Each
differs in angle, distance and camera move. In order: low skimming lateral across
the ridges, top-down on the mint half-moon, slow pull-back to the hero frame. No
repeats.
```

## Patterns for plant ads

- **Hidden transformation, honestly.** Plantlet under the dome, plant when the dome lifts. Never ask the model to grow the plant. Never both in frame. Because the plantlet is what ships, the plantlet gets its own honest beat *before* the cover, with the overlay saying what it is.
- **Start every segment on the action.** If the beat is opening the box, the lid is already lifting in frame one of the segment. No hands approaching.
- **Hands sell, faces cost.** Keep people to hands unless the brief is a founder piece.
- **Slow camera, fast cuts.** Plants don't move; the edit does. Eight segments in 15 seconds with slow pushes reads as premium; two long slow shots read as a screensaver.
- **The leaf is the product block.** Three varied leaf macros with per-shot distances and angles. Prefer angle shots to action shots: a hand misting the leaf is a high-difficulty shot; a macro from a new angle is cheap.
- **Keep the background alive but still.** Other plants at the far end of the shelf, out of focus, *never change*.
- **Two logo placements maximum** — box and endcard — and *the logo appears nowhere else, no other text in frame.* If the box isn't in the film, endcard only.
- **9:16 means vertical composition.** The plant fills height, not width. Hands enter from the bottom edge. The endcard sits in the centre band.
