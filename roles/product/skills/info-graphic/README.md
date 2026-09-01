# info-graphic

> **Original author: 花叔 · 花生 (alchaincyf)** — derived from
> [huashu-design](https://github.com/alchaincyf/huashu-design) at commit `a790f70`, MIT licensed,
> Copyright (c) 2026 alchaincyf. Split out and adapted for Claude Cowork by SuperTurbo.
> See NOTICE.md for the full provenance and LICENSE for the terms.

One page where the data is the subject and there is nothing to click. Not a deck, not a
prototype, not a dashboard.

## What it does

Builds a print quality infographic as a single self contained HTML page, then exports it to PNG,
PDF or SVG. Picks a visual style deliberately from a catalogue of named treatments rather than
defaulting to whatever comes out first, then verifies the render before handing it over.

## The rules it enforces

**Real data or no infographic.** If the user has not supplied numbers it asks for them. It will
not generate plausible looking sample data to fill a layout, because an infographic built on
invented numbers looks authoritative and is therefore worse than no infographic at all.

**One claim, not a summary.** Everything on the page defends a single sentence or gets cut.

**It looks at what it made.** Renders the page, measures contrast with proper alpha compositing
against every ancestor background, checks the smallest type size, checks for horizontal overflow,
and checks the claim still survives at thumbnail size. A run that fails the gate gets fixed and
re-measured, not shipped with a caveat.

## Runtime

Zero install. Uses the Chromium already present in the Cowork container for rendering and PDF
export, and Python with PIL for raster work. No npm install, no API keys, no sibling skill.

## Files

    SKILL.md                            the skill itself
    references/design-styles.md         the style catalogue it chooses from
    references/typography.md            type scales and pairing rules
    references/scene-templates.md       layout skeletons
    references/content-guidelines.md    what earns a place on the page
    references/verification.md          the render and measure gate

## Adjusting it

Edit SKILL.md and the reference files in place, then re-zip the folder so that SKILL.md sits at
the archive root:

    cd info-graphic && zip -r ../info-graphic.skill . -x '.*' && cd ..

Keep LICENSE and NOTICE.md in the archive. The MIT licence requires the copyright notice to travel
with the work, including in modified versions.
