---
name: app-web-prototype
description: "Build a clickable high fidelity app or web prototype as a single self contained HTML file, with working navigation, real state and a proper device frame. Use when someone wants a prototype, a clickable mockup, an app mockup, screens they can click through, an iOS or Android prototype, a web page prototype, or says \"make this real enough to demo\" or \"I want to click through the flow\". Not for production code and not for static pictures of screens."
---

# App / Web Prototype

A prototype somebody can **click**. Static screenshots of screens are not this skill's output. If
the buttons do not do anything, you have not finished.

Wrong skill if: they want production code with a backend, a paged deck (deck-builder), or a single
still page of data (info-graphic).

## Architecture: single file by default

Inline React with Babel in one HTML file that opens on a double click of a `file://` path. Local
images base64 embedded. Only split into multiple files past roughly 1000 lines, and if you do,
include the `python3 -m http.server` instruction, because Babel fetches over XHR and CORS blocks it
on `file://`.

Three rules that break the build if ignored, full detail in `references/react-setup.md`:

1. **Never `const styles = {...}`.** Multiple components collide. Use `cardStyles`, `headerStyles`
2. **Scope is not shared** between `<script type="text/babel">` blocks. Export with
   `Object.assign(window, {...})`
3. **Never `scrollIntoView`.** It breaks container scrolling. Use another DOM scroll method

Pin React and Babel versions. Unpinned CDN versions break silently later.

## Device frames are not hand written

Use the shipped components. Do not draw a Dynamic Island, a status bar, a home indicator or window
chrome yourself, because the island is a fixed 124 by 36 with very tight status bar margins and
hand written versions are wrong roughly every time.

| Target | Component |
|---|---|
| iOS | `assets/ios_frame.jsx` |
| Android | `assets/android_frame.jsx` |
| Desktop app | `assets/macos_window.jsx` |
| Web page | `assets/browser_window.jsx` |
| Several screens side by side | `assets/design_canvas.jsx` |
| Transitions | `assets/animations.jsx` |

Read the file and inline it into your HTML.

## Real images before design, not after

Run the honesty test on every image: **remove it, is information lost?** No loss means it is
decoration, so leave it out. Decorative stock photography is slop.

Where to source: user brand assets through the asset protocol below, Unsplash and Pexels for
general scenes, Wikimedia Commons and Met Open Access for historical and natural subjects. Base64
embed everything so the file survives being moved.

## Default delivery shape

**Four to six main screens laid out together, each one independently interactive.** Do not ask the
user to choose between static and interactive, just build interactive. Each screen is its own small
state machine: tabs switch, buttons respond, modals open and close.

Deviate only if the user explicitly asks for a single flow demo or for static screens.

## Information density

Default to restraint: one less container, one less border, one less decorative icon.

Switch to **high density** when the product's selling point is intelligence, data or context
awareness, such as a dashboard, tracker, copilot or analytics tool. High density means at least
three pieces of **real differentiating information** per screen. It does not mean more decorative
icons, which stay banned either way.

## Taste anchors

- A serif display face such as Newsreader, Source Serif or EB Garamond, with `-apple-system` body
- One base colour with actual warmth, plus a single accent used consistently
- One detail taken to 120 per cent that is worth screenshotting. Everything else at 80

## Verify before delivering

Non negotiable. Run three click tests: navigate into a detail view, hit the key annotated action,
switch a tab. **`pageerror` must be zero.**

```bash
CHROME=$(find /opt/pw-browsers -maxdepth 4 -type f -name chrome | head -1)
"$CHROME" --headless --disable-gpu --no-sandbox --screenshot=proto.png --window-size=1440,900 prototype.html
```

Then open the screenshot and look at it. Interaction bugs are invisible in source. See
`references/verification.md`.

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
