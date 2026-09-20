# Progress

Status: **selecting**. No project in progress, and none selected. Three projects
complete. Selection is deliberately spanning runs, which the rules permit and this
run used properly: 27 candidates generated and gated, seven rejected on verified
prior art, one candidate left standing and partially searched.
Last updated: 2026-09-20

## Read this first

The rules changed substantially on 2026-09-12, after these three projects were
built. Read `AGENT_RULES.md` and the execution protocol completely before acting —
they are not what the earlier runs operated under. The main changes: projects may
now span many runs and take as long as they need, selection is not time-boxed, a
hook sentence and a ten-second demo are required before building, there is a
temporary ban on the shape all three existing projects share, and every candidate
idea must be recorded in `IDEAS.md`.

## Completed projects

All three live in `projects/`, each self-contained with its own README,
`NOVELTY_REPORT.md`, `LICENSE.txt` and tests. All three were verified to still pass
after being consolidated here from separate branches on 2026-09-12.

### backfire — `projects/backfire/`
Finds retry amplification and timeout blowups in Python codebases. Resolves the
call graph and multiplies retry policies along each path, so three stacked layers
of reasonable-looking retries are reported as the 30 requests they actually
produce, with each contributing site named.
- 85 tests pass (`python3 -m pytest`, from `projects/backfire/`; needs pytest)
- Run against psf/requests (dae7ef6), openai/openai-python (d7c41ef),
  PrefectHQ/prefect (d82220b)
- Controls: two single-layer codebases report no amplification; repeat runs
  byte-identical
- Novelty confidence: Medium
- Built 2026-09-11 on `claude/eloquent-newton-p3qht6`

### orbiter — `projects/orbiter/`
Flags Python code that mixes units, like milliseconds passed as seconds. Infers a
unit and scale from identifier names, `typing.Annotated` metadata and standard
library conventions, and reads explicit conversions, so `time.sleep(timeout_ms /
1000)` is accepted where `time.sleep(timeout_ms)` is reported.
- 151 tests pass (`python3 -m unittest discover -s tests -t .`, from
  `projects/orbiter/`)
- Benchmark: 19 of 19 seeded mistakes detected, 0 findings on unmarked lines,
  2 documented known misses
- Controls: null control (unit tokens stripped from identifiers) gives 0 findings;
  determinism control identical across runs; paired correct/incorrect twins
- Clean on 1,748 real files (`/usr/lib/python3.11`, `/usr/lib/python3/dist-packages`)
- Reproduce evidence: `python3 evidence/run_evidence.py > evidence/results.md`
- Novelty confidence: Medium
- Built 2026-09-12 on `claude/optimistic-pasteur-metblz`

### cutline — `projects/cutline/`
Reads one plain-text plan and decides whether everything fits. When it does not, it
prints the over-subscribed window as a certificate that can be checked by hand, the
cheapest set of tasks to cut, and the earliest deadline that would let each cut task
stay.
- 120 tests pass (`python3 -m unittest discover -s tests -t .`, from
  `projects/cutline/`), including a fresh-virtualenv install check
- Controls: both feasibility methods agreed on 500 of 500 random plans; cut matched
  exhaustive enumeration 200 of 200; verdict survived task reordering and a one-week
  shift 200 of 200 each; 10 of 10 scenarios byte-identical on re-run
- Known limitation, recorded rather than hidden: the worst-case row of the timing
  table reports "not proven minimal" because it exhausts the node budget
- Novelty confidence: Medium
- Built 2026-09-12 on `claude/optimistic-pasteur-metblz`

## Consolidation, 2026-09-12

These three projects were built on three separate branches, none of which could see
the others. That directly cost usage: two runs independently generated, searched and
rejected the same cron-linter candidate, because neither knew the other had done it.
All three folders are now on `main` under `projects/`, so every future run starts
with the full back catalogue visible. The original branches are untouched and retain
the detailed per-run history, including each project's own novelty search narrative.

## Run of 2026-09-20 — selection only, no implementation (Outcome E)

No code was written, and none should have been. Selection has not converged, and the
rules are explicit that manufacturing an implementation to make a run look
productive is the failure mode to avoid. What the run produced instead is in
`IDEAS.md`: a 27-candidate pool, a second wave generated after the first one failed,
seven verified rejections with their closest prior art inspected directly, five
unsearched leads recorded so they are never re-generated blind, and one candidate
that survived.

### What was searched, so no run repeats it

Nine searches, each with several query formulations, across academic literature,
GitHub and package ecosystems, live web tools, and vendor documentation. Rejected on
prior art, with the closest match inspected directly in every case:

1. **Room geometry from acoustic echoes** — PNAS 2013, ICASSP 2016, EchoScan
   (TASLP 2024, code released), dEchorate, pyroomacoustics.
2. **Isospectral drums** — eigendrum.com, which ships the isospectral pair as a
   preset. Fetched and read directly.
3. **TrueType hinting stepped in a browser** — FontLab TTH Debugger. Fetched and
   read directly; it is the candidate exactly, in the same medium.
4. **Regex disagreement witnesses** — gruhn's RegExp Equivalence Checker.
5. **Reflowing mathematical typesetting** — MathJax v4 shipped automatic line
   breaking; `breqn` before it.
6. **Puzzle generation with a uniqueness proof and graded difficulty** — AAAI 2007
   framework, plus standard practice in puzzle generators.
7. **Digital joins for manuscript fragments** — IJCV 2010 through 2026; also fails
   Gate B here on corpus access and compute.

One candidate was rejected with **no** prior art found, on honesty rather than
novelty: mining OpenStreetMap history for streets a city has lost would mostly
detect map corrections, not physical change, so the hook would have been a false
statement about what the code observes.

### The finding, which is the run's real output

All four of the strongest first-wave candidates already existed, and three of them
existed as the whole idea including its surprise. That is structural, not bad luck:
Gate F selects for ideas whose appeal is legible on description, and legible-on-
description is exactly what everyone else can see too. Gate F and Gate C pull
against each other, and nothing in the rules said so before. `IDEAS.md` records the
three bands where the tension resolves — work past the point a hobby project stops,
a resource that does not exist, and a vantage point few people occupy — and the next
wave is to be generated inside them rather than by free association.

### What this run did not do, and why

No finalist scores and no pairwise comparison appear in `IDEAS.md` for this run.
That is not an omission: scoring applies to finalists, and no candidate reached the
finalist stage — the four that were strong enough to score died on prior art before
scoring would have meant anything. Scoring and the pairwise "which would I be more
upset to see someone else ship first" comparison resume the moment W2 or wave three
puts two candidates side by side. No red-team pass appears either, for the same
reason: there is no winner to argue against yet.

### What is unresolved

Whether **W2** — a cited, source-linked record of what clocks actually read before
standard time — survives a proper search and Gate B. It is the only candidate that
got *stronger* when searched: the tz database's own documentation says it does not
attempt accurate pre-1970 civil time, that most of its pre-1970 entries come from
uncited sources including astrology books, and that zones differing only before 1970
are now merged away into a file it calls less reliable. The gap is documented by the
incumbent. The risk is equally documented and must not be waved past: much of the
information was lost or never recorded, so the honest project is one bounded region
and period, not the world.

### Next concrete steps, in order

1. Re-read `IDEAS.md` sections 5 and 0 — the sleep-on-it re-read. What must survive
   the gap here is the *finding* and the W2 lead, not a shortlist, because nothing
   was shortlisted.
2. Search W2 properly under Section 6: `github.com/dfl/tz_history` (seen in results,
   not yet examined), historical-GIS and genealogy tooling, historical-astronomy
   software, the tz mailing list's own sourcing threads, and any cited historical
   time dataset. Then settle Gate B: pick a candidate region and period and confirm
   its primary sources can actually be obtained and read in this environment,
   **before** committing, not at milestone four.
3. If W2 survives, write its hook sentence, definition of done, and milestone
   ladder into `TASKS.json` with a vertical slice as milestone 1 — one town, one
   decade, one cited transition, drawn. If it does not survive, record the rejection
   and generate wave three inside the three bands.
4. Do not re-search the five recorded leads (C9, C10, C12, C13, C20) from scratch —
   `IDEAS.md` names the specific prior art to check for each.

## What the next run should know

1. **No project is in progress.** `current_project` is null. Selection is the job,
   and it is already underway — start from the run log above, not from a blank page.
2. **Selection is not time-boxed.** A run whose entire output is a documented search
   and one excellent decision is a successful run. Record it here and in `IDEAS.md`
   and stop. Do not implement something to make the run look productive.
3. **All three existing projects are the same shape** — a Python static analyzer
   that reads source files, prints findings and returns an exit code. That shape is
   banned for now. So is anything whose primary interface is "run a command, read a
   report". See the shape ban in `AGENT_RULES.md`.
4. **Check `IDEAS.md` before generating candidates.** The cron linter, the
   swapped-argument detector and the CSV anti-join tool are settled rejections with
   prior-art links. Do not re-search them.
5. **There is an unshipped primitive already in this repository.** `cutline`
   contains an engine that proves a set of commitments cannot all be met, emits a
   checkable certificate, and computes the provably cheapest subset to drop,
   verified against exhaustive enumeration. It shipped inside a day planner. It
   generalises to sprints, cloud budgets, timetables and CI minutes. If a candidate
   would build on it, that is a strong starting point — and re-scoping it as the
   primitive it is would satisfy the ship-the-primitive rule.
