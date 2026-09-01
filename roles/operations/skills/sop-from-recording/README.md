# sop-from-recording

An agent skill that turns a screen recording of real work into a standard operating procedure -
and, more importantly, into an honest list of everything the recording did not say.

## The problem it solves

Record someone doing their job, hand the transcript to an LLM, ask for an SOP, and you get a
clean document full of invented specifics. "Wait a few days" becomes "wait 5 working days".
"Check whether the order is old" becomes a step with no indication of where "old" is read from.
The result looks finished, which is the dangerous part: nobody downstream can tell which numbers
came from the business and which came from the model.

That matters most when the SOP is a stepping stone to automation. A human reading a vague step
fills the blank without noticing. An agent cannot, and an agent given an invented threshold will
apply it consistently and wrongly.

## What it does

Produces two files:

- **a SOP** - scope, steps, decision rules, thresholds, escalation points, failure paths,
  definition of done
- **a gap report** - every open question, sorted by whether it blocks execution, merely risks a
  wrong outcome, or is cosmetic

Rather than filling gaps, it marks them and writes the question to ask the process owner. A SOP
with 14 marked gaps is a working document; a SOP with 14 invented values is a trap.

It also flags the things that specifically break when a procedure is later translated into an
agent protocol: cross-references to other procedures (protocols must stand alone), conditions
with no named source system, data whose existence in the system was never confirmed, tone
instructions tangled into steps, unhandled failure branches, and requests that carry more than
one topic at once.

Translating the SOP into a protocol is deliberately out of scope. That step depends on the target
platform; this skill's job is to make sure nothing is quietly missing before you get there.

## Install

Claude Code, personal skills:

```bash
git clone https://github.com/ralph-oei/sop-from-recording ~/.claude/skills/sop-from-recording
```

Or drop the directory into any skills path your agent runtime reads
(`~/.agents/skills/` works across several of them).

## Use

Export the transcript from Loom, Zoom, Teams or YouTube, then:

> Here's the transcript of a recording where our support lead walks through how they handle
> delivery complaints. Turn it into an SOP.

The skill works from text. It does not need the video file, and it does not need a link.

Output follows the language of the transcript - a Dutch recording produces a Dutch SOP.

## Contents

| File | What's in it |
|---|---|
| `SKILL.md` | The method: read whole, segment, extract, check gaps, write, deliver |
| `references/sop-template.md` | The template, with a required thresholds table |
| `references/gap-checklist.md` | 11 categories of gap, why each one blocks automation, what to ask |
| `references/worked-example.md` | One messy fragment taken apart, with the careless version alongside |

## Licence

MIT.
