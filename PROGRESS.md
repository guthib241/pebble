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

Four further searches were run after the decision, to get the novelty record for
`pivot` most of the way done before next run needs it:

11. Forums, package registries and GitHub for an existing implementation of the
    everyday question → nothing usable found; what exists is the
    [moving sofa problem](https://en.wikipedia.org/wiki/Moving_sofa_problem) (a
    different question: the largest shape that fits, not whether *your* shape fits),
    [SofaBounds](https://github.com/ykallus/SofaBounds) computing bounds for it with
    CGAL and GMP, and student-style breadth-first searches over discretised states.
12. Certified collision-free configuration space → **the most important find of the
    run, and it cuts against the project.** C-IRIS certifies collision-free convex
    regions in a *rational parameterisation* of configuration space using
    sums-of-squares — the same tangent-half-angle trick `pivot` was going to use to
    keep arithmetic exact — and it is **implemented and open source inside Drake**
    ([arXiv:2302.12219](https://arxiv.org/pdf/2302.12219),
    [arXiv:2205.03690](https://arxiv.org/pdf/2205.03690), and 2026 follow-up work,
    [arXiv:2410.12649](https://arxiv.org/pdf/2410.12649)). It is aimed at robot
    manipulators, certifies *free* regions rather than impossibility, and needs an SOS
    solver, but it means the "certified free space by exact arithmetic" idea is not
    itself new. What remains unclaimed after this search is narrower and must be stated
    that way: the **"no" answer** — a checkable certificate that no motion exists,
    with the pinch point and the smallest dimensional change that would fix it — for an
    ordinary object in an ordinary floor plan, with no solver dependency.
13. Professional moving practice → the procedure is done by hand and written up as
    folklore: measure every doorway, hallway and stairwell at its narrowest point, then
    reason about the piece's diagonal clearing the door height while its thickness
    clears the width. Moving-industry software is about pricing and virtual surveys,
    not geometry. This is the "still done by hand, repeatedly" signal, recorded rather
    than assumed.
14. Open-source planners generally → sampling planners (OMPL, Klampt) and collision
    libraries; none answers "no path exists".

**The question the confirmation re-read has to answer**, stated plainly so it cannot
be skipped: after C-IRIS, is `pivot` still materially different, or is it an
application of published and implemented work? My answer today is that the
impossibility certificate and the minimal fix are the difference and the free-space
side is not, so the project has to be built and claimed around the "no" answer. If the
next run disagrees with that, the honest move is to drop it and go to section 5 of
`IDEAS.md`, not to soften the wording.

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
