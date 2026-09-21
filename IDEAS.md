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


**Considered and passed over on 2026-09-21, with reasons** (recorded here so the owner can
push back):

* The two parts the original analysis thought were unclaimed — evolution at the level of
  whole projects, and a taste signal personal to one owner — were not searched this run,
  because the second one is blocked regardless. The taste model needs a body of the owner's
  own delight ratings and there are none. Nothing in this environment can manufacture them
  honestly, and inventing them would violate Section 19.
* The bounded first milestone that would be legal to build — one archive, one descriptor
  scheme, real candidates, a visible result — is a machine for choosing projects, not a
  project. This repository already has one of those: `AGENT_RULES.md` plus `IDEAS.md`, which
  now carry tail sampling, first-idea rejection, descriptors, pairwise comparison and
  red-teaming. Building a second, programmatic copy of the selection process would spend a
  long project on the meta-level while the object level stays empty at three items.
* It stays live, not rejected. What would change the answer: a file of the owner's own
  ratings appearing in this repository, or the object-level catalogue growing enough that
  covering its space is a real problem rather than a hypothetical one.

### (add yours below)

---

## 1. Rejected — failed the rules

Ideas that failed a gate for reasons other than prior art: not feasible here, no
definition of done, no first step, no real problem, inside the shape ban, or
memorable but useless.

Format: **name** — date. Hook attempt. Which gate failed and exactly why.

All entries below are from the candidate pool of 2026-09-21 (see section 5) unless
dated otherwise. Descriptor format: `{interaction model, data source, medium, domain}`.

### cutline-core — extract the infeasibility-certificate engine as its own project
2026-09-21. p ~ 0.45 — **this run's first idea, and rejected as a final answer** under the
generation rules. Hook attempt: "Proves your plan is impossible, then tells you the single
cheapest thing to drop." Descriptor: `{command -> report, one text file, text, planning}`.
Fails **Gate E**: `projects/cutline/` already contains this engine, verified against
exhaustive enumeration; re-shipping it under a new name is a near-duplicate of an existing
project folder. Also inside the shape ban (run a command, read a report). `PROGRESS.md`
recommended it as a starting point, which is exactly why it arrived first and exactly why
it is the mode. What would change this: a binding that makes the certificate *visible and
manipulable* rather than printed — that is a different project, and it goes in section 3
if anyone writes a hook for it.

### keyed — real-time video matting without a green screen
2026-09-21. p ~ 0.07. Hook attempt: "Pulls a clean matte off footage shot in a normal room,
live." Descriptor: `{live video, camera footage, moving image, VFX}`. Fails **Gate B** in
this environment: the core is a learned matting model, this container has no GPU (4 CPU
cores, 15 GB RAM, no CUDA), and the standard corpora are large downloads this disk and
policy cannot responsibly host. Recorded rather than dropped because `REFERENCES.md` names
Corridor's keying work and `AGENT_RULES.md` names a matting engine as the scale of thing
worth months. What would have to be true: GPU access and a lawfully obtainable training
corpus, or a genuinely classical formulation whose quality can be measured without training.

### flow-audible — hear a program's control flow while it runs
2026-09-21. p ~ 0.04. Hook attempt: "You can hear which loop is hot." Fails **Gate A**: a
profiler answers the same question better, and nothing concrete becomes possible. The hook
is also a category ("sonification of X"). Descriptor: `{listen, running process, audio,
developer tooling}`.

### spectral-source — a language whose source code is a spectrogram
2026-09-21. p ~ 0.02, a deliberate tail draw. Hook attempt: "The program is a picture of a
sound, and the sound is the program." Memorable and useless: fails **Gate A**, which Gate F
does not override.

### shadowclock — date and time a photograph from the shadows in it
2026-09-21. p ~ 0.06. Hook attempt: "Tell me when this photo was taken, from the shadows."
Rejected on **Section 24 judgement**, not on prior art: end to end this is a tool for
working out when and where a photograph of someone was taken, built unprompted. The
technique is established OSINT chronolocation, so the novelty was capped anyway. Not
pursued, and not to be re-generated as a "forensics" project without the owner asking.

### undecant — reverse engineer a commercial game's save format
2026-09-21. p ~ 0.05. Hook attempt: "Shows you the world hidden inside your save file."
Fails **Gate B** under the reverse-engineering limits in `AGENT_RULES.md`: this environment
has no lawfully obtained artifact to examine. The technique stays approved; this particular
target is not reachable from here.

### lattice — a maze generator with provable structural guarantees
2026-09-21. p ~ 0.02. Hook attempt: "Every maze it makes is provably unlike every other one
it has made." Fails **Gate A**: no problem, and the demo is a maze.

### fatfinger — score keyboard layouts against the typos people really make
2026-09-21. p ~ 0.03. Hook attempt: "A keyboard layout judged on the mistakes real people
make, mined from a million 'fix typo' commits." Descriptor: `{study, public commit corpus,
chart, input design}`. Fails **Gate B** on data scale here (the commit corpus is a
multi-terabyte archive) and **Gate F**: the output is a study, not a thing.

### renamer — specify and visualise git's rename-detection heuristics
2026-09-21. p ~ 0.03. Hook attempt: "Shows you why git thought your file was renamed."
Fails **Gate F**: interesting only to people who already know what rename detection is, and
the ten-second artifact is a diagram of a heuristic.

### repo-song — turn a repository's history into music
2026-09-21. p ~ 0.04. Hook attempt: "Hear your project's release cycle." Fails **Gate A**:
a toy with no capability, and the form is well trodden.

### playground-instances — a puzzle game whose levels are real unsolved instances
2026-09-21. p ~ 0.04. Hook attempt: "Every level you solve is a problem nobody had solved."
Descriptor: `{play, open combinatorial instances, interactive, human computation}`. Held
back by **Gate B**'s clause on depending on indefinite external work: its value is realised
only if strangers play it, which this environment cannot cause. Kept as a live direction if
it is ever paired with a result that stands without players.

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


### structural diff for music notation — settled (2026-09-21)
Hook attempt: "Shows you what changed between two versions of a score."
Searched: web search on symbolic music diff, score comparison, edit distance; PyPI; GitHub;
ACM DL. Prior art, inspected directly:
[musicdiff](https://github.com/gregchapman-dev/musicdiff) (PyPI `musicdiff`, music21-based,
compares two scores in any format music21/converter21 can parse, renders marked-up PDFs,
built for evaluating optical music recognition), and
["A diff procedure for music score files", DLfM 2019](https://dl.acm.org/doi/abs/10.1145/3358664.3358671).
Materially equivalent as a *diff*. This matters for the project selected in section 4:
the diff half is prior art and is credited as such; the merge half is what is unclaimed.

### declarative grammar for data sonification — settled (2026-09-21)
Hook attempt: "Vega-Lite, but the chart is a sound." Prior art: Erie, a declarative grammar
for data sonification (CHI 2024), plus Sonification Workstation and TwoTone. Same problem,
same user, same workflow.

### a rhythm language you can hear — settled (2026-09-21)
Hook attempt: "Polyrhythms become one line you can type." Prior art:
[TidalCycles](https://tidalcycles.org/) and [Strudel](https://strudel.cc/), which are
mature, widely used, and do exactly this.

### regex ranking — ask a pattern for its billionth matching string — set aside (2026-09-21)
Hook attempt: "Type a pattern and ask for the billionth string it matches — instantly."
Reached the finalist round (scores in section 5) and lost on originality. Ranking and
unranking of regular languages is classic theory (Goldberg and Sipser; the ranking function
and its inverse come from the automaton's adjacency matrix), with existing implementations
including RANS, and `exrex` covers naive enumeration. The engineering would be real; the
primitive is not new, which caps novelty confidence before the first line is written.

### byte-level "surprise map" of a binary file — settled (2026-09-21)
Hook attempt: "See the shape of a file you have never opened." Prior art:
[binvis.io](https://binvis.io/) (Aldo Cortesi) renders binaries as images by byte class and
entropy. Materially equivalent.

### semantic merge for Jupyter notebooks — settled (2026-09-21)
Prior art: [nbdime](https://github.com/jupyter/nbdime), which is exactly this, including
git integration.

### edit-robust addressing for spans of text — settled (2026-09-21)
Hook attempt: "A pointer into a document that survives the document being rewritten."
Prior art: Hypothesis fuzzy anchoring, URL text fragments (`#:~:text=`), and CRDT position
schemes (Peritext, Fugue, Yjs relative positions). Crowded, and the remaining gap is a
research question rather than a buildable distinction.

### isochrone maps of reachable-by-9am — settled (2026-09-21)
Prior art: Mapnificent, TravelTime, and many OSM/GTFS isochrone services.

### bit-level floating point visualiser — settled (2026-09-21)
Prior art: float.exposed, Float Toy, and several IEEE-754 explorers.

### structural diff and merge for spreadsheets — set aside (2026-09-21)
Hook attempt: "Merges two people's edits to the same spreadsheet without losing either."
Prior art: Microsoft Spreadsheet Compare, `daff` (tabular diff/merge with a defined format),
and several commercial workbook-compare products. The formula-aware merge is thinner ground,
but the category is occupied and the demo is a table.

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


### grammar inference from a corpus of unknown-format files — 2026-09-21
Hook attempts: "Point it at a thousand files of a format nobody documented and it writes the
specification." / "Works out a file format by looking at enough examples."
Descriptor: `{batch, corpus of binaries, structure map, reverse engineering}`. Real, hard,
and in the approved reverse-engineering register. Held here because the honest validation
story is weak — an inferred grammar that is *wrong in an unusual case* looks identical to a
correct one from the outside — and the ten-second artifact is a structure dump. What would
move it: a target format where ground truth is independently checkable, so the claim becomes
measurable rather than plausible.

### structural diff for vector artwork — 2026-09-21
Hook attempt: "Shows you what changed between two drawings, in terms of the drawing."
Held: "a diff for X" is a category label. Kept deliberately as a **candidate second binding**
for the timeline-merge primitive selected in section 4 — if that core is right, SVG paths are
another timeline-ish structure it should be able to reconcile.

### optimal line breaking for subtitles — 2026-09-21
Hook attempt: "Subtitles broken where a typesetter would break them." Genuinely useful,
genuinely unglamorous, no hook a stranger repeats. Also a candidate later binding for the
selected primitive (subtitle files are timelines).

### numbers that remember where they came from — 2026-09-21
Hook attempt: "Every number in the result can tell you which inputs made it." A primitive
with no demo: the interesting part is invisible at the moment it matters.

### take alignment for recorded audio — 2026-09-21
Hook attempt: "Finds the differences between two takes of the same performance." Held as a
later binding of the selected primitive rather than its own project; alone it reads as a
utility.

### scribble on a QR code and watch it repair itself — 2026-09-21
p ~ 0.05. Hook attempt: "Draw on a QR code and watch the error correction put it back
together, symbol by symbol." Descriptor: `{draw on it, the code itself, interactive visual,
explanation}`. **The strongest ten-second demo in the whole pool**, and it reached the
finalist round (section 5). It loses on **Gate A** and reach: it explains something rather
than enabling anything, and QR explainers and QR-art tools are numerous. Kept here because
the interaction — damage it and watch the repair happen live — is reusable in a project that
also has a capability behind it.

### catastrophic backtracking as a landscape you can walk — 2026-09-21
Hook attempt: "Walk around inside the reason your regex hangs." Good demo, small reach,
and regex101 already shows the step count that makes the point.

### CRDT for musical time — 2026-09-21
Hook attempt: "Two people edit the same bar at once and both edits survive." Not its own
project: it is the *real-time* sibling of the asynchronous problem selected in section 4,
and at least one collaborative sheet-music editor has already mapped notation onto CRDTs.
Recorded so the next run does not confuse the two problems — an ancestor-based merge and a
convergent live editor are different capabilities.

### the geographic spread of a word through a century of newspapers — 2026-09-21
Hook attempt: "Watch a word enter the language, city by city." Held on **Gate B** data scale
(the OCR archive is far larger than this container's 30 GB of writable disk) and on Gate F:
the artifact is an animated chart, and the genre is well populated.

### a playable proof — 2026-09-21
Hook attempt: "The puzzle you just solved is the proof." Held: no concrete first step that
does not require the whole design to be solved first, which is the third failure mode in
Gate B.

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

### comping (proposed name) — selected 2026-09-21, **pending the sleep-on-it re-read**
Status: chosen as the next project, not yet started. Under the generation rules the
shortlist must survive being re-read at the start of the next run before any implementation
begins. No code exists, `current_project` is still null, and the next run's first job is to
re-read this entry cold and either confirm it or say why not.

**Hook sentence (verbatim, to be carried into the README if confirmed):**

> Two people edited the same song. This works out what each of them changed, combines both,
> and plays you the one bar where they actually disagree.

Gate F check: understandable with no context (yes), surprising (a merge conflict you listen
to), concrete (names what happens), not a category label (it is not "a diff tool for MIDI").

**What it is.** A three-way merge for music: given a common ancestor and two edited versions,
work out each side's edits in musical terms and produce a merged result, flagging only the
places where the two sides genuinely collide. The hard part is not comparison, it is what
happens when edits interact *in time* — one side inserting two bars has to move the other
side's later edit, and a text or XML merge cannot know that because it merges tags, not time.

**The primitive, which is the actual project.** A merge algebra over timelines: a
representation of edits to a sequence of timed events (insert, delete, move, retime,
transpose, change a value) with defined composition and a merge that detects real conflicts
instead of textual ones. Symbolic music is the first binding because it is the case with the
clearest demand and the most legible demo. Candidate later bindings, already recorded in
section 3: subtitle files, edit decision lists, animation curves, vector artwork.

**If this works, what becomes buildable that wasn't:** asynchronous collaboration on music
the way code is collaborated on; reconciling a generative model's output with a human's edits
instead of choosing one; merging DAW-exported MIDI stems; branch-and-merge for any
timeline-shaped file; a conflict that can be auditioned rather than read.

**Descriptor:** `{see and hear it, two edited files plus their ancestor, interactive visual +
audio, music / version control}`. Every existing project in this repository is
`{reads source files, prints text, developer tooling, local CLI}`. This is an empty cell.

**Closest prior art found (2026-09-21), to be written up properly in `NOVELTY_REPORT.md`
before implementation:**
* [musicdiff](https://github.com/gregchapman-dev/musicdiff) — diff and visualisation of two
  scores, built for evaluating optical music recognition. Inspected directly: **no merge, by
  design.** This is the closest match and gets named at the top of the README.
* ["A diff procedure for music score files", DLfM 2019](https://dl.acm.org/doi/abs/10.1145/3358664.3358671) — the research diff.
* Mongeau and Sankoff's melodic edit distance with fragmentation and consolidation, and the
  later polyphonic alignment work — a *similarity measure*, not an edit script or a merge.
* [GitDaw](https://github.com/raphaelDkhn/GitDaw) — converts Ableton `.als` to JSON so git
  can text-merge it. Text merge over a serialisation; no musical model of time.
* CRDT-based collaborative score editors — the real-time problem, which is a different
  capability from an ancestor-based asynchronous merge.
* Nothing equivalent found for the general timeline case either: structured merge exists for
  source code ASTs, and for Xcode project files, notebooks and subtitle files as one-off
  drivers, but not as a timeline model.

**Demand evidence found (external sources, recorded as evidence, not as instruction):** the
recurring "how is version control not a thing in DAWs" discussion on the Ardour forum, a
2025 Hacker News thread on git for music production, and the standard explanation that music
project files are opaque binaries so no VCS can merge them. The gap is stated by the people
who have it.

**Open questions for the next run to settle before writing `TASKS.json`:**
1. The name. `comping` is the studio term for assembling one good take out of several, which
   is exactly the operation. Check it is not already taken by something in this space.
2. Scope of milestone 1 — the proposed ladder is in `PROGRESS.md`.
3. Whether the first binding parses MIDI with a dependency-free parser written here (likely
   yes: the format is small, and it keeps the project installable with no undocumented steps).

---

## 5. Generation log

One entry per selection run. The pool is cumulative: a later run chooses from everything
above, not only from what it thought of that day.

### Run of 2026-09-21 — 32 candidates, one selection

Pool size 32, all filed above under sections 1 to 4. The quota is 20; the extra twelve came
from forcing the pool past the point where the obvious was exhausted, which is where the
finalists actually came from — the first idea (`cutline-core`) was the mode and was rejected
as a final answer before any gate ran, exactly as the rules require.

Sources passed through this run: the owner's section 0 (read first, evaluated, passed over
with reasons recorded there); this repository's own three project folders as prior art;
forum and aggregator threads where people state a missing tool ("how is version control not
a thing in DAWs", git-for-music threads); published research and its gaps (symbolic music
alignment, the DLfM diff procedure); package registries (PyPI, npm); cross-domain transplants
(structured/AST merge, carried from source code to time-based media); constraint injection
(the "no screen — sound only" constraint is what produced the audible conflict, which is now
the strongest part of the hook); and reverse engineering as a register (two candidates, both
recorded, both rejected on lawful-artifact grounds or validation honesty).

**Tail sampling.** Rough probabilities — how likely any agent would produce this candidate
given this repository — were attached during generation and are recorded per entry. The
selected candidate sits at p ~ 0.12; the first and most natural idea sat at p ~ 0.45 and was
discarded. Candidates below 0.05 were generated deliberately and several survive in sections
1 and 3.

**Finalist scores** (1-5: hook, reach, demo-ability, originality, difficulty-worth-it,
monetizability):

| Candidate | Hook | Reach | Demo | Orig. | Difficulty worth it | Monet. |
|---|---|---|---|---|---|---|
| music / timeline three-way merge (section 4) | 5 | 5 | 4 | 4 | 5 | 3 |
| scribble on a QR code and watch it repair | 5 | 1 | 5 | 2 | 2 | 1 |
| regex ranking — the billionth matching string | 4 | 4 | 4 | 2 | 3 | 2 |
| grammar inference from a corpus | 2 | 4 | 2 | 3 | 4 | 3 |
| cutline-core (first idea) | 3 | 4 | 2 | 1 | 3 | 3 |

Writing a 1 next to originality for `cutline-core` ended the argument for it, which is what
the scores are for.

**Pairwise — "which would I be more upset to see someone else ship first?"**
* merge vs. QR: **merge.** The QR page would be a pleasure and I would not mind; several
  already exist. Someone shipping a working structural merge for music would be genuinely
  annoying, because the demand has been stated for a decade and the ground is open.
* merge vs. regex ranking: **merge.** Ranking regular languages is solved theory; being
  beaten to an implementation of known theory is not upsetting.
* merge vs. grammar inference: **merge**, on demo and on the honesty of the validation story.

**Red team of the winner, argued in bad faith, then answered:**

* *"musicdiff already does this, and git already merges MusicXML as text."* — musicdiff
  diffs and does not merge; that is confirmed by direct inspection, and it is credited at
  the top of the README. Text merge over XML is the thing that fails: it reconciles tags,
  and the interesting failures are about time. One side inserting two bars must move the
  other side's later edit, and no text merge can know that.
* *"CRDT editors already solved collaborative music."* — they solve the live case where both
  people are online. An ancestor, two files, and no network is a different problem and the
  one people actually have.
* *"This is a git merge driver. That is a category label and a command-line tool — the shape
  this repository keeps producing."* — the strongest objection, and the one to hold myself
  to: if it ships as a CLI that prints a report, it has failed. The deliverable is the thing
  you see and hear — piano rolls with each side's changes, the merged result playing, and the
  conflict auditionable as A versus B. The merge driver is a thin adapter, one binding among
  several, and it is not the project.
* *"Musicians do not use git and never will."* — the input is two versions of a file and
  their ancestor, which arrive by many routes that are not git: a collaborator's export, a
  DAW's own backup, a student's attempt against the teacher's score, a model's variation
  against the human original. The last of these did not exist as a common case until
  recently, and nothing reconciles it today.
* *"The algebra is only interesting to the person who wrote it."* — true of the algebra by
  itself, which is why the algebra is not what gets shown. It is what makes the merge
  correct instead of plausible, and it is checkable: property tests, exhaustive verification
  on small cases, and the control that disjoint edits must never conflict.

An objection that is **not** fully answered, recorded honestly: whether musically-aware
alignment without a reliable ancestor (milestone 3) is achievable at a quality worth
claiming. If it is not, the project still stands on milestones 1, 2 and 4 with that
limitation stated, and this note is the evidence that it was foreseen rather than discovered
late.
