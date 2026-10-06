# Catalogue backup

`products-full.jsonl` — a complete Shopify Admin API export of all 309 products,
taken immediately **before** any merge or deletion of duplicate listings.

Captured per product: id, handle, title, status, productType, vendor, tags,
descriptionHtml, SEO title/description, options with option-value ids, media
(image URLs + alt text) and every variant with id, title, SKU, price,
compareAtPrice, inventoryQuantity, inventoryPolicy and selectedOptions.

Format is Shopify bulk-operation JSONL: a line without `__parentId` is a product;
lines carrying `__parentId` are that product's media and variants.

## Why it exists

Duplicate listings are being merged into a single page per plant, and the losing
listing is deleted permanently at the store owner's instruction. Deletion in
Shopify is irreversible and takes the product URL with it, so this file is the
recovery record: every field needed to recreate a deleted listing is here.
Image binaries are not included — only their CDN URLs, which remain valid while
the files stay in Shopify Files.

## Restoring a deleted product

    python3 - <<'PY'
    import json
    h='philodendron-florida-ghost-pre-order'
    for l in open('catalog-backup/products-full.jsonl'):
        d=json.loads(l)
        if d.get('handle')==h: print(json.dumps(d,indent=2))
    PY

Then recreate with `productCreate` + `productVariantsBulkCreate`, and re-point the
URL redirect. Note the original product id will not be reused.
