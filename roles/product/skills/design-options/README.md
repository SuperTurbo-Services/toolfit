# design-options

> **Original author: 花叔 · 花生 (alchaincyf)** — derived from
> [huashu-design](https://github.com/alchaincyf/huashu-design) at commit `a790f70`, MIT licensed,
> Copyright (c) 2026 alchaincyf. Split out and adapted for Claude Cowork by SuperTurbo.
> See NOTICE.md for the full provenance and LICENSE for the terms.

Variations inside a direction that is already settled. The big fork was chosen elsewhere.

## What it does

Explores the space around an agreed look, in one of two modes, and picking the right one matters:

**Side by side canvas** when the variations differ structurally: layout, hierarchy, section order,
component pattern. Differences you cannot express as a slider. Each variation is rendered as a
complete artifact and laid out on one pan and zoom canvas, labelled with what changed.

**Live Tweaks** when the variations are parametric: palette, type scale, spacing rhythm, density,
corner radius, accent colour. One artifact with a control panel, so the user explores the space
themselves without a regeneration round trip.

## Its precondition

It checks for `direction-approved.md`. If no direction has been chosen it hands off to
`direction-advisor` and says why, rather than inventing a direction and then generating variations
of a guess.

That handoff is through a file on disk, not a skill call, so `direction-advisor` does not need to
be installed for this one to work. It just will not have a direction to work from.

## Runtime

Zero install. React with Babel inline in a single HTML file, rendered by the container's Chromium.
No npm install, no API keys, no sibling skill required.

## Files

    SKILL.md                            the skill itself
    assets/design_canvas.jsx            the pan and zoom canvas for side by side mode
    references/tweaks-system.md         the Live Tweaks control panel pattern
    references/react-setup.md           the three rules that break the build if ignored
    references/design-styles.md         the style catalogue
    references/content-guidelines.md    what earns a place

## Adjusting it

Edit the source, then re-zip with SKILL.md at the archive root:

    cd design-options && zip -r design-options.skill . -x '.*' -x 'design-options.skill'

Keep LICENSE and NOTICE.md in the archive. MIT requires the copyright notice to travel with
modified versions.
