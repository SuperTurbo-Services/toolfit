# NOTICE — code-review

## Authorship, three parties

| Role | Who | What they made | Licence |
|---|---|---|---|
| **Original author** | **Lauren Tan** (x.com/poteto). React core team, React Compiler. Previously Meta and Netflix, currently Cursor | The engineering content. The 21 principles, the playbooks, the workflows, the sub-skill bodies, the subagent prompts. **All of it.** | MIT, (c) 2026 Lauren Tan |
| **Port** | **Eric Litman** (`ericlitman/open-pstack`) | Translated pstack from Cursor to Claude Code and Codex. The base this skill was derived from | MIT |
| **This packaging** | **Turbo Guo, SuperTurbo** | Collapsed a 52-skill plugin into one skill. Wrote `SKILL.md` as the dispatcher. Substituted vendor model names for roles. Replaced plugin-level agents with reference prompts. Selected what to keep and what to cut | MIT, inherited |

**SuperTurbo did not write the engineering content.** We tested it, judged it worth
installing, cut the parts that only run in Cursor, and packaged what is left so it fits a
plugin bundle without a hook or an agent tree.

## Renamed 27 August 2026

Turbo renamed this from `code-assistant` to `code-review`. **Two cautions were raised at
the time and are recorded here rather than lost.**

1. **`/code-review` may collide with Claude Code's built-in `/review`.** A separate
   skills project, `raddue/crucible`, documents renaming its own `/code-review` to
   `temper` specifically "to avoid collision with Claude Code's built-in `/review`". Test
   the invocation before this is listed.
2. **The name is narrower than the skill.** Reviewing a diff is one of 14 playbooks. The
   other 13 are bug fix, feature, refactoring, performance, hillclimb, runtime forensics,
   trace forensics, prototype, investigation, eval, authoring a skill, session pickup and
   pause safely. A buyer reading "code review" will not expect a bug reproduction
   workflow. The `description` frontmatter was widened to compensate; the folder name was
   not, on Turbo's instruction.

## Listing name

**Code Review**, engineering content by Lauren Tan.

The copyright is **Lauren Tan personally, not Cursor Inc**, even though upstream lives in
the `cursor/plugins` org monorepo. If the listing mentions Cursor, it must read as "by a
developer who works at Cursor". **Never shorten it to "from Cursor"** and never place it
beside Cursor branding. MIT conveys copyright permission only and grants no trademark or
endorsement rights.

## Provenance

| Field | Value |
|---|---|
| Original | https://github.com/cursor/plugins/tree/main/pstack, (c) 2026 Lauren Tan, MIT |
| Port used as the base | https://github.com/ericlitman/open-pstack, MIT |
| Base commit | `27e0ce32be3dfc496d1372a4f3d45d91d15007da` |
| Date derived | 27 August 2026 |
| Role / Tier | Developer / NECESSARY |
| Folder | `code-review` (renamed from `code-assistant`, 27 Aug 2026) |
| Licence | MIT. `LICENSE` ships alongside and must travel in every copy |

**THIS IS A DERIVATIVE WORK, NOT A VERBATIM COPY.** The unmodified upstream copy lives at
`Official/Developer/_reference/pstack/`, outside both sellable tiers, and must never be
edited. It is the evidence that proves what was taken and what changed. This folder is the
separate name and separate folder that a derivative requires.

## What was taken, unmodified

- **The 21 principles.** Bodies verbatim in `references/principles.md`. Only the heading
  level was normalised so 21 files read as one document, and each principle's own
  `description` was appended as a "When it applies" line.
- **9 playbooks, byte for byte.** authoring-a-skill, eval, investigation, pause-safely,
  prototype, runtime-forensics, session-pickup, trace-forensics, worktree-cleanup.
- **19 sub-skill bodies**, byte for byte, in `references/skills/`.
- **2 subagent role prompts**, byte for byte, in `references/agents/`.

## What was changed

- **5 playbooks had vendor model names replaced with roles.** bug-fix, feature, hillclimb,
  perf-issue, refactoring. `GPT-5.6 Sol max` became "your strongest reasoning model",
  `Grok 4.6 xhigh` became "your fastest capable model", `Fable 5 max` became "your
  strongest judgment model". Nothing else in those files moved.
- **`SKILL.md` is newly authored by SuperTurbo.** It is the dispatcher: the trigger list,
  the playbook table, the subagent substitution, the reply rules and the honest list of
  what was dropped. Structure follows upstream's `poteto-mode/SKILL.md`; the file is not
  a copy of it.
- **Named agents became role prompts.** Upstream calls `subagent_type: "comment-sicko"`.
  Agent definitions are plugin-level and a skill cannot ship them, so the skill now
  instructs the agent to spawn a general-purpose subagent with the prompt file instead.

## What was deliberately not carried

- **The session-start hook.** Plugin-level, impossible in a skill. **This is the real
  functional loss.** Upstream fires automatically; this must be invoked, or named in a
  CLAUDE.md or AGENTS.md.
- **8 autonomous playbooks.** autonomous-run, autopilot-full, autopilot-stack, shipping,
  babysit, multi-phase-plan, opening-a-pr, visual-parity. All depend on Cursor's `/loop`
  or a Graphite stacked-PR workflow. They also drive work to merged without stopping,
  which must never point at a client repository.
- **`orchestrate.md`**, 17,948 chars. Program-scale, multi-day, fleets of subagents.
  Correct for its author, wrong for the buyer this catalog serves.
- **The 7 `cursor-team-kit` skills** that open-pstack imports (deslop, fix-ci,
  fix-merge-conflicts, get-pr-comments, make-pr-easy-to-review,
  thermo-nuclear-code-quality-review, what-did-i-get-done). Excluded on purpose so this
  folder carries **one** copyright and one LICENSE rather than three. They are (c) 2026
  Cursor, MIT, and can be added later if the second notice is added with them.
- **The Bun and TypeScript tooling** under `poteto-mode/scripts/`.

## Rights, four modes

| Mode | Allowed | Note |
|---|---|---|
| **R** Run in an engagement | YES | MIT |
| **L** Link + tutorial | YES | Point at upstream, not at this folder |
| **H** Host on superturbo.com | YES | `LICENSE` and this NOTICE must travel |
| **D** Modify further | YES | A further derivative gets its own folder and notice again |

## Why this exists

Upstream is a plugin: 52 skills, 12 agents, 4 hooks, two manifests. The SuperTurbo
delivery pipeline builds **one** plugin per customer from chosen skill folders, and a
second plugin cannot nest inside it. Merging upstream in would have cost 13 hardcoded
`pstack:` namespace edits, a session-start hook firing for every buyer in the bundle
including ones who never chose it, and roughly 3,194 always-on tokens on every order.

As one skill the always-on cost is a single name and description. The 195 KB of
references load only when the skill activates.

## Verification, 27 August 2026

- `LICENSE` read directly from the base repo. MIT, (c) 2026 Lauren Tan.
- Gate 6 PII sweep run on the derived files. Result recorded below this line at build time.
