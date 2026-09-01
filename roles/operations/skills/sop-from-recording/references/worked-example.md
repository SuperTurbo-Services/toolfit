# Worked example

## Contents

- The transcript fragment
- What comes out of it
- What a careless conversion produces instead
- The four judgement calls in this fragment

One short fragment, taken apart. It is deliberately dense: eleven lines of messy speech carrying
almost every decision this skill asks you to make.

---

## The transcript fragment

A support agent explains how they handle "my machine has stopped working". Machine-transcribed,
uncorrected.

```
so uh when someone writes in that the machine is dead, first thing
i do is i pull up the serial. it's usually in the mail, if not i
ask. then i check in servicedesk, uh, sorry, in the warranty
tool, whether it's still covered.
and if it is covered then it's easy, we just book the pickup.
if it's out of warranty i have to tell them it's chargeable and
you want to be a bit gentle about that because people get annoyed.
um. if they bought it less than a couple of months outside the
window i'll usually still cover it, depends a bit on the customer.
oh and before all that, obviously, you check whether they already
have a ticket open. sorry, i skipped that.
```

---

## What comes out of it

### Steps

```markdown
1. Check whether this customer already has an open ticket. [GAP-1]
2. Find the serial number in the customer's message. If it is not there, ask for it.
3. Look up in the warranty tool whether the machine is still covered. [GAP-2]
4. Follow the decision rules below.
```

Note the order. The ticket check is spoken last and prefixed with "sorry, i skipped that", so it is
step 1. This is the whole reason for reading the transcript through before writing anything.

### Decision rules

```markdown
| # | Condition | Then | Read from |
|---|---|---|---|
| 1 | Machine is still under warranty | Book the pickup | warranty tool [GAP-2] |
| 2 | Out of warranty | Tell the customer the repair is chargeable | warranty tool [GAP-2] |
| 3 | Out of warranty, but only just | May still be covered [GAP-3] | see Escalation |
```

### Thresholds

```markdown
| Threshold | Value | Source |
|---|---|---|
| How far outside the warranty window you still cover it | **unknown** | GAP-3 |
```

One row, and its value is "unknown". That is a correct thresholds table. The number is missing
from the recording, so it is missing from the SOP.

### Escalation: decisions a person makes

```markdown
- **Whether to cover a repair that falls just outside warranty.** The recording says "depends a
  bit on the customer". Marked as a judgement call, not as a gap. What the person needs in front
  of them: the purchase date, the warranty end date, and the customer's history.
```

### Tone observations

```markdown
- When telling someone a repair is chargeable, be gentle about it. People get annoyed.
```

### Gap report entries

```markdown
### GAP-3: How far outside the warranty window do you still cover a repair?
**Where:** decision rule 3, thresholds
**Consequence if left open:** blocking - the rule has no executable form. Every colleague picks a
different number, and it decides who pays.
**Question:** You said that if someone is only just outside the warranty window you'll usually
still cover it. In practice, how far outside is still fine?
```

---

## What a careless conversion produces instead

Every line below is wrong, and every one of them reads better than the correct version. That is
the problem this skill exists for.

| Careless output | Why it's wrong |
|---|---|
| `3. Check the machine's status in Servicedesk.` | Records the retracted word. They corrected themselves to "the warranty tool" mid-sentence |
| `| Purchased less than 2 months outside the window | Cover the repair |` | Invented. "A couple of months" was never a number, and this one now looks like policy |
| Ticket check as step 5, in spoken order | Encodes the order of the talking, not the order of the work |
| `2. Politely inform the customer that the repair is chargeable.` | Welds the tone into the step. "Politely" is not an action, and most agent platforms set tone globally |
| No mention of who decides the borderline cases | Turns a judgement call into a silent rule, and it will be wrong in exactly the cases a person was handling well |

---

## The four judgement calls in this fragment

**"Servicedesk, uh, sorry, the warranty tool" is a correction, not two systems.** Take the
correction. The wrong turn does not go in the steps. It only goes in Failure paths if it is a trap
others would fall into, and here it is not - it was a slip of the tongue.

**"A couple of months" is a gap. "Depends a bit on the customer" is not.** They sit in the same
sentence and they are opposite cases. The first is a number the person has in their head and can
tell you. The second is genuine discretion, and pressing for a rule would produce a fake one. Ask
about the first; record the second as escalation. See gap checklist categories 1 and 9, and the
tiebreak between them.

**"Whether it's still covered" needs a source, even though the tool is named.** You know they look
in the warranty tool. You do not know which field, or what it says when a machine is halfway
through a claim. That is GAP-2, and it is the difference between a step someone can execute and a
step someone can only watch.

**"Obviously, you check whether they already have a ticket open" is not obvious.** It is the one
step the demonstrator nearly forgot, in a recording about their own daily work. Treat the word
"obviously" as a signal that something is about to be under-specified, not as permission to skip it.
