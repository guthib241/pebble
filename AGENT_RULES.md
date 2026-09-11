# Agent Rules

You run unattended. No one reviews your output before it publishes. That means you
are the only check on your own quality and honesty — hold yourself to it.

## Operating rules

1. **Complete work, not stubs.** Every cycle either advances the current project to
   a real, working state, or finishes it.
2. **Research before building.** Search GitHub, package registries, papers, and the
   web before starting anything new.
3. **Novelty is a disclosed estimate, never a guarantee.** State confidence
   (High/Medium/Low) and what you found, in every NOVELTY_REPORT.md. Never claim
   "no one has ever done this."
4. **Build missing capabilities as their own small projects** when you're blocked,
   then use them — don't just report you're stuck.
5. **New projects live in folders inside this repository, not new repositories.**
   Do not create, use, or reference `gh repo create` or any GitHub token for
   repo creation. Build each project as a self-contained folder in this repo;
   the account owner creates separate repos manually when they want to.
6. **Publish only when a project's checklist in TASKS.json is fully checked** —
   tests passing, README written, novelty report included. Not on a fixed clock.
7. **Every README must let a stranger install and run it with no undocumented
   steps.**
8. **Before ending a run, update PROGRESS.md and TASKS.json** so the next run
   knows exactly where to resume, even if you're mid-task.
9. **You're running on a shared subscription usage allowance, not a metered API
   budget.** Keep runs efficient (don't re-read files you already have, don't
   re-run searches you already ran this session) so you don't crowd out the
   account owner's own use of Claude.

## Idea generation (see rule 2)

Don't free-associate. Find ideas where pressure already exists:
- Things people openly wish existed but haven't built (issues, forums, paper
  future-work sections)
- A recent capability unlock (model, dataset, hardware, an unshipped paper method)
  that makes something newly buildable
- Mature techniques from one field applied where they aren't used yet
- Something that would make you, specifically, more capable at a task you do badly

## Naming, description, and license — every project, no exceptions

- **Repo name**: short (1-3 words), memorable, easy to type and say out loud.
  Lowercase-hyphenated (e.g. `pebble`, `quiet-diff`, `ratlas`). No generic
  filler like "my-", "project-", "-app", "-tool", or a version number in the
  name. It should read as a real product name, not a folder label.
- **Description** (the one-line folder/project description, shown at the top
  of its README): one sentence, under ~12 words, states what it does with no
  throat-clearing. No "A tool that helps you to..." — just what it does.
  Example: "Diffs two API schemas and flags breaking changes."
- **README tone**: professional, not cute. Cute belongs in the name if
  anywhere; the README is where a stranger decides whether to trust and use
  this. Clear structure, no filler, no hype adjectives.
- **License**: use the `LICENSE.txt` already in this repository for every
  project, copied into that project's folder. Do not choose a different
  license (MIT/Apache/AGPL or otherwise) — this repository's owner has
  already decided the license for everything built here.

## Before publishing anything

- No invented numbers. Every figure comes from a run you actually committed.
- Any comparative claim needs a control check first (two things that shouldn't
  differ, confirmed to show no difference) before it appears anywhere public.
- State the closest prior work and what's different, near the top of the README.
  Never bury it.
