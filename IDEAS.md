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
* Include a behaviour descriptor — `{interaction model, data source, medium,
  domain}` — so repeated cells are visible. All three existing projects share one:
  reads source files, prints text, developer tooling, local CLI.
* For finalists, include the 1-5 scores (hook, reach, demo-ability, originality,
  difficulty-worth-it, monetizability) and the pairwise comparison result.
* An idea may be **moved** between sections when something real changes — a hook
  is found, prior art turns out to be weaker than it looked, the environment gains
  a capability. Moving it means editing its entry and noting what changed and
  when. It does not mean deleting the history.
* Never move an idea upward to justify building it. If the reason for the move is
  "I want to build this," that is not a reason.

---

## 0. The owner's ideas — read first, every run

Ideas from the repository owner. They are not exempt from any gate: prior art,
problem value, feasibility and the hook all apply exactly as they do to your own
candidates. But they are considered **first**, and if you pass on one you record why
here, in a sentence, so the owner can see your reasoning and push back.

Treat a half-formed entry as a seed, not a specification. "Green screen but for X",
a dataset someone noticed, a stray observation — the value is the direction. Your
job is to find the buildable, surprising version of it.

Owner: add anything here, any time, in any state. One line is enough.

### Pebble Evolve — an evolutionary loop that breeds projects instead of picking one
Added 2026-09-13, from an external analysis of this repository.

The proposal: stop selecting one project per run. Instead keep a population, mutate
it, score each child on correctness plus distance from everything already built plus
a personal taste signal, and keep the surprising winners in an archive organised by
behaviour descriptor — so the system covers the space of possible projects rather
than converging on one. Related real work, all verified to exist: AlphaEvolve
(DeepMind, 2025), FunSearch, OpenEvolve, and ShinkaEvolve (Sakana AI,
arXiv:2509.19349, Apache-2.0, reports a state-of-the-art circle packing result from
150 samples using parent sampling, code-novelty rejection sampling and bandit-based
model-ensemble selection). Quality-diversity background: MAP-Elites and novelty
search. Interestingness-as-filter background: OMNI and OMNI-EPIC.

**Status: not yet evaluated.** It has not been through the gates and must not be
started as though it had. Specific things to resolve first:

* **Prior art is crowded.** Evolutionary LLM code search is an active, published,
  open-source field. Anything resembling "an evolutionary loop over programs" fails
  the material equivalence test on its own. The parts that looked unclaimed in the
  original analysis are (a) applying this at the level of whole user-facing
  projects rather than single algorithms or functions, and (b) a taste signal
  personal to one owner rather than a generic interestingness model. Those two are
  the claim to test, and they must be searched properly, not assumed.
* **The taste model needs data that does not exist yet.** It requires a body of the
  owner's own delight ratings. There are none. Until there are, that component
  cannot be built and must not be described as though it could.
* **Novelty scores are gameable.** The original proposal included a numeric novelty
  threshold. Do not adopt that: a fabricated score violates Section 19, and
  superficially-different-but-trivial output scores well on exactly this kind of
  metric. The generation mechanics already in `AGENT_RULES.md` take the useful parts
  — tail sampling, first-idea rejection, behaviour descriptors, pairwise comparison,
  red-teaming — without inventing a number.
* **Scope.** Implemented in full this is a product, not a project in this
  repository's sense. A bounded first milestone would be a vertical slice: one
  archive, one descriptor scheme, real candidates, and a visible result — not the
  whole engine.

Also from that analysis and already adopted into the rules, so not pending:
verbalized sampling / tail sampling, rejecting your own first idea, constraint
injection, cross-domain transfer, behaviour descriptors, and the red-team pass.

**Agent response, run of 2026-09-13.** Considered first, as the section requires.
Passing on it this run, and the reason is not the crowded prior art: it is that
Pebble Evolve is machinery for choosing projects rather than a project. It produces
nothing a stranger could open, use or be surprised by, which is the thing this
repository is short of after three analyzers. The two genuinely unclaimed parts named
above — evolution at the level of whole projects, and a taste signal personal to one
owner — are also the two that cannot be built yet: the first is hard to evaluate
without many completed projects to evolve from (there are three), and the second
needs a body of the owner's own delight ratings that does not exist. The useful
mechanics have already been absorbed into `AGENT_RULES.md` and are in force in this
run: tail sampling, first-idea rejection, behaviour descriptors, pairwise comparison,
red-teaming. Worth revisiting once this repository holds enough finished work to
evolve, or once the owner starts recording ratings. Push back if you disagree — it is
your idea and the reasoning above is the whole of my objection.

### (add yours below)

---

## 1. Rejected — failed the rules

Ideas that failed a gate for reasons other than prior art: not feasible here, no
definition of done, no first step, no real problem, inside the shape ban, or
memorable but useless.

Format: **name** — date. Hook attempt. Which gate failed and exactly why.

_Entries below were rejected on a gate other than prior art. Every candidate
generated in a run is recorded somewhere in this file; see section 5 for the
ungated pool._

### viewshed atlas — "see exactly what is visible from any point on Earth, offline" — rejected 2026-09-13
p ~ 0.07. Descriptor: {query a map, public elevation rasters, interactive map, geography}.
Gate B. The core needs multi-gigabyte elevation tiles, and every run starts in a fresh
container with an empty disk, so the data would have to be re-fetched each run to do
anything at all. Also has visible prior art in the hiking world (HeyWhatsThat,
PeakFinder), unverified this run. The buildable residue — exact viewshed algorithms on
small synthetic terrain — is a toy, not the idea.

### expired-patent mechanism library — "every mechanism humanity patented, animated and free to use" — rejected 2026-09-13
p ~ 0.03. Descriptor: {browse a catalogue, bulk patent archives, animated diagrams, mechanical design}.
Gate B. The mechanisms live in scanned line drawings; extracting kinematics from them is
a vision project several times larger than the idea itself, and the text alone does not
contain the geometry. Also overlaps the existing digitised *507 Mechanical Movements*
animations. Kept because the underlying observation is good: expired patents are a large,
public, almost unused design corpus. If the drawings were ever vectorised by someone
else, this becomes buildable.

### oversize-load route feasibility — "tells a trucker which bridge will stop them" — rejected 2026-09-13
p ~ 0.04. Descriptor: {enter a route, public road and clearance data, map plus verdict, logistics}.
Gate B for the data, not the mathematics: bridge and overhead clearance data is patchy,
partly proprietary, and wrong in exactly the cases that matter. Recorded because the
geometry underneath it is the same engine as the selected project, and it becomes a
credible application if a clearance dataset ever becomes reachable.


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

### dissection engine — rejected 2026-09-13 (this run's first idea, rejected as first ideas must be)
Hook attempt: "Cuts any shape into pieces that rearrange into any other shape of the
same area." p ~ 0.08. Descriptor: {give two shapes, none, animation, recreational geometry}.
Generated first this run, which under the generation rules disqualifies it as a final
answer on its own; it then failed on prior art as well. The Wallace-Bolyai-Gerwien
construction is 190 years old and the software space is occupied:
[Weitz's interactive Polygons](https://weitz.de/polygons/) turns an arbitrary polygon into
a rectangle by animated cuts, Greg Frederickson has catalogued and
[animated](https://www.cs.purdue.edu/homes/gnf/book2/tab_anims.html) swing- and
twist-hinged dissections for decades, and
[Wang et al., Bridges 2012](https://archive.bridgesmathart.org/2012/bridges2012-49.pdf)
published an algorithm for creating dissection puzzles between two shapes. The parts I
thought were unclaimed — exact arithmetic over quadratic extensions, machine-checkable
certificates that the pieces tile both shapes — are a quality difference inside an
occupied category, which Gate E rejects.

### linkage synthesis from a drawn curve — rejected 2026-09-13
Hook attempt: "Draw any shape and get a machine of rods and hinges that traces it."
p ~ 0.06. Descriptor: {draw a curve, none, animation plus printable parts, mechanism design}.
A strong hook attached to a solved problem.
[MotionGen](https://deshpandeshrinath.github.io/assets/papers/motiongen.pdf) is a public
web and mobile app that takes sketched poses and returns four-bar linkages that achieve
them, and the generative-synthesis literature is active:
[C-VAE four-bar synthesis, JCDE 2024](https://dx.doi.org/10.1093/jcde/qwae084),
[arXiv:2402.14882](https://arxiv.org/html/2402.14882v1), and
[MechaFormer, arXiv:2508.09005](https://arxiv.org/pdf/2508.09005). Same input, same
output, same user.

### aperiodic-monotile pattern engine — rejected 2026-09-13
Hook attempt: "Wallpaper that never repeats, cut from a single tile." p ~ 0.12.
Descriptor: {set parameters, none, printable and cuttable patterns, design}.
The hat and spectre tiles are recent (2023), but the generator space filled immediately:
[shrx/spectre](https://github.com/shrx/spectre),
[christianp/aperiodic-monotile](https://github.com/christianp/aperiodic-monotile),
[vmagnin/hat_polykite](https://github.com/vmagnin/hat_polykite) (which already targets
laser cutting), and [Xuth/spectre](https://github.com/Xuth/spectre). A textures-for-
graphics angle might still be open, but it is a small idea wearing a recent discovery.

### caustic lens designer — rejected 2026-09-13
Hook attempt: "A clear sheet of plastic that throws a photograph on the wall when you hold
it up to the sun." p ~ 0.05. Descriptor: {upload an image, none, physical object, optics}.
Possibly the best hook generated this run, and thoroughly taken: Matt Ferraro's
`causticsEngineering` ([github.com/mattferraro](https://github.com/mattferraro)) is the
well-known open implementation, [dylanmsu/poisson_caustic_design](https://github.com/dylanmsu/poisson_caustic_design)
is a portable C++ one, the method comes from published work (Yue et al. 2014; Disney
Research 2014; [MIT Media Lab, Refraction](https://www.media.mit.edu/projects/refraction/overview/)),
and people are already 3D-printing caustic clock faces from it.

### fold-and-cut solver — rejected 2026-09-13
Hook attempt: "Fold the paper the way it says and one straight cut gives you any shape you
asked for." p ~ 0.05. Descriptor: {give a shape, none, printable crease pattern, origami}.
Demaine, Demaine and Lubiw proved it in 1999 and the implementations are public:
[erikdemaine.org/foldcut](https://erikdemaine.org/foldcut/),
[6849-2020/fold-and-cut-2010](https://github.com/6849-2020/fold-and-cut-2010),
[6849-2020/fold-and-cut-2017](https://github.com/6849-2020/fold-and-cut-2017),
[nadvornix/fold-and-cut](https://github.com/nadvornix/fold-and-cut), and a browser
[One-Cut Helper](https://urjudged.github.io/oneCutTheorem/).

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

_Added 2026-09-13. The entries below are this run's candidates that survived
feasibility and originality but not Gate F. Each records what the hook would have to
become._

### recoverable secret phrase — 2026-09-13
Hook attempt: "A backup phrase that still works when you misremember two of the words."
p ~ 0.04. Descriptor: {type a phrase, none, a working key, security}.
Real capability (error-correcting codes over a wordlist, in the family of fuzzy
extractors), genuinely wanted, and demonstrable in seconds. Held back for two reasons:
prior art is close and unsearched this run (fuzzy extractors, SLIP-39, published
typo-tolerant password work), and it is the one candidate whose failure mode is
somebody losing access to real money. If pursued, it needs a security argument written
before any code, not after. What would make it hyped: a demo where a deliberately
mangled phrase still opens the box, with the exact tolerance stated.

### inverse physics shot solver — 2026-09-13
Hook attempt: "Say where you want the ball to stop; it tells you how to hit it."
p ~ 0.07. Descriptor: {pick a target, none, animation, games and simulation}.
Fun, visual, and sitting inside the well-populated differentiable-physics field, with
billiards specifically already served by open simulators. Would need a capability those
do not have — proven-correct shots rather than optimised ones, say — to be worth months.

### pop-up card compiler — 2026-09-13
Hook attempt: "Print this page, cut along the lines, and a castle stands up out of it."
p ~ 0.06. Descriptor: {give a shape, none, printable paper object, papercraft}.
Excellent hook, and the demo is a photograph. Two problems: the research is published
(computational pop-up design, SIGGRAPH-era work, not searched in detail this run), and
nothing in this environment can verify that a paper mechanism actually works — only that
the simulation says so. Honest validation would have to stop at geometry.

### stable graph layout — 2026-09-13
Hook attempt: "Add one box and the diagram stays where it was." p ~ 0.10.
Descriptor: {edit a graph, user's diagram, interactive picture, visualization}.
A real and widely felt irritation, but it has an established research name (dynamic
graph drawing, mental-map preservation), which the rules treat as a signal to push
further rather than a validated gap.

### pagination that cannot skip or duplicate — 2026-09-13
Hook attempt: "An infinite scroll that never shows you the same post twice or hides one."
p ~ 0.06. Descriptor: {call an API, a changing collection, a library, backend infrastructure}.
Genuine, under-specified problem; the fix is mostly known folklore (keyset cursors,
snapshots). Fails Gate F: nothing to look at, and the surprise is only legible to people
who have been bitten.

### bidirectional spreadsheet — 2026-09-13
Hook attempt: "Type the answer you want in any cell and it tells you what the inputs have
to be." p ~ 0.08. Descriptor: {edit a sheet, user's numbers, interactive page, productivity}.
Goal Seek and Solver already occupy the obvious version; the interesting version —
every formula as a relation, solve any subset — is a real primitive but needs a
nonlinear solver and a story for why ambiguity is presented rather than hidden.

### undo for the shell — 2026-09-13
Hook attempt: "Run anything, then take it back." p ~ 0.05.
Descriptor: {run a command, the filesystem, a CLI, developer tooling}.
Feasible on Linux with overlay filesystems, and the pain is real. Sits close to existing
answers (snapshots, containers, trash tools), lands squarely in the repository's
over-occupied cell, and a tool whose failure mode is destroying files needs more
certainty than one run of searching gives.

### archive that still opens in fifty years — 2026-09-13
Hook attempt: "A file that can rebuild itself after the disk rots." p ~ 0.07.
Descriptor: {store a file, user's data, a file format, archival}.
Overlaps PAR2, BagIt and paper-backup formats (not searched this run). The honest gap
might be self-describing recovery — the archive carrying its own decoder — but that is
close to a solved trick and the demo is hard to make visible.

### perfect-play engine for arbitrary deterministic programs — 2026-09-13
Hook attempt: "Give it any program and it finds the exact inputs that beat it."
p ~ 0.04. Descriptor: {point at a binary, none, a recorded run, program analysis}.
The tool-assisted-speedrun community has done this for emulated games for twenty years;
generalising it is really symbolic execution, which is a mature field. Kept because the
framing is unusually vivid and might survive a narrower target.

### superoptimiser for spreadsheet formulas — 2026-09-13
Hook attempt: "Rewrites your spreadsheet formula into the shortest one that behaves
identically." p ~ 0.03. Descriptor: {paste a formula, user's sheet, text output, productivity}.
Small, tidy, plausibly unclaimed, and nobody would tell a friend about it.

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

### pivot — selected 2026-09-13, pending the sleep-on-it re-read
**Hook sentence:** *Finds the way to turn your sofa through the door — or proves there
isn't one, and names the centimetre that would fix it.*

One-line description: plans how to move furniture through tight spaces, or proves it
cannot be done.
Descriptor: {describe a space and an object, user's measurements, animation plus a
checkable proof, everyday logistics and geometry}. Every cell differs from the three
existing projects.

**Status: chosen, not started.** Rule 7 of the generation section requires the
shortlist to survive a re-read at the start of the next run before any implementation.
Nothing has been built. The next run re-reads this entry first, and either confirms and
starts milestone 1 or records why it changed its mind.

**What it does.** You give it a space — a floor plan, a corridor with a corner, a
stairwell described by a few measurements — and an object. It returns one of three
answers, each with evidence:

* a motion: the sequence of positions and rotations that gets the object through,
  animated, and written out as instructions a person can follow;
* a proof of impossibility: the pinch point shown, plus the smallest dimensional change
  that would make it possible ("18 mm more doorway", "take the door off its hinges");
* an explicit "too tight to decide", when the geometry falls inside the solver's stated
  resolution limit. It never guesses.

**Why this and not the others.** Scores, 1-5:

| candidate | hook | reach | demo | originality | difficulty worth it | money | 
| --- | --- | --- | --- | --- | --- | --- |
| pivot | 5 | 4 | 5 | 4 | 5 | 4 |
| pop-up card compiler | 5 | 2 | 5 | 2 | 3 | 2 |
| recoverable secret phrase | 4 | 3 | 3 | 3 | 3 | 3 |
| inverse physics shot solver | 4 | 2 | 5 | 2 | 3 | 2 |

Pairwise, on "which would I be more upset to see someone else ship first": pivot beat
the pop-up compiler (whose method is published and whose validation stops at
simulation), pivot beat the recoverable phrase (better hook on pivot, and the phrase's
failure mode is someone losing real money), pivot beat the shot solver (differentiable
physics is a crowded field and the result would be an optimisation, not a guarantee).

**Closest prior art, and what differs.** Two populated spaces, with a gap between them.

*Consumer tools* are closed-form calculators: a rectangle against a doorway, a tilt
angle from trigonometry
([example](https://enkledesigns.com/will-sofa-fit-through-door-calculator/), and many
near-identical others). The closest product is the closed-source
[Smart Moving: Furniture helper](https://apps.apple.com/us/app/smart-moving-furniture-helper/id1666262699),
whose listing says it considers rotations, angle turns and tilting; it is a measuring
app, and none of these express a floor plan, plan a path, or say anything when the
answer is no.

*Research* has the hard version and no usable artifact. Exact planners date to the
1980s; the cylindrical-algebraic-decomposition route to the original piano-movers
formulation is described as still infeasible after 25 years of improvement
([arXiv:1309.1588](https://arxiv.org/pdf/1309.1588)). Yap and colleagues' soft
subdivision search gives *resolution-exact* planners for SE(2)
([arXiv:1704.05123](https://arxiv.org/abs/1704.05123),
[arXiv:1903.09416](https://arxiv.org/abs/1903.09416)) — the guarantee is stated
relative to a resolution parameter, and no public implementation surfaced in this
run's searches. Infeasibility proofs are an active topic
([arXiv:2406.04795](https://arxiv.org/pdf/2406.04795),
[arXiv:2501.11434](https://arxiv.org/pdf/2501.11434)). The "smallest change that makes
it possible" idea is **not new either**: minimum constraint removal and minimum
constraint displacement are established
([arXiv:2305.01272](https://arxiv.org/pdf/2305.01272)). Industrial CAD tools do
collision-free extraction paths (Siemens NX; Autodesk's *Assemble Them All*,
SIGGRAPH Asia 2022), for CAD assemblies and not for rooms, and not with a proof you
can check. Open-source sampling planners (OMPL) cannot answer "no" at all.

The distinguishing capability to be tested, stated as a claim that could fail: an
open, offline planner that answers the everyday question from ordinary measurements,
and whose three possible answers each come with something a person can verify — a
certified-clear motion, a certified blocking cover, or an honest refusal. Novelty
confidence will not exceed Medium given the research above, and the README will say so.

**Red team, argued in bad faith, then answered.**

1. *"It is a sofa calculator with extra steps."* — The calculators cannot represent an
   L-shaped corridor, a landing, or a doorway with a radiator beside it, and give no
   answer at all when the object does not fit. The test that settles this: cases those
   tools cannot even express must be the demo, not the edge case.
2. *"A stranger shrugs — people just try it and find out."* — They do, and then they
   damage the wall or pay movers to take a window out. The demo answers this rather
   than the argument: an animation of the turn, and a red pinch point with a number
   next to it.
3. *"Certificates and exact arithmetic are the author's private pleasure."* — If it
   says yes and the answer is wrong, the product is worthless; exactness is the
   product. And the "18 mm" answer only exists because the geometry is exact.
4. *"Yap already did this."* — Resolution-exactness answers relative to a parameter;
   this aims at a checkable certificate and an honest refusal instead. That difference
   is real but narrow, which is why confidence is capped at Medium and SSS is named at
   the top of the README rather than buried.
5. *"You will ship 2D and call it finished."* — The definition of done in `TASKS.json`
   includes the 3D stairwell case, and milestone status is per-milestone. If 3D
   defeats the approach, that is Outcome D — written down as a failure, not relabelled
   as success.

**Late find, recorded against my own interest (2026-09-13).** After the decision, a
further search turned up C-IRIS: certified collision-free convex regions in a rational
parameterisation of configuration space, via sums-of-squares, **already implemented and
open source in Drake** ([arXiv:2302.12219](https://arxiv.org/pdf/2302.12219),
[arXiv:2205.03690](https://arxiv.org/pdf/2205.03690),
[arXiv:2410.12649](https://arxiv.org/pdf/2410.12649)). It uses the same tangent
half-angle substitution this project intended to use. It targets robot manipulators,
certifies free regions rather than impossibility, and depends on an SOS solver — but
the "certified free space by exact arithmetic" part of the plan is not new and must not
be presented as new. What survives: the **"no" answer** with a certificate a person can
check, the smallest dimensional change that would fix it, and the everyday problem
framing with no solver dependency. The confirmation re-read must decide whether that
residue is enough. If it is not, drop the candidate rather than rewording it.

Also found, and different problems rather than prior art: the
[moving sofa problem](https://en.wikipedia.org/wiki/Moving_sofa_problem) asks for the
largest shape that can turn a corner, and [SofaBounds](https://github.com/ykallus/SofaBounds)
computes bounds for it. Demand evidence, for the README: professional movers do this by
hand, measuring each narrow point and reasoning about the piece's diagonal against the
door height, and moving-industry software addresses pricing and surveys rather than
geometry.

**Alternate names considered:** `jamb`, `shoehorn`, `wiggle`. `pivot` won on
memorability; the collision with the common word is a known cost.

---

_This entry replaced the "no project currently selected" note that stood here since
the consolidation. It is the first candidate chosen under the full rule set._

---

## 5. Pool — generated this run, not yet gated

The generation rules require at least 20 candidates recorded before any gate runs.
Sections 1 to 4 hold the ones that were gated. This section holds the rest: real
candidates, generated and written down, not yet searched or scored. They cost nothing
to keep and a future run starts from them instead of from nothing.

Move an entry up into sections 1-4 when it is actually gated, and record what the
search found. "Prior art suspected" below means exactly that — a recollection, not a
search result, and not to be repeated as fact.

Generated 2026-09-13 (p = rough probability that any agent would produce this idea;
the rules ask for tails, so low is the point):

* **container and truck loading, with the move included** — p 0.05. {plan a load, user's
  dimensions, animation, logistics}. Not just whether the boxes fit by volume but
  whether they can physically be got in through the door. Same engine as `pivot`;
  recorded as a later application rather than a rival.
* **smallest doorway that passes a given object** — p 0.03. {design query, user's object,
  a number and a drawing, architecture}. The inverse of `pivot`, for architects sizing
  equipment routes; the same engine run backwards.
* **sheet-goods nesting and cut lists** — p 0.15. {upload parts, user's geometry, cut
  diagram, fabrication}. Prior art suspected and strong (Deepnest, SVGnest,
  OpenCutList). Modal idea; recorded so no future run re-generates it blind.
* **paper backup with error correction** — p 0.06. {print a page, user's file, paper,
  archival}. Prior art suspected (PAR2, paperbak, Optar, Colorsafe).
* **one converter for every CAD and mesh format** — p 0.09. {convert a file, user's
  models, files, engineering}. Prior art suspected (assimp, meshio, OpenCASCADE).
* **room acoustics from a floor plan** — p 0.08. {draw a room, none, audio, acoustics}.
  Prior art suspected (pyroomacoustics and the FDTD literature).
* **embroidery and knitting machine formats** — p 0.05. {convert a design, machine
  formats, stitched object, textiles}. Prior art suspected (pyembroidery).
* **offline tide prediction anywhere** — p 0.06. {ask for a place and date, public
  harmonic constants, chart, marine}. Prior art suspected (XTide).
* **transit isochrones, offline and instant** — p 0.07. {click a map, public GTFS feeds,
  map, transport}. Prior art suspected (OpenTripPlanner, r5).
* **shape search for mechanical parts** — p 0.04. {sketch a part, a parts catalogue,
  search results, making}. Blocked mainly by catalogue terms of use.
* **a file that renders itself anywhere** — p 0.07. {open a file, user's data, the file
  itself, formats}. Self-describing polyglot data; suspected to be a known trick.
* **explain this pixel** — p 0.04. {click an output, a running program, an interactive
  trace, developer tooling}. Click any output and see the exact chain of operations
  and inputs that produced it. Closest known relative: the Whyline, and dynamic
  program slicing.
* **exact-arithmetic 2D physics with perfect replay** — p 0.05. {run a simulation, none,
  animation, games and systems}. Deterministic to the bit on any machine, rewindable
  exactly. The open question is whether rational coordinates stay bounded through
  collisions; if they do not, the idea is dead and that is worth knowing.
* **a drum machine driven by how you type** — p 0.03. {type, your own keystrokes, audio,
  toys}. Recorded as a tail sample. Charming, small, no claimed capability.
* **filesystem where unopened files decay** — p 0.02. {leave files alone, your own disk,
  a filesystem, art}. Pure tail sample; almost certainly fails Gate A.
