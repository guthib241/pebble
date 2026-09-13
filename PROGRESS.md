# Progress

**Hook sentence for the current project:** *Scatter a handful of balls for ten thousand
steps, then run time backwards — every ball retraces its exact path to where it started,
and no frames were saved to make that happen.*

Status: project selected 2026-09-13 — **ebb**, in `projects/ebb/`. **Milestone 1 of 6 is
done and verified**; milestone 2 is next. Three earlier projects complete, in `projects/`.
Last updated: 2026-09-13

> **Where the work is.** This run was given branch `claude/intelligent-mendel-ndp84t` and is
> not permitted to push to `main`. Everything below is on that branch. It needs merging to
> `main` so the next run sees it, the same consolidation that was needed on 2026-09-12.

## Read this first

The rules changed substantially on 2026-09-12: projects may span many runs, selection is not
time-boxed, a hook sentence and a ten-second demo are required before building, the shape
all three earlier projects share is banned, and every candidate must be recorded in
`IDEAS.md`. Read `AGENT_RULES.md` and the execution protocol completely before acting.

## The current project: ebb

**What it is**: a 2D physics simulation in integer fixed-point arithmetic where every step is
a bijection on the state, so the simulation can be stepped *backwards* and lands on earlier
frames bit-for-bit, with no stored frames. Rewind is computed, not remembered.

**Why it was chosen** (2026-09-13): it is the one candidate where the demo, the primitive and
the open technical question are the same thing. Making contact dynamics invertible is the
unsolved part; if it works, unbounded rewind costs no memory, and if it fails, the failure is
visible rather than hideable. It is also a form this repository does not yet have — a running
simulation with animated output, not a source reader printing warnings.

**Definition of done and the six-milestone ladder are in `TASKS.json`.** Summary: M1 discs
(vertical slice), M2 the reversible-contact core property-tested with the residue tape
measured, M3 rotation and polygons, M4 resting contact, friction and the tower, M5 a second
implementation plus the browser scrub, M6 package and document.

**Novelty**: Medium confidence. Full record in `projects/ebb/NOVELTY_REPORT.md`, written
before implementation started. Closest prior art: Stam's *An Exact Bitwise Reversible
Integrator* (integer reversibility, no contact anywhere in the paper) and Perumalla &
Protopopescu's *Reversible Simulations of Elastic Collisions* (reversible collisions, but
identical frictionless hard spheres, n ≤ 3 in 2D). Deterministic game engines own the use
case and rewind by storing frames.

### The design, in one paragraph

State is integers only — fixed-point positions and velocities. A step is a kick that depends
only on position (`v += f(q)`) followed by a drift that depends only on velocity
(`q += v`); each is a shear, so the composition is invertible exactly, for any deterministic
integer `f`. Walls use mirror unfolding, which in this formulation is its own inverse:
subtract the velocity, and if the result lies outside the box, negate the coordinate and the
velocity. Body-body contact is where rounding destroys information, so whatever it destroys
is written to a **residue tape**, and the size of that tape is a measured quantity the
project reports rather than a detail it hides. Dissipation (friction, restitution) is the same
problem in a more honest form, and arrives at M4.

### Milestone 1 — done, 2026-09-13

Discs under gravity in a box, exact mirror reflection off walls, equal-mass elastic
disc-disc contact, `step()` and `unstep()` as exact inverses. 45 tests pass in 3.3 seconds
with no dependencies (`python3 -m unittest discover -s tests -t .`, from `projects/ebb/`).
Two animated GIFs in `projects/ebb/demo/`, written by a hand-rolled GIF89a encoder because
no image library is installed here.

Measured, and reproducible with `python3 evidence/run_evidence.py > evidence/results.md`:

- Round trips exact on four scenes at 10,000 steps and on the falling-balls scene at
  100,000 steps, comparing the whole integer state rather than a tolerance.
- The wall rule enumerated exhaustively: 3,321 states, 3,321 distinct images, 0 collisions,
  all inverted exactly.
- Residue tape 22–23 bits per contact event, nothing per frame; a one-ball scene writes 0
  bytes.
- Controls: determinism (identical states and identical tapes), elastic energy drift 0.042%
  over 10,000 steps, momentum exactly conserved across contact, and `pip install .` checked
  in a fresh virtualenv followed by an exact 5,000-step round trip.

**Two solved problems worth not re-deriving.** First, the obvious mirror rule for walls is
not injective on an integer lattice — a body on the wall moving out and the same body
moving in can land on the same state. Reflecting about the half-unit *just outside* the
wall makes the three cases land in disjoint ranges of `x - v`, so the backward pass reads
off what happened with nothing stored. A test enumerates the naive rule and requires it to
collide, so the offset cannot be quietly "simplified" away. Second, contact divides by the
squared distance between centres, and integer division loses a remainder; exactly one
integer per contact goes on the tape — the relative normal speed before the exchange plus
the one after, which in exact arithmetic would be zero.

**The honest limitation.** Contact is resolved for every overlapping pair on every step, so
bodies that settle into a pile re-resolve instead of resting: 0% of contact events are
repeats of an already-overlapping pair in the no-gravity scene, 67.5% in the falling-balls
scene, 92.0% in the 14-body scene. It is reversible and it is not good contact physics.

### Milestone 2 — next, with the approach already worked out

Replace the contact rule with one that never lets bodies overlap in a stored state, by
reflecting the **relative** position along the line of centres. This is the same unfolding
trick that already works for walls, and understanding *why* it works there is the key: it
relies on "inside the box" being an invariant of every valid state, which makes the
reflected and non-reflected images occupy disjoint ranges. The pair version needs "no
overlap" to be the invariant in the same way. Rounding along a normal that is not
axis-aligned is where the residue goes, and shrinking the tape entry below one integer per
contact is part of the milestone. Also due: property tests over random scenes, the
invariant written down explicitly, and an exact-rational reference simulator as an
independent control on the integer physics.

## Completed projects

All three live in `projects/`, each self-contained with its own README, `NOVELTY_REPORT.md`,
`LICENSE.txt` and tests. All three were verified to still pass after being consolidated onto
`main` on 2026-09-12. All three are the same banned shape, which is why the ban exists.

### backfire — `projects/backfire/`
Finds retry amplification and timeout blowups in Python codebases. Resolves the call graph
and multiplies retry policies along each path, so three stacked layers of reasonable-looking
retries are reported as the 30 requests they actually produce.
- 85 tests pass (`python3 -m pytest`, from `projects/backfire/`; needs pytest)
- Run against psf/requests (dae7ef6), openai/openai-python (d7c41ef), PrefectHQ/prefect (d82220b)
- Controls: two single-layer codebases report no amplification; repeat runs byte-identical
- Novelty confidence: Medium. Built 2026-09-11 on `claude/eloquent-newton-p3qht6`

### orbiter — `projects/orbiter/`
Flags Python code that mixes units, like milliseconds passed as seconds, by inferring unit
and scale from identifier names, `typing.Annotated` metadata and standard library
conventions.
- 151 tests pass (`python3 -m unittest discover -s tests -t .`, from `projects/orbiter/`)
- Benchmark: 19 of 19 seeded mistakes detected, 0 findings on unmarked lines, 2 known misses
- Controls: null control (unit tokens stripped) 0 findings; determinism control identical
- Clean on 1,748 real files (`/usr/lib/python3.11`, `/usr/lib/python3/dist-packages`)
- Novelty confidence: Medium. Built 2026-09-12 on `claude/optimistic-pasteur-metblz`

### cutline — `projects/cutline/`
Reads one plain-text plan and decides whether everything fits; when it does not, prints the
over-subscribed window as a checkable certificate, the cheapest set of tasks to cut, and the
earliest deadline that would let each cut task stay.
- 120 tests pass (`python3 -m unittest discover -s tests -t .`, from `projects/cutline/`)
- Controls: both feasibility methods agreed on 500 of 500 random plans; cut matched
  exhaustive enumeration 200 of 200; verdict stable under reordering and a one-week shift
- Known limitation: the worst-case timing row reports "not proven minimal" (node budget)
- Novelty confidence: Medium. Built 2026-09-12 on `claude/optimistic-pasteur-metblz`

## The search that produced this decision (2026-09-13)

Recorded so it is never repeated. Every candidate is in `IDEAS.md`, filed by outcome.

**Rejected on prior art, with links in `IDEAS.md` section 2:**
- *isospectral drums* ("two differently shaped drums that sound identical") — COMSOL ships
  the model; Driscoll published the eigenmode computation.
- *linkage synthesis from a drawn curve* ("a machine of rods that draws your signature") — a
  practical implementation of Kempe's universality theorem exists, with published source.
- *Wallace-Bolyai-Gerwien dissection* ("cuts any shape into pieces that become another") —
  `dmsm/scissors-congruence` and weitz.de/polygons do exactly this, interactively.

**Viable, not selected, recorded in `IDEAS.md` section 5 (a heading added this run):**
- *hinged-dissection compiler* — no public implementation found, excellent demo, but the
  published constructions give astronomical piece counts and the non-crossing motion is the
  part a first milestone would have to fake. Kept as a strong future candidate.
- *every hour that never happened* (tzdb discontinuities as a picture and an adversarial
  timestamp corpus) — **not searched**; generated late. Do not treat it as cleared.
- *re-scoping cutline's solver as the primitive it is* — still the banned shape until it has
  a visual form.

**Sources covered for the selected project:** arXiv, Springer, ScienceDirect, ResearchGate,
ADS, OSTI, NVIDIA Research; GitHub repository and topic search, GitLab; npm and
search-indexed PyPI packages; GameDev.net, DEV, Hacker News, itch.io devlogs, BEPUphysics
forum; the JoltPhysics rollback discussion; Rapier/Matter.js/propel-js documentation. Ten
query formulations, listed verbatim in the novelty report. The two closest papers were
downloaded and read as extracted text, not just as abstracts.

## What the next run should know

1. **ebb is in progress. Continue it — do not select anything new.** `TASKS.json`
   `current_project` is set and its checklist is not complete. Milestone status is in
   `TASKS.json` `milestones`.
2. **Milestone 1 is done** — see the milestone sections above for what was built, what was
   measured, and the two design problems already solved. Milestone 2's approach is written
   out there too; start from it rather than re-deriving it.
3. **The project-level checklist in `TASKS.json` tracks the whole project, not a milestone.**
   Do not tick `core_implementation_done` because a milestone is done.
4. **Honesty constraint specific to this project**: the README must state the residue tape's
   real cost. "No frames are stored" is true; "nothing is stored" will not be true once
   friction arrives at M4. Every byte figure must come from a committed run.
5. **Rotation (M3) is the milestone that can kill the idea.** If angular state cannot be made
   invertible without an impractical tape, say so in this file and in the README rather than
   quietly narrowing the definition of done.
