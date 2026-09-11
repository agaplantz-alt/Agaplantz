# Acclimation Guarantee — rollout changelog

Draft theme **`149825486927`** ("AgaPlantz 2026 — acclimation guarantee"), duplicated from
MAIN `149711487055`. Preview: https://agaplantz.com/?preview_theme_id=149825486927

## The guarantee

Every plant, 30 days from the delivery scan. Under $200 a free replacement; $200 and over a
replacement at 50% of what the customer paid. Customer pays $14.99 replacement shipping, per
parcel not per plant. One replacement per plant; store credit if the variety has sold out.
Conditions: photos, and that they followed the Acclimation Guide. Claims to
`info@agaplantz.com`.

The 24-hour DOA claim is kept separate and unchanged — it can end in a full refund with no
shipping charge, which is better for the customer. The guarantee covers day two to day 30.

## What changed in the theme

| File | Change |
| --- | --- |
| `snippets/acclimation-guarantee-badge.liquid` | **new** — every word of guarantee copy lives here |
| `blocks/acclimation-guarantee.liquid` | **new** — product block, tier follows the selected variant |
| `templates/page.acclimation-guarantee.json` | **new** — the page, native blocks, editable in the theme editor |
| `templates/product.json`, `product.tissue-culture.json` | badge inserted under Add to Cart |
| `sections/header-group.json` | guarantee announcement slide, first in the rotation |
| `snippets/cart-summary.liquid` | one line above checkout — covers cart page *and* drawer |
| `sections/footer-group.json` | sixth policy link → guarantee; contact email → `info@` |
| `blocks/ai_gen_block_651bd33.liquid` | footer block gained a `policy_link_6` slot |
| `templates/page.faq.json` | answers 4 and 5 rewritten to point at the guarantee |
| `blocks/ai_gen_block_7be2211.liquid` | guide: callout at the top, closing Q at the bottom |
| `templates/page.contact.json` | contact email → `info@` |

## Applied to the live store already (not theme)

- Page `/pages/acclimation-guarantee` created, published, with a plain-HTML body as a
  fallback for any theme that lacks the template.
- Main menu: "Acclimation Guarantee" added after "Acclimation Guide".
- Payment Policy page body: email → `info@agaplantz.com`.
- Contact page SEO description: was literally `Sandhuagam16@gmail.com`, now real copy.

## Verified

- **Tier flips with the variant.** Devil Monster pre-order, the only in-stock listing whose
  variants straddle $200: `?variant=45989665603663` ($150) reads "Free replacement within 30
  days"; `?variant=45988645666895` ($204) reads "Replacement at 50% of what you paid".
- **Exactly one badge per product page** — it does not leak onto the recommendation cards
  below, which is the bug the `Save X%` badge hit on its first attempt.
- Cart page and cart drawer each render the line once.
- Zero `Liquid error` on every page fetched.
- Sitewide sweep, 17 pages: `agaplantz@gmail.com` **0**, `Sandhuagam16@gmail.com` **0**.
- Every uploaded file's `checksumMd5` matches the local copy. Both hand-edited Liquid files
  were verified by reverse-applying the edits and matching the original md5 byte for byte.

## Still needs you

1. **Paste three policies** — `docs/policy-paste/`, into Settings → Policies. I cannot write
   them: the app lacks the `write_legal_policies` scope. Until then the guarantee is
   advertised on every product page and contradicted by the refund policy behind it. These
   were rebuilt from the current live text, so pasting will not undo your email change. The
   refund one also fixes a pre-existing error: it said "Free shipping on orders over $120"
   where everything else says $180.
2. **Publish theme `149825486927`.**
3. **`shop.contactEmail` is still `Agaplantz@gmail.com`** — Settings → Store details. That is
   the *sender* on every order confirmation, so until it changes the whole site says info@
   but your emails still come from the Gmail.

## Flagged, not changed

- **Order confirmation / shipping notification emails** carry no guarantee mention. Suggested
  line, for Settings → Notifications: *"Your plant is covered by our Acclimation Guarantee for
  30 days from delivery — see agaplantz.com/pages/acclimation-guarantee."* Transactional email
  should not change without you seeing it, so I left it.
- **Product descriptions** — untouched, as you asked.
- **The Acclimation Service add-on ($12+, sold on tissue-culture pages) is an unresolved
  edge case.** If a customer pays *you* to acclimate the plant, the guarantee's condition
  "you followed the Acclimation Guide" does not really apply — you did the acclimating. Worth
  deciding: does a serviced plant get the guarantee automatically? I would say yes, and it is
  a strong selling point for the add-on, but it is your call and it is not written anywhere.
- **Pre Order page** — checked, clean. Its only refund language is about supplier availability.

## Internal note — how to handle a claim

A customer emails `info@agaplantz.com` within 30 days of their delivery date with an order
number and photos. Check three things: the delivery scan is inside 30 days, the photos show
the actual plant, and nothing in them says clear neglect — sitting in water, scorched in
direct sun, or no humidity setup at all. If it passes, look up what they paid for that plant:
under $200 the replacement is free and you invoice $14.99 shipping; $200 and over you invoice
50% of the line price they paid plus the $14.99. One replacement per plant, same variety where
possible, store credit for the plant price if it has sold out. Shipping is one $14.99 per
parcel, so if two plants are being replaced together it stays $14.99. If the plant arrived
dead or badly damaged and they contacted us within 24 hours, that is a DOA claim instead —
better for them, since it can be a full refund with no shipping charge. Aim to reply in 24–48
hours, and send replacements with the next batch going out.
