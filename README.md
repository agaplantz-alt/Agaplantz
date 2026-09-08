# Agaplantz
Na

## Claude Ads

This repo enables the [Claude Ads](https://github.com/AgriciDaniel/claude-ads)
Claude Code plugin via `.claude/settings.json`. See
[docs/claude-ads-setup.md](docs/claude-ads-setup.md) for install, verification,
and removal steps.

## Product listing skill

`.claude/skills/agaplantz-product-listing/` teaches Claude Code how to build
and update agaplantz.com product listings in the store's existing shape
(three-variant single-plant listings and two-variant pack listings, SKU and
tag schemes, description voice and disclaimers). It drafts the full listing
for review and only creates or updates the Shopify product as a DRAFT after
explicit confirmation. It loads automatically when this repo is open in
Claude Code; the Shopify connector must be connected for the store checks.
