---
name: sop-from-recording
description: "Use when someone has a screen recording, screencast, Loom, Zoom capture or video walkthrough of how a work process is actually done, or its transcript, and needs a written standard operating procedure out of it - especially when that procedure will later have to be automated, handed to an AI agent, or turned into a support protocol."
---

# SOP From Recording

## Overview

A recording shows what one person did once. An SOP states what anyone should do every time.
Everything hard about this conversion lives in that gap, and it is the same gap that blocks
automation later: a human watching the recording fills the blanks without noticing, an agent
cannot.

**Core rule: you never fill a gap yourself.** You mark it and ask the person who owns the
process. An invented threshold reads exactly like a real one, and nobody downstream can tell
them apart.

The deliverable is two documents: an SOP that stands on its own, and a gap report that lists
every open question in the order that matters. Translating the SOP into an agent protocol is
separate work and out of scope here.

## When to use

- A transcript or recording of someone doing real work exists, and there is no written procedure
- A procedure exists but was written from theory, and the recording shows the real path
- A process needs to be automated and someone asked "so what are the actual rules?"

**Not for:** writing an SOP from scratch with no recording (no evidence to hold you honest),
summarising a meeting, or documenting software features rather than a work process.

## Input

Ask for a **transcript as text**. Loom, Zoom, Teams and YouTube all export one. Do not ask the
user to paste a video link and do not try to watch the recording; a transcript is enough and
keeps this portable.

Also useful, never required: screenshots, the person's own notes, an existing template the
company already uses.

Output language follows the transcript. A Dutch recording produces a Dutch SOP. This file is in
English so the skill can be shared; the artefacts it produces are not.

## The method

### 1. Read the whole transcript first

Read it end to end before writing a single line of SOP. Do not summarise as you go and do not
start the template early. Processes get explained out of order: people mention the exception in
minute 2 and the rule in minute 19. If you start extracting on the first pass you will encode
the order of the talking, not the order of the work.

### 2. Segment into processes

Most recordings contain more than one process. Decide the split before you write anything, and
say the split out loud to the user.

One SOP per process. Two things are separate processes when they have a different **trigger**,
a different **end state**, or a different **owner**. They are one process when the second thing
only ever happens as a step inside the first.

Split too coarsely and every rule turns into "it depends". Split too finely and you get a pile
of fragments that each assume the others.

**When there is more than one:** one SOP file per process, because they will be maintained,
approved and automated separately. One gap report for the whole recording, with a single
continuous numbering, because the person answering wants one list and not three. Open with the
split and the reason for it.

**When there is none, say so.** Some recordings contain no process at all: a conversation about
why a system is broken, a complaint about a vendor, a discussion of what people wish they had.
These are worth writing up - they are usually dense with category 11 material - but not as an SOP.
Write a findings note instead, state in its first lines why no SOP came out of it, and never
manufacture steps to fill the template. A recording that shows nobody doing anything cannot
produce a procedure, and an SOP invented to have something to hand over is the worst possible
output of this skill.

**What a findings note is.** One file, written to disk, and it is the only file you produce for
this recording. It has four sections in this order and no others:

```markdown
# [Subject]

## Why no SOP came out of this recording
[Two or three sentences. What the recording turned out to be.]

## What was observed
[Prose. Quote where the wording matters.]

## System limitations
| Limitation | What it costs |

## Who decides
| Limitation | Party |
```

The `Party` cells hold a party and nothing else: a role, a team, a vendor. "Systems team". "The
platform vendor". A cell that contains a verb is a recommendation wearing a table, and the reader
cannot tell it apart from something the recording said.

The note reports what the recording contains and stops there. What to do about it takes context
you do not have.

### 3. Extract into the template

Use `references/sop-template.md`. Fill each field using only what was said or shown.

**Read `references/worked-example.md` before your first extraction.** It takes one messy fragment
apart line by line and shows what comes out, what a careless conversion produces instead, and why
two vague phrases in the same sentence get opposite treatment.

**The evidence rule:** every line in the SOP traces back to one of three things.

| Allowed source | Example |
|---|---|
| Something spoken | "we always check the order number first" |
| Something shown on screen | a filter being clicked, a field being read |
| Something the user confirmed when you asked | an answer to a gap question |

Anything else is a gap, including things that are obviously true. "Obviously you check whether
the customer already got a reply" is exactly the kind of step that turns out to be false, or to
be someone else's job.

Where the recording gives a rule but not its boundary, write the rule and mark the boundary.
"Wait a few days" becomes a step with a `[GAP-3]` marker, not a step that says 5 days.

**Leave the demonstration behind.** A recording of real work is full of real people: the customer
whose complaint was opened to show the screen, their address, their order number, the colleague
mentioned in passing. The SOP describes the process, not the cases used to demonstrate it.

| In the recording | In the SOP |
|---|---|
| The customer in the example case | Nothing. Describe the step, not the case |
| Their email, order number, address, phone | Nothing, including inside quoted text |
| The person being recorded, and their colleagues | The role: "support agent", "warehouse". Not the name |
| A name that is genuinely the only route to something | The name, plus a note that it is a single point of failure |
| Where a number came from, when you cite it | The kind of source. "The example order shown", not the order number |

Quote verbatim for two reasons only: to show a garbled phrase the owner needs to recognise, and to
preserve how something was said when tone matters. Strip identifiers out of the quote either way -
a quote is evidence of wording, not of who was involved.

This is not legal advice and it is not the whole of your obligations. It is the minimum that keeps
a document about how work is done from becoming a document about who it was done to.

### 4. Run the gap checklist

Walk `references/gap-checklist.md` in full, category by category. Do not skip categories that
"clearly don't apply" - they are the ones that get missed. Number every gap you find and put the
marker in the SOP at the exact spot it belongs.

### 5. Write both documents

**Two files, one SOP per process plus one gap report, and those are the only files you write.**
No summary document, no overview, no notes file. Everything you would put in a third file already
has a home: findings about tooling go in the SOP's system limitations, open questions go in the
gap report, and what you think should happen next goes nowhere, because that is the reader's
call and not yours.

The gap report is separate so the process owner can answer it without reading the whole procedure,
and so it can be closed off and thrown away while the SOP lives on.

For each gap: what is missing, where it sits in the SOP, what happens if it stays open, and the
question to ask. Write the question as **"what do you do now"**, not "what should the rule be".
People can describe their own behaviour; they freeze when asked to write policy, and a policy
question quietly promotes you into a decision that is not yours.

**Then check the pair before you hand anything over.** Run these four, fix what fails, and run
them again. Each one catches a failure that is invisible in the finished document.

1. **Every `[GAP-n]` marker in the SOP resolves to an entry in the report**, and every entry is
   referenced from the SOP. An orphan marker points at nothing; an unreferenced entry gets
   answered and then nobody knows where the answer goes.
2. **Every number in the SOP appears in a table row with a source.** Grep for digits. A number
   that is not in the thresholds table or the observations table is one you invented.
3. **Every decision rule has a source column filled in**, or a gap marker in it. A rule whose
   condition cannot be read anywhere is not a rule.
4. **No step contains a word describing manner** rather than action - politely, carefully,
   thoroughly, appropriately. Those belong in tone observations or are hiding a missing
   instruction.
5. **No personal data from the demonstration survived.** Write down every name, email address,
   order number, reference and address that appears in the transcript, then search both finished
   documents for each one. Search the tables too. This is a mechanical check, not a reread - the
   leak is never in the steps, it is in a source column or a parenthesis where you were explaining
   where something came from.

### 6. Deliver, sorted by what blocks automation

Order the gaps by consequence, not by where they appear in the document:

1. **Blocking** - the step cannot be executed without an answer **by someone who was not in the
   room**: a new colleague, or a machine. The person who was recorded can execute all of it; that
   is not the test. A missing threshold, an unnamed source of truth, a decision rule with no
   stated condition
2. **Risky** - the step can be executed but will be wrong in a knowable fraction of cases
3. **Cosmetic** - naming, wording, an unverified spelling

Say plainly which gaps must be closed before anyone tries to automate this, and which can be
left open. Then stop. Do not translate anything into a protocol, and do not offer a best guess
for the blocking gaps as a starting point.

## Red flags - stop and mark a gap instead

Every one of these thoughts means you are about to invent something:

- "5 working days is a reasonable default here"
- "I'll put a placeholder in so the document reads well"
- "Any sensible person would check X first"
- "They clearly meant Y even though they said Z"
- "This gap is too small to bother them with"
- "I'll note it in a comment at the bottom rather than break the flow"
- "The template needs a value in this field"
- "I've marked it as a gap, so I can put my best guess next to it"

That last one is the one that slips through, because it looks like diligence. A marker does not
license an answer beside it. If the recording never says what happens when the invoice comes in
*lower* than expected, the cell holds the marker and nothing else - not the marker plus the
obvious action. A reader skims the action and never reads the marker.

An SOP with 14 marked gaps is a working document. An SOP with 14 invented values is a trap,
because it looks finished.

## Common mistakes

| Mistake | Fix |
|---|---|
| Documenting the talking order | Read fully first, then structure by the work |
| Keeping backtracking in the steps | Document the correct path; move the wrong turn to Failure paths |
| One giant SOP for three processes | Segment in phase 2 and say the split out loud |
| Steps that read "handle it appropriately" | Name the action, or mark it as a judgement call and escalate |
| Tone advice inside a step | Tone is not a step. Move it out; see gap category 6 |
| Silently correcting a garbled system name | Mark it. A wrong system name breaks every integration built on it |
| Answering a gap because the user seems busy | The gap is the deliverable. Ship it open |
| Asking the process owner about a broken tool | That is category 11. Record it and cost it, don't ask |

## Non-goals

- **No protocol translation.** This skill produces an SOP. Turning it into an agent protocol,
  with whatever structure the target platform wants, is separate work.
- **No validation on the user's behalf.** You do not decide whether the process is any good.
- **No invented numbers, names, or steps.** Ever, including as placeholders.
