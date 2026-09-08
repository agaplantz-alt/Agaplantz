# Stage 0 — plant ad formats, angles and truth rules

Read this before starting any ad. It answers the questions the video model can't: where the ad runs, how long it is, what it's allowed to claim.

## Platform specs

| Placement | Aspect | Pixels | Length | Notes |
|---|---|---|---|---|
| Meta Reels / Stories, TikTok in-feed | 9:16 | 1080 × 1920 | 6–15s (15s default) | Sound-off first. Hook must land visually by 2.0s. |
| Meta feed (FB/IG) | 1:1 or 4:5 | 1080 × 1080 / 1080 × 1350 | 6–15s | Cropped from the 9:16 master when the framing allows; otherwise its own prompt |
| Site header, YouTube pre-roll, brand film | 16:9 | 1920 × 1080 | 15–30s | The only place a 30-second piece earns its length |

Generate the 9:16 master first. Most video models take an aspect ratio parameter; state it in FORMAT MODE and again in the style tail.

## Safe zones for 9:16

Platform UI covers the frame edges. Anything that matters — the plant, the overlay text, the logo — lives inside the centre band:

```
SAFE ZONE LOCK
Top 14% of frame and bottom 20% of frame are reserved for platform UI and overlay
text: nothing essential is composed there. The hero plant, hands and any logo sit in
the central 66% of frame height and the central 80% of frame width.
```

## Ad structures by length

**6-second bumper** (feed, retargeting): HOOK → PRODUCT → CTA. One shot, one move, one cut to endcard. No transformation, no story.

**15-second Reel** (default, cold and warm traffic): four beats, eight segments.

| Beat | Time | What happens | Overlay |
|---|---|---|---|
| Hook | 0.0–2.0 | Something that stops the thumb: macro of the leaf trait, or the box opening | The hook line |
| Desire | 2.0–7.0 | The plant, honestly, in a real Canadian room; hands interact | (none) |
| Proof / offer | 7.0–12.0 | What you actually get — plantlet, vessel, or rooted plant — plus the one true claim | The claim |
| CTA | 12.0–15.0 | Hero hold, logo endcard | CTA + price if accurate |

**30-second film** (site, YouTube): the long-form architecture in `example-pizza-30s.md` — hidden transformation, edit acceleration, a product block of five or six varied shots.

## Hooks that work for plant buyers

Borrowed from the store's marketing playbook. Use only the ones that are true for this plant and this offer.

- "POV: you finally found the plant."
- "Your collection is missing this one."
- "Rare doesn't have to mean impossible to afford."
- "Just landed at AgaPlantz."
- "Lab-grown. Pest-free. Canadian."
- "Can you name this plant?"
- "The plant everyone asks us about."
- "Want a rare plant without the rare-plant stress?"

Hooks are overlays, not model text. The model provides the picture the hook sits on.

## Angles

Pick one per ad. Two angles in one 15-second ad is a muddle.

| Angle | Buyer's feeling | What the picture shows | When it's true |
|---|---|---|---|
| Rarity | "I've been looking for this" | Macro on the defining trait; the plant alone | Genuinely uncommon variety |
| Collector | "My shelf needs it" | Plant joining a shelf of others | Always |
| Value | "Rare at that price?" | Plant + honest plantlet + price overlay | Pre-order price is genuinely lower than market |
| New arrival | "First to get it" | Box opening, vessel lifted out | New batch or new listing |
| Beginner | "I could keep this alive" | Hands, dome, calm room, no drama | Plant is genuinely forgiving (not most variegated Alocasias) |
| Discovery | "What is that?" | Leaf so close it's abstract, then the reveal | Striking trait: metallic, velvet, neon |

## What a pre-order ad must show

A pre-order customer receives a tissue-culture plantlet: small, pale, often in or just out of a sealed vessel with gel. The acclimated plant on the shelf is what it becomes with care. An ad that shows only the shelf plant sells something the box doesn't contain.

Rule: any pre-order ad includes at least one segment with the plantlet honestly in frame, and the overlay on that segment says what it is ("tissue-culture plantlet — what arrives in your box"). The ad can and should also show the acclimated plant; the two are linked by the LEAF LOCK so they read as the same variety.

## Truth rules

From the shipping, refund and pre-order policies and the support inbox. They override the brief, the angle and any hook.

- **Variegation is not guaranteed** to persist or develop. Any overlay showing a variegated plant carries "representative plant — variegation varies" or the ad avoids the claim entirely.
- **Never show or state a delivery date.** "Ships after the batch closes" is fine. A date on screen is not, even the current cut-off — ads outlive it.
- **Never invent scarcity.** Quantity claims come from Shopify inventory at the moment the ad is made, and are worded so they age ("limited batch", not "3 left").
- **Canada only.** No US flags, no "worldwide shipping", no USD.
- **No survival, growth-rate or "easy care" claims** for plants the store's own listings don't describe that way.
- **No care how-to** in the ad. A watering shot is fine as texture; "water once a week" as an overlay is a promise.
- **Price on screen only if it's the live price** for the exact variant shown (pre-order vs ready-to-ship vs acclimated differ), in CAD, and it's the price the click lands on.
- **Free shipping** threshold appears only as "free shipping over $180" and only if it's still the live threshold.
- **No pesticide, fungicide or dosage** language, ever.

When a hook Agam asked for breaks one of these, say which rule, offer the nearest true version, and build that.

## Handing off to the editor

The model produces picture and SFX. The editor adds overlays, music, captions and the endcard link. Deliver alongside the prompt a five-line overlay sheet so the edit doesn't have to reverse-engineer the intent:

```
OVERLAYS (editor)
0.0–2.0   hook line, centre band, one line
7.0–12.0  "tissue-culture plantlet — what arrives in your box" (pre-order only)
12.0–15.0 CTA + price if live; logo endcard from file
Music     none / bed at −18 LUFS under SFX
Captions  burn-in if any voice; otherwise none
```
