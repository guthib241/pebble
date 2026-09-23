# Progress

Status: **no project in progress, and none selected.** Run of 2026-09-23 was a selection
run — Outcome E under Section 29. Thirty candidates were generated and recorded in
`IDEAS.md`, eight searches were run, four candidates were killed on prior art
with links, and one provisional winner is on the shortlist awaiting the mandatory
cold re-read. No implementation was produced, and none should have been.
Last updated: 2026-09-23

## Provisional hook sentence (not yet committed to)

> **"Grab the answer and drag it, and the numbers that produced it rearrange themselves
> to agree."**

Provisional. It belongs to the shortlisted candidate in `IDEAS.md` section 5, which has
not been selected and must survive a cold re-read first.

## Read this first

The rules changed substantially on 2026-09-12, after the three completed projects were
built, and were extended on 2026-09-13. Read `AGENT_RULES.md` and the execution protocol
completely before acting. The main points that bind the next run: projects may span many
runs, selection is not time-boxed, a hook sentence and a ten-second demo are required
before building, the shape all three existing projects share is banned, every candidate
must be recorded in `IDEAS.md`, and a shortlist must survive a re-read after a gap before
implementation starts.

## What happened on 2026-09-23

Phase 1 intake completed: `AGENT_RULES.md`, the execution protocol, `PROGRESS.md`,
`TASKS.json`, `IDEAS.md` and `REFERENCES.md` were all read in full. Phase 1.5:
`current_project` was null and no checklist was outstanding, so Section 4 selection was
the run's job.

**Environment capability check, run before Gate B was applied to anything** — this had
not been recorded before and changes what is feasible here. Available: Python 3.11.15,
Node 22.22.2 with npm 10.9.7, gcc, g++, make, cargo, go, and a Playwright browser bundle
at `/opt/pw-browsers` containing Chromium, a headless shell and ffmpeg. 4 CPUs, 15 GB
RAM, ~30 GB free disk. Not present: numpy, scipy, Pillow (installable), and no GPU was
detected. **Consequence: interactive and visual projects are demo-able in this
environment.** A browser page can be driven and screenshotted, and ffmpeg can turn frames
into an animation, so the ten-second-demo requirement no longer pushes toward text
output. Previous runs appear to have assumed otherwise.

**Candidate generation.** Thirty candidates, generated before any gate ran, deliberately
spanning shapes: interactive and visual work, games and toys, datasets, languages and
formats, primitives, audio, and four inverse-design geometry tricks. The first idea
generated — repackaging `cutline`'s minimal-cut engine as a standalone library — was
recorded and rejected as a final answer under the first-idea rule, as required. Its
mechanism survives as one component of the shortlisted candidate, which is the legitimate
way to reuse it.

**Searches run this run** (do not repeat these):

1. `fold-and-cut theorem solver implementation crease pattern straight skeleton github`
2. `draw a curve generate linkage mechanism that traces it interactive web tool Kempe universality implementation`
3. `"linkage" synthesis open source software draw path "four-bar" OR "six-bar" web app trace arbitrary curve signature github`
4. `CAD sketch over-constrained diagnosis minimal conflicting constraint set explain which constraints conflict solver`
5. `non-circular gear generation arbitrary closed curve conjugate profile tool generate meshing gears from any shape`
6. `tz database comments political history of time zone changes interactive visualization every clock change`
7. `bidirectional spreadsheet drag the output value and inputs adjust back-solve constraint UI ThingLab goal seek generalized`
8. `LLM evolutionary search over whole software projects quality diversity archive open-ended project generation 2026`

**Four candidates killed on prior art**, all recorded in `IDEAS.md` section 2 with links:
the fold-and-cut one-cut solver, a linkage that traces a curve you drew, a minimal-conflict
explainer for over-constrained CAD sketches, and gears generated from two drawn curves.

The lesson from those four is worth more than the rejections, and is recorded in
`IDEAS.md` section 2: each was an inverse-design magic trick whose *method* is published
and whose only gap is that no pleasant implementation exists. Gate E rejects exactly that
— "interesting only because it is well-executed". A future run that gets excited by a
geometry trick should search the method before the tool. It costs one query.

**The owner's idea, Pebble Evolve, was considered first**, as section 0 requires, and one
search was run to advance it rather than defer it a third time. Not selected this run, and
not rejected: the buildable part is crowded, and the distinguishing part — a taste signal
from the owner's own ratings — needs data that does not exist in the repository yet. The
reasoning is written into section 0 so the owner can push back on it.

## What the next run must do, in order

1. **Re-read `IDEAS.md` section 5 cold, before anything else.** That is the sleep-on-it
   gate, and it is the whole reason this run stopped where it did. Say plainly whether the
   entry still reads well. If it needs talking up, drop it and keep searching — infatuation
   does not survive a gap, and a good idea reads better the second time.
2. **If it survives, finish its prior-art search.** The open question is named in the
   entry: whether any shipped tool already offers continuous dragging of any variable in a
   general nonlinear model with least-change semantics. Specifically to check — Apparatus
   (Toby Schachman), Sketch-n-Sketch, Cassowary and its descendants, Grasshopper with
   Kangaroo, Desmos draggable parameters, Geogebra, Modelica and other acausal modelling
   tools, and the bidirectional-transformation and lenses literature. **Acausal modelling
   is the sharpest risk.** If a shipped acausal tool does this, the candidate is dead and
   moves to section 2 with links — that is a successful rejection, not a failed run.
3. **Only then** write `NOVELTY_REPORT.md`, fill in `definition_of_done` and a milestone
   ladder in `TASKS.json`, and make milestone 1 a vertical slice: the exposure-triangle
   demo, draggable, in a browser, crude but genuinely working end to end.
4. **If it dies**, go back to generation. `IDEAS.md` now holds thirty candidates; section
   3 holds five parked ones with a note on what would move each of them, and two of those
   five have never been searched at all.

## Completed projects

All three live in `projects/`, each self-contained with its own README,
`NOVELTY_REPORT.md`, `LICENSE.txt` and tests. All three were verified to still pass after
being consolidated onto `main` on 2026-09-12. None of them meets the current rules; each
one's specific failure is recorded in `TASKS.json` and in `IDEAS.md`.

### backfire — `projects/backfire/`
Finds retry amplification and timeout blowups in Python codebases. Resolves the call graph
and multiplies retry policies along each path, so three stacked layers of reasonable-looking
retries are reported as the 30 requests they actually produce, with each contributing site
named.
- 85 tests pass (`python3 -m pytest`, from `projects/backfire/`; needs pytest)
- Run against psf/requests (dae7ef6), openai/openai-python (d7c41ef), PrefectHQ/prefect (d82220b)
- Controls: two single-layer codebases report no amplification; repeat runs byte-identical
- Novelty confidence: Medium
- Built 2026-09-11 on `claude/eloquent-newton-p3qht6`

### orbiter — `projects/orbiter/`
Flags Python code that mixes units, like milliseconds passed as seconds. Infers a unit and
scale from identifier names, `typing.Annotated` metadata and standard library conventions,
and reads explicit conversions, so `time.sleep(timeout_ms / 1000)` is accepted where
`time.sleep(timeout_ms)` is reported.
- 151 tests pass (`python3 -m unittest discover -s tests -t .`, from `projects/orbiter/`)
- Benchmark: 19 of 19 seeded mistakes detected, 0 findings on unmarked lines, 2 documented known misses
- Controls: null control (unit tokens stripped from identifiers) gives 0 findings;
  determinism control identical across runs; paired correct/incorrect twins
- Clean on 1,748 real files (`/usr/lib/python3.11`, `/usr/lib/python3/dist-packages`)
- Reproduce evidence: `python3 evidence/run_evidence.py > evidence/results.md`
- Novelty confidence: Medium
- Built 2026-09-12 on `claude/optimistic-pasteur-metblz`

### cutline — `projects/cutline/`
Reads one plain-text plan and decides whether everything fits. When it does not, it prints
the over-subscribed window as a certificate that can be checked by hand, the cheapest set
of tasks to cut, and the earliest deadline that would let each cut task stay.
- 120 tests pass (`python3 -m unittest discover -s tests -t .`, from `projects/cutline/`),
  including a fresh-virtualenv install check
- Controls: both feasibility methods agreed on 500 of 500 random plans; cut matched
  exhaustive enumeration 200 of 200; verdict survived task reordering and a one-week shift
  200 of 200 each; 10 of 10 scenarios byte-identical on re-run
- Known limitation, recorded rather than hidden: the worst-case row of the timing table
  reports "not proven minimal" because it exhausts the node budget
- Novelty confidence: Medium
- Built 2026-09-12 on `claude/optimistic-pasteur-metblz`

## Standing notes for every run

1. **Check `IDEAS.md` before generating candidates.** The cron linter, the swapped-argument
   detector and the CSV anti-join tool are settled rejections with prior-art links, and as
   of 2026-09-23 so are the four geometry tricks. Do not re-search any of them.
2. **All three existing projects are the same shape** — a Python static analyzer that reads
   source files, prints findings and returns an exit code. That shape is banned, as is
   anything whose primary interface is "run a command, read a report".
3. **There is an unshipped primitive already here.** `cutline` contains an engine that
   proves a set of commitments cannot all be met, emits a checkable certificate, and
   computes the provably cheapest subset to drop, verified against exhaustive enumeration.
   Reusing it as a component inside something of a different shape is legitimate;
   repackaging it as a library is the first idea and was rejected as such on 2026-09-23.
4. **Consolidation, 2026-09-12.** The three projects were built on three separate branches
   that could not see each other, which cost usage directly: two runs independently
   generated, searched and rejected the same cron-linter candidate. All three folders are
   now on `main` under `projects/`. The original branches are untouched and retain the
   detailed per-run history.
