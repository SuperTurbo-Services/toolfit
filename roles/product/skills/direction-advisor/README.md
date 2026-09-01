# direction-advisor

> **Original author: 花叔 · 花生 (alchaincyf)** — derived from
> [huashu-design](https://github.com/alchaincyf/huashu-design) at commit `a790f70`, MIT licensed,
> Copyright (c) 2026 alchaincyf. Split out and adapted for Claude Cowork by SuperTurbo.
> See NOTICE.md for the full provenance and LICENSE for the terms.

Three real drafts, then stop and let the user choose. That is the whole job.

## What it does

Runs at the start of design work, before anything gets built. Renders three genuinely different
draft treatments of the same brief, presents them, and records the decision to
`direction-approved.md`. Production skills read that file and execute the chosen direction.

It does not produce the finished design. It produces the choice.

## The rule that makes it work

**Never ask the user to pick between text descriptions.** "Would you like minimal, bold, or
editorial?" is an invalid question, because they have nothing to look at. It renders three things.

This holds even when the brief seems clear. A supplied style word narrows the interpretive space
but does not transfer the right to choose: "Apple style" legitimately means a deep dark treatment,
a large white serif treatment, or a product colour immersion, and which one is the user's call.

The three drafts must be genuinely different, not three tints of one idea. Each one passes the
same readability gate the finished work would have to pass, so the choice is between three real
options rather than between one good draft and two strawmen.

## The handoff

Writes `direction-approved.md` to disk. Any production skill picks it up from there, so no skill
depends on any other skill being installed.

## Runtime

Zero install. Renders drafts with the container's Chromium. No npm install, no API keys, no
sibling skill required.

## Files

    SKILL.md                            the skill itself
    references/design-styles.md         the style catalogue the three drafts are drawn from
    references/design-context.md        reading the brief before drafting
    references/workflow.md              the gate sequence and the approval file format
    references/content-guidelines.md    what goes in a draft

## Adjusting it

Edit SKILL.md and the reference files in place, then re-zip the folder so that SKILL.md sits at
the archive root:

    cd direction-advisor && zip -r ../direction-advisor.skill . -x '.*' && cd ..

Keep LICENSE and NOTICE.md in the archive. The MIT licence requires the copyright notice to travel
with the work, including in modified versions.
