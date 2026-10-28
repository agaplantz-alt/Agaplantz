# AgaPlantz theme files

Source of truth for the customisations applied to the AgaPlantz storefront.
Base theme: **Horizon 4.1.4**. Only the files below differ from stock; everything
else is untouched Horizon.

> Read `../CLAUDE.md` first — it covers the theme workflow (the live theme cannot be
> written to), the upload mechanism, and the Horizon gotchas that cost the most time.

| File | Purpose |
| --- | --- |
| `config/settings_data.json` | Global design tokens — palette, typography, buttons, cards |
| `templates/index.json` | Homepage section layout |
| `templates/list-collections.json` | Curated `/collections` page |
| `sections/footer-group.json` | Footer — shared by every page |

The homepage layout, design tokens and catalogue decisions are documented in
`../CLAUDE.md` rather than repeated here, so there is one place to keep current.

## Footer

`sections/footer-group.json` carries two AI-generated blocks. The second
(`ai_gen_block_651bd33`) had `show_social_links: true` with every social URL blank, so
it rendered a second bare "Follow us on" heading under the real one in
`ai_gen_block_fa8568c`. Set to `false`.

Both blocks hardcode colours rather than reading the palette, so they were retinted by
hand (`#f5f5f5`→`#F2EBDE`, `#ffffff`→`#FBF8F2`, `#000000`→`#2F2A22`,
`#dfdfdf`→`#DED3C2`).

Their `range` settings enforce step values — `icon_size`, `icon_spacing`,
`heading_spacing`, `padding_top`/`padding_bottom` are step-5 and `heading_size` is
step-2. Off-step values are rejected by `themeFilesUpsert` with
`FILE_VALIDATION_ERROR`.

## Hero

`templates/index.json` → `sections.hero_main` carries a `custom-liquid` block
(`hero_css`) holding a `<style>` tag. It exists because Horizon's type scale is a
single fixed rem value at every breakpoint, so there is no setting that can make the
heading smaller on a phone without also shrinking it on desktop. The CSS overrides the
inline `--font-size` custom properties below 749px only.

If you regenerate this template, keep that block and keep it first in `block_order`.

## Keep the app embeds

`config/settings_data.json` carries five app embed blocks — Inbox, Loox, Forms, Koala,
Google/YouTube. They must survive every write to that file or conversion tracking
breaks.
