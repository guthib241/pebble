# Progress

Status: **selection run — no project in progress, no code written.** A candidate has
been chosen and is waiting on the mandatory re-read before implementation starts.
Last updated: 2026-09-13 (run 4)

## The hook sentence for the selected candidate

> **Finds the way to turn your sofa through the door — or proves there isn't one, and
> names the centimetre that would fix it.**

Working name: `pivot`. Full entry, scores, prior art and red team: `IDEAS.md` section 4.

## What this run did

Phase 1 intake against the rules as they stand on `main` today, which changed during
the run: `REFERENCES.md` is new, and `AGENT_RULES.md` gained mandatory generation
mechanics (a 20-candidate quota, first-idea rejection, tail sampling, behaviour
descriptors, scoring, pairwise comparison, a written red team, and a sleep-on-it rule).
The run was re-started against the new files rather than continued against the old.

Then: the owner's idea in `IDEAS.md` section 0 was evaluated first and passed on with a
reason recorded there; 34 candidates were generated and written into `IDEAS.md`; the
five strongest were searched for prior art; four finalists were scored and compared
pairwise; the winner was red-teamed in writing.

**No implementation was produced, and none should have been** — rule 7 of the
generation section requires the shortlist to survive a re-read at the start of the next
run first. This is Outcome E in the protocol's stop conditions.

## Searches actually run this run — do not repeat these

Web search, 2026-09-13. Each line is a query family and what it settled:

1. Polygon dissection / Wallace-Bolyai-Gerwien implementations → **taken** (Weitz's
   Polygons, Frederickson's animations, Wang et al. Bridges 2012).
2. Hinged dissection generators and animations → **taken** (same sources).
3. Linkage synthesis from a drawn curve → **taken** (MotionGen; C-VAE and transformer
   synthesis papers, 2024-25).
4. Aperiodic monotile (hat/spectre) pattern generators → **taken** (four public
   generators, one already aimed at laser cutting).
5. Caustic surface design → **taken** (Ferraro's causticsEngineering,
   dylanmsu/poisson_caustic_design, published methods).
6. Fold-and-cut solvers → **taken** (Demaine's page plus four public implementations).
7. "Will it fit" consumer furniture tools → **closed-form calculators only**; closest
   product is a closed-source measuring app.
8. Exact / certifying / resolution-exact motion planning, SE(2), no-path proofs →
   **research exists, usable open implementations did not surface** (Yap's soft
   subdivision search; CAD-based exact planning described as infeasible in practice;
   2024-25 infeasibility-proof papers).
9. Minimum constraint removal / displacement — the "smallest change that makes it
   feasible" idea → **established research**, so that feature is not a novelty claim.
10. Assembly and disassembly path planning → **commercial (Siemens NX) and research
    (Autodesk, SIGGRAPH Asia 2022)**; nothing open, exact and certifying.

Environment checks: Python 3.11.15 and Node 22 present, PyPI reachable, no numpy,
scipy, sympy, Pillow, matplotlib, cairo, pytest, z3 or shapely preinstalled, no ffmpeg
or ImageMagick. A project that wants images or animation in this repository has to
write its own encoders or install dependencies at run time; `pivot` is planned as
pure standard library for exactly this reason.

## Where things stand

* `TASKS.json` → `current_project` is still `null`. The chosen candidate sits under
  `pending_selection`, with a draft definition of done and milestone ladder.
* Nothing has been built. There is no `projects/pivot/` folder yet, deliberately.
* The next run's first action is to re-read the `pivot` entry in `IDEAS.md` section 4
  cold, then either confirm it — move it into `current_project`, write
  `NOVELTY_REPORT.md`, and build milestone 1 — or record honestly why it reads worse
  the second time and go back to the pool in section 5.

## Milestone 1, when it is confirmed

The vertical slice, per Gate D: two dimensions, top down. A rectangular object and an
L-shaped corridor, exact rational arithmetic, and one of the three answers with its
evidence, rendered as an animation committed to the repository. The control check is
already identified and is unusually good: for a zero-width rod moving around a
right-angled corner between corridors of widths a and b, the longest rod that fits is
known in closed form, so the planner's feasibility boundary can be checked against
mathematics rather than against itself.

## Completed projects

All three live in `projects/`, each self-contained with its own README,
`NOVELTY_REPORT.md`, `LICENSE.txt` and tests. All three were verified to still pass
after being consolidated onto `main` on 2026-09-12.

### backfire — `projects/backfire/`
Finds retry amplification and timeout blowups in Python codebases. 85 tests pass
(`python3 -m pytest`, from `projects/backfire/`, needs pytest). Run against psf/requests
(dae7ef6), openai/openai-python (d7c41ef), PrefectHQ/prefect (d82220b). Controls: two
single-layer codebases report no amplification; repeat runs byte-identical. Novelty
confidence: Medium. Built 2026-09-11 on `claude/eloquent-newton-p3qht6`.

### orbiter — `projects/orbiter/`
Flags Python code that mixes units, like milliseconds passed as seconds. 151 tests pass
(`python3 -m unittest discover -s tests -t .`, from `projects/orbiter/`). Benchmark: 19
of 19 seeded mistakes detected, 0 findings on unmarked lines, 2 documented known misses.
Controls: null control gives 0 findings; determinism control identical across runs.
Clean on 1,748 real files. Reproduce: `python3 evidence/run_evidence.py >
evidence/results.md`. Novelty confidence: Medium. Built 2026-09-12 on
`claude/optimistic-pasteur-metblz`.

### cutline — `projects/cutline/`
Reads one plain-text plan and decides whether everything fits, printing the
over-subscribed window as a checkable certificate, the cheapest set of tasks to cut, and
the earliest deadline that would let each cut task stay. 120 tests pass (`python3 -m
unittest discover -s tests -t .`, from `projects/cutline/`), including a fresh-virtualenv
install check. Controls: both feasibility methods agreed on 500 of 500 random plans; cut
matched exhaustive enumeration 200 of 200; verdict survived reordering and a one-week
shift, 200 of 200 each. Known limitation, recorded rather than hidden: the worst-case
timing row reports "not proven minimal" because it exhausts the node budget. Novelty
confidence: Medium. Built 2026-09-12 on `claude/optimistic-pasteur-metblz`.

## What the next run should know

1. **Re-read `IDEAS.md` section 4 before anything else.** The sleep-on-it rule exists
   to catch infatuation; treat the entry as an argument to be checked, not a decision
   already made.
2. **The pool in `IDEAS.md` section 5 is the fallback**, not a blank page. Fifteen
   ungated candidates are sitting there with descriptors and suspicions attached.
3. **Ten searches are recorded above.** Repeating any of them is wasted usage.
4. **All three existing projects share one behaviour cell** — reads source files,
   prints text, developer tooling, local CLI — and the shape ban is still in force.
   `pivot` was chosen partly because every part of its descriptor differs.
5. **`pivot` has no code yet.** If the next run confirms it, `NOVELTY_REPORT.md` comes
   before implementation, per protocol section 12.
