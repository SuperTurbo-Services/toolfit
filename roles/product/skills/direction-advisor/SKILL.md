---
name: direction-advisor
description: "Choose a visual direction BEFORE production starts, by rendering three genuinely different draft treatments and letting the user pick. Use at the beginning of new design work, when the brief is vague, when someone says \"make it look good\", \"I do not know what style I want\", \"show me some directions\", or when a look has not been agreed yet. Outputs three drafts plus a recorded decision, not a finished design. For variations inside an already agreed direction use design-options. To review existing work use design-critique."
---

# Direction Advisor

Three real drafts, then stop and let the user choose. That is the whole job.

**You do not produce the finished design.** You produce the choice. Another skill executes it once
`direction-approved.md` exists.

## The iron law

**Never ask the user to pick between text descriptions.** "Would you like minimal, bold, or
editorial?" is an invalid question, because they have nothing to look at. Render three things.

This holds even when the brief seems clear. A supplied style word narrows the interpretive space,
it does not transfer the right to choose. "Apple style" legitimately means a deep space dark
treatment, a large white serif treatment, or a product colour immersion. Which one is the user's
call, not yours.

Same when a brand is supplied: all three drafts use the same real brand assets, and differ in
design interpretation.

## Process

**1. Ask, once.** At most three questions: audience, core message, emotional register. In the same
message ask for materials: project name, logo, brand colours, type rules, and any reference site or
screenshot they like. If they do not answer, proceed on stated assumptions rather than waiting.

**2. Restate.** At least 200 words in your own words: the real need, the audience, the setting, the
register, and what they have not said out loud. End by saying you will build three versions. **Do
not end by asking which direction they want.**

**3. Write the spec.** At least 500 words, and this is the only shared input the three drafts get,
so thin here means all three drift. Cover: what the thing is, audience and setting, content
sections, register keywords, **output format and exact pixel dimensions**, known constraints, image
needs, and the visual motif specific to this content.

**4. Settle images before drafting.** Ask whether images are essential to the content. Museum,
history, nature, product and place content nearly always needs real images. Tools, data and pure
argument may not. **If unsure, treat them as essential.** Source real images first and share the
same set across all three drafts. Wikimedia Commons, Met Open Access and Biodiversity Heritage
Library for historical and natural subjects, Unsplash and Pexels for general. Run the honesty test
on each: remove this image, is information lost? If nothing is lost it is decoration, so cut it.

**5. Build three, independently.** Use the three logics in the kernel below. If you can spawn
subagents, run them in parallel with independent context. If not, run them serially, clearing your
memory of the previous one each time, and still produce three. Never collapse to one.

**6. Present and stop.** Show all three with a screenshot each, and for each state which logic
produced it, which specific style, benchmark or studio it used, and one sentence on why. **Then end
your turn.** Do not choose on the user's behalf, including in unattended sessions. This is the one
decision only the user can make.

**7. Record.** Write the user's choice verbatim into `direction-approved.md`, along with the three
screenshot paths. Mixing is allowed: "the roulette colours with the studio layout".

## Draft form by output type

| Output | Each direction is |
|---|---|
| Page, infographic, prototype | one complete HTML plus a screenshot |
| Multi page deck | two representative pages |
| Animation or film | one direction board: a real rendered hero frame or two, a colour strip, a one line register statement, a named reference work. Not three finished films |
| Cover or single image | one real rendered image |

## Rendering the drafts

```bash
CHROME=$(find /opt/pw-browsers -maxdepth 4 -type f -name chrome | head -1)
"$CHROME" --headless --disable-gpu --no-sandbox --screenshot=dir1.png --window-size=1440,900 d1.html
```

Use 1920x1080 for deck pages. Save drafts to `<project>/design-demos/<logic-name>.html`, never a
temp directory. Before presenting, confirm three HTML files actually exist. Fewer than three means
you skipped a logic, so go back and finish.

## The three exemptions

Skip the gate only when the user says so explicitly in this session, when iterating inside an
already approved direction, or for mechanical non design work such as export or a bug fix. Record
any exemption in `direction-approved.md` in the user's own words.

The 60 style library, partitioned into web 20, deck 20 and infographic 20 with fidelity ratings and
open source font suggestions: `references/design-styles.md`. Pick the partition by output form, not
by subject matter.

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
