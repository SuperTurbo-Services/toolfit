---
name: info-graphic
description: "Build a print quality infographic or data visualisation as a single self contained HTML page, exporting to PDF, PNG or SVG. Use when someone wants an infographic, a data visualisation poster, a one page explainer, a chart led summary, a \"make this data look good\" request, or any single page where data is the subject and there is nothing to click. Not for slide decks and not for interactive dashboards."
---

# Info-graphic

One page where **the data is the subject and there is nothing to click**. That is the boundary. A
deck is paged. A prototype is clickable. A dashboard is live. An infographic explains itself
standing still, in print or in a scroll.

Wrong skill if: the user wants pages that advance (deck-builder), screens that respond
(app-web-prototype), or a live view of changing data.

## Before anything

**Real data or no infographic.** If the user has not supplied numbers, ask for them. Do not invent
figures, and do not generate plausible looking sample data to fill a layout. An infographic built on
invented numbers is worse than no infographic, because it looks authoritative.

If they supply a source, verify it under Principle 0 below and record it in `product-facts.md`. Put
the source line on the artifact itself. An infographic without attribution is not finished.

## Form follows the data, not a template

Answer these before choosing any layout:

- **What is the single claim?** If you cannot state it in one sentence, the piece has no spine
- **What shape is the data?** Comparison, composition, change over time, distribution, flow,
  relationship. The shape picks the chart, not your preference
- **Reading distance?** Held in the hand, on a screen at a metre, or on a wall
- **What is the visual motif?** The element unique to this content that no other subject would
  have. If you cannot name one you are decorating a template

## Style

Use the **infographic partition, 20 styles**, from `references/design-styles.md`. Take that
partition specifically. The web partition is for pages and the deck partition is for slides, and
before August 2026 infographics were forced into the web partition and came out looking like
landing pages. Do not repeat that.

Layout patterns by scene: `references/scene-templates.md`.
Typography, which carries most of the quality here: `references/typography.md`.

## Craft rules that decide whether it reads as designed

- **Precise CSS Grid columns.** A real column structure, not stacked divs with margins
- **`text-wrap: pretty`** on every text block. Cheap, and one of the details that separates
  designed from generated
- **A type scale with real jumps.** Adjacent sizes at least 25 per cent apart, otherwise nothing
  reads as a level
- **Number formatting is typography.** Tabular figures for anything aligned in a column, consistent
  decimal places, units stated once rather than repeated on every value
- **Every chart earns its place.** Four numbers is a sentence, not a chart. Use a chart when the
  shape carries meaning the numbers alone do not
- **Label directly.** Put the label on the thing. A legend forces the eye to bounce
- **Never a pie chart with more than three slices**, and never one at all if a bar would compare
  more honestly

## Build and export

Single self contained HTML. Fonts by webfont link or system stack, images base64 embedded.

```bash
CHROME=$(find /opt/pw-browsers -maxdepth 4 -type f -name chrome | head -1)

# vector PDF, best for print, text stays selectable
"$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
  --print-to-pdf=out.pdf infographic.html

# high resolution PNG, set the window to the artboard size
"$CHROME" --headless --disable-gpu --no-sandbox \
  --screenshot=out.png --window-size=1600,2400 --force-device-scale-factor=2 infographic.html
```

For SVG, author the chart as inline SVG in the page and extract that node. Do not rasterise and
call it vector.

Downsample for thumbnails with Pillow, which is installed:

```bash
python3 -c "from PIL import Image; im=Image.open('out.png'); im.thumbnail((800,800)); im.convert('RGB').save('thumb.jpg',quality=85)"
```

## Before delivering

Render it and look at it. Check the one sentence claim survives at thumbnail size, every number
traces to the source, contrast passes at 4.5:1, and nothing is a chart that should have been a
sentence. See `references/verification.md`.

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
