# motion-design

> **Original author: 花叔 · 花生 (alchaincyf)** — derived from
> [huashu-design](https://github.com/alchaincyf/huashu-design) at commit `a790f70`, MIT licensed,
> Copyright (c) 2026 alchaincyf. Split out and adapted for Claude Cowork by SuperTurbo.
> See NOTICE.md for the full provenance and LICENSE for the terms.

Timeline driven animation authored as HTML, rendered to video with sound.

## What it does

Storyboard first, then code, then render to MP4 or GIF. The default deliverable is an MP4 **with
audio**, because a silent render reads as cheap: the viewer subconsciously registers movement with
no sonic response. It skips audio only when told to.

Every shot begins as a still frame that happens to move. Films of 20 seconds or more get a
director's notes file before any code is written.

## The audio position

Sound effects and music are separate jobs on separate frequency bands, and doing only music is
about a third of the work. SFX carry the high frequencies and mark events; music carries the low
frequencies and sets the register. `references/audio-design-rules.md` has the ffmpeg templates and
the loudness targets.

## What is bundled and what is not

**Bundled: all 37 sound effects** (478,089 B), across container, feedback, impact, keyboard, magic,
progress, terminal and UI categories. `references/sfx-library.md` is the index.

**Not bundled: the six background music tracks.** This is the one deliberate omission in the whole
set, and it is the reason this package is 603,720 B instead of tens of megabytes. Upstream's BGM
files are 26.6 MB of a 33 MB uncompressed project, which is 80.6% of its weight, and they are
assets rather than method. The mixing recipe, the loudness targets and the frequency separation
rules all ship intact.

So `add-music.sh --mood=tech` will not find a track. It fails with an explanatory message rather
than a bare error, and there are two ways forward:

    bash scripts/add-music.sh in.mp4 --music=/path/to/your-track.mp3

or restore the presets by downloading `bgm-<mood>.mp3` from
`https://github.com/alchaincyf/huashu-design/tree/main/assets` into `assets/`.

**A caveat I am not going to paper over:** the 37 SFX ship under the repository's MIT licence, and
upstream describes them as generated in house (30 batch generated plus 7 retained from an earlier
pass, per `references/sfx-library.md`). I have not independently verified the provenance of the 7
retained files. For internal work this is fine. Before these go into a client deliverable or a
public launch film, confirm that upstream holds the rights to those seven.

## Runtime

Zero install. ffmpeg 6.1.1 and Chromium are both already in the Cowork container, which is what
makes headless rendering and mixing possible without a toolchain. No npm install, no API keys, no
sibling skill required.

## Files

    SKILL.md                             the skill itself
    assets/animations.jsx                easing and timeline primitives
    assets/cursor.jsx                    synthetic cursor for UI demos
    assets/sfx/                          37 mp3 sound effects in 8 categories
    scripts/render-video.js              headless frame capture
    scripts/render-video-seek.js         deterministic seek based capture
    scripts/add-music.sh                 BGM mixing, patched for the missing presets
    scripts/convert-formats.sh           MP4 and GIF conversion
    scripts/verify-video.sh              hard checks on the output file
    references/storyboard-basics.md      the shot card format
    references/animation-best-practices.md  pacing, easing, the four recipes
    references/animation-pitfalls.md     the ways this goes wrong
    references/camera-language.md        move vocabulary
    references/cinematic-patterns.md     shot patterns including dual track audio
    references/audio-design-rules.md     SFX and BGM mixing, ffmpeg templates
    references/sfx-library.md            the sound effect index
    references/gsap-recipes.md           timeline structures
    references/video-export.md           the export pipeline
    references/ui-demo-animation.md      animating real interfaces
    references/animations.md             the full technical flow
    references/content-guidelines.md     what earns a shot

## Adjusting it

    cd motion-design && zip -r motion-design.skill . -x '.*' -x 'motion-design.skill'

Keep LICENSE and NOTICE.md in the archive. MIT requires the copyright notice to travel with
modified versions.
