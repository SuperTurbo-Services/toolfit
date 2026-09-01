# NOTICE

## Author

**This skill is not SuperTurbo's work. It was written by Ralph Oei.**

- **Author:** Ralph Oei
- **Source:** https://github.com/ralph-oei/sop-from-recording
- **Licence:** MIT, Copyright (c) 2026 Ralph Oei
- **Commit copied:** `0a5393605f0f30aea4a652da9d5f23677e9b7673`
- **Copied:** 26 Aug 2026
- **Role and tier:** Operations, ADDITIONAL

Any copy that leaves this folder, in any form, must carry `LICENSE` with it. The MIT text says so
in terms: "The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software." Removing the author's name is not an option, and it is
not made acceptable by rewriting the prose around it.

## This copy is UNMODIFIED

Six files, fetched byte for byte from the pinned commit above:

```
SKILL.md
README.md
LICENSE
references/sop-template.md
references/gap-checklist.md
references/worked-example.md
```

**Nothing has been edited.** This is not a derivative work and must not be presented as one.
If SuperTurbo later builds a version with a vertical gap checklist layered on top, that is a
separate folder, a separate name, and a NOTICE that states plainly what was taken and what was
added. Do not edit these files in place.

**Not copied:** the upstream `evaluations/` directory, which holds four JSON test cases, a
RESULTS.md and fixtures. Those are the author's development artifacts and are not needed to run
the skill. They remain at the source if a regression check is ever wanted.

## Rights position, against the four mode model

See [[superturbo_skill_listing_rights]] for the model.

| Mode | Status under MIT | Note |
|---|---|---|
| **R** Run during an engagement | Clear | No conditions beyond keeping LICENSE with the files |
| **L** Link plus tutorial, client installs from the author's source | Clear | **The house default, and the recommended mode for this skill** |
| **H** Host on superturbo.com, redistribution | Permitted, with LICENSE and the copyright notice attached | See the flag below |
| **D** Modify and rebrand | Permitted, with LICENSE and the copyright notice attached, and the change stated | Not exercised here |

**FLAG, read before this is listed anywhere.** The house default is L: the client installs from
the author's repo and pays for the tutorial, which is not distribution. This folder holds a
verbatim copy, which is closer to H. MIT permits it. But it makes `Official/` hold third party IP
for the first time, and everything else in `Official/` so far is SuperTurbo's own or an internal
tool. Decide deliberately whether the landing page **links** this skill or **hosts** it, because
the two carry different obligations and a different story to the client.

The honest framing to a client either way: SuperTurbo did not write this, tested it, judged it
worth installing, and teaches the workflow around it. That is the position in
[[superturbo_positioning]], and it survives being asked "did you build this?" A copy in a folder
implying authorship does not.

## Why it is ADDITIONAL and not NECESSARY

By Screen B, the recurrence test in [[superturbo_skill_listing_rights]]: can a re run produce a
diff rather than a repeat? No. A process is recorded and documented once, then the SOP is
maintained by hand. That is episodic, so ADDITIONAL. Move it to NECESSARY only if a client is
found who genuinely re records processes on a cycle.

## Verification done on copy, 26 Aug 2026

- Fetched from a pinned commit SHA, not from `main`, so this copy is reproducible
- `LICENSE` present and carries the copyright line
- Swept all six files for email addresses: **none found.** This is the Gate 6 check that has
  caught an upstream author's live contact address before. It is clean here
- Files not opened for editing at any point

## What SuperTurbo would add, if it ever builds its own version

The method and the 11 gap categories are the author's and are already strong. The gap this leaves
is vertical: the checklist does not know to go looking for the questions that recur in insurance,
title and accounting workflows. It waits to trip over them. A SuperTurbo version would layer a
per vertical gap checklist on top of the 11 general categories. **Price the vertical layer, never
the method.**
