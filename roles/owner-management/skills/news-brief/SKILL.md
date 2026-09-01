---
name: news-brief
description: "Ask the reader which field they follow and the one question they most want answered, search the live web, then deliver a briefing in the conversation: three headlines up top, then five stories, each with what it is, the impact, and what to do about it. Trigger on 'news brief', 'what's happening in', 'catch me up on', 'brief me on the news', 'what's new in my industry', 'anything I should know about', 'weekly brief', 'industry update', or any request for current news in a named field. Do NOT use when the user hands over source material to summarize, or wants a scheduled recurring job rather than an answer now."
---

# News Brief

A briefing is not a news list. A list tells the reader what happened. A briefing
tells them what it means for them and what to do by Friday. The difference is
entirely in the third bullet, and that bullet is the reason anyone pays for this.

Two rules govern everything below:

1. **Never invent.** Every claim traces to a search result you actually read.
   No result, no item.
2. **Never pad.** Five strong stories or fewer. Four real ones beat five where
   the fifth is filler, and saying so builds more trust than hiding it.

---

## Step 1 · Ask two questions, in one call

Do not skip this and do not guess. The answers decide which searches you run and
what the action bullet says. Use `AskUserQuestion` with both questions in a
single call so the reader answers once.

**Question 1 · Field.** Header "Field". Offer four options drawn from what you
already know about the reader, and let them type their own. Good defaults when
you know nothing: AI and technology; their own industry, named if you know it;
markets and macro; policy and regulation. Be specific in the option labels.
A field like "technology" is too wide to search well; "AI infrastructure and
chips" produces a usable brief.

**Question 2 · The lens.** Header "Most want to know". This is the question they
most want answered, and it is what makes the brief theirs rather than generic.
Offer these four, phrased in their words:

- **What changed since last week** for someone who is keeping up
- **What threatens my business** for someone protecting a position
- **Where the opening is** for someone looking for a move to make
- **What I should be able to speak to** for someone with a meeting coming

Whatever they pick becomes the standing instruction for the third bullet of
every story. A reader who chose "what threatens my business" gets defensive
actions; a reader who chose "where the opening is" gets moves to make. The same
five stories produce a different brief for each.

If the session is unattended or `AskUserQuestion` is unavailable, pick the most
likely field from context, default the lens to "what changed since last week",
say both assumptions in one line at the top, and carry on.

**Window.** Default to the last seven days. Say the window in the header so the
reader knows what they are looking at. Use the last twenty four hours only if
they ask for today, and thirty days if the field moves slowly.

---

## Step 2 · Search, from at least five angles

Use `mcp__exa__web_search_exa` as the primary search tool. Fall back to
`WebSearch` if exa is unavailable, and use `mcp__exa__web_fetch_exa` or
`WebFetch` to read any story you are going to write an impact bullet about.
**Do not write an impact bullet from a search snippet alone.** A snippet is
enough to rank a story; it is not enough to say what it means.

Run the searches in parallel, in one message. One query is not a sweep. Vary
the angle, because each angle surfaces stories the others miss:

| Angle | What it catches |
|---|---|
| Plain news in the field, with the month and year in the query | The obvious top stories |
| Money: funding, acquisitions, layoffs, earnings | Who is getting stronger and weaker |
| Rules: regulation, lawsuits, policy, standards | The constraints arriving later |
| Products: launches, releases, pricing changes | What competitors can now do |
| The reader's own lens, as a literal query | The story only they would care about |

Add a sixth query for the reader's named company or competitors when you know
them.

Then filter, in this order, and expect most candidates to fail:

- **Recency.** Inside the window, with a publication date you can see. A story
  you cannot date does not go in the brief.
- **Relevance.** Does it touch something the reader is responsible for? Not
  "is it interesting". Responsible for.
- **Consequence.** Would anything be different if they knew this? An
  announcement with no downstream effect is not news, it is a press release.

**When a story is undated but too relevant to cut.** The recency filter will
sometimes reject the single most useful item in the sweep, because a company
page or a marketplace carries no publication date. Do not silently include it
and do not silently drop it. Run it, and put the weakness where the date would
go: "Undated launch, counts read [today]". One such item per brief at most, and
never in the top three, which are reserved for things you can date. A brief that
shows its soft spot is trusted further than one that hides it.

Prefer primary sources and established outlets. Where a claim is contested or
rests on a single unnamed source, say so in the item rather than laundering it
into a fact.

---

## Step 3 · Write the brief, in this format exactly

Deliver it in the conversation. Write no files unless asked.

**Emoji are structure, not decoration.** Each one is fixed and carries meaning,
so a reader learns to scan by them. Never invent new ones and never sprinkle
extras into the prose.

| Emoji | Fixed meaning |
|---|---|
| 📡 | The brief header |
| 🔎 | The lens line |
| ⚡ | The top block |
| 1️⃣ to 5️⃣ | Story rank |
| 📰 | The source line |

**The three bullets carry no emoji.** Their bold labels already name them, and a
marker in front of a label that says the same thing is noise. Emoji earn their
place where there is no label: on the header, the top block, the rank and the
source line.

Each story also takes one category emoji next to its headline, picked from this
list only: 🛠️ product or platform · 💰 money, funding or deals · ⚖️ rules,
regulation or legal · 📊 market shift or data · 🔬 research or capability.

````markdown
## 📡 [Field] · [window, e.g. 17 to 24 August 2026]

🔎 **Reading for:** [the lens they picked, in one short phrase]

### ⚡ The three that matter

1. **[[Four to six word bold claim.]](url)** [One short line of detail.]
2. **[[Bold claim.]](url)** [Detail.]
3. **[[Bold claim.]](url)** [Detail.]

---

### 1️⃣ [category emoji] **[[Headline]](url)**

- **What it is.** [The fact. Under 25 words.]
- **The impact.** [What it does to the reader. Under 30 words.]
- **Do this.** [One short sentence. Under 20 words.]

📰 *[Outlet], [date]*

### 2️⃣ [category emoji] **[[Headline]](url)**

[same shape, through 5️⃣]
````

**Every bullet is one sentence.** Two only when the first cannot stand alone.
If a bullet runs past its word cap, the sentence is carrying two ideas: cut the
weaker one rather than adding a comma. Long bullets are the most common way this
format dies.

**The headline is the link.** Every story title is a markdown link straight to
the source, and so is each bold claim in the top block. The reader clicks the
thing they are reading, never a bare URL parked at the end. The 📰 line then
carries outlet and date only, with no repeated link.

A story with no link does not run. If the only trace of it is a paywalled page
or an aggregator with no original, either find the primary source or drop the
story. Where an item genuinely has several sources, link the headline to the
best one and put the others on the 📰 line.

**Bold carries the scan.** In the top block, bold the claim and leave the detail
plain, so the three bold fragments read as a sentence on their own. In the
stories, bold the label and the headline only. Do not bold inside the prose,
because bold everywhere is bold nowhere.

**The top block is a summary, not extra stories.** The three entries are stories
1, 2 and 3 compressed, so a reader who stops there still leaves with the
important part. Rank all five by consequence first, then recency. Never promote
a story to the top three because it is the newest.

---

## The three bullets, and how each one fails

**What it is** fails by burying the news. Lead with the fact. "OpenAI cut API
prices 40 percent on Tuesday" is right; "In a move that reflects intensifying
competition across the model provider landscape, OpenAI announced" is wrong.

**The impact** fails by being generic. "This could have significant implications
for the industry" is a sentence that fits any story ever written, which means it
carries nothing. Name the mechanism and who it lands on: "Your inference costs
drop about a third if you switch, but your differentiation drops with them,
because your competitors get the same cut on the same day."

**Do this** fails by being passive. Ban these: monitor, keep an eye
on, stay tuned, watch closely, consider evaluating. They are the sound of having
no view. Every action names a thing the reader does: a number to re-run, a person
to call, a page to rewrite, a decision to bring forward, a supplier to ask. If
a story genuinely calls for no action, the honest bullet is "Nothing this week.
This matters in Q1 when the rule takes effect, so put it on the January list",
which is still a specific instruction.

---

## Quality bar, before you send

- [ ] Exactly three headlines up top, and they match stories 1 to 3
- [ ] Five stories, or fewer with a one line explanation of why
- [ ] Every story carries all three bullets, none merged, none skipped
- [ ] Every headline is a live link to its source, and every top-block claim too
- [ ] The 📰 line carries outlet and date only, with no repeated URL
- [ ] Every bullet is one sentence and inside its word cap
- [ ] Emoji are only the fixed set, none invented, none on the three bullets
- [ ] Every date falls inside the stated window
- [ ] No action bullet contains monitor, watch, keep an eye on, or stay tuned
- [ ] Each impact bullet would be wrong for a reader with a different lens.
      If it reads the same for all four lenses, it is generic, rewrite it
- [ ] No claim appears that you did not read in a source
- [ ] The whole brief reads in under two minutes

---

## Anti-patterns

- **Do not open with preamble.** No "here is your brief" and no "I searched
  several sources". The header, then the three headlines.
- **Do not pad to five.** If only three stories clear the bar, ship three and
  say the field was quiet. A padded brief teaches the reader to skim, and once
  they skim they never come back to reading.
- **Do not write a topic where a headline belongs.** "AI regulation update" is
  a folder name. "EU delays the AI Act's high risk provisions to 2028" is a
  headline.
- **Do not repeat the same story twice** because two outlets covered it. Merge
  them and cite the better source.
- **Do not let a single vendor's blog become three stories.** One company, one
  slot, unless two genuinely separate things happened.
- **Do not smuggle opinion into the What it is bullet.** Opinion belongs in
  impact, where the reader can see it is yours.

---

## When the reader comes back

If they ask for a brief again in the same field, open by saying what changed
since the last one and drop any story you already gave them. The value of the
second brief is entirely in the diff. Keep the field and lens they picked last
time rather than asking again, and confirm in one line that you are reusing
them.
