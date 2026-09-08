#!/usr/bin/env python3
"""Build a Shopify listing spec for an AgaPlantz product.

Applies the store's conventions (handle, product type, tags, variants,
SKUs, suggested ready-to-ship price, SEO fields) deterministically and
prints them as JSON. The description is written separately — see
references/description-guide.md.

Usage:
    python build_listing.py "Philodendron Gloriosum Variegated" --preorder 84 \
        --moq 10 --sku 100187 --variegated

    python build_listing.py "Alocasia Tiny Dancers" --preorder 28 --moq 100 \
        --sku 100752 --pack 5 --min-order 5

Pack listings (--pack N) get the pack-style pre-order variant title, no
Ready-to-Ship variant, the packN / min-order-N tags, and the bold pack
paragraph for the description.

Anything not supplied is emitted as "[TO CONFIRM]" rather than guessed —
SKU numbers and acclimated prices are Agam's to set.
"""

import argparse
import json
import math
import re
import sys
import unicodedata

# --- slug -------------------------------------------------------------------
# Same behaviour as the `slugify` library in agaplantz-alt/slugify: lowercase,
# accents folded to ASCII, runs of non-alphanumerics collapse to one separator.

_NON_WORD = re.compile(r"[^a-z0-9]+")


def slugify(text, separator="-"):
    normalized = unicodedata.normalize("NFKD", text)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    collapsed = _NON_WORD.sub(separator, ascii_only.lower())
    return collapsed.strip(separator)


# --- conventions -------------------------------------------------------------

VENDOR = "AgaPlantz"
HANDLE_SUFFIX = "-pre-order"
TO_CONFIRM = "[TO CONFIRM]"

VARIEGATED_CLOSER = (
    "<p><strong>Leaf coloration and variegation may naturally vary depending "
    "on lighting, maturity, and growing conditions.</strong></p>"
)
PLAIN_CLOSER = (
    "<p><strong>Each plant is unique — size, shape, and leaf count vary "
    "naturally. Photos are representative of the variety, not the exact plant "
    "shipped.</strong></p>"
)

# Words that mean the plant has colour/variegation to disclaim, if --variegated
# wasn't passed explicitly.
_VARIEGATION_HINTS = (
    "variegat", "albo", "aurea", "mint", "pink", "marble", "electro",
    "white", "gold", "golden", "yellow", "caramel", "sport",
)


def looks_variegated(title):
    t = title.lower()
    return any(h in t for h in _VARIEGATION_HINTS)


def suggest_rts(preorder):
    """Ready-to-ship ≈ pre-order × 1.10, rounded up to the dollar.

    Reproduces most of the catalogue (54→60, 42→48, 174→192, 30→33, 108→120,
    60→66); a couple of listings sit a few dollars higher, so this is a
    suggestion for Agam to confirm, not a rule.
    """
    return math.ceil(preorder * 1.10)


def money(value):
    return f"{value:.2f}"


PACK_TITLE = {5: "Tissue Culture (Pre-Order) - Pack of 5", 30: "Tissue Culture (Pre-Order) - 30 Plant Pack"}
_NUM_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 10: "ten", 12: "twelve", 20: "twenty", 30: "thirty", 50: "fifty"}


def pack_variant_title(n):
    return PACK_TITLE.get(n, f"Tissue Culture (Pre-Order) - Pack of {n}")


def pack_paragraph(n):
    word = _NUM_WORDS.get(n, str(n))
    return (f"<p><strong>Ships as a set of {word} tissue-culture plantlets.</strong> "
            "This variety is grown and shipped in sealed multiples rather than as single plants, "
            f"so the pack is priced well below {word} singles.</p>")


def build(title, preorder, moq=None, sku=None, rts=None, acclimated=None,
          pack=None, variegated=None, genus=None, min_order=None):
    title = " ".join(title.split())
    genus = (genus or title.split()[0]).strip().capitalize()
    if variegated is None:
        variegated = looks_variegated(title)

    sku_base = f"PH-{int(sku):06d}" if sku is not None else TO_CONFIRM
    sku_ac = f"{sku_base}-AC" if sku is not None else TO_CONFIRM

    rts_price = rts if rts is not None else suggest_rts(preorder)

    tags = [
        genus,
        title,
        "collector plant",
        f"moq{int(moq)}" if moq is not None else None,
        "Pre-Order",
        f"Rare {genus}",
        "rare houseplants Canada",
        "Tissue culture",
    ]
    if pack:
        tags.append(f"pack{int(pack)}")
    if min_order:
        tags.append(f"min-order-{int(min_order)}")
    tags = [t for t in tags if t]

    seo_title = f"{title} | Tissue Culture | AgaPlantz"
    if len(seo_title) > 60:
        seo_title = f"{title} | AgaPlantz"

    spec = {
        "title": title,
        "handle": slugify(title) + HANDLE_SUFFIX,
        "productType": genus.upper(),
        "vendor": VENDOR,
        "status": "DRAFT",
        "tags": sorted(tags, key=str.lower),
        "format": "pack" if pack else "single",
        "variants": [
            {
                "title": pack_variant_title(int(pack)) if pack else "Tissue Culture (Pre-Order)",
                "sku": sku_base,
                "price": money(preorder),
                "priceNote": f"per pack of {int(pack)}" if pack else "per plant",
                "inventoryItem": {"tracked": True},
            },
            {
                "title": "Acclimated Plant",
                "sku": sku_ac,
                "price": money(acclimated) if acclimated is not None else TO_CONFIRM,
                "inventoryItem": {"tracked": True},
            },
        ] + ([] if pack else [
            {
                "title": "Tissue Culture (Ready to Ship)",
                "sku": None,
                "price": money(rts_price),
                "priceNote": "confirmed" if rts is not None else "suggested: pre-order × 1.10, confirm with Agam",
                "inventoryItem": {"tracked": True},
            },
        ]),
        "packParagraph": pack_paragraph(int(pack)) if pack else None,
        "descriptionCloser": VARIEGATED_CLOSER if variegated else PLAIN_CLOSER,
        "variegated": variegated,
        "seo": {
            "title": seo_title,
            "metaDescription": TO_CONFIRM + " (write ≤155 chars, plant name first; see description-guide.md)",
        },
        "openItems": [],
    }

    open_items = []
    if moq is None:
        open_items.append("MOQ (sets the moqN tag) — tag omitted until known")
    if sku is None:
        open_items.append("SKU catalogue number (PH-1xxxxx)")
    if acclimated is None:
        open_items.append("Acclimated Plant price")
    if rts is None and not pack:
        open_items.append("Ready to Ship price (suggested value needs confirmation)")
    open_items.append("Image URLs (public HTTPS)")
    open_items.append("Description body (write per description-guide.md)")
    spec["openItems"] = open_items
    return spec


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("title", help="Product title, e.g. 'Alocasia Melo Albo Variegated'")
    p.add_argument("--preorder", type=float, required=True, help="Tissue Culture (Pre-Order) price in CAD")
    p.add_argument("--moq", type=int, help="Lab minimum order quantity → moqN tag")
    p.add_argument("--sku", type=int, help="Six-digit catalogue number after PH-, e.g. 100187")
    p.add_argument("--rts", type=float, help="Ready to Ship price (otherwise suggested at ×1.10)")
    p.add_argument("--acclimated", type=float, help="Acclimated Plant price (no formula; Agam sets it)")
    p.add_argument("--pack", type=int, help="Multi-pack size → pack-style variant title, packN tag, no Ready-to-Ship variant")
    p.add_argument("--min-order", type=int, help="Minimum line quantity at checkout → min-order-N tag")
    p.add_argument("--genus", help="Override genus (default: first word of title)")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--variegated", dest="variegated", action="store_true", default=None)
    g.add_argument("--not-variegated", dest="variegated", action="store_false")
    args = p.parse_args(argv)

    spec = build(args.title, args.preorder, moq=args.moq, sku=args.sku, rts=args.rts,
                 acclimated=args.acclimated, pack=args.pack, variegated=args.variegated,
                 genus=args.genus, min_order=args.min_order)
    json.dump(spec, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
