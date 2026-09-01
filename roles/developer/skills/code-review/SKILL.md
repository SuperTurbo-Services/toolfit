---
name: code-review
description: "Rigorous engineering discipline for code work. Forces a plan, matches the task to a playbook, applies 21 engineering principles, and refuses to declare done without runtime evidence. Use for reviewing a diff before merge, and for any non-trivial feature, bug fix, refactor, performance work, investigation, or multi-step code change. Not for one-line edits or pure questions."
---

# Code Review

Write less code, better. This is a discipline layer, not a code generator. Its job is to
stop an agent shipping plausible work it has not verified.

**Engineering content by Lauren Tan (`pstack`), MIT. Claude Code and Codex port by Eric
Litman (`open-pstack`), MIT. Packaged as a single skill and adjusted by Turbo Guo,
SuperTurbo. See NOTICE.md. SuperTurbo did not write the engineering content.**

## Non-negotiables

**Start every multi-step task with a todo list whose first item is to read
`references/principles.md` in full.** Then name, in your reply, the principles that
shaped a decision and what each one changed. A principle cited with no decision behind
it means you skipped it.

Triggers, in order of how often they fire:

- Any code. Name the data shape first, and choose its organising structure.
- Code crossing a function boundary. Read `references/skills/architect.md` and explore
  two or three designs before implementing.
- Nontrivial change or "are we sure?". Read `references/skills/how.md`. For motivation
  questions also read `references/skills/why.md`.
- About to ask the user "which approach". Classify it first. If the answer is a fact you
  could observe by running something, it is not the user's to answer. Sketch it with the
  Prototype playbook and let the result decide. Reserve the question for a genuine
  preference call no experiment can settle.
- Parallel fan-out. `references/skills/swarm.md` for coverage and exploration.
  `references/skills/arena.md` for design bakeoffs with grafting.
- Contested design. `references/skills/interrogate.md` before shipping.
- Any prose you write, including your own reply. `references/skills/unslop.md`.
- Docs, READMEs, PR descriptions, commit messages.
  `references/skills/technical-writing.md`.
- Before review. `references/skills/no-comments.md`.
- A change you do not trust. `references/skills/blast-radius.md`.

## Playbooks

**Match the task to a playbook, open its file, and copy its steps into your todo list
verbatim, before any task-specific todos and before you reason about the task.**

The failure mode is reading a playbook and then writing a bespoke plan that quietly drops
its named steps. A step you choose not to do stays in the list with a one-line
`skip: <reason>`. Skipping silently is not allowed.

| Task | Playbook |
|---|---|
| Read-only question. How does X work, why was Y built this way, are we sure about Z | `references/playbooks/investigation.md` |
| A reported defect to reproduce, root-cause and fix with runtime evidence | `references/playbooks/bug-fix.md` |
| New or changed behaviour, built from a named data shape | `references/playbooks/feature.md` |
| A behaviour-preserving change to structure or shape | `references/playbooks/refactoring.md` |
| A measured slowness to trace and improve against a baseline | `references/playbooks/perf-issue.md` |
| Sustained improvement of one metric against a target, with a decision log | `references/playbooks/hillclimb.md` |
| A live runtime symptom to diagnose from instrumentation | `references/playbooks/runtime-forensics.md` |
| A captured profiling artifact handed to you after the fact | `references/playbooks/trace-forensics.md` |
| A throwaway sketch to settle a design or empirical fork cheaply | `references/playbooks/prototype.md` |
| Writing or editing a SKILL.md | `references/playbooks/authoring-a-skill.md` |
| Testing whether a skill or prompt change actually changes behaviour | `references/playbooks/eval.md` |
| Resuming or taking over a prior agent's in-flight work | `references/playbooks/session-pickup.md` |
| Suspending work cleanly so it can be resumed | `references/playbooks/pause-safely.md` |
| Reclaiming disk from merged or abandoned worktrees | `references/playbooks/worktree-cleanup.md` |

When no playbook fits, read `references/skills/figure-it-out.md` and design one.

## Subagents

Upstream ships named agent definitions at the plugin level. A skill cannot. So where a
playbook or reference calls for a named agent, spawn a general-purpose subagent and pass
it the matching role prompt as its instructions:

| Upstream agent | Use instead |
|---|---|
| `comment-sicko` | `references/agents/comment-sicko.md` |
| `poteto-agent` | `references/agents/poteto-agent.md` |

Route bulk reading to subagents and keep only summaries in the main thread. Give every
writing subagent its own worktree or output directory so two never write the same file.

## Models

Upstream routes work to different vendors by strength. This version does not, because it
cannot assume you have more than one. Where a reference names a model, read it as a role:
your strongest reasoning model for bugs and performance, your fastest capable model for
mechanical work, your strongest judgment model for prose and design calls. One model for
all three is fine and is the default.

## Writing the reply

Write it clean as you draft. The cleanup-afterwards pass has been measured to fail, so do
not generate the bad sentence in the first place.

- Short declarative sentences. One thought per sentence.
- **The long-dash character is banned outright.** A bullet joining a filename to its
  description with a dash becomes a sentence. A bold header joined to its text by a dash
  becomes its own sentence.
- A colon as a mid-sentence connector is out. A colon before a list is fine.
- Terse is not an excuse to drop content. Every item the playbook's reply names stays.
- Frame impact for the consumer and for the maintainer. Say what an end user notices, and
  what the next engineer who owns this code inherits. If you cannot say either, the work
  or the explanation is off.
- Never fabricate a link, citation or transcript reference. Cite only artifacts you
  produced or read this session.

## What this version does not do

Stated plainly so nobody discovers it mid-task.

- **It does not fire on its own.** Upstream ships a session-start hook that injects the
  mandate automatically. Hooks are plugin-level and a skill cannot register one. Invoke
  this skill by name, or add one line to your CLAUDE.md or AGENTS.md telling the agent to
  read it before non-trivial code work.
- **No multi-vendor model routing.** See Models above.
- **Eight autonomous playbooks were removed**, not ported. Upstream's `autonomous-run`,
  `autopilot-full`, `autopilot-stack`, `shipping`, `babysit`, `multi-phase-plan`,
  `opening-a-pr` and `visual-parity` depend on Cursor's `/loop` and on a Graphite
  stacked-PR workflow. They also drive work to merged without stopping, which is not
  something to point at a client repository. Use upstream in Cursor if you want them.
- **No bundled tooling.** Upstream ships Bun and TypeScript scripts. Those are a plugin's
  to carry, not a skill's.
