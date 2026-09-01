---
name: motion-design
description: "Build a timeline driven animation as HTML and export it to MP4 or GIF with sound effects and background music. Use when someone wants an animation, a motion graphic, a product launch video, an explainer video, an animated demo, a promo film, or asks to turn a concept into a video or export an animation to MP4 or GIF. Not for CSS micro interactions inside an existing page."
---

# Motion Design

Timeline driven animation authored as HTML, rendered to video. Not scattered CSS transitions on a
web page, which is a different job.

**The default deliverable is an MP4 with audio.** A silent render is a half finished product,
because the viewer subconsciously registers movement with no sonic response and reads it as cheap.
Skip audio only if the user says "no audio", "picture only", or "I will dub it myself".

## Storyboard before code, always

Every shot begins as a still frame that happens to move. Before writing anything, produce the
lightweight storyboard cards in `references/storyboard-basics.md`: one card per shot, with the
camera column and the acceptance frame number.

Films of 20 seconds or more additionally need a director's notes file before work starts. Launch
film scale, meaning brand promos and anything pitched at "Apple quality", upgrades that to the long
form structure in `references/launch-film-director-notes.md` if present in your install.

**Read `references/animation-pitfalls.md` before your first line of animation code.** It is the
longest reference in this skill for a reason.

## The failure that ruins most AI animation

Each scene laid out independently, cues fading up, scenes cross fading the whole page. That is a
**PowerPoint with music**, and it is the single most common way this work goes wrong.

Instead: the whole film is one continuous movement. Choose one or two hero elements that persist
across scenes, and make each section a change of state for that hero, in position, scale or form.
Morph between sections rather than cutting. If any frame in your film has nothing moving, the frame
is dead.

Narrative and easing grammar: `references/animation-best-practices.md`. Shot level movement,
meaning zoom, pan, orbit and parallax with a budget: `references/camera-language.md`. GSAP
implementation recipes: `references/gsap-recipes.md`. If the subject is a product interface:
`references/ui-demo-animation.md` and `assets/cursor.jsx`.

## Two technical rules that break video rendering

If you hand write a Stage or Sprite instead of using `assets/animations.jsx`:

1. Set `window.__ready = true` synchronously on the first tick
2. When `window.__recording === true`, force `loop = false`

Miss either and the recording is broken. Never draw a progress bar, timecode or credit strip inside
the frame, since the Stage chrome already owns those.

## Render, no installation needed

ffmpeg 6.x and headless Chromium are both already present.

```bash
# confirm the toolchain
ffmpeg -version | head -1
CHROME=$(find /opt/pw-browsers -maxdepth 4 -type f -name chrome | head -1)

# frame accurate capture, then encode
node scripts/render-video.js animation.html out.mp4          # 25fps
node scripts/render-video-seek.js animation.html out.mp4 --fps=60   # deterministic, no dropped frames

bash scripts/convert-formats.sh out.mp4     # 60fps variant plus palette optimised GIF
bash scripts/add-music.sh out.mp4 tech      # background music bed
```

The shipped scripts launch Chromium through Playwright. Playwright resolves globally here, but it
looks for its own browser build, so pass the container binary:

```js
chromium.launch({ executablePath: process.env.CHROME_BIN })
```

Export it as `CHROME_BIN` before running any render script.

## Audio is two tracks, not one

Sound effects and music are separate jobs on separate frequency bands, and doing only music is a
third of the work.

- **SFX** carry the high frequencies and mark events. 37 prepared files in `assets/sfx/`. Density
  by scene type: a launch hero runs around six cues per ten seconds, a tool demo runs zero to two.
  Cue design and ffmpeg mixing templates: `references/audio-design-rules.md` and
  `references/sfx-library.md`
- **Music** carries the low frequencies and sets the register

**Verify the audio stream exists before you call it done:**

```bash
ffprobe -select_streams a -show_streams out.mp4 2>/dev/null | grep -c codec_type
```

Zero means there is no audio track, which means it is not finished.

## Before delivering

Run `bash scripts/verify-video.sh out.mp4` and actually watch the extracted frames. Check for black
frames, dead stretches where nothing moves, the hero element persisting across cuts, and sound
effects landing on the events they are supposed to mark.

---

## Runtime: check before you build

This skill is built for the Claude Cowork container and needs **no installation**. Verify once per
session, then use whatever is present:

```bash
CHROME=$(find /opt/pw-browsers -maxdepth 4 -type f -name chrome | head -1)   # headless Chromium
node -e "require.resolve('pdf-lib')"      # pdf-lib is installed globally (NODE_PATH is set)
python3 -c "import pptx, PIL, pypdf"      # python-pptx, Pillow, pypdf all present
ffmpeg -version | head -1                 # ffmpeg 6.x present
```

Rules:

- **Never run `npm install` first.** Detect, then fall back only if something is genuinely missing.
- Chromium's own CLI covers most work with no Node at all:
  `"$CHROME" --headless --disable-gpu --no-sandbox --screenshot=out.png --window-size=1600,900 page.html`
  `"$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer --print-to-pdf=out.pdf page.html`
- If a required tool is missing, **stop and say which one**. Never produce a silently degraded
  artifact, such as a video with no audio track.

## Principle 0 — verify facts before you assume

**Highest priority. This runs before clarifying questions**, because if the facts are wrong every
question you ask is crooked.

Any factual claim about a product, version, spec, release date or event must be checked with
`WebSearch` first. Write findings to `product-facts.md`. Never assert from training memory.

Banned openings. If you catch yourself starting a sentence this way, stop and search:

- "I remember X hasn't launched yet"
- "X is currently version N"
- "As far as I know the specs are..."

A search costs ten seconds. A wrong assumption costs two hours of rework.

## The three direction gate

**Any task that produces new visual design must show three real drafts and then stop.**

No exemption for a specified style. No exemption for a supplied brand. A style word narrows the
interpretive space, it does not transfer the right to choose. "Apple style" admits at least three
legitimate readings and picking among them is the user's call.

**Never ask the user to choose between text descriptions.** They have nothing to judge on. Render
three things they can look at, present them together, and end your turn.

Generate the three from deliberately different logics so they cannot converge:

1. **Roulette.** Run `date +%S`, compute `seconds % 20 + 1`, take that style from the matching
   partition of `references/design-styles.md`. This uses the clock as a dice roll to break the
   model's pull toward safe minimalism.
2. **Benchmark.** Pick a real award winning example (Awwwards, FWA, Apple Design Award), confirm
   it exists with `WebSearch`, deconstruct its design language, transfer it to this content.
3. **Studio.** If budget were unlimited, which studio suits this user and this product? Pentagram,
   Collins, IDEO, Kenya Hara, the Stripe team. Design through that philosophy.

All three use the same real content, and their layout skeletons must differ structurally. Two
versions sharing a skeleton with swapped colours is a reskin and reviewers spot it immediately.

**Readability floor, which no style temperature overrides:** body text 14px or larger, labels 12px
or larger, body contrast 4.5:1 or better. Whitespace must be composition with a clear focal point,
not absent content.

Once the user picks, write their choice **in their own words** to `direction-approved.md`.

## Gate files

Checkpoints get steamrolled in long sessions by "continue" and "go faster", so they are files on
disk. A missing file means the step did not happen, and any agent or hook can check.

| File | Written when | Required for |
|---|---|---|
| `product-facts.md` | after Principle 0 search | anything naming a real product |
| `brand-spec.md` | after the asset protocol | anything touching a real brand |
| `direction-approved.md` | after the user picks a direction | before full production |

"The user said continue" authorises moving to the next step. It does not authorise skipping a gate
inside that step. If the user explicitly skips one, record that in the file in their own words.

## Core asset protocol

Triggered two ways, and the second is the one people miss: you are making material **for** a brand,
or your design **displays** one or more recognisable real products, such as a comparison, a ranking
or a review.

**If a nameable product appears in the design, its official logo is a required asset**, not a nice
to have. Assets outrank specifications. Besides the brand colour you obviously need the logo and
the product shot, otherwise what are you actually expressing?

Priority order: **logo, then product renders, then UI screenshots, then colour values, then fonts.**

Five steps: ask for the full asset list at once, search official channels (`brand.com/brand`,
press kit, official social), download with fallbacks per asset type, verify the assets are real
rather than grepping colours alone, then freeze everything into `brand-spec.md`.

For a single file deliverable that opens on a double click, **logos and images must be base64
embedded**. Relative paths break the moment the file is moved.

## Anti AI slop

This is not aesthetic fussiness. It is a logic chain:

1. The client wants their brand recognised
2. AI default output is the average of the training corpus, which is every brand blended together
3. Blended means no brand is recognisable
4. So AI default output dilutes the client's brand

Avoid, unless the brand itself genuinely uses it, which is the only legitimate exception:

| Avoid | Why |
|---|---|
| Aggressive purple gradients | The training corpus formula for "tech", on every SaaS landing page |
| Emoji as icons | The "not professional enough so add emoji" tell |
| Rounded card plus left colour accent bar | 2020 to 2024 Material and Tailwind cliche, now visual noise |
| SVG drawn people, faces, objects | AI drawn figures always have misplaced features |
| CSS silhouettes standing in for a real product shot | Every product ends up looking identical, brand recognition goes to zero |
| Inter, Roboto, Arial or system fonts as display faces | Too common to read as designed |
| Uniform dark navy `#0D1117` plus generic cyan or purple neon glow | One specific lazy combination, not all dark designs |

Prefer: `text-wrap: pretty`, CSS Grid, `oklch()` colours or values already in the spec, real
photography over drawn SVG, and one detail taken to 120 per cent rather than everything at 100.

**Placeholders beat bad implementations.** A grey box labelled "product shot to come" is ten times
better than a hand drawn SVG pretending to be one. Never invent data that looks like real data.

## Language

Reply in the language the user writes in. **When the deliverable is in English, use standard
straight quotation marks.** The upstream typographic rule preferring corner brackets is a Chinese
convention and must not be applied to English copy.

The reference files under `references/` are written in Chinese. Read them directly. They are
instructions to you, not templates for output.

---

## Attribution

Derived from **huashu-design** by 花叔 · 花生 (alchaincyf), MIT licensed.
Upstream: https://github.com/alchaincyf/huashu-design (commit `a790f70`)
Copyright (c) 2026 alchaincyf (花叔 · 花生). Full terms in LICENSE, provenance in NOTICE.md.

Split into a single function skill and adapted for the Claude Cowork runtime by SuperTurbo.
