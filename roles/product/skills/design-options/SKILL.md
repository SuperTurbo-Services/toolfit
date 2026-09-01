---
name: design-options
description: "Explore variations of a design whose direction is ALREADY AGREED, shown side by side on one canvas or as live controls the viewer can adjust without regenerating. Use when someone asks for alternatives, variants, \"try a few versions\", wants to compare layouts or palettes, or wants sliders to tune colours, spacing and type. Requires direction-approved.md or a settled look: if no direction is chosen yet use direction-advisor instead."
---

# Design Options

Variations **inside a direction that is already settled**. The big fork was chosen elsewhere. Your
job is the space around that choice.

Wrong skill if there is no agreed direction yet. Check for `direction-approved.md`. If it does not
exist and the user has not clearly settled a look, hand off to `direction-advisor` and say why.

## Two modes, and picking the right one matters

**Side by side canvas.** Use when the variations differ structurally: layout, hierarchy, section
order, component pattern. Differences you cannot express as a slider. Render each variation as a
complete artifact and lay them on one pan and zoom canvas using `assets/design_canvas.jsx`, each
labelled with what changed.

**Live Tweaks.** Use when the variations are parametric: palette, type scale, spacing rhythm,
density, corner radius, accent colour. One artifact with a control panel, so the user explores the
whole space themselves instead of asking you for version four.

If you find yourself producing more than about five near identical files that differ by a colour,
you picked the wrong mode. Rebuild it as Tweaks.

## Varying along one axis at a time

State the axis before you build. Mixed axis variations cannot be compared, because the user cannot
tell which change caused the effect they like.

| Axis | Varies | Holds constant |
|---|---|---|
| Layout | Structure, grid, section order | Palette, type, content |
| Palette | Colour system only | Layout, type, content |
| Type | Family, scale, weight | Layout, palette, content |
| Density | Spacing, information per screen | Everything else |
| Motion | Transitions and easing | The static design |

**Always the same real content across variations.** Different copy in different versions makes the
comparison worthless.

## Tweaks implementation

Pure front end, CSS custom properties, no host messaging. Bind every control to a `--tweak-*`
variable, persist to `localStorage` so a reload does not lose the state, and provide a reset. The
panel toggles out of the way, because the user needs to see the design without it.

Full pattern: `references/tweaks-system.md`. React and Babel pinning rules if the artifact uses
them: `references/react-setup.md`.

## Presenting

Render each variation and show the images together, never a list of file paths.

```bash
CHROME=$(find /opt/pw-browsers -maxdepth 4 -type f -name chrome | head -1)
for f in v1 v2 v3; do
  "$CHROME" --headless --disable-gpu --no-sandbox --screenshot=$f.png --window-size=1440,900 $f.html
done
```

For each variation say what changed and what it costs. Every option is a trade, and naming the
trade is the actual value you add over generating more files. "Denser, so more fits above the fold,
but the scanning pause between sections is gone."

Recommend one. The user asked for options, not for abdication.

## Rules

- **Never mix axes in one comparison set**
- **Never vary the content between variations**
- Three to five options. Beyond that the user stops comparing and starts skimming
- Structural differences go on a canvas, parametric differences go in Tweaks. Not the reverse
- Keep the readability floor in every variation. A palette option that fails contrast is not an
  option, so do not present it

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
