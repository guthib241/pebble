# Ideas

Every idea ever considered in this repository, kept permanently.

Nothing is deleted from this file. An idea that was rejected stays recorded with
the reason, so no future run spends usage rediscovering it, re-searching it, or
re-arguing it. Three runs have already lost time to this: two of them
independently generated the same cron-linter idea and independently searched and
rejected it, because neither could see the other's work.

**Read this file during Phase 1 intake, before generating any candidate.** It is
part of the repository's memory, not an appendix.

Every project referenced below exists on `main` under `projects/`, so a candidate can
be compared against the real code rather than against a description of it.

## How to use it

* Every candidate that gets as far as being considered goes in, whatever happens
  to it. No idea is too dead to record.
* File it under exactly one heading, by outcome.
* Include the date, the hook sentence attempt (even a failed one), what was
  searched, and the specific reason for the outcome. Links to prior art are
  required in section 2.
* An idea may be **moved** between sections when something real changes — a hook
  is found, prior art turns out to be weaker than it looked, the environment gains
  a capability. Moving it means editing its entry and noting what changed and
  when. It does not mean deleting the history.
* Never move an idea upward to justify building it. If the reason for the move is
  "I want to build this," that is not a reason.

---

## 1. Rejected — failed the rules

Ideas that failed a gate for reasons other than prior art: not feasible here, no
definition of done, no first step, no real problem, inside the shape ban, or
memorable but useless.

Format: **name** — date. Hook attempt. Which gate failed and exactly why.

_(none yet — the entries below were all rejected on prior art or on hype)_

---

## 2. Already done by someone else

Ideas dropped because materially equivalent work exists. Prior-art links are
mandatory. These are settled: do not re-search them without a specific reason to
think the landscape has changed, and if you do, record what changed.

### cron / crontab linter — rejected twice (2026-09-11, 2026-09-12)
Hook attempt: "checks your crontab for daylight-saving and escaping mistakes."
Considered independently on two runs, searched and rejected both times. Prior art:
[CronLens](https://github.com/SNO7E-G/CronLens) (lints cron expressions with DST,
overlap and thundering-herd warnings),
[cron-doctor](https://github.com/HeytalePazguato/cron-doctor) (ten lint checks),
[cronlint](https://github.com/zbcdo/cronlint), and `cronkit` (CLI crontab linting
with overlap detection and schedule projection). Same problem, same user, same
workflow. **Settled — do not consider a third time.** Also now inside the shape
ban.

### swapped-argument detector for Python — set aside (2026-09-12)
Hook attempt: "finds function calls whose arguments are in the wrong order."
Not built because the capability exists as research work, which would have capped
novelty confidence. Prior art: the DeepBugs IntelliJ plugin (incorrect function
arguments in Python), and
[eth-sri/learning-real-bug-detector](https://github.com/eth-sri/learning-real-bug-detector)
(argument-swap task). Also now inside the shape ban.

### CSV anti-join / join-diagnosis tool — rejected (2026-09-12)
Hook attempt: "tells you why your two spreadsheets didn't line up."
Prior art: Apify's CSV Anti-Join Finder, and the R package `joinspy`. Materially
equivalent.

### isospectral drums — rejected (2026-09-13)
Hook attempt: "Two drums shaped completely differently that sound identical, note for
note." Searched: arXiv ("Hearing shapes of drums", arXiv:1101.1239; "We can't hear the
shape of a drum: revisited in 3D", arXiv:1701.05984), COMSOL model gallery, Driscoll's
*Eigenmodes of Isospectral Drums*. Prior art:
[COMSOL's Isospectral Drums model](https://www.comsol.com/model/isospectral-drums-119)
(strikes the drum and computes the spectrum of modes that make up its sound) and
Driscoll's published eigenmode computation of the Gordon-Webb-Wolpert pair. Same object,
same demonstration, same audience. The mathematics is also 1992 and widely exposited, so
the project would have been a re-presentation rather than a capability.

### linkage synthesis from a drawn curve — rejected (2026-09-13)
Hook attempt: "Give it your signature and it designs a machine of rods and pins that
draws it." Searched: Kempe's universality theorem literature, "Synthesis of Linkages to
Trace Plane Curves" (Springer), "Automated generation of Kempe linkages for algebraic
curves and surfaces", "Elementary proofs of Kempe universality" (arXiv:1511.09002).
Prior art: [A Practical Implementation of Kempe's Universality
Theorem](https://laurahallock.org/files/projects_old/kempe_report.pdf) (working software
that constrains a tracing node to a given algebraic curve and derives the rest of the
linkage), plus the Liu & McCarthy designs with SageMath source published. Curve in,
linkage out, already implemented.

### Wallace-Bolyai-Gerwien dissection demo — rejected (2026-09-13)
Hook attempt: "Cuts any shape into pieces that rearrange into any other shape of the same
area." Prior art: [dmsm/scissors-congruence](https://github.com/dmsm/scissors-congruence)
(interactive demonstration of exactly this) and [weitz.de/polygons/](https://weitz.de/polygons/)
(draw an arbitrary polygon, watch it cut and rearranged into a rectangle). Materially
equivalent, including the interaction.

---

## 3. Not hyped — passed the other rules, failed the hook

**This section is a resource, not a graveyard.** These ideas are real, buildable,
unclaimed, and satisfy the rules on problem value, feasibility, originality and
completeness. They failed only Gate F: no hook sentence a stranger would repeat,
or nothing that can be shown in ten seconds.

They are kept because a hook can be found later. An idea moves to section 4 when
someone writes a hook sentence that genuinely passes all four tests — surprising,
concrete, context-free, not a category label — or when the framing changes so that
the interesting part becomes the project. Very often the fix is scope, not
wording: the boring application was hiding a primitive worth building on its own.

Record for each: the hook attempts that failed, and what would have to be true for
it to become hyped.

### backfire (built 2026-09-11, `projects/backfire/`) — belongs here by today's rules
"Finds retry amplification and timeout blowups in Python codebases." Genuinely
useful, honestly validated, 85 tests. Fails Gate F: a category label, no demo, and
inside the shape ban. What would make it hyped: the composed-retry-multiplication
result shown **visually** — a diagram or animation of one click fanning out into
thirty requests across the call graph. The engine is interesting; the CLI report
hides it.

### orbiter (built 2026-09-12, `projects/orbiter/`) — belongs here by today's rules
"Flags Python code that mixes units, like milliseconds passed as seconds." Strong
validation, 151 tests, real controls. Fails Gate F for the same reasons. What
would make it hyped: unit inference as something you can *see* — units propagating
through an expression live as you type, rather than a warning printed after.

---

## 4. Hyped and selected — building, or built

Ideas that passed every gate including Gate F, with a hook sentence that holds.
Each entry keeps its hook sentence verbatim, its status, and a link to its folder.
An entry stays here after completion; this doubles as the repository's back
catalogue.

### cutline (built 2026-09-12, `projects/cutline/`) — partially qualifies
Shipped as: "Reads one plain-text plan and decides whether everything fits."
Contains a genuinely strong idea that was not surfaced: an engine that **proves**
a set of commitments cannot all be met, emits a certificate you can check by hand,
and computes the provably cheapest subset to drop — verified against exhaustive
enumeration, 200 of 200. Better hook, available the whole time: *"Proves your plan
is impossible, then tells you the single cheapest thing to drop."* That engine
generalises to sprints, cloud budgets, timetables and CI minutes, and should have
been the project with the planner as one demo. Recorded as the worked example of
the ship-the-primitive rule.

### ebb (selected 2026-09-13, `projects/ebb/`) — in progress
Hook sentence, verbatim: *"Scatter a handful of balls for ten thousand steps, then run time
backwards — every ball retraces its exact path to where it started, and no frames were saved
to make that happen."*
A 2D physics simulation whose every step is a bijection on integer state, so rewind is
computed instead of remembered. Searched across bit-reversible integrators, reverse
computation in parallel discrete-event simulation, deterministic game-physics engines, and
the physics of frictional reversibility; ten query formulations; the two closest matches
read at full text. Closest prior art: Jos Stam's *An Exact Bitwise Reversible Integrator*
(arXiv:2207.07695 — integer reversibility, and zero occurrences of "collision" or "contact"
in the paper) and Perumalla & Protopopescu's *Reversible Simulations of Elastic Collisions*
(arXiv:1302.1126 — reversible collisions, but identical frictionless hard spheres, n ≤ 3 in
2D). Deterministic engines such as Rapier and SG Physics 2D own the use case and rewind by
storing frames. Novelty confidence Medium; full record in `projects/ebb/NOVELTY_REPORT.md`.
Why it was chosen over the others above: it is the only candidate where the demo, the
primitive and the open technical question are the same thing — if contact can be made
invertible, rewind becomes free, and if it cannot, the project says so visibly.
---

## 5. Considered, viable, not selected this cycle

A heading added 2026-09-13. These candidates are not rejected: nothing disqualified them.
They cleared the gates as far as they were taken, and another candidate was chosen ahead of
them in the same cycle. They are recorded in full so a future run can pick one up without
repeating the search, and so the reason for *not* choosing them stays visible.

### hinged-dissection compiler — viable, 2026-09-13
Hook attempt (passes, in my judgement): "Cuts any shape into pieces joined by hinges that
swing round to become any other shape of the same area."
Searched: arXiv and Demaine's publication list ("Hinged Dissections Exist", Abbott, Abel,
Charlton, Demaine, Demaine & Kominers; "Hinged Dissection of Polyominoes and Polyforms",
Demaine, Demaine, Eppstein & Friedman, CCCG'99 / Computational Geometry), Eppstein's
Geometry Junkyard hinge page, GitHub code search for hinged dissection implementations.
**No public implementation was found** — the theorems are published and constructive, the
software appears not to exist. The demo would be outstanding (one shape swinging into
another).
Why not selected: the published constructions reach astronomical piece counts, and the hard
part — a continuous motion between the two configurations that never self-intersects — is
the part a first milestone would have to fake or omit, which is exactly what the rules
forbid. It needs a run that can afford to spend its first milestone establishing whether
practical piece counts are reachable at all. Kept as a strong candidate, not a dead one.
*If picked up*: start from the polyform result (midpoint cuts around each vertex), not the
general theorem, and treat non-crossing motion as the make-or-break question.

### every hour that never happened — viable but unsearched, 2026-09-13
Hook attempt: "Shows you every hour in history that never happened, and every hour that
happened twice."
The IANA time zone database records every civil clock change on Earth since the 1830s, and
`/usr/share/zoneinfo` is present in this environment, so the data is local and free. Two
artifacts: a rendered picture of every local-time discontinuity in recorded history, and a
corpus of adversarial timestamps (gaps, folds, sub-minute offsets, the day Samoa deleted)
generated from real transitions rather than invented.
Why not selected: **no prior-art search was run on it** — it was generated late and another
candidate was chosen first. Do not treat it as cleared. Likely neighbours to check before
building: tzdb visualisations, Hypothesis's datetime strategies, `dateutil`/`zoneinfo` test
corpora, and the "falsehoods programmers believe about time" lineage.

### re-scoping cutline's engine as the primitive it is — viable, considered again 2026-09-13
Recorded in section 4 as the worked example of the ship-the-primitive rule, and reconsidered
this cycle as a candidate in its own right: lift the certificate-and-cheapest-cut solver out
of the day planner and ship it as the general thing, with the planner as one demo.
Why not selected: still the same shape this repository already has three of — a command that
reads a file and prints a verdict — and the shape ban is in force until the repository holds
projects in at least three genuinely different forms. Worth doing, and it will be a better
project once a run can give the certificate a visual form rather than a printout.

