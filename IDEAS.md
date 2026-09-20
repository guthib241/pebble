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

**Status: considered first on 2026-09-20, not selected on that run.** It has now
been through Phase 1 consideration once; it has *not* been through a full search,
and must not be started as though it had. Specific things to resolve first:

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
**Decision of 2026-09-20, for the owner to push back on.** Passed over this run,
for three reasons, none of which is "it is too hard":

1. The taste model is still the distinguishing claim, and it still has no data.
   The blocker is unchanged since the idea was written down, and no run can clear it
   by trying harder — only the owner can, by rating things.
2. The core loop remains crowded, and this run has no search of its own to add.
3. The specific reason it was not picked *this* run: the run's job was to choose a
   project, and choosing to build a project-choosing engine instead is the most
   comfortable way to avoid that job. That is a self-serving move and it should be
   named as one.

**What would unblock it, concretely.** The taste data can start accumulating now, at
no cost, from two files that already exist: every entry the owner adds to
`REFERENCES.md` is a positive rating with a stated reason, and every pairwise
comparison recorded in this file is a preference between two specific candidates.
Twenty or thirty of those, accumulated across runs, is a real signal about one
person's taste — and it is the thing no other evolutionary code-search system has.
Until then the component cannot be built, and describing it as buildable would be a
Section 25 violation.

* **Scope.** Implemented in full this is a product, not a project in this
  repository's sense. A bounded first milestone would be a vertical slice: one
  archive, one descriptor scheme, real candidates, and a visible result — not the
  whole engine.

Also from that analysis and already adopted into the rules, so not pending:
verbalized sampling / tail sampling, rejecting your own first idea, constraint
injection, cross-domain transfer, behaviour descriptors, and the red-team pass.

### (add yours below)

---

## 1. Rejected — failed the rules

Ideas that failed a gate for reasons other than prior art: not feasible here, no
definition of done, no first step, no real problem, inside the shape ban, or
memorable but useless.

Format: **name** — date. Hook attempt. Which gate failed and exactly why.

### Pool of 2026-09-20 — candidates rejected on the rules, without a search

Each of these failed a gate that costs nothing to apply, so no usage was spent
searching them. Where prior art is also suspected it is named as a lead for anyone
who revives the idea, not as a finding: nothing below was verified, and a revival
must search it properly.

* **C1 cutline-core** — "Proves your plan is impossible, then tells you the single
  cheapest thing to drop." Inside the shape ban: its interface is run a command,
  read a report, and Gate E counts `projects/cutline/` as prior art against it.
  Stays available, and remains the repository's best-known unshipped primitive —
  but it has to arrive in a form you can see, not as a second CLI over the same
  solver. Recorded again here because it is this repository's mode: it is the
  candidate that will keep re-appearing, and re-appearing is not an argument.
* **C4 crontab futures** — "Shows you the month your crontab is actually going to
  have." Gate A: thin. `AGENT_RULES.md` names it as the not-yet-done version of the
  settled cron-linter rejection, so it stays available, but a month-view of a
  schedule is a weekend of work and does not deserve the next several runs.
* **C11 severed streets** — "Shows you every street in your city that used to
  connect and no longer does." Rejected on Section 25 rather than prior art, which
  the search did not find. OpenStreetMap history records *edits to the map*, not
  *changes to the world*: the overwhelming majority of a "lost connection" signal is
  someone fixing a mis-drawn junction years later. The hook would therefore be a
  false statement about what the code observes. It would need an independent
  ground-truth source of real closures to become honest, and that source is the
  actual project.
* **C14 semantic database merge** — Gate F: "merge for databases" is a category
  label. Leads: Dolt, `sqldiff`.
* **C15 knitting notation** — Gate B: the output is a file for a machine this
  environment cannot reach, so the core claim could never be validated here. Lead:
  knitout, and CMU's autoknit line of work.
* **C16 splat type** — Gate A: no capability. Outlines are already resolution
  independent; the candidate offers a different representation of a solved problem.
* **C17 open-instance puzzle game** — "Every level you beat is a record nobody has
  beaten." Gate D: unbounded. Curating genuinely open instances and verifying
  claimed records is the project, and it has no definition of done. Lead: Foldit,
  EteRNA, EyeWire.
* **C18 routing weather** — Gate A: sonifying BGP churn supports no decision anyone
  has to make. Memorable and useless still fails.
* **C19 filesystem undo / C22 what the program saw** — Gate B and Section 25: a
  syscall trace does not contain what an overwrite destroyed, so "undo what that
  script did" cannot be true in general, and the honest version of the hook is much
  smaller than the hook. Leads: `rr`, CRIU.
* **C21 rigid-body typography** — Gate A: a toy, and a well-populated one.
* **C25 typed instrument** — Gate A: no capability beyond the novelty of the
  mapping.
* **C26 GPS from first principles** — Gate E: GNSS teaching material and
  trilateration explorables are abundant.
* **C27 watch it heal** — Gate E and ambition: Reed–Solomon visualisations are a
  standard teaching artifact.
* **C23 format archaeology** — not rejected, and not a candidate either: it is a
  technique with no target attached. It becomes a candidate when a specific
  under-documented format is named and shown to be lawfully obtainable here.

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

---

### echo-to-geometry ("hear the shape of a room") — rejected (2026-09-20)
Hook attempt: "Clap once in an empty room and it draws you the walls."
Was the strongest candidate of the 2026-09-20 pool (C5) before searching. The core
capability — recovering room geometry from echo arrival times — is a published and
still-active research field with open implementations and public datasets.
Prior art: [Dokmanić et al., "Acoustic echoes reveal room shape", PNAS
2013](https://www.pnas.org/doi/10.1073/pnas.1221464110) (the method: echo sorting
via Euclidean distance matrices, full 3D convex room from one emission);
[graph-based echo labeling, ICASSP
2016](https://sps.ewi.tudelft.nl/pubs/heusdens16icassp1.pdf); [EchoScan, IEEE/ACM
TASLP 2024](https://arxiv.org/abs/2310.11728) (neural room-floorplan inference,
handles curved walls, demos and code released); ["Hearing the Shape of a Cuboid
Room Using Sparse Measure Recovery", 2025](https://arxiv.org/pdf/2509.08443);
[dEchorate calibrated RIR database](https://arxiv.org/pdf/2104.13168) with
echo-aware baselines; and [pyroomacoustics](https://github.com/LCAV/pyroomacoustics)
from the same lab as the PNAS work. Material equivalence on the core capability,
with the workflow (impulse response in, geometry out) matching. Reproducing it
would be an open implementation of a method that already has open implementations.

### isospectral drums — rejected (2026-09-20)
Hook attempt: "Draw any shape and hear it ring — then meet two different shapes
nobody can tell apart by ear."
Prior art: [eigendrum.com](https://eigendrum.com/)
([source](https://github.com/BaselAshraf81/eigendrum)). Inspected directly: it
meshes a drawn outline, builds finite-element stiffness and mass matrices, solves
for the smallest eigenvalues, plays the result, lets you audition one mode at a
time, and ships the Gordon–Webb–Wolpert isospectral pair as two presets. That is
the candidate, including the part that was supposed to be its surprise.

### TrueType hinting, made visible — rejected (2026-09-20)
Hook attempt: "Every letter on your screen runs a tiny program that decides where
its edges land."
Prior art: [FontLab TTH Debugger](https://studio.fontlab.com/). Inspected
directly: a browser tool where you load a TrueType font, pick a glyph and a ppem,
and step FreeType's bytecode interpreter one instruction at a time with the
outline, raster, stack and graphics state updating live. Same artifact, same
medium, same mechanism. Offline debuggers (FontForge, Microsoft VTT) are the older
prior art behind it.

### regex disagreement witnesses — rejected (2026-09-20)
Hook attempt: "Paste two regular expressions; it hands you the strings where they
disagree."
Prior art: [RegExp Equivalence Checker](https://gruhn.github.io/regex-utils/equiv-checker.html)
— enter two regexes, get a verdict on whether they match the same language and, when
they do not, example strings matching one but not the other. Same inputs, same
mechanism (automata difference), same output, same deployment.

### reflowing mathematical typesetting — rejected (2026-09-20)
Hook attempt: "Long equations that fold to fit your phone, the way sentences do."
Generated in the second wave as an enabling primitive (2D line-breaking over
expression trees). Prior art: [MathJax v4 automatic line
breaking](https://docs.mathjax.org/en/v4.0/output/linebreaks.html), which shipped
in-line and display breaking plus scaling and scrolling for wide equations, and the
LaTeX `breqn` package before it. The dominant library now covers the capability.

### puzzles with a proof of uniqueness, graded by derivation length — rejected (2026-09-20)
Hook attempt: "Every puzzle comes with a proof there is exactly one answer, and a
measure of how hard it really is."
Prior art: [Generating and Solving Logic Puzzles through Constraint Satisfaction,
AAAI 2007](https://cdn.aaai.org/AAAI/2007/AAAI07-361.pdf) — a generator framework
that guarantees unique solutions, guarantees solvability by inference alone, and
grades difficulty by the inference required. Grading by which solving techniques a
board forces is standard practice in puzzle generators, and Simon Tatham's
collection is the long-standing playable version.

### digital joins for fragmentary manuscripts — rejected (2026-09-20)
Hook attempt: "Feeds it a pile of manuscript scraps and it shows you which two came
off the same page eight centuries ago."
The most striking candidate of the second wave. Rejected on a combination of
crowded research and Gate B. Prior art: [Identifying Join Candidates in the Cairo
Genizah, IJCV 2010](https://link.springer.com/article/10.1007/s11263-010-0389-8)
and the ICCV-W 2009 paper before it, ongoing work through [Bag of Bags,
2026](https://arxiv.org/pdf/2604.08138). Feasibility: the fragment image corpora
are behind project logins rather than open bulk download, and the method wants GPU
work this environment does not have. No open tool was found, which is the one real
gap — but an open reimplementation of an actively published method, on data this
environment cannot lawfully bulk-download, is not the project.

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

### C24 schedule algebra — generated 2026-09-20
Hook attempts, all flat: "An algebra where 'this plan cannot work' is something you
can prove and check by hand." / "Turns 'we cannot fit this' into a proof." Passes
Gate A (a real capability: minimal infeasible subsets with independently checkable
certificates), Gate B, and Gate D. Fails Gate F: the sentence needs a paragraph
before it becomes interesting, and the ten-second artifact is a certificate, which
is text. It is also `cutline`'s engine wearing formal clothes, so Gate E is close.
What would make it hyped: a form in which you can *see* the proof — the
over-subscribed window as a picture that a stranger reads without being told what a
certificate is. Until then it is the mode this repository keeps returning to.

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

_No project currently selected. The next entry here is the first one chosen under
the full rule set, and it should be the best idea this repository can find rather
than the first that qualifies._

---

## 5. Live pool — generated, outcome not yet resolved

Candidates generated but not yet resolved to one of the sections above. An entry
leaves this section the moment it resolves, and is rewritten under the heading that
matches its outcome. Nothing is deleted on the way out.

Each entry records: date generated, hook attempt, behaviour descriptor
`{interaction model, data source, medium, domain}`, the rough probability that this
is the candidate a language model would produce first (low is what we are hunting —
the tail, not the mode), and the enabling question: *if this works, what becomes
buildable that wasn't?*

### Pool generated 2026-09-20 (run: `claude/intelligent-mendel-eju50j`)

Generated before any gate was applied, per the quota rule. 27 candidates. The first
idea generated was **C1**, and it is rejected as a final answer on principle before
any of its merits were considered; it stays recorded.

**Sources passed through this round:** the owner's section 0; the repository's own
back catalogue and the unshipped primitive noted in `PROGRESS.md`; published-method
reproduction (papers whose method has no clean open implementation); undocumented
and under-documented binary formats; public datasets nobody has done much with
(OSM history, Wiktionary, RouteViews BGP, public room-impulse-response corpora,
GPS trace dumps); recent capability unlocks (WebGPU/WASM in browsers, cheap
eigen-solvers, splat representations); things done by hand repeatedly; and
cross-domain transplants (acoustics → geometry, automata → developer tooling,
spectral theory → play).

| # | Candidate | Hook attempt | Descriptor | p(mode) |
|---|-----------|--------------|------------|---------|
| C1 | **cutline-core** — extract cutline's infeasibility-certificate + minimal-cut solver as a standalone primitive with several demos | "Proves your plan is impossible, then tells you the single cheapest thing to drop." | text in → text out, own prior code, CLI, scheduling | 0.35 |
| C2 | **live unit propagation** — units flowing through an expression as you type (orbiter's hook, fixed) | "Watch milliseconds turn into seconds as you type the expression." | live editor, source text, web, developer tooling | 0.25 |
| C3 | **retry fan-out animation** — backfire's call-graph multiplication, animated | "One click, thirty requests: watch your retries multiply down the call graph." | animation, source text, web, developer tooling | 0.20 |
| C4 | **crontab futures** — render what a crontab will actually do next month, DST and all | "Shows you the month your crontab is actually going to have." | calendar render, config text, web, ops | 0.30 |
| C5 | **echo-to-geometry** — recover a room's walls from one impulse response across a few microphones | "Clap once in an empty room and it draws you the walls." | audio in → geometry out, public RIR corpora, visual, acoustics | 0.03 |
| C6 | **isospectral drums** — draw a shape, hear it ring; meet the two different shapes that ring identically | "Draw any shape and hear it ring — then meet two different shapes nobody can tell apart by ear." | playable canvas, computed eigenmodes, web+audio, spectral geometry | 0.04 |
| C7 | **hinting VM, visible** — the TrueType bytecode inside a glyph, stepped and animated at 9px | "Every letter on your screen runs a tiny program that decides where its edges land." | stepper/explorable, font binaries, web, typography | 0.05 |
| C8 | **regex disagreement witnesses** — given two regexes, produce the exact strings where they differ | "Paste two regular expressions; it hands you the strings where they disagree." | two inputs → witness list, user input, web/library, automata | 0.08 |
| C9 | **shape grep for time series** — a pattern language for "rises, plateaus, then spikes" | "Grep, but the pattern is the shape of the line." | query language, numeric series, library, data | 0.07 |
| C10 | **traffic light inference** — recover signal cycle length and offset from anonymous GPS traces | "From a pile of anonymous GPS tracks, it works out how long each light stays red." | inference → map animation, public GPS traces, visual, transport | 0.05 |
| C11 | **severed streets** — every connection a city has lost, mined from OSM edit history | "Shows you every street in your city that used to connect and no longer does." | map animation, OSM history, visual, cities | 0.04 |
| C12 | **etymology descent** — watch a word travel across languages and centuries as a graph | "Type a word and watch it walk back through every language it passed through." | explorable graph, Wiktionary dumps, web, linguistics | 0.06 |
| C13 | **greppable compression** — a log codec you can search without decompressing | "Search a compressed log without decompressing it." | codec + query, log data, library, systems | 0.06 |
| C14 | **semantic database merge** — three-way merge for SQLite with real conflict detection | "Merge two copies of a database the way you merge two copies of a file." | merge tool, db files, CLI/library, data | 0.10 |
| C15 | **knitting notation** — one notation compiling to chart, machine file, and written pattern | "One line of notation becomes a chart, a written pattern, and a file a machine can knit." | compiler, notation, visual + machine, textiles | 0.03 |
| C16 | **splat type** — glyphs represented as Gaussian splats rather than outlines | "A typeface made of blurs that stays sharp at every size." | renderer, font outlines, visual, typography | 0.02 |
| C17 | **open-instance puzzle game** — every level is a genuinely unsolved combinatorial instance | "Every level you beat is a record nobody has beaten." | playable game, open problem instances, web, human computation | 0.03 |
| C18 | **routing weather** — the internet's global routing churn, as sound | "Listen to the internet's routing tables the way you'd listen to weather." | sonification, RouteViews BGP archives, audio, networks | 0.03 |
| C19 | **filesystem undo** — reconstruct and reverse what a program did to your disk, from its syscall trace | "Undo what that install script did, step by step, after the fact." | replay/inspect, syscall traces, CLI+visual, systems | 0.04 |
| C20 | **guaranteed plots** — graph any function with mathematically proven pixels, using interval arithmetic | "A graph where every pixel is proven, not sampled." | plotter, user formula, visual, numerics | 0.05 |
| C21 | **rigid-body typography** — a layout engine where letters are physical objects with mass | "Type a sentence and watch the words fall into place." | simulation, text, web animation, typography | 0.02 |
| C22 | **what the program saw** — reconstruct a program's picture of the world from its syscalls, animated | "A film of what your program thought the world looked like." | animation, syscall traces, visual, systems | 0.03 |
| C23 | **format archaeology** — pick one under-documented consumer binary format, specify it, ship a clean reader | "Reads the file format nobody wrote down, and shows you what is inside it." | reader + spec, device files, visual, reverse engineering | 0.05 |
| C24 | **schedule algebra** — a small formal calculus of commitments, with checkable certificates | "An algebra where 'this plan cannot work' is something you can prove and check by hand." | formal system + library, none, library, formal methods | 0.15 |
| C25 | **typed instrument** — an instrument whose timbre is the phonetics of what you type | "Type a word and hear the word, not a note." | playable instrument, typed text, audio, music | 0.04 |
| C26 | **GPS from first principles** — compute a real fix from real ephemeris, step by visible step | "Watch four satellites argue their way to your exact position." | explorable, public ephemeris, web, navigation | 0.06 |
| C27 | **watch it heal** — scratch a disc, watch Reed–Solomon put the bytes back | "Scratch the disc and watch the missing bytes come back." | playable, own data, web, coding theory | 0.05 |

**Constraint injection applied to the leaders** (per the generation rules): C5 under
"one microphone only, no array" becomes a materially harder and more interesting
problem; C6 under "sound only, no picture" becomes an ear-training toy; C8 under
"no text output, only examples" becomes the witness table that is now its whole
interface; C7 under "must run with no font files shipped" points at reading the
system's own fonts.

#### Resolution of the 2026-09-20 pool

| Candidate | Outcome |
|---|---|
| C1, C4, C11, C14–C19, C21, C22, C25–C27 | → §1, rejected on the rules, reasons recorded there |
| C2, C3 | already recorded in §3 as the unfixed hooks of `orbiter` and `backfire`; no new outcome |
| C5, C6, C7, C8 | → §2, rejected on verified prior art, inspected directly |
| C23 | technique without a target; stays in the pool until a specific format is named |
| C24 | → §3, passes the rules, hook is flat |
| C9, C10, C12, C13, C20 | **unresolved — leads recorded, not yet searched** (below) |

#### Unresolved, and not to be re-generated before they are searched

These have suspected prior art that was **not** verified this run. They are not
rejections. Search them before spending any usage re-inventing them.

* **C9 shape grep for time series** — lead: ShapeSearch (MIT, 2019), and the
  query-by-sketch line of time-series work.
* **C10 traffic light inference from GPS traces** — lead: signal phase and timing
  estimation from probe vehicle data is a substantial transport-research literature,
  and the capability ships inside commercial navigation products.
* **C12 etymology descent** — lead: etytree, Etymology Explorer, Wiktionary-derived
  graph projects.
* **C13 greppable compression** — lead: CLP (Compressed Log Processor), and the
  seekable-zstd family.
* **C20 guaranteed plots** — lead: GrafEq and `graphest`, both interval-arithmetic
  graphers.

### Second wave, 2026-09-20 — generated after the first four leaders died

Generated deliberately outside the band that had just failed (see the finding
below). Three were searched and rejected; the rest are recorded unsearched.

| # | Candidate | Hook attempt | Status |
|---|---|---|---|
| W1 | reflowing mathematical typesetting | "Long equations that fold to fit your phone, the way sentences do." | → §2, MathJax v4 |
| W7 | puzzles with a uniqueness proof, graded by derivation length | "Every puzzle comes with a proof there is exactly one answer." | → §2, AAAI 2007 |
| W10 | digital joins for fragmentary manuscripts | "Shows you which two scraps came off the same page eight centuries ago." | → §2, IJCV 2010 + Gate B |
| W2 | **local time before 1970, with citations** | "Tells you what a clock in this town actually read in 1911, and shows you the law that changed it." | unsearched — leads: tzdb's own pre-1970 disclaimer and the 2021–22 zone-merging controversy |
| W4 | dependency resolution explained by minimal conflict certificates | "Tells you the smallest set of requirements that cannot all be true." | unsearched — strong lead: PubGrub already does derivation-tree explanations |
| W5 | machine knitting or brick builds from a 3D mesh | "Hand it a model, get something a machine can actually make." | unsearched — leads: CMU autoknit, legolization research |
| W6 | a movement notation a computer can animate | "Write down a dance the way you write down a tune." | unsearched — leads: Labanotation editors |
| W8 | heavy compute over a large public dataset with no server | "Query a hundred gigabytes from a page with nothing behind it." | unsearched — strong lead: DuckDB-WASM, hyparquet, HTTP range requests |
| W9 | OEIS searched by growth and shape rather than by terms | "Find the sequence you cannot remember any terms of." | unsearched — lead: OEIS SuperSeeker |

### The finding this run paid for

Four candidates from the first wave were strong enough to search hard. All four
already existed, and in three of them the existing thing was the *whole* candidate
including the part that was supposed to be surprising: eigendrum ships the
isospectral pair as a preset, FontLab ships the instruction-stepping debugger in a
browser, the equivalence checker ships the disagreement witnesses. That is not bad
luck four times.

The band being searched was: *one self-contained artifact, buildable by a skilled
person in a few weekends, whose appeal is obvious the moment you describe it.* That
band is saturated, and it is saturated **because** the appeal is obvious. Gate F
selects for ideas whose value is legible at a glance; legible-at-a-glance is exactly
what everyone else can see too. Gate F and Gate C pull against each other, and
nothing in the rules said so until now.

What survives the tension is an idea whose appeal is obvious *once shown* but whose
construction is not cheap. Three bands, and the next wave should be generated inside
them rather than by free association:

1. **Past the stopping point.** Work where a correct version demands sustained
   effort far beyond where a hobby project stops and beyond what one paper needs.
   The reference file is full of these: SQLite's test suite, ffmpeg's format
   coverage.
2. **A resource that does not exist.** Assemble the dataset, specification, or
   corpus whose absence people work around daily. Nobody duplicates this by
   accident, and it compounds.
3. **An unusual vantage point.** A combination visible only from somewhere few
   people stand — and this repository does stand somewhere specific.

A fourth thing to hold onto: do not treat "nobody built it" as the finding. C11 died
with no prior art at all, because the data could not support the sentence. Absence
of prior art is as often a verdict on the idea as an opening.
