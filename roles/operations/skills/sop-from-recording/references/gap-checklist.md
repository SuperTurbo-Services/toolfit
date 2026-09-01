# Gap checklist

## Contents

There are **11 categories**, plus a note on how to write a gap up. Walk all of them.

1. Quantities without a number
2. Decisions with no named source of truth
3. Garbled transcription
4. Cross-references to other procedures
5. Implicit knowledge
6. Tone mixed into instruction
7. Missing failure paths
8. Data whose existence is unconfirmed
9. Human judgement steps
10. Requests that carry more than one topic
11. Missing capability, not missing information
12. *(not a category)* Writing up a gap

Categories 6, 9 and 11 do **not** produce questions for the process owner. They route to other
sections of the SOP. Everything else produces a question.

---

Walk every category. Do not skip the ones that look inapplicable - those are the ones that get
missed. For each hit, number it (`GAP-1`, `GAP-2`, ...), place the marker in the SOP at the exact
step it belongs to, and write the entry in the gap report.

The categories are ordered roughly by how often they block automation, not by how often they
occur.

---

## 1. Quantities without a number

**Looks like:** "a few days", "a while", "when it takes too long", "a small amount", "if it's an
expensive order", "shortly after".

**Why it blocks:** a human reads "a few days" and does something sensible. A protocol needs an
integer. This is the single most common blocker, and it is usually resolvable in one sentence
from the process owner.

**Ask:** "You said you wait a few days before you chase it. In practice, when do you stop waiting
and start looking into it yourself?"

**Never:** pick a plausible number because the sentence reads badly without one.

**Tiebreak with category 9.** Some vague quantities are judgement calls wearing a number's
clothing, and the two categories pull opposite ways: this one says always ask, category 9 says
never press. Ask once, softly, and let the answer decide. If the person describes doing the same
thing every time, it was a threshold and you now have it. If they describe weighing several things
afresh each case, it is judgement - move it to the escalation section and stop asking. "It depends"
is the answer, not a failure to answer.

---

## 2. Decisions with no named source of truth

**Looks like:** "if the order is already old", "if the customer has ordered before", "check
whether it has shipped".

**Why it blocks:** the condition is clear, the lookup is not. Which system, which screen, which
field? A human knows where to look because they have the tab open. Anything automating this
needs a field name, and often an API that may not exist.

**Ask:** "Where do you see that? Which screen, and which field on it?"

**Record in the SOP** as a decision rule with three columns: condition, action, and where the
condition is read from. If the source is unknown, the rule is incomplete, not merely unpolished.

---

## 3. Garbled transcription

**Looks like:** system names, product names, field labels and people's names as rendered by an
automatic transcriber, which garbles them constantly and confidently. Also, and more dangerously,
whole sentences destroyed mid-instruction: a clause that starts as a rule and dissolves into
nonsense.

**Why it blocks:** a wrong system name propagates into every integration, ticket and prompt built
downstream, and looks authoritative the whole way. A destroyed sentence is worse, because it is
usually destroyed at exactly the interesting moment - the transcriber copes fine with pleasantries
and fails on the specific thing that was being explained.

**Handling:** if you are confident of the correction (an obvious phonetic mangling of a name that
appears correctly elsewhere in the same transcript), correct it silently. Otherwise mark it and
quote the transcript verbatim, so the owner can recognise their own words.

**Severity is not uniform.** A system name, a field name or a broken instruction is never
cosmetic - everything built later rests on it. A person's name or a product spelling usually is.

**Ask:** "The recording says 'X' here - is that [your guess], or something else?" For a broken
sentence: quote the surrounding lines and ask what was being said.

---

## 4. Cross-references to other procedures

**Looks like:** "same as with returns", "you know the drill", "like I showed earlier", "then the
normal process".

**Why it blocks:** whatever this SOP becomes, it has to work when read alone. An agent handling
one contact does not get to go and read the neighbouring protocol first, and a new employee
reading this SOP on day one has not seen the other one either.

**Handling:** resolve it. Either the referenced steps are in this recording, in which case write
them out here in full even at the cost of duplication, or they are not, in which case that is a
gap and the SOP is incomplete without a second recording.

**Ask:** "You mention it goes like the returns process. Do we have that written down anywhere, or
should we record that one too?"

---

## 5. Implicit knowledge

**Looks like:** a step that only works if you already know something the recording never says.
The tell is that the demonstrator does something without narrating it, or narrates a result
without the action that produced it.

**Why it blocks:** it is the hardest category to spot, because it is invisible by definition. The
reliable way to find it is to reread the steps and ask, at each one: could someone who started
this week do this from the text alone?

**Ask:** "Between step 4 and step 5 something happens that I can't see. What do you do there?"

---

## 6. Tone mixed into instruction

**Looks like:** "then you tell them nicely that it can't be done", "be a bit apologetic", "keep it
friendly", "you don't want to sound like a robot about it".

**Why it blocks:** two different things are wearing one sentence. The instruction ("communicate
that it cannot be done") belongs in the SOP. The tone belongs in a style guide, and most agent
platforms configure tone globally rather than per step - mixing it in means it gets applied
inconsistently or lost entirely.

**Handling:** split them. Keep the action in the step. Collect the tone observations in a
separate section at the end of the SOP, marked as input for a style guide rather than as steps.
Do not delete them; they are often the most valuable thing in the recording.

---

## 7. Missing failure paths

**Looks like:** a happy path with no branch. The lookup returns nothing. The system is down. The
customer does not reply. The data contradicts itself. The recording almost never covers these,
because the demonstrator picked a case that works.

**Why it blocks:** in practice a meaningful share of cases go down these branches, and something
automating the process will hit them on day one. An unhandled branch is where automation does
visible damage.

**Ask:** "What do you do when you look it up and there's nothing there?" - once per lookup step,
not once per SOP.

---

## 8. Data whose existence is unconfirmed

**Looks like:** a step that assumes information is available, when the recording never shows it
on screen. Frequently paired with category 2.

**Why it blocks:** it is the difference between a step that needs writing and a step that needs a
system change first. Those have wildly different costs, and conflating them makes an SOP look
cheap to automate when it is not.

**Handling:** mark it as a data dependency, distinct from a normal gap, by adding
`**Data dependency:** yes` as a fifth line of the gap entry. Note whether the information was
actually visible on screen in the recording or only spoken about. Without that flag the entry
looks like a question someone can answer in a sentence, when the honest answer may be "we would
have to build that first".

**Ask:** "Is that information available in the system, or is it something you know from
elsewhere?"

---

## 9. Human judgement steps

**Looks like:** "you get a feel for it", "depends on the customer", "sometimes I just make an
exception", "if they seem genuinely upset".

**Why it blocks:** it does not, if handled correctly. It blocks badly when treated as a gap to be
closed - pushing for a rule where none exists produces a fake rule that will be wrong in exactly
the cases the human was handling well.

**Handling:** mark it as an escalation point, not a gap. The SOP says: this decision is made by a
person, here is the information they need in front of them to make it. Do not press for a rule.

**Ask, but softly:** "Is there a line where you always do the same thing, or does it genuinely
depend every time?" - and take "it depends" as a complete answer.

**The deliberate non-rule is a different animal.** Sometimes the discretion is not an accident but
a policy: management has decided people should judge each case, and they are right to. You will
hear it as "everyone gets the room to decide how to solve it". Mark these too, but change the
question. Not "what is the rule", which implies there should be one, but **"do you want a rule
here?"** - and route that question to whoever sets policy, not to the person doing the work.

**When a whole process runs on deliberate discretion**, say that in the SOP's opening lines rather
than burying it in one gap. It changes what the process can become: the honest options are to
write down limits and accept a stiffer outcome, or to keep the judgement with a person and let
automation do the preparation instead. That is the reader's decision to make, and they can only
make it if you put it in front of them.

---

## 10. Requests that carry more than one topic

**Looks like:** the recording deals with one clean case, but the demonstrator mentions in passing
that messages usually contain two or three questions at once.

**Why it blocks:** SOPs are written per topic; real work arrives per contact. Anything automating
this needs a stated rule for what happens when one contact spans three procedures and only two of
them are written up. Most platforms will happily answer the two and quietly drop the third.

**Ask:** "When someone asks about a delivery and a return in one message, is that handled as one
thing or two?"

**Record** the answer in the SOP's scope section, not in the steps.

---

## 11. Missing capability, not missing information

**Looks like:** the demonstrator working around the tool rather than with it. Copying an identifier
from one screen into another by hand. A link that is configured but does not work. A rule that is
set up but switched off. "It would be nice if the system just showed that." A comparison to a
previous employer's setup.

**Why it matters:** these are not gaps in the procedure and no question to the process owner will
close them. Asking one anyway makes you look like you were not paying attention. But they are
usually the most valuable thing in the recording, because they explain where the time goes and
they decide whether the process can be automated at all - a step that depends on a human reading
a screen that has no API is not automatable, however well documented.

**Handling:** collect them in their own section of the SOP, separate from the gaps. State for each
one what it costs: extra handling time, a branch that cannot be checked, information that is not
visible anywhere. Do not soften them into suggestions and do not turn them into steps.

**Do not ask what to do about it.** Record it, cost it, and route it to whoever owns the tooling.

**One question is allowed:** how often it happens. "Roughly how many times a week do you have to
go hunting like that?" A limitation without a frequency cannot be costed, and an uncosted
limitation loses every argument against the people who have to fix it.

---

## Writing up a gap

Every entry gets four lines:

```
### GAP-3: How long is "a few days"?
**Where:** step 4, delayed delivery
**Consequence if left open:** blocking - the step cannot be executed without a number
**Question:** You say you ask the customer for a few days' patience. In practice, when do you
stop waiting and start chasing it yourself?
```

Consequence is one of **blocking**, **risky**, or **cosmetic**. Sort the report by that, not by
where the gaps appear in the SOP.
