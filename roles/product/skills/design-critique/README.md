# design-critique

> **Original author: 花叔 · 花生 (alchaincyf)** — derived from
> [huashu-design](https://github.com/alchaincyf/huashu-design) at commit `a790f70`, MIT licensed,
> Copyright (c) 2026 alchaincyf. Split out and adapted for Claude Cowork by SuperTurbo.
> See NOTICE.md for the full provenance and LICENSE for the terms.

Reviews work that already exists. Critiques the design, never the designer.

## What it does

Takes a URL, screenshot, HTML file, PDF, deck or prototype, renders it, measures it, and returns a
score with a prioritised fix list. It does not produce designs. If the user wants something made,
it says so and stops.

## Why it is the odd one out

It is the smallest of the seven skills and the only one that carries no production kernel. A
reviewer that also knows how to generate three directions will start generating instead of
reviewing, so the generation machinery is deliberately absent. That is also why it is the only one
that is genuinely independent: it reviews work rather than producing it, so it needs nothing handed
to it and hands nothing on.

## What it actually measures

It renders the target rather than judging from a description, then takes real measurements:
contrast ratios computed with alpha compositing against every ancestor background, type sizes,
overflow at the viewport widths that matter, and tap target sizes. A screenshot that looks clipped
gets checked against `scrollWidth` before it is called a bug, because the render is not the site.

Findings are separated into measured failures and matters of taste, and the two are never mixed.

## Runtime

Zero install. Uses the container's Chromium for rendering and measurement. No npm install, no API
keys, no sibling skill required.

## Files

    SKILL.md                            the skill itself
    references/critique-guide.md        the scoring dimensions and the fix ranking
    references/content-guidelines.md    the standard the work is held to

## Adjusting it

Edit SKILL.md and the reference files in place, then re-zip the folder so that SKILL.md sits at
the archive root:

    cd design-critique && zip -r ../design-critique.skill . -x '.*' && cd ..

Keep LICENSE and NOTICE.md in the archive. The MIT licence requires the copyright notice to travel
with the work, including in modified versions.
