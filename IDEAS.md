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

**Considered first on 2026-09-22, and passed on again.** Reason, for the owner: the
taste signal is the part that makes it different from AlphaEvolve, FunSearch,
OpenEvolve and ShinkaEvolve, and it needs a body of your own ratings that does not
exist yet — so today it would be built without the one component that distinguishes
it. If you want this to move, the unblocking step is small and is yours, not mine:
start rating things you find delightful (a line each in `REFERENCES.md` is enough),
and once there are enough of them the candidate changes shape completely. Pushing
back is welcome — say so here and it goes to the front of the next run.

### (add yours below)

---

## 1. Rejected — failed the rules

Ideas that failed a gate for reasons other than prior art: not feasible here, no
definition of done, no first step, no real problem, inside the shape ban, or
memorable but useless.

Format: **name** — date. Hook attempt. Which gate failed and exactly why.

### live-data variable font — rejected 2026-09-22
Hook attempt: "a typeface whose weight is your server load." Fails Gate A: no
concrete problem and no capability — the data is already legible as a number, and
rendering it as letterform weight removes precision without adding anything. A
demo with nothing underneath it. Descriptor `{watch, live metrics, type specimen,
typography}`.

### self-rendering data file — rejected 2026-09-22
Hook attempt: "a CSV that opens as an interactive chart in any browser and still
parses as a CSV." Fails Gate A for the same reason: the polyglot trick is the
whole idea, and the problem it solves (looking at a table) is solved many times
over. Kept because the underlying observation — that a file can carry its own
viewer — may be worth something attached to a format that actually needs one.
Descriptor `{open file, any table, self-rendering page, formats}`.

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

### retroactive data structures — rejected 2026-09-22
Hook attempt: "Insert an event into the past and the present recomputes itself,
without replaying history." Strong hook, genuine upstream primitive, published
theory (Demaine, Iacono, Langerman). Rejected on prior art: public implementations
already exist — [csvoss/retroactive](https://github.com/csvoss/retroactive)
(partial and full retroactivity in Python, with docs),
[6851-2021/retroactive-pq](https://github.com/6851-2021/retroactive-pq) (partially
retroactive priority queues plus an experimental fully retroactive version using
hierarchical checkpointing),
[6851-2021/retroactive-priority-queue](https://github.com/6851-2021/retroactive-priority-queue),
[chshersh/retroactive-priority-queue](https://github.com/chshersh/retroactive-priority-queue)
(O(log m) update), and
[panwaria/RetroactiveDataStructures](https://github.com/panwaria/RetroactiveDataStructures)
(retroactive BST, hash, union-sameset). Adjacent and larger prior art: self-adjusting
computation and incremental dataflow (Adapton, differential dataflow), which already
answer "change an input in the past, propagate to the output efficiently". A better
engineered library would be execution quality, not a new idea. Descriptor
`{timeline editing, operation log, library + visual, algorithms}`.
**Direction the rejection leaves open:** the versions that are *not* done are
retroactivity for structures nobody has done it for, and a visual language for
editing an operation timeline. Neither is currently strong enough to carry a project.

### draw a curve, get the linkage that traces it — rejected 2026-09-22
Hook attempt: "Draw a shape and it hands you a machine of rods that traces it
forever." Rejected on prior art: this is the path-synthesis field.
[MotionGen / MotionGen Pro](https://www.stonybrook.edu/commcms/motiongen/) takes
sketched poses and computes the four-bar linkages that achieve them; SALAR
Mechanism Synthesizer is an open-source path-synthesis package with four
optimizers; and the theory side is covered by Kempe's universality theorem plus
[modern constructive work](https://arxiv.org/pdf/1509.08690) and Liu & McCarthy,
*Synthesis of Linkages to Trace Plane Curves*. Same input, same output, same
mechanism. Descriptor `{draw, user sketch, animation, geometry/mechanism}`.

### un-evolve a word (reverse sound change) — rejected 2026-09-22
Hook attempt: "Type an English word and watch it walk backwards through two
thousand years of sound changes to its ancestors." Rejected on prior art:
[rsca, a reversible sound change applier](https://000024.org/rsca.html), does
exactly this — it unapplies sound changes and reconstructs the complete set of
proto-forms that would yield a given word, with the forward run as its check.
Forward application is covered by [Lexurgy](https://github.com/def-gthill/lexurgy)
and the older SCA². Descriptor `{type a word, etymology rules, interactive tree,
linguistics}`.

### Suspected prior art — named from background knowledge, not searched this run

These four were eliminated during generation on prior art I am confident exists but
did **not** verify with a search on 2026-09-22. Recorded so the pool is complete and
so a future run knows the status is *unverified*, not settled. Verify before
reconsidering or citing any of them.

* **probabilistic spreadsheet (every cell a distribution)** — Guesstimate, Squiggle, Causal.
* **de-plotting: chart image back to numbers** — WebPlotDigitizer, and the ChartOCR / DePlot line of research.
* **lossy time-series codec with hard per-point error bounds** — SZ, ZFP, Sprintz, Gorilla.
* **flatten a 3D model into a sewing or knitting pattern** — autoknit / KnitKit and garment-CAD systems.

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

### stable graph layout — considered 2026-09-22
Hook attempt: "your graph stops jumping when the data changes." Fails Gate F: that
is a complaint, not a hook, and the fix is invisible to anyone who has not watched
the broken version first. The pain is real (people hand-place nodes because layouts
re-shuffle), but the field is well worked: dynamic graph drawing and mental-map
preservation have a large literature
([incremental layout for online dynamic graphs](https://vis.cs.ucdavis.edu/papers/tarik_incremental.pdf),
[North & Woodhull, on-line hierarchical drawing](https://www.graphviz.org/documentation/NW01.pdf)),
and incremental modes already ship in webcola and ELK. What would make it hyped: a
result, not a feature — a stability measure with a control showing a standard layout
fails it, shown as two animations side by side. Descriptor `{watch, live graph
stream, animation, visualization}`.

### dashcam telemetry — considered 2026-09-22, search incomplete
Hook attempt: "Drop in a dashcam clip and it draws the drive — speed, turns and
all — out of bytes the file was never documented to contain." A legitimate reverse
engineering target: each vendor (Novatek, Viofo, BlackVue, Garmin) embeds GPS and
accelerometer streams in undocumented atoms. **Not eliminated, not cleared**: exiftool
is known to decode several Novatek variants, which may or may not be materially
equivalent, and that was not checked this run. Needs: a real prior-art search, and a
lawfully obtained sample clip, which this environment does not currently have — that
second point is the harder one and may fail Gate B. Descriptor `{drop a file,
consumer device output, map + trace, reverse engineering}`.

### the National Bridge Inventory as one image — considered 2026-09-22
Hook attempt: "Watch every bridge in America age." Real, large, public, annual
inspection data since 1992. Fails Gate F on crowding rather than on prior art:
condition dashboards and "deficient bridges" maps are a genre, and the hook is a
category of infographic rather than a surprise. What would make it hyped: a finding
in the data that nobody has reported, shown as the demo. Descriptor `{scrub a year,
federal bulk data, map/animation, civic data}`.

### animated geometry proofs — the reach candidate, 2026-09-22
Hook attempt: "State a theorem; the proof it gives back is an animation you can
watch." Generated deliberately as the candidate more ambitious than I am confident I
can finish, as the rules require. Not selected: prior art is heavy (GeoGebra
Discovery, JGEX, Wu's method implementations, AlphaGeometry) and, more decisively,
I could not name a bounded first milestone that produces a working vertical slice —
which fails Gate D as currently understood. Kept because the *proof-as-animation*
framing is the interesting half and may survive attached to a different subject.
Descriptor `{state a theorem, formal geometry, animation, formal methods}`.

### re-scoping cutline's certificate solver as a standalone primitive — considered 2026-09-22
Hook attempt: "Proves your plan is impossible, then tells you the single cheapest
thing to drop." This is the repository's own recorded suggestion and it was taken
seriously this run. Not selected, for two reasons. First, Gate E: the engine already
exists in `projects/cutline/`, so the work would be repackaging and generalising code
this repository has already written, and every cycle is supposed to go somewhere new.
Second, the shape is unchanged — text in, certificate out, which is what the shape ban
exists to stop. It stays available: if a future project needs an infeasibility
certificate as a component, this is the piece to lift and generalise then, in service
of something else. Descriptor `{run, plain-text constraints, text certificate,
planning}`.

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

### book pagination engine — provisionally selected 2026-09-22, **not yet started**

**Status: provisional.** Under the sleep-on-it rule this selection is not final until
it survives a re-read at the start of the next run. No implementation exists, no name
is fixed, and the novelty report is unfinished. If the next run re-reads this and the
idea has gone flat, it goes back to the pool and that is the correct outcome.

**Hook sentence (provisional):** *"Lays out a book so no figure drifts away from the
sentence that mentions it, and proves no other arrangement scores better under the
rules you set."*

Gate F check: understandable with no context (anyone who has read a textbook has
turned back three pages looking for figure 4); surprising (that page layout has a
provably best answer at all, rather than being craft); concrete (names what happens);
not a category label. The second clause is a factual claim and constrains the build:
it may only be written down if the solver is exact under a stated cost model and is
verified against exhaustive enumeration on small instances. If that verification
fails, the clause comes out.

**What it is.** A standalone engine that takes a structured document — text, figures,
tables, footnotes, and where each figure is referenced — and decides all page breaks
and float placements *globally*, minimising a documented, user-editable cost
(figure-to-mention distance, widows and orphans, page fill, spread balance) rather
than greedily page by page as every shipping system does. The engine is the project;
a book renderer and an interactive page-grid you can drag and pin figures in are its
demos, per the ship-the-primitive rule.

**Demo (ten seconds, legible from three metres):** the same document laid out twice as
a grid of page thumbnails — greedy on the left with arrows showing how far each figure
sits from its mention, optimised on the right with those arrows collapsed. The
constraint "legible from three metres" is what produced the thumbnail-grid-plus-arrows
form; a PDF to open and study would not have qualified.

**Why it is not a repeat of anything here:** no source files are read, nothing is
warned about, no exit code is the point, and the output is a rendered page rather than
a report. Descriptor `{drag/pin + batch, structured document + font metrics, rendered
pages, typesetting}` — an empty cell against the three existing projects' shared
`{reads source files, prints text, developer tooling, local CLI}`.

**If this works, what becomes buildable that wasn't:** globally optimised layout for
anything with a text stream and floats — EPUB and reflowable readers that stop
stranding figures, subtitle segmentation (pool #10), automated journal and report
production, and layout that re-optimises live while you edit. A usable, non-TeX,
open implementation of that method is the piece all of those are missing.

**Prior art found so far (2026-09-22, search incomplete — see below):**
* [Mittelbach, *A general framework for globally optimized pagination*](https://onlinelibrary.wiley.com/doi/10.1111/coin.12165)
  (Computational Intelligence 2019; the DocEng 2016 version won best paper) — the
  closest prior art by a wide margin, and the method this would implement. It handles
  float placement inside the optimisation with a flexible constraint model. Mittelbach
  states the work remains **at prototype stage**, unreleased, pending time and funding.
* [Brüggemann-Klein, Klein & Wohlfeil, *On the Pagination of Complex Documents*](https://link.springer.com/chapter/10.1007/3-540-36477-3_5)
  — dynamic-programming pagination, globally optimal page-break sequences avoiding
  widows and orphans.
* Plass (1981), *Optimal pagination techniques for automatic typesetting systems* —
  the NP-hardness results for the general problem.
* [lua-widow-control](https://tug.org/TUGboat/tb43-1/tb133chernoff-widows.html) and
  Mittelbach's `widows-and-orphans` package — shipping, but widows and orphans only,
  no float optimisation.
* Shipping systems: TeX/LaTeX (greedy page builder plus a local float algorithm),
  Typst, SILE, Patoline, InDesign, Prince, Vivliostyle, Speedata. None found so far
  performs global optimisation over float placement.
* Demand, unmet and public: Typst issues
  [#5558](https://github.com/typst/typst/issues/5558) ("with many figures, figures get
  pushed quite far from where they are first mentioned"),
  [#3967](https://github.com/typst/typst/issues/3967) (placement relative to the
  reference), [#6392](https://github.com/typst/typst/issues/6392), and Quarto
  discussion [#8801](https://github.com/orgs/quarto-dev/discussions/8801).

**Scores** (hook, reach, demo-ability, originality, difficulty-worth-it,
monetizability): **4, 5, 5, 4, 5, 4**. Originality is 4 rather than 5 because the
optimisation method is published; what is unbuilt is the public implementation, the
verification layer and the interaction.

**Pairwise — "which would I be more upset to see someone else ship first?"**
* vs retroactive data structures (#1): pagination. Someone shipping a retroactive
  structures library would not sting, because several already exist.
* vs draw-a-curve-to-linkage (#2): pagination. MotionGen already exists and is good.
* vs animated geometry proofs (#19): pagination. The geometry candidate is more
  exciting and I cannot bound its first milestone, which is exactly the trade the
  rules say to resolve in favour of the one that can start.

**Red team (written in bad faith, then answered):**
1. *"This is a homework reimplementation of a paper by the LaTeX maintainer."* Partly
   fair, and it must be said in the README at the top. The parts that are not in the
   paper: a standalone engine not welded to TeX, an exactness check against exhaustive
   enumeration, per-break explanations, and interactive re-pagination under pinning.
   Novelty confidence will be capped at Medium and the phrasing stays "no public
   implementation found within the documented search scope".
2. *"Nobody cares where figures land."* The Typst and Quarto threads above are people
   caring, and LaTeX's `[htbp]`/`\FloatBarrier` folklore is a decades-old workaround
   culture. Publishers pay humans to push figures around by hand.
3. *"It degenerates into a command that prints a PDF — the banned shape in a new
   coat."* The live risk. Mitigation is structural: the demo artifact is a rendered
   page grid, and milestone 1 is not allowed to be a CLI that emits a file with nothing
   to look at.
4. *"Only the author cares about widow counts."* True of widow counts, which is why the
   demo is built on figure drift — the one failure a stranger recognises instantly.
5. *"Optimising an aesthetic is a category error; you will optimise a made-up cost."*
   The strongest objection. Answer: the cost model is an explicit input, stated and
   editable, and the claim is never "this is more beautiful" but "this satisfies the
   stated constraints and no arrangement scores better under them". Any comparison
   against a greedy baseline must hold line-breaking, fonts and content fixed and vary
   only the page-break strategy.

**Must close before implementation begins (novelty report is not complete):**
* registry searches: PyPI, npm, crates.io, CTAN, plus GitHub code search;
* direct inspection of the Mittelbach 2019 and Brüggemann-Klein papers for the exact
  cost model and what each does and does not cover;
* whether Mittelbach's prototype has been released since 2019 (TUGboat, CTAN, LaTeX3 news);
* what Patoline, SILE, Typst and Vivliostyle actually do at page-break time, read from
  their source or docs rather than assumed;
* name selection (`quire`, `galley`, `forme`, `signature` are the current shortlist);
* definition of done and the milestone ladder, written into `TASKS.json` before any code.

_This is the first entry chosen under the full rule set. It is provisional by design:
the rules require it to survive one gap before anything is built._

---

## 5. Candidate pool — generation logs

The complete generation record for each selection run: every candidate produced,
before any gate ran, with its rough probability (tail sampling — low means
deliberately unlikely to be the first thing anyone would propose), its behaviour
descriptor, and where it ended up. Candidates with a settled outcome also have a
full entry in sections 1-4; candidates still open live only here, with what remains
unsearched.

### Run 2026-09-22 — 24 candidates

Sources passed through this run: published-method-with-no-implementation hunting,
paper future work, issue trackers with unmet demand (Typst, Quarto), reverse
engineering targets, unexploited public datasets, cross-domain transplants,
things done by hand repeatedly, the owner's section 0, and this repository's own
back catalogue.

First idea generated this run: **#6, dashcam telemetry format**. Rejected as a
final answer under the first-idea rule and left in the pool; the 23 that follow
were generated as structural alternatives, not variations of it.

| # | Candidate | p | Descriptor `{interaction, data source, medium, domain}` | Outcome |
|---|-----------|---|--------------------------------------------------------|---------|
| 1 | Retroactive data structures: insert an operation into the past, present recomputes without replay | 0.05 | `{timeline editing, operation log, library + visual, algorithms}` | §2 — searched, prior art |
| 2 | Draw a curve, get the rod linkage that traces it | 0.04 | `{draw, user sketch, animation, geometry/mechanism}` | §2 — searched, prior art |
| 3 | Un-evolve a word: walk a modern word backwards through sound changes to its ancestors | 0.05 | `{type a word, etymology rules, interactive tree, linguistics}` | §2 — searched, prior art |
| 4 | Globally optimal book pagination with floats, plus interactive re-pagination | 0.03 | `{drag/pin + batch, structured document + font metrics, rendered pages, typesetting}` | §4 — **provisionally selected** |
| 5 | Graph layout that does not jump when the data changes | 0.08 | `{watch, live graph stream, animation, visualization}` | §3 — searched, hook too weak |
| 6 | Dashcam telemetry: spec the undocumented per-vendor GPS atoms, draw the drive from the video file | 0.06 | `{drop a file, consumer device output, map + trace, reverse engineering}` | §3 — search incomplete |
| 7 | Three-way structural merge for spreadsheets | 0.10 | `{merge, two edited xlsx files, visual diff, version control}` | open — unsearched |
| 8 | Puzzle generator that guarantees the solution needs exactly the techniques you chose, and shows the deduction path | 0.07 | `{play, generated, playable + animation, puzzles}` | open — unsearched |
| 9 | Inverse procedural generation: describe the world you want, search for the seed that makes it | 0.06 | `{describe, generator internals, visual, procedural generation}` | open — unsearched |
| 10 | Knuth-Plass for subtitles: optimal line and timing segmentation | 0.05 | `{watch, transcript + audio, video overlay, media}` | open — downstream of #4's engine family |
| 11 | Civil-time primitive covering the whole tzdb history, local-mean-time era included | 0.09 | `{query, tzdb full history, library + visual, time}` | open — unsearched |
| 12 | Three-way merge for video/audio edit timelines | 0.05 | `{merge, OTIO/EDL files, timeline view, media production}` | open — unsearched |
| 13 | A debugger you listen to: program execution as sound, no screen | 0.06 | `{listen, live execution trace, audio only, developer capability}` | open — hook risk unresolved |
| 14 | A variable font whose axes are driven by live data | 0.12 | `{watch, live metrics, type specimen, typography}` | §1 — no real problem |
| 15 | Spreadsheet where every cell is a probability distribution | 0.12 | `{edit cells, user input, interactive sheet, estimation}` | §2 — known prior art |
| 16 | De-plotting: read the numbers back out of a chart image | 0.11 | `{upload image, published figures, data table, data recovery}` | §2 — known prior art |
| 17 | Time-series codec: lossy with hard per-point error bounds, queryable compressed | 0.10 | `{library call, sensor streams, library, systems}` | §2 — known prior art |
| 18 | Flatten a 3D model into a sewing or knitting pattern you can cut | 0.04 | `{upload model, 3D mesh, printable pattern, fabrication}` | §2 — known prior art |
| 19 | Geometry theorem prover whose proof output is an animation | 0.03 | `{state a theorem, formal geometry, animation, formal methods}` | §3 — the reach candidate; cannot be bounded yet |
| 20 | A data file that is also its own interactive viewer | 0.07 | `{open file, any table, self-rendering page, formats}` | §1 — gimmick, fails Gate A |
| 21 | Watch every bridge in America age: the National Bridge Inventory as one image | 0.08 | `{scrub a year, federal bulk data, map/animation, civic data}` | §3 — dashboards exist, hook weak |
| 22 | Superoptimizer for spreadsheet formulas | 0.04 | `{paste a formula, user input, rewritten formula, optimization}` | open — Gate A weak |
| 23 | Re-scope `cutline`'s infeasibility-certificate solver as the standalone primitive it is | 0.15 | `{run, plain-text constraints, text certificate, planning}` | §3 — own prior art, shape unchanged |
| 24 | Pebble Evolve (owner's idea, section 0) — breed projects instead of selecting one | — | `{autonomous loop, own repository, archive, meta}` | §0 — considered first, passed this run, reason recorded there |

Constraint injection was applied to the winner (#4) rather than to the pool at
large: the constraint **"must be legible from three metres away"** changed the
plan, because it forces the demo to be a grid of page thumbnails with the
figure-to-mention distance drawn as an arrow, rather than a PDF a reader has to
open and study. That is now the intended demo. The constraints "must work
offline" and "core has no dependencies beyond font metrics" were also accepted;
`{one file}` was rejected as it would fight the milestone ladder.
