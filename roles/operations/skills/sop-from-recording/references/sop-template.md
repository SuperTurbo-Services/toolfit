# SOP template

Fill every field. A field with nothing behind it in the recording gets a gap marker, never a
plausible value and never a blank.

**One exception, and it is not a loophole.** A field that cannot apply to this process gets
`Not applicable: [why]` instead. A purely internal routing procedure has no tone section because
nobody is written to; a read-only check has no failure path that costs anything. Use this only
when you can state the reason in the same breath, and never for a field that is merely empty
because the recording skipped it - that is a gap.

Write the SOP in the language of the transcript. The field names below are English so the
template can be shared; translate them.

---

```markdown
# [Process name]

**Purpose:** [What is achieved when this is done correctly. One sentence.]

## Scope

**Applies when:** [The trigger. An event, a message type, a moment in time, a frequency.]
**Does not apply when:** [The nearest neighbouring process this gets confused with.]
**Multiple topics in one request:** [What happens when this arrives alongside another topic.
See gap checklist category 10.]

## Owner and systems

**Owner:** [Role, not a person's name, unless the person genuinely is the only one who does it.]
**Systems used:** [Each system, and what access level is needed in it.]
**Needed before you start:** [Information that must already be in hand.]

## Steps

1. [One action. Imperative. Exact button, menu, and field names from the recording.]
2. [One action. If you write "and" or "then also", split it into two steps.]
3. [...]

## Decision rules

Every branch in the steps above appears here as a row. If a condition has no readable source,
the row is incomplete and needs a gap marker.

| Condition | Then | Read from |
|---|---|---|
| [When this is true] | [Do this] | [System + screen + field] |

## Thresholds

REQUIRED. Every number that **governs a decision** gets a row here, including ones that feel
obvious. A governing number without a row is an invented number.

| Threshold | Value | Source |
|---|---|---|
| [What it governs] | [The value, or GAP-n] | [Stated in recording / confirmed by owner / GAP-n] |

Numbers that appear in the recording but govern nothing - the size of a queue that day, the price
of the example order, a figure quoted from a customer's own message - go in a second table below,
labelled as observations. They are listed so that nobody later mistakes them for rules.

| Number in the recording | Value | Kind of source |
|---|---|---|

The third column holds the **kind** of source, never its identity: "the example order shown",
"a figure the customer quoted", "the queue at the time of recording". Not the order number, not
the customer, not the date it happened. This column is the one place where stripping the
demonstration case is easy to forget, because citing where a number came from feels like rigour.
A number nobody can trace back to a person is the whole point of putting it here.

## Escalation: decisions a person makes

[Steps that genuinely require human judgement. For each: what is being decided, who decides, and
what they need in front of them. This section is a feature, not a shortfall - see gap checklist
category 9.]

## Failure paths

| What goes wrong | What to do |
|---|---|
| [Lookup returns nothing] | [...] |
| [System unavailable] | [...] |
| [No reply from the other party] | [...] |

## System limitations

[Things the recording revealed about the tools rather than the procedure: manual copying between
screens, a link that is configured but broken, information that exists nowhere. Not gaps, and no
question to the process owner closes them. State what each one costs. See gap checklist category
11.]

## Definition of done

- [ ] [Verifiable end state, observable by someone who was not present]
- [ ] [...]

## Tone observations

[Anything the demonstrator said about how to communicate, kept separate from the steps. Input for
a style guide, not instructions. See gap checklist category 6.]

## Open gaps

[GAP-1] [one line each, pointing at the gap report]
[GAP-2] ...
```

---

## Notes on filling it

**Steps.** One action each. Quote UI elements exactly as they appear: **Save**, **Next**,
**Order status**. If the recording shows a screen whose state matters and is hard to describe,
add `[screenshot: what should be visible]` on its own line under the step.

**Backtracking.** When the demonstrator makes a wrong turn and corrects it, the steps get the
correct path only. The wrong turn goes in Failure paths if it is a trap others would fall into,
and is dropped otherwise.

**Decision rules vs steps.** If a step contains an "if", it has a row in Decision rules. The step
itself stays readable: "3. Check whether the order has shipped (see decision rules, row 2)."

**Thresholds.** This table is the single most useful artefact for whoever automates this later.
It is also where invented values hide, which is why every row carries its source.
