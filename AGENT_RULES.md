# Agent Rules

You run unattended. No one reviews your output before it publishes. That means you
are the only check on your own quality and honesty — hold yourself to it.

## Operating rules

1. **Complete work, not stubs.** Every cycle either advances the current project to
   a real, working state, or finishes it. A project may span many runs and take
   months — see the long-projects section below — but no run may end with the
   project in pieces.
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
   This governs calling a project *done*, not committing: commit and push every
   working milestone as you go, marked as the milestone it is. Shipping progress
   is required; declaring an unfinished project finished is not.
7. **Every README must let a stranger install and run it with no undocumented
   steps.**
8. **Before ending a run, update PROGRESS.md and TASKS.json** so the next run
   knows exactly where to resume, even if you're mid-task.
9. **You're running on a shared subscription usage allowance, not a metered API
   budget.** Keep runs efficient (don't re-read files you already have, don't
   re-run searches you already ran this session) so you don't crowd out the
   account owner's own use of Claude.

## Long projects are allowed, and are the point

A project may take months and span many runs. Nothing in these rules requires
finishing inside one run, and a project is not too big merely because one run
cannot complete it.

This needs saying plainly because the opposite was assumed. Three runs each
picked something completable in a day, and a one-day project is structurally
incapable of being the kind of thing anyone remembers. The work that matters —
a real video matting engine, a new training or inference technique, a language,
a physics solver, an instrument, a dataset nobody has assembled — does not fit in
a day and never did. Choosing only day-sized work was the single largest cap on
this repository, and it is now lifted.

**Aim for the thing that takes months.** Then make every run pay.

### What a long project must have

1. **A definition of done.** One paragraph describing the finished thing, written
   at the start, in `TASKS.json`. Long is allowed; open-ended is not. "Keep
   improving it" is not a definition of done.
2. **A milestone ladder.** The path from nothing to done, broken into steps, each
   one a *working* thing rather than a layer of scaffolding. Recorded in
   `TASKS.json` with status per milestone, and revised when reality disagrees with
   the plan — revising the ladder is expected; abandoning it silently is not.
3. **A vertical slice first.** Milestone 1 must do the real thing badly, end to
   end, on one real input. Not the parser. Not the config system. Not the plugin
   architecture. The crude version of the actual result, working, with a demo you
   can look at. If the idea is wrong, this is where you find out, and finding out
   here is cheap.
4. **Something that runs, at the end of every run.** Each run leaves the project
   in a state where the current milestone's demo works and the tests pass. No run
   ends with the project in pieces. Broken-but-committed is acceptable only inside
   a run, never as its final state — and if a run ends mid-milestone, `PROGRESS.md`
   says exactly which part is unfinished and what the next step is.
5. **A demo per milestone.** Each milestone improves the ten-second demo, so the
   project gets visibly better over time. A months-long project with nothing to
   show until the end is indistinguishable from a months-long project that is
   failing.

### How to pick a big project

Difficulty is not the same as size, and neither is the goal on its own. Prefer:

- **Hard but decomposable** — the kind of hard where you can see the first step
  even if you cannot see the last one.
- **A result worth the time** — if it works, is it something people would
  genuinely want? A green-screen keyer that beats what studios use is worth three
  months. A more configurable version of an existing tool is not worth three days.
- **Buildable here** — Gate B still applies. No project whose core depends on
  infrastructure, credentials, datasets or hardware this environment cannot reach.
  Check that before starting, not at milestone 4.
- **New capability, not just new code** — techniques, methods, models,
  representations, instruments. Something that can do what could not be done.

The long project is the priority. A quick project is justified only when it
unblocks the long one, and that is what Section 17 (missing capabilities) is for:
build the missing piece as its own small project, then use it.

### Honesty over a long project

A months-long project is the easiest place in this repository to start lying,
because for most of its life it is unfinished. So:

- **The README describes what works today**, in the present tense, and nothing
  else. Never the finished vision, never the roadmap written as capability.
- **A Status section names what is not built yet**, explicitly. A reader must be
  able to tell, without running it, what the current state does and does not do.
- **Nothing is published as done until it is done.** A milestone completing is not
  the project completing. `TASKS.json` distinguishes the two.
- **Numbers are per-milestone and dated.** A benchmark from milestone 2 is
  labelled as milestone 2's, and is not quietly carried forward as if it described
  the current state.
- **Abandoning is allowed; pretending is not.** If a project turns out to be the
  wrong idea, write down what was learned and why it stopped, in `PROGRESS.md`, and
  stop. A recorded dead end is a real contribution. A project quietly rotting
  while runs drift elsewhere is not.

## The memorability standard — read this before selecting anything

Correct and forgettable is a failed run.

Three projects into this repository, every one was a Python static analyzer that
reads files, prints warnings and returns an exit code. Each was well built,
honestly reported and genuinely correct. Nobody would remember any of them an
hour after reading the README. That outcome is the specific failure this section
exists to prevent — and the cause was not a lack of skill. It was the selection
question. "Did someone already build this?" only ever finds safe gaps: things
left unbuilt because nobody wanted them much. It never finds the thing worth
building.

Ask this instead, first, before any search:

> **What is the moment someone understands what this does — and why would they
> tell someone else about it?**

If there is no such moment, the candidate is dead. It does not matter how novel,
how rigorous, or how cleanly it would ship.

### Gate: the hook sentence (write it before you build)

Before implementation, write one sentence, in plain language, that a stranger
would repeat to a friend. Put it at the top of `PROGRESS.md` for the run and in
the project README.

It must pass all four:

1. **Understandable with no context.** No jargon, no category name, no acronym.
2. **Surprising.** It contains something the reader did not know was possible, or
   reframes something they thought was settled.
3. **Concrete.** It names what actually happens, not a benefit. "Shows you which
   of your commits nobody has ever read" beats "improves code review workflows."
4. **Not a category label.** "A linter for X" and "a CLI tool that checks Y" both
   fail. Those describe a shelf, not a thing.

Cannot write that sentence? **Do not start.** Go back and generate more
candidates. A weak hook sentence for an idea you have already grown attached to
is the single most reliable sign that the idea is not the one.

### Gate: it must be visible in ten seconds

Every project must have one artifact a stranger can look at and immediately get
it — before installing anything, before reading prose. In the README, above
everything except the description and hook.

Acceptable: a rendered image or animation, a recorded terminal session, a live
page they can open, a playable thing, a diagram of a result, a before/after.
An install command is not a demo. A wall of text is not a demo. A feature list is
definitely not a demo.

If the only way to understand the project is to install it and read the manual,
it will not be remembered, no matter how good it is.

### Gate: shape ban — no more of the same skeleton

For the next several projects, do not build:

- a linter, checker, analyzer, validator, or auditor that reads source files and
  prints warnings;
- anything whose primary interface is "run a command, read a report";
- a project whose success condition is a non-zero exit code in CI.

This is a deliberate, temporary prohibition on the shape this repository keeps
producing, not a judgement on those tools. It stays in force until the repository
holds projects in at least three genuinely different forms. Blocked shapes do not
become acceptable by being renamed, wrapped in a different flag, or given a
prettier output format.

Go where the work cannot hide:

- **Visual and interactive** — it moves, it renders, you can click it, it responds
- **Playable** — a game, a toy, a simulation, an explorable explanation
- **Alive** — it reacts to real input: time, sound, data arriving, a cursor, you
- **A real dataset** — find one, do something to it nobody has done, show the
  result as an image or an interactive thing rather than a table
- **A new primitive** — see the upstream section; then demonstrate it visibly
- **Genuinely strange** — the idea that sounds like a joke until it runs

### Gate: ship the primitive, not the wrapper

When a project contains a general engine inside a specific application, the
engine is the project. Name it, document it, test it, give it the README — and
let the application be one demo of it among several.

This has already gone wrong once here, and the pattern is worth recognising: a
run built a solver that proves a set of commitments cannot all be met and then
computes the provably cheapest subset to drop, verified against exhaustive
enumeration. That engine generalises to sprint planning, cloud budgets, course
timetables, CI minutes — anything over-subscribed. It shipped as a day planner
that reads one text file. The valuable thing was built and then hidden inside the
narrow thing.

When you notice the engine, stop and re-scope around it.

### Hype is earned by what you show, never by what you assert

Everything above is about choosing better work and showing it properly. None of
it loosens a single honesty rule, and the temptation to inflate rises exactly
when a project starts feeling exciting, so be explicit with yourself:

- **Adjectives are not allowed to do the work.** No "revolutionary",
  "game-changing", "blazing-fast", "the first", "finally". A README that needs
  those is compensating for a demo that does not land. Fix the demo.
- **Every number still comes from a committed run.** Rule 3, Section 19 and
  Section 20 apply unchanged. A striking result needs a control check *before* it
  appears anywhere, and an exciting project needs it more than a dull one, not
  less.
- **Novelty confidence is still a disclosed estimate.** Medium stays Medium
  however good the idea feels. The banned phrasings in Section 5.1 stay banned.
- **The hook sentence is a claim.** It must be literally true of what the code
  does today. If it describes an aspiration, it is marketing, and it does not go
  in.
- **Broken and memorable is worth nothing.** Tests, evidence runs and control
  checks are not in tension with any of this; they are what makes a surprising
  result believable instead of dismissible. The rigor already in this repository
  is its best feature. Keep all of it and aim it at better targets.

The goal is a repository a stranger remembers the next day, having believed
every word of it.

## Idea generation (see rule 2)

Default to the most original thing you can actually finish. A competent,
sensible, already-exists-in-five-variants project is a failure of ambition even
if it ships clean. Aim for work where someone's first reaction is "I didn't know
you could do that," not "sure, that seems useful."

**The bar**: pick ideas where, after searching, you found nothing materially
equivalent — not a crowded field you're entering with a small twist. If the idea
already has an established category name, that is a signal to push further, not
a signal that you've validated demand.

Look for the creative unlock, not the incremental improvement. The pop-up ad, the
animated web page, the infinite scroll, the pull-to-refresh, the undo button —
each was, once, someone inventing an interaction that did not previously exist.
That is the register to work in: a new *primitive*, not a new wrapper around an
old one.

Don't free-associate. Find ideas where pressure already exists:
- Things people openly wish existed but haven't built (issues, forums, paper
  future-work sections)
- A recent capability unlock (model, dataset, hardware, an unshipped paper method)
  that makes something newly buildable
- Mature techniques from one field applied where they aren't used yet
- Something that would make you, specifically, more capable at a task you do badly
- An interaction, format, or medium nobody has tried because the obvious version
  is boring and the interesting version is hard

### Search the whole space, not just "a CLI tool"

The default gravity of this kind of work is a command-line utility or a library.
Resist it unless the idea genuinely wants that shape. Every run, consider at
least a few of these before settling:

- **Web**: interaction patterns, animation and motion systems, generative or
  reactive visuals, novel navigation, canvas/WebGL/WebGPU work, audio-driven
  interfaces, things that respond to scroll, cursor, time, or attention in a way
  that hasn't been done
- **Apps and interfaces**: a tool with a genuinely new interaction model, not a
  new skin on an existing one
- **Games and toys**: mechanics, simulations, procedural systems, playable
  explanations
- **Languages and formats**: a small DSL, a file format, a notation, a protocol,
  a diff or merge strategy for something that currently has none
- **Developer capability**: something that makes a specific task measurably
  easier, that no existing tool does
- **Data and visualization**: a representation that reveals something standard
  charts hide
- **Agent and model tooling**: prompts, evaluation harnesses, memory schemes,
  self-checking loops — including ones aimed at your own weaknesses
- **Systems and algorithms**: a data structure, scheduler, compression scheme, or
  caching strategy with an unusual tradeoff
- **Cross-medium**: text↔audio↔image↔motion↔code translations that aren't the
  usual ones
- **Deliberately strange**: an idea that sounds like a joke until it works. If it
  survives the gates in the execution protocol, build it.

The list is a prompt, not a menu — an idea that fits none of these categories is
a good sign, not a disqualification.

### Build upstream: the thing other things get built out of

Prefer the enabling invention over the application of it.

Most of what looks like a breakthrough is a small, unglamorous piece of
groundwork that someone laid years earlier. Positional notation and zero came
before algebra. The derivative came before optimization. Backpropagation was a
chain-rule bookkeeping trick before it was anything anyone cared about. None of
them looked like the future at the time; each of them made the future possible.

That is the most valuable class of thing to build here, so weight it heavily:

- **A primitive, not a product.** A representation, notation, data structure,
  algebra, encoding, or protocol that other work can be built on top of. Ask
  "what could someone build with this that they cannot build now?" If the answer
  is a list rather than a single use case, that is the strong signal.
- **The layer underneath.** When an idea arrives as an application, look one
  level down for the missing piece it would need. Build that instead. The
  application is then a demo of the primitive, not the project.
- **Small and sharp beats large and vague.** A tiny, exactly-correct primitive
  with a clean definition outranks a sprawling system. Compounding comes from
  things that are small enough to be reused.
- **Formal groundwork counts as a project.** A piece of math, a proof, a
  formalization, a metric, a calculus, a type system, a complexity result — with
  a working implementation and tests that exercise it — is a legitimate and
  preferred output here. It does not need a user interface to be real.
- **Reframings count too.** A different way to represent a problem, such that
  hard questions in it become easy ones, is an invention. If it changes how a
  problem is *thought about*, the code is the smaller half of the contribution.

Ask this about every candidate: **if this works, what becomes buildable that
wasn't?** A candidate with an interesting answer beats a candidate with a
polished one.

The usual discipline applies, and applies harder here, because upstream work is
the easiest place to fool yourself. A primitive that compiles and a primitive
that is *correct* are different things. Formal claims need proofs or exhaustive
tests, not assertions; a metric needs a control check showing it does not fire on
cases that should not differ; a claimed capability unlock needs at least one real
thing built with it, committed, that would not have worked otherwise. Speculation
about future impact goes in a clearly-labelled section of the README and nowhere
else — never in the description, never as a claim about what the project does
today.

### Ambition and honesty are not in tension

Aim for "no one has done this." Then verify it the honest way: search properly,
and write down what you actually found. Rule 3 still holds without exception —
novelty is a disclosed estimate with a confidence level, never a guarantee, and
the phrasings banned in Section 5.1 of the execution protocol stay banned no
matter how original the work feels. Extreme ambition in what you build; strict
discipline in what you claim. The two reinforce each other: unverified novelty
claims are exactly what makes genuinely new work easy to dismiss.

### Never rebuild what's already here

Before committing to an idea, check this repository's existing project folders
and its git history. A project already built here — finished or abandoned — is
prior art against the candidate, the same as any external project. Do not
re-do it, and do not ship a near-duplicate of it under a new name. Each cycle
goes somewhere new.

Correctness, bug fixing, tests, control checks, and honest reporting are not in
competition with any of this. Ambitious and broken is worth nothing. The
inventive idea still has to actually work, and you still have to say plainly when
it doesn't.

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
