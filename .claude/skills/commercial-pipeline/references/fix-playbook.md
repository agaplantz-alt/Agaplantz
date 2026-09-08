# Stage 3 — fix playbook

When Agam reports a problem: name the failure, apply the fix, rewrite **only** the affected sections, and say what to re-batch. Never re-roll an unchanged prompt.

## The master rule

**If something keeps breaking between cuts, stop describing it better inside every shot. Give it its own lock.**

Position, orientation, facing, leaf count, variegation, which hands — anything that must survive multiple cuts gets promoted out of the segment descriptions into a hard rule of its own, stated in absolutes:

```
THE PLANT HAS EXACTLY FIVE LEAVES. THE POT NEVER MOVES OR TURNS.
```

Adding more careful description inside each of eight segments does not work. This is the single highest-value lesson in the workflow.

## Failure catalogue — plants

| Symptom | Cause | Fix |
|---|---|---|
| Leaf count changes between cuts | No LEAF LOCK, or count not restated per segment | LEAF LOCK with the count in absolutes, explicit negation (*no leaf appears, unfurls, grows, drops*), restated in every segment |
| Variegation wanders — mint on a different leaf, more white, pattern spreads | Leaf map written as adjectives | Rewrite the LEAF MAP in physical terms: which leaf, which half, which colour, and *the same leaves carry the same sectors in every shot* |
| Variegation turns white/pink/yellow | Model's prior for "variegated" | Name the colours that are **not** present: *no white, no pink, no yellow, no cream* |
| The plant "grows" — bigger, more leaves, a new leaf unfurling | Model treats a plant as a time-lapse subject | LEAF LOCK negation plus a PHYSICS line: *the plant does not grow, unfurl or move on its own in real time* |
| A second plant appears on the shelf | Never stated that only one exists | Definition clause: *there is only ever ONE of the plant in the film*; background plants described as *never changing* |
| Leaves flutter, wave, or breathe | No wind rule | PHYSICS: *leaves sway once when the pot is set down and settle within a second; no wind, no flutter* |
| Water drops appear, or run down leaves | Reference or prompt had "dewy", "fresh", "misted" | Remove every moisture word; state *dry leaves, no droplets*. If a mist shot is scripted, it's one segment and the drops don't carry to the next |
| Pot changes colour, shape, or material | Pot not locked | POT line inside the GEOMETRY LOCK: one colour, one shape, restated |
| Pot rotates to show a better leaf | Model improving composition | *THE POT NEVER TURNS. Do not rotate it to favour a leaf. Do not re-centre it* |
| Pot teleports from box to shelf | Legit move never shown | Second anchor plus a visible on-screen transit (the lift) |
| Plantlet looks like a mature plant, or a salad | No honest scale, or a vague leaf paragraph | Real size on the plantlet's reference line (*fits inside a closed hand*), same LEAF MAP language, *thin pale roots, trace of clear gel* |
| Plantlet and plant don't read as the same variety | Leaf paragraphs written separately | Copy the LEAF LOCK verbatim between both assets and both reference lines, adjusting only count and size |
| Dome swap looks like a morph | Model asked to transform | Hide it: plantlet before the dome, plant after, never both in frame. Tell the change with light. *No glow effects, no magic* |
| Condensation runs as drops or fogs the whole dome | No dome physics | DOME LOCK: *even soft haze on the inside, never running drops* |
| Soil spills, or the soil surface changes | Not locked | *Soil surface flat and undisturbed; nothing leaves the pot* |
| Hands have the wrong number of fingers, or a second pair appears | No HANDS LOCK | HANDS LOCK: two hands, five fingers, one anchor (ring), *the only hands in the film* |
| Hands grab the leaves | Action written as intent | Direct it: *by the rim, thumb outside, never touching a leaf* |
| A face or torso enters frame | Prompt said "person" | *No face, no forearm above the elbow* in HANDS LOCK and POSITIVE LOCKS |
| Text appears on the pot, vessel or box | No TEXT RULE | TEXT RULE: *the model renders no text of any kind*; logo only from the file at the scripted time |
| Logo comes out mangled | Redrawn too often or generated | Never generate it. Two placements maximum, both named, *appears nowhere else* |
| Hero is cut off by platform UI | No safe zone | SAFE ZONE LOCK; recompose the hero into the central 66% of height |
| Ad reads as a screensaver | Two long slow shots | Eight segments in 15s, slow camera, fast cuts, LEAF VARIETY LOCK |
| Leaf macros all look the same | No variety rule | LEAF VARIETY LOCK plus a distinct distance and angle in each lens lock |
| Nothing feels like it changes | One light state | Two named states, defined by sources, transition bound to a frame (the dome lift) |
| Looks like a render / CGI plant | Flat perfect leaves, dead background | Real wear: *one leaf with a small dry edge, faint dust on the pot rim*; background plants alive but *never changing* |
| Background plants change between cuts | Not locked | One line in LOCATION MAP: *background plants stay green, out of focus, and never change* |
| Shows a delivery date, a price, or "3 left" in the picture | Overlay content leaked into the prompt | Strip it from the prompt; it belongs to the editor's overlay sheet and must pass the truth rules |
| Version got worse after improvements | Complexity budget spent | Revert to the last clean version and ship it |

## Failure catalogue — general

Kept from the original workflow; still true for any film.

| Symptom | Cause | Fix |
|---|---|---|
| Object drifts or rotates between cuts | No dedicated rule; re-described per shot | Its own GEOMETRY LOCK in caps, with explicit negation of every drift mode |
| Object still drifts after a geometry lock | Lock anchored to screen coordinates | Re-anchor to a world landmark — a shelf end, a window mullion, a distance from another object |
| Object re-centres itself shot to shot | Model correcting composition | *Do not re-centre it, do not re-frame around it, do not correct its position to match a previous shot* |
| Transformation looks fake | Model asked to morph | Hide it: A before the cover, B after, never both in frame, tell it with light |
| Product shot looks cheap | Camera below the product | Camera slightly **above** looking down; *never shot from below* |
| Lighting states written but ignored | Written as prose decoration | Tag every segment with its state like a lens lock; bind transitions to a frame |
| Middle drags | Time spent on setup | Start segments on the action; delete the run-up rather than shortening it |
| No tension (30s films) | Edit and subject at the same rate | EDIT ACCELERATION LOCK with named exceptions |
| Reference line contradicts its own image | Written from the plan | Rewrite every reference line to describe what actually generated |

## How the iteration actually goes

**v1 — baseline.** Describe the whole ad in plain English, nothing clever. The concept usually works immediately; three or four specific things break — for plants, nearly always leaf count and variegation. Diagnose them as named problems.

**v2 — targeted fixes.** Apply the catalogue fixes for each named problem. Reliably much better and reliably still has the continuity problem, because v2 fixes are usually applied inside the segments.

**v3 — promote to locks.** The thing that kept breaking gets its own rule. LEAF LOCK written in physical terms. Setup deleted. Leaf block expanded to three varied shots. This is normally the winner.

**v4 and v5 — the trap.** More hands, a face, a misting shot, a second plant for "collection" feel. Individually every change is an improvement. Together they make the output worse.

> **Every prompt has a complexity budget.** Once a prompt is generating clean results, one more brilliant idea often just gives the model one more thing to get wrong. Know when to stop and ship.

## Batching

Several generations per version, never one. Generate four, compare side by side on the judging criteria you named, keep what works. For a 15-second plant Reel expect six to eight generations, of which two or three are actual prompt changes. If only one in four is clean, that is normal. Keep it and stop.

## When renumbering segments

Deleting or adding a segment shifts every ID after it. Lens locks, light state ranges, LEAF LOCK restatements, anchors and cross-references all name segments by ID, so they all have to be rewritten together. Say so when delivering — the overlay sheet references timings and needs to re-sync too.
