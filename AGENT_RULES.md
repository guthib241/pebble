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
5. **You may create repos, branches, PRs, releases inside this org**, via `gh`,
   using $GH_TOKEN. Never touch anything outside this org.
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
- **Description** (the one-line GitHub repo description, shown under the
  name): one sentence, under ~12 words, states what it does with no throat-
  clearing. No "A tool that helps you to..." — just what it does. Example:
  "Diffs two API schemas and flags breaking changes."
- **README tone**: professional, not cute. Cute belongs in the name if
  anywhere; the README is where a stranger decides whether to trust and use
  this. Clear structure, no filler, no hype adjectives.
- **License**: choose deliberately, state the choice and why in the README,
  don't default silently.
  - MIT or Apache-2.0 for something meant to spread and be reused freely
    (Apache-2.0 if patent grant language matters for the domain)
  - AGPL-3.0 if the project is the kind of thing someone could wrap as a
    hosted service without contributing back, and you want to prevent that
  - Note in NOVELTY_REPORT.md or the README which one was picked and why in
    one sentence — not a legal essay, just the reasoning

## Before publishing anything

- No invented numbers. Every figure comes from a run you actually committed.
- Any comparative claim needs a control check first (two things that shouldn't
  differ, confirmed to show no difference) before it appears anywhere public.
- State the closest prior work and what's different, near the top of the README.
  Never bury it.
