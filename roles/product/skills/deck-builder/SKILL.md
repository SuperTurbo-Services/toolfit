---
name: deck-builder
description: "Build a presentation deck as HTML slides at 1920x1080 and export to PDF or editable PPTX. Use when someone wants a slide deck, a presentation, a pitch deck, a keynote, a PPT, a board deck, wants slides made from a document, or asks to turn a report into a presentation. Produces browser presentable HTML plus a PDF, with PowerPoint export on request."
---

# Deck Builder

HTML slides at 1920x1080, presentable in a browser, exportable to PDF and to PowerPoint.

Wrong skill if: they want one page that stands alone (info-graphic), or screens to click through
(app-web-prototype).

## Decide the architecture first

Getting this wrong means fighting CSS scope and specificity for the rest of the job.

**Multi file with an overview wall. This is the default for almost every deck.** Each slide is its
own HTML file, assembled by `assets/deck_index.html`. Copy that file to `index.html` and edit its
MANIFEST. **Do not rewrite the overview logic.** It already solves three problems people hit:
tilt rendering, click hit areas, and thumbnail cropping.

**Single file** only for five slides or fewer, where you are certain no overview wall is needed, or
where slides must share JavaScript state. Uses `assets/deck_stage.js`. Two hard constraints: the
script tag goes **after** `</deck-stage>`, and `display: flex` belongs on `.active`, not on the
section. See `references/slide-decks.md`.

## Five slides or more: showcase two first

Build two representative slides, agree the visual grammar, then batch the rest. Skipping this means
a wrong direction costs you N slides of rework instead of two.

## Style

Use the **deck partition, 20 styles**, from `references/design-styles.md`. Not the web partition.
Typography carries most of the perceived quality here: `references/typography.md`.

Page numbers live on the deck shell, never inside a slide. Slides that carry their own numbering
produce two competing counters on screen.

## Export, no installation needed

**PDF, the default, produced automatically without being asked:**

```bash
CHROME=$(find /opt/pw-browsers -maxdepth 4 -type f -name chrome | head -1)
for f in slides/*.html; do
  "$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
    --print-to-pdf="${f%.html}.pdf" "$f"
done
python3 -c "
from pypdf import PdfWriter; import glob
w=PdfWriter()
for p in sorted(glob.glob('slides/*.pdf')): w.append(p)
w.write('deck.pdf')"
```

Text stays vector and selectable. `pdf-lib` is also available globally if you prefer it, and
`scripts/export_deck_pdf.mjs` uses that route.

**Thumbnails for the gallery overview:**

```bash
"$CHROME" --headless --disable-gpu --no-sandbox --screenshot=big.png --window-size=1920,1080 slide.html
python3 -c "from PIL import Image; im=Image.open('big.png'); im.thumbnail((1600,1600)); im.convert('RGB').save('thumb.jpg',quality=85)"
```

Keep thumbnails at 1000px or wider or they blur on hover.

**Editable PPTX, only when asked.** Two routes, and be honest about the difference:

*No installation, lower fidelity.* `python-pptx` is present. Real editable text frames, but you
place elements yourself rather than translating the HTML:

```bash
python3 -c "
from pptx import Presentation; from pptx.util import Inches, Pt
p=Presentation(); p.slide_width=Inches(13.333); p.slide_height=Inches(7.5)
s=p.slides.add_slide(p.slide_layouts[6])
tb=s.shapes.add_textbox(Inches(1),Inches(3),Inches(11),Inches(1.5))
tb.text_frame.text='Title'; tb.text_frame.paragraphs[0].runs[0].font.size=Pt(54)
p.save('deck.pptx')"
```

*Higher fidelity, needs one install.* `scripts/html2pptx.js` reads computed styles off the DOM and
translates each element into a native PowerPoint object, which is markedly better, but it requires
`npm i pptxgenjs` and the HTML must satisfy four hard constraints in `references/editable-pptx.md`.

**Never degrade the HTML design to satisfy the PPTX exporter.** If something will not translate,
export it faithfully as PDF and tell the user exactly what PowerPoint would have lost.

## Verify

Render every slide, look at the images, confirm nothing overflows its frame and the type scale
holds at 1920x1080. See `references/verification.md`.

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
