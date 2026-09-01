# deck-builder

> **Original author: 花叔 · 花生 (alchaincyf)** — derived from
> [huashu-design](https://github.com/alchaincyf/huashu-design) at commit `a790f70`, MIT licensed,
> Copyright (c) 2026 alchaincyf. Split out and adapted for Claude Cowork by SuperTurbo.
> See NOTICE.md for the full provenance and LICENSE for the terms.

HTML slides at 1920x1080, presentable in a browser, exportable to PDF and to PowerPoint.

## What it does

Turns a brief or a document into a deck. Multi file with an overview wall is the default for
almost every deck: each slide is its own HTML file, assembled by `assets/deck_index.html`. Single
file is reserved for five slides or fewer.

The overview logic in `deck_index.html` is meant to be copied and configured, not rewritten. It
already solves three problems that are annoying to rediscover: tilt rendering, click hit areas,
and thumbnail cropping.

## Export

    scripts/export_deck_pdf.mjs         slides to PDF
    scripts/export_deck_stage_pdf.mjs   staged build variant
    scripts/export_deck_pptx.mjs        editable PowerPoint
    scripts/gen_deck_thumbs.mjs         overview wall thumbnails
    scripts/html2pptx.js                the HTML to PPTX shape mapper

**Honest note on PPTX fidelity.** PDF export is exact, because it is the browser printing what it
already rendered. PowerPoint export is a translation: HTML boxes and text become PowerPoint shapes
and text boxes. Simple layouts survive well and stay editable, which is usually the point of
asking for PPTX. Elaborate CSS does not always survive. If the deck must look exactly as designed,
deliver the PDF and offer the PPTX alongside it rather than instead of it.

## Runtime

Zero install. Rendering and PDF export use the container's Chromium. No npm install, no API keys,
no sibling skill required.

## Files

    SKILL.md                            the skill itself
    assets/deck_index.html              the overview wall, copy and edit its MANIFEST
    assets/deck_stage.js                staged build and presenter behaviour
    scripts/                            the five export and thumbnail scripts above
    references/slide-decks.md           structure, pacing, slide anatomy
    references/editable-pptx.md         what survives the PPTX translation and what does not
    references/verification.md          the render and measure gate
    references/typography.md            type scales at 1920x1080
    references/design-styles.md         the style catalogue
    references/brand-asset-protocol.md  handling real logos and brand colours
    references/content-guidelines.md    what earns a slide

## Adjusting it

    cd deck-builder && zip -r deck-builder.skill . -x '.*' -x 'deck-builder.skill'

Keep LICENSE and NOTICE.md in the archive. MIT requires the copyright notice to travel with
modified versions.
