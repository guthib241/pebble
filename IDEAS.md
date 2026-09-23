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


**Considered again 2026-09-23. Not selected this run, and not rejected.** One search
was run to advance it rather than defer it again: `LLM evolutionary search over whole
software projects quality diversity archive open-ended project generation 2026`. The
field is more crowded than it was in 2025, not less — MAP-Elites-plus-LLM archives are
now routine, OpenEvolve combines island evolution with a low-dimensional MAP-Elites
archive, ShinkaEvolve adds weighted archive sampling and novelty filters, and 2026
work extends quality-diversity search into red-teaming, materials discovery and test
generation ([LEVI](https://arxiv.org/pdf/2605.09764),
[DEI](https://arxiv.org/pdf/2605.27130),
[QD for LLM safety](https://arxiv.org/abs/2606.00801),
[LLEMA](https://github.com/scientific-discovery/LLEMA)).

What that search did **not** settle, and what a future run must search before this can
be selected: whether anyone runs evolution at the level of *whole user-facing projects*
rather than single functions, algorithms or prompts. That is still the one claim worth
testing, and it remains untested.

The second distinguishing claim — a taste signal personal to this repository's owner —
is still unbuildable for the same reason as before: it needs a body of the owner's own
delight ratings, and none exist in the repository. `REFERENCES.md` is the closest thing
to that data and currently holds ten entries, all of them inherited examples rather than
ratings of candidates this system produced. Until the owner has rated real candidates,
this component cannot be built and must not be described as though it could.

Honest reason for passing this run: the part that is buildable today is the part that is
crowded, and the part that would distinguish it needs data that does not exist yet. That
is a sequencing problem, not a verdict on the idea.

### (add yours below)

---

## 1. Rejected — failed the rules

Ideas that failed a gate for reasons other than prior art: not feasible here, no
definition of done, no first step, no real problem, inside the shape ban, or
memorable but useless.

Format: **name** — date. Hook attempt. Which gate failed and exactly why.

### How the 2026-09-23 pool was generated

Thirty candidates were generated before any gate was applied, in one pass, across
sections 1 through 4 of this file. Sources passed through: the owner's section 0,
reverse-engineering targets, unexploited datasets, published methods with no usable
implementation, cross-domain transplants, things done by hand repeatedly, and
constraint injection (no text, sound only, one file, must be legible in ten seconds).
The first idea generated was recorded and rejected as a final answer, as required.

**Honesty note on the entries in this section.** Four candidates were searched properly
this run and are filed in section 2 with links. The candidates below that name prior art
were rejected on **recalled** prior art, not on a search performed this run. The named
work is from memory and is unverified. Any future run that wants to revive one of these
must search it first and record what it found — do not treat these names as evidence.

### cutline's engine as a standalone library — 2026-09-23 (FIRST IDEA, rejected as final answer)
Hook attempt: "Proves a set of commitments cannot all be met and names the cheapest one
to drop." Descriptor: {batch command, user text file, text, planning}.
This is the move the repository's own notes suggest, which is exactly why it is the mode:
any agent reading `PROGRESS.md` would produce it. Rejected as a final answer under the
first-idea rule, and separately it lands in the occupied cell — the same run-a-command,
read-a-report shape the shape ban exists to stop. **Kept as a component, not a project:**
the minimal-conflict idea inside it survives into the 2026-09-23 shortlist as one part of
a different thing, which is the right use for it.

### Program sonification debugger — 2026-09-23
Hook attempt: "You hear your program run, and a bug sounds wrong before you can see it."
Descriptor: {listening, execution traces, audio, developer tooling}. Constraint-injected
candidate (sound only, no screen). Fails on validation, not on hook: the central claim —
that a listener notices a fault sooner by ear — cannot be established here without human
listeners, and Section 19 forbids asserting it without evidence. What remains buildable
is a sonifier whose value claim cannot be tested, which fails Gate A. Recalled prior art
(unverified): program-sonification research, Sonic Pi as a substrate.

### Explorable-explanation compiler — 2026-09-23
Hook attempt: "Write a derivation in plain text; every number in it becomes draggable."
Descriptor: {reading and dragging, author's prose, web, education}. Recalled prior art
(unverified): Tangle.js, Idyll, Observable. Crowded category with mature entries.

### Time-travel state scrubber — 2026-09-23
Hook attempt: "Scrub your running program backwards like video." Descriptor: {scrubbing,
program state, web, developer tooling}. Recalled prior art (unverified): rr, replay.io,
Redux DevTools. Materially covered.

### Optical-flow text diff — 2026-09-23
Hook attempt: "Diffs text the way a video codec tracks motion, so moved blocks read as
moves." Descriptor: {reading, two files, text, developer tooling}. Recalled prior art
(unverified): difftastic, `git --color-moved`. Also inside the shape ban.

### Error-correcting human-readable identifiers — 2026-09-23
Hook attempt: "Identifiers that catch their own typos when a person reads them aloud."
Descriptor: {typing, identifiers, text, systems}. Recalled prior art (unverified):
Crockford base32, Damm and Verhoeff checksums, what3words. Solved several times.

### Polyglot file format — 2026-09-23
Hook attempt: "One file that is a valid image and a valid archive at the same time."
Descriptor: {opening a file, bytes, file, systems}. Fails Gate A: no concrete problem,
novelty alone. Recalled prior art (unverified): PoC||GTFO.

### Lossy compression for logs that keeps queries exact — 2026-09-23
Hook attempt: "Throws away the words in your logs and keeps the answers." Descriptor:
{querying, log streams, text, systems}. Recalled prior art (unverified): CLP, LogZip.

### CRDT for vector drawings — 2026-09-23
Hook attempt: "Two people edit the same drawing offline and it merges without a
conflict." Descriptor: {drawing, shared document, canvas, collaboration}. Recalled prior
art (unverified): Automerge, Figma's published model. Materially covered.

### Pattern language for 2D grids — 2026-09-23
Hook attempt: "Regex, but it matches shapes in a grid instead of characters in a line."
Descriptor: {querying, tilemaps and images, text, systems}. Recalled prior art
(unverified): MarkovJunior, Wang tiles, 2D pattern-matching literature.

### TrueType hinting bytecode visual debugger — 2026-09-23
Hook attempt: "Watch a letter bend itself onto the pixel grid, one instruction at a
time." Descriptor: {step-through, font binaries, canvas, typography}. Strong reverse-
engineering candidate, and the demo would land. Recalled prior art (unverified):
Microsoft's Visual TrueType, FreeType's ftgrid, FontForge's hinting debugger — this is
precisely what VTT was built for. Revive only with a search.

### Motion-preserving, identity-destroying video codec — 2026-09-23
Hook attempt: "A recording where you can see exactly what happened and never who did
it." Descriptor: {watching, video, video, privacy}. Recalled prior art (unverified):
a large video-anonymisation literature. Also Gate B: no GPU here, and the claim that
identity is unrecoverable would need an attack model this run cannot validate.

### Packing planner for a van or a suitcase — 2026-09-23
Hook attempt: "Tells you the order to load the van and proves it all fits." Descriptor:
{planning, an inventory, 3D view, logistics}. Monetizable and real, which Gate A now
counts equally. Recalled prior art (unverified): a mature commercial load-planning
sector. Also structurally close to `cutline` — same feasibility-plus-certificate core in
a different costume.

### Three centuries of punctuation — 2026-09-23
Hook attempt: "Watch the semicolon die, one decade at a time." Descriptor: {reading a
chart, Project Gutenberg, web, linguistics}. Fails Gate A and Gate D: it is a finding,
not a project, and "keep charting things" has no definition of done. Recalled prior art
(unverified): Google Ngrams already answers the underlying question.

### Legislation as a repository with blame — 2026-09-23
Hook attempt: "git blame for the law: who changed this sentence, and when." Descriptor:
{browsing, legal corpora, web, civic}. Recalled prior art (unverified): several US Code
git-history projects, legislation.gov.uk's own change data. Partially covered, and the
uncovered part is jurisdiction-by-jurisdiction data plumbing rather than an idea.

### Puzzle generator that proves its puzzle is unique — 2026-09-23
Hook attempt: "Removes clues until exactly one answer survives, and proves it."
Descriptor: {playing, generated grids, web, games}. Recalled prior art (unverified):
essentially every serious Sudoku generator already does uniqueness checking.

### Solid whose three shadows spell three words — 2026-09-23
Hook attempt: "One object, three walls, three different words in its shadow."
Descriptor: {looking, user's words, 3D render, art}. The demo is superb. Recalled prior
art (unverified): Mitra and Pauly's Shadow Art (2009) and a large maker following.

### Digital sundial — 2026-09-23
Hook attempt: "A lump of plastic whose shadow reads out the time in numerals."
Descriptor: {looking, solar geometry, 3D render, art}. Recalled prior art (unverified):
the Scharstein and Gunn digital sundial, widely reproduced as a 3D print.

### Caustic surface design — 2026-09-23
Hook attempt: "A clear sheet of plastic that throws a photograph onto the wall."
Descriptor: {looking, an image, 3D render, optics}. Recalled prior art (unverified):
Disney Research caustics work and the Rayform commercialisation.

### Spreadsheet cell explainer — 2026-09-23
Hook attempt: "Tells you which three inputs actually decided this number." Descriptor:
{inspecting, a spreadsheet, text panel, productivity}. Recalled prior art (unverified):
trace-precedents plus sensitivity analysis, both long-standing. The interesting half of
this — grabbing the number and dragging it — became the 2026-09-23 shortlist entry.

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


### fold-and-cut solver — rejected (2026-09-23)
Hook attempt: "Fold the paper as shown, make one straight cut, and your name falls out."
Descriptor: {folding a printout, a drawn shape, paper and animation, geometry}. One of
the best hooks generated this run, and the reason it is filed here rather than built.
Searched: `fold-and-cut theorem solver implementation crease pattern straight skeleton
github`. Prior art found and inspected at the listing level:
[Erik Demaine's fold-and-cut page](https://erikdemaine.org/foldcut/) (the origin of the
theorem and a hub for implementations),
[6849-2020/fold-and-cut-2010](https://github.com/6849-2020/fold-and-cut-2010) (Java,
straight-skeleton method),
[6849-2020/fold-and-cut-2017](https://github.com/6849-2020/fold-and-cut-2017)
(CoffeeScript, same method),
[nadvornix/fold-and-cut](https://github.com/nadvornix/fold-and-cut), and
[One-Cut Helper](https://urjudged.github.io/oneCutTheorem/), a browser tool.
Material equivalence: same input (a straight-line drawing), same mechanism (straight
skeleton plus perpendiculars), same output (a crease pattern), same workflow, and one of
them already runs in a browser. What would be left is robustness and presentation, which
Gate E rejects explicitly — "interesting only because it is well-executed".
**Settled unless a specific reason appears to think the landscape changed.**

### A linkage that draws a curve you drew — rejected (2026-09-23)
Hook attempt: "Draw your signature and it builds a machine of rods and hinges that signs
it for you." Descriptor: {drawing, a user curve, animation, mechanisms}. Searched twice:
`draw a curve generate linkage mechanism that traces it interactive web tool Kempe
universality implementation`, then `"linkage" synthesis open source software draw path
"four-bar" OR "six-bar" web app trace arbitrary curve signature github`.
Prior art found: [LInK](https://github.com/ahnobari/LInK) — ships a demo where you draw
your own target curve and it synthesises a linkage, which is this candidate's exact
workflow; [four-bar-rs](https://github.com/KmolYuan/four-bar-rs) — simulator and
synthesis tool; [FourBarVis](https://github.com/stivio00/FourBarVis); the SALAR
Mechanism Synthesizer, published as
[an open-source tool for path synthesis of four-bar mechanisms](https://www.sciencedirect.com/science/article/abs/pii/S0094114X21003438).
The "sign your name" framing is itself established in the literature —
[Kempe's universality theorem](https://en.wikipedia.org/wiki/Kempe%27s_universality_theorem)
and McCarthy's group's Bézier-based drawing linkages, which explicitly describe a linkage
that signs a name and writes cursive Chinese
([lecture](https://mechanicaldesign101.com/video/kinematics-lecture-design-of-a-linkage-system-to-a-draw-curve/)).
Material equivalence: yes, on input, mechanism, output and workflow.

### Minimal-conflict explainer for over-constrained CAD sketches — rejected (2026-09-23)
Hook attempt: "Your drawing is impossible, and here are the two rules that cannot both
be true." Descriptor: {dragging, a user sketch, canvas, CAD}. This was the strongest
cross-domain transplant in the pool — the `cutline` minimal-cut idea moved into geometry.
Searched: `CAD sketch over-constrained diagnosis minimal conflicting constraint set
explain which constraints conflict solver`. Prior art found:
[An Efficient Diagnosis Algorithm for Inconsistent Constraint Sets](https://arxiv.org/pdf/2102.09005)
(minimal conflicts plus hitting sets — precisely the proposed mechanism),
[On Limitations of the Witness Configuration Method](https://arxiv.org/pdf/1904.00526)
(the geometric-constraint-solving case), and shipped tooling:
[Onshape's Sketch Constraint Manager](https://www.onshape.com/en/resource-center/tech-tips/sketch-constraint-manager)
and Fusion's constraint diagnosis, which already highlight conflicting constraints.
Material equivalence: the mechanism is published and the capability is shipped in
commercial CAD. Rejected.

### Gears generated from two drawn curves — rejected (2026-09-23)
Hook attempt: "Draw two doodles and it turns them into gears that actually mesh."
Descriptor: {drawing, user curves, animation, mechanisms}. Searched: `non-circular gear
generation arbitrary closed curve conjugate profile tool generate meshing gears from any
shape`. Prior art: non-circular gear design and generation is a mature field with worked
methods for conjugate pitch curves from arbitrary profiles — for example
[Noncircular Gears: Design and Generation](https://www.researchgate.net/publication/288577552_Noncircular_gears_Design_and_generation),
[a closed-complex-equation approach to arbitrary gear profiles](https://www.researchgate.net/publication/264380005_A_New_Approach_for_Designing_Gear_Profiles_using_Closed_Complex_Equations),
and [conjugate pairs for closed pitch curves](https://www.nature.com/articles/s41598-022-22139-7),
alongside an automatic non-circular gear design method. The mechanism is published;
what is missing is an accessible tool, which is execution rather than idea. Rejected on
the same grounds as fold-and-cut.

**Pattern worth recording, because it shaped this run.** Four separate candidates —
fold-and-cut, linkages, gears, CAD conflict diagnosis — died the same death: a beautiful
inverse-design trick whose method is published and whose only gap is that no pleasant
implementation exists. A future run that finds itself excited by a geometry magic trick
should expect this outcome and search the *method*, not the *tool*, first. It is the
cheapest possible way to kill these candidates, and it takes one query.

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


### Every clock change ever made, and why — parked 2026-09-23
Hook attempts: "Every time a government has changed what time it is, on one map." /
"The tz database is a political history of the twentieth century, and nobody reads it."
Descriptor: {exploring, IANA tzdb plus its source comments, web map and timeline,
history}. Searched: `tz database comments political history of time zone changes
interactive visualization every clock change`. No materially equivalent interactive
visualisation surfaced; the results were the database itself
([eggert/tz](https://github.com/eggert/tz),
[IANA](https://www.iana.org/time-zones)), parsers, and version-to-version diff viewers.
The dataset is genuinely under-exploited: the tzdb source files carry human comments
citing decrees and newspaper reports for individual transitions, and that commentary is
the interesting half.
Parked rather than selected because of **reach**, not hook: it is a thing to look at
once. It enables nothing further, and Gate D's definition of done would be arbitrary
("enough countries"). What would move it to section 4: a version where the reader can do
something the data makes newly possible, rather than browse it.

### Draw the shape you are looking for in a time series — parked 2026-09-23
Hook attempt: "Draw a squiggle and it finds every place your data did that."
Descriptor: {sketching a query, numeric streams, canvas, data analysis}. Not searched
this run. Recalled prior art (unverified): sketch-based time-series query research —
QetCH, Zenvisage, and shape-search features in commercial monitoring tools. Parked
pending a real search; do not build before running it.

### Answers that come with a receipt — parked 2026-09-23
Hook attempt: "Your program's answer arrives with a receipt, and a second, much smaller
program checks the receipt without redoing the work." Descriptor: {calling a library,
any computation, code, computer science}. The highest-reach candidate in the pool: a
library of certifying algorithms — shortest path, max flow, matching, convex hull,
primality, linear-programming duality — each returning a witness that an independent
verifier of a few dozen lines can check. If it works, every answer a program produces
can be audited by something small enough to trust.
Parked on **demo-ability**, which scored 2. There is no ten-second artifact: the
interesting event is a wrong answer being caught, which is invisible. Recalled prior art
(unverified): the certifying-algorithms literature from Mehlhorn's group, and LEDA, which
built witnesses into a commercial library in the 1990s. What would move it to section 4:
a demo where the verifier catching a deliberately corrupted answer is something you
watch, not something you read.

### The same date, read five different ways — parked 2026-09-23
Hook attempt: "One date string, thirty parsers, five different days." Descriptor:
{comparing, generated corpus plus many runtimes, web matrix, correctness}. Differential
testing of date and time parsing across languages and libraries, assembled as a dataset
and rendered as a matrix. Buildable here — Python, Node, Go, Rust and C are all
installed. Not searched this run. Parked because the honest worry is that it is a strong
blog post rather than a project with a definition of done, and because the JSON and URL
equivalents are well-trodden. What would move it: a result found in the data that is
surprising on its own, not just the fact that implementations differ.

### A straight-skeleton implementation that does not fall over — parked 2026-09-23
Hook attempt: none that passes; it is a category label. Descriptor: {calling a library,
polygons, code, geometry}. Surfaced as the primitive underneath the rejected fold-and-cut
candidate, and it is a real pain point — robust open implementations are scarce. Kept
here because a primitive with no hook is exactly what section 3 is for, and because a
future geometry project may need it as a component under the missing-capabilities rule.

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

## 5. Shortlist carried to the next run — not yet selected

Under the sleep-on-it rule, a shortlist must survive a cold re-read at the start of the
following run before implementation begins. Nothing below is selected. The next run reads
this section first, decides whether it still holds, and only then either promotes an entry
to section 4 or keeps searching.

### Finalist scores, 2026-09-23

Scored 1-5 on hook, reach, demo-ability, originality, difficulty-worth-it, monetizability.

| Candidate | Hook | Reach | Demo | Orig. | Diff. | Money |
| --- | --- | --- | --- | --- | --- | --- |
| Drag the answer (below) | 4 | 5 | 5 | 3 | 4 | 4 |
| Answers that come with a receipt | 4 | 5 | 2 | 3 | 4 | 2 |
| The same date, read five ways | 4 | 3 | 4 | 3 | 2 | 1 |
| Every clock change ever made | 3 | 2 | 5 | 3 | 2 | 1 |

Originality is capped at 3 for all four until their prior-art searches are finished; none
has yet earned more. Pairwise, on "which would I be more upset to see someone else ship
first": drag-the-answer beat the receipts library (same reach, and one of them can be
shown); drag-the-answer beat the date corpus (the corpus is a finding, not a capability);
the receipts library beat the clock-change map (reach). Drag-the-answer advances as the
provisional winner.

### Drag the answer — provisional winner, 2026-09-23

Hook attempt: **"Grab the answer and drag it, and the numbers that produced it rearrange
themselves to agree."**

Descriptor: {direct manipulation, a model the user wrote, interactive canvas, general
computing}. This is an empty cell. Every project in this repository sits in {reads source
files, prints text, developer tooling, local CLI}.

What it is: a small solver over a set of user-declared relations between numbers, where
any variable — input or output — can be grabbed and dragged continuously, and everything
else re-solves to keep the relations true. Three parts, in order of how much of the idea
they carry:

1. **Least-change back-solve.** A drag is under-determined: many assignments satisfy the
   relations. The solver moves the other variables as little as possible, which is the
   same trick inverse kinematics uses, and it is what makes dragging feel like a physical
   object rather than a random jump.
2. **Pinning.** Hold some variables fixed and the drag must route around them. This is
   where the interaction becomes expressive rather than a toy.
3. **Minimal conflict explanation.** When a drag is impossible given what is pinned, say
   which pins fight, and name the smallest set to release. This is `cutline`'s engine in
   its continuous form, which is the legitimate way to reuse it — as a component inside a
   different thing, not as a repackaging of it.

The ten-second demo, which decided the scoring: the exposure triangle. Drag shutter speed
and watch aperture and ISO slide to hold the exposure; pin ISO and watch the aperture take
the whole correction; pin both and watch it refuse and say why. A stranger who has held a
camera understands it with no words at all.

If this works, what becomes buildable that was not: any calculator, pricing model, recipe,
budget, dosage chart or design tool where the interesting question is "what would have to
be true for this number to be that instead" — asked by dragging, and answered
continuously, instead of by a modal dialog that solves for one variable.

**Red team, written before any decision to build.**

* *Closest existing thing.* Excel's Goal Seek and Solver; the constraint-UI lineage
  running from ThingLab through Cassowary into Auto Layout; published work on
  [bidirectional spreadsheet formulas](https://www.dcc.fc.up.pt/~hpacheco/publications/vlhcc14ss.pdf)
  and [constraint satisfaction in the spreadsheet paradigm](https://arxiv.org/pdf/cs/0701109);
  and, closest in spirit, the direct-manipulation programming environments — Apparatus and
  Sketch-n-Sketch — where editing the output edits the program.
* *Why a stranger would shrug.* "That is Goal Seek." The answer: Goal Seek is modal, runs
  once, solves for exactly one variable, and has no notion of moving the others as little
  as possible. None of the three parts above is what it does. But this answer is an
  argument, not evidence, and arguments are what this file exists to catch.
* *The part only interesting to its author.* The least-change mathematics. Nobody using it
  will know or care that a pseudo-inverse is involved; they will only notice if it feels
  wrong. That means the maths is table stakes, not the contribution, and the contribution
  has to be the interaction.
* *Objection that is not yet answered.* Whether a shipped tool already offers continuous
  drag over a general nonlinear model. Searched once this run — `bidirectional spreadsheet
  drag the output value and inputs adjust back-solve constraint UI ThingLab goal seek
  generalized` — which surfaced the academic lineage and Goal Seek but no such tool. That
  is one query. It is not enough.

**Before this may be promoted to section 4, the next run must:**

1. Re-read this entry cold and say plainly whether it still reads well. If it needed
   talking up, drop it — that is the infatuation test.
2. Finish the prior-art search. Specifically: Apparatus (Toby Schachman), Sketch-n-Sketch,
   Cassowary and its descendants, Grasshopper with Kangaroo, Desmos draggable parameters,
   Geogebra, Modelica and acausal modelling tools, and the bidirectional-transformation
   and lenses literature. Acausal modelling is the sharpest risk: solving relations in any
   direction is exactly what it does, and if a shipped acausal tool offers continuous
   dragging with least-change semantics, this candidate is dead and should be moved to
   section 2 with links.
3. Only then write `NOVELTY_REPORT.md`, a definition of done and a milestone ladder whose
   first rung is a vertical slice — the exposure triangle, draggable, in a browser, crude
   but real — before writing anything else.
