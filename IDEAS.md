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
* A candidate that is still being decided on goes in section 5 (under deliberation),
  with its scores and the specific open question blocking the choice. It leaves
  section 5 the moment the question is answered — upward to 4, or down to 1, 2 or 3.
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

**Status: evaluated 2026-09-18 and passed on — see the verdict below.** The concerns
that were open before that evaluation, kept because they are what the verdict rests on:

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

**Verdict, 2026-09-18 (first formal evaluation): passed on, for now — Gate C and Gate B.**
Searched this run: "evolutionary search over whole software projects LLM agent population
MAP-Elites quality diversity 2026" and "ShinkaEvolve OpenEvolve AlphaEvolve evolve entire
applications not just functions". The part the owner's note flagged as possibly unclaimed —
evolution at the level of whole projects rather than single functions — is now claimed:
[EvoLattice](https://arxiv.org/html/2512.13857v1) evolves a population held inside one
artifact across agent-level behaviours, [CodeEvolve](https://arxiv.org/html/2510.14150v1)
is an open-source evolutionary coding agent, [DEI](https://arxiv.org/pdf/2605.27130) is a
distributed quality-diversity framework using heterogeneous LLMs as mutation operators, and
the field is described in survey terms as having moved "from evolving single mathematical
functions to entire codebases". The remaining genuinely unclaimed part is the second one —
a taste signal personal to one owner — and that still cannot be built, because it needs a
body of the owner's own delight ratings and none exist. So the buildable part is taken and
the untaken part is not buildable.

One sentence for the owner, per the rule on passing on an owner idea: **the "whole projects
rather than single functions" gap closed between the idea being written down and being
evaluated, and what is left of it needs training data about your taste that does not exist
yet.** If you want this anyway, the version that would work is the reverse of the proposal:
not an engine, but you rating a few dozen past candidates in `IDEAS.md` for delight, which
would create the missing data and is cheap. Push back here if you disagree — this is a
judgement call about prior art, not a refusal.

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

### Run of 2026-09-18 — pool of 29 candidates

This run generated a pool of 29 candidates before any gate was applied, per the
quota rule. They are filed below across sections 1, 2, 3 and 5. Rough probabilities
are this agent's estimate of how likely a generic agent, given this repository,
would produce that candidate — recorded because the rule is to prefer the tail,
and recording the number makes it possible to check afterwards whether the rule
was actually followed rather than merely cited.

**C1 — cutline's solver, re-scoped as a standalone primitive** — 2026-09-18. p≈0.45.
Hook attempt: "Proves your plan is impossible, then tells you the single cheapest
thing to drop." Descriptor: `{batch, text plan, printed text, planning, local CLI}`.
**Rejected as this run's answer under the first-idea rule.** It was the first thing
generated, it is what `PROGRESS.md` points at, and any agent reading this repository
would produce it — which is the definition of the mode. It is not rejected as *work*:
re-scoping `cutline` around its engine remains a legitimate task, and it stays
recorded in section 4 as the worked example of the ship-the-primitive rule. It is
rejected as a *selection*, because choosing it would mean this run generated one idea
and stopped.

**C4 — crontab rendered as the calendar it actually produces** — 2026-09-18. p≈0.20.
Hook attempt: "Shows you what your crontab will really do next month." Descriptor:
`{batch, config file, calendar render, ops, local CLI}`. **Gate F.** The hook is a
category label once the novelty of "as a calendar" wears off, and crontab.guru
already prints the next runs, so the surprise is thin. Named in `AGENT_RULES.md` as
an example of reframing a dead idea, not as an endorsement of this one.

**C5 — a memory format for agents** — 2026-09-18. p≈0.35. Hook attempt: "Gives an
agent a memory that survives being restarted." Descriptor: `{batch, agent state,
file format, agent tooling}`. **Gate E.** Crowded to the point of being a product
category, and meta-work about agents rather than a capability.

**C6 — sonification of public seismometer data** — 2026-09-18. p≈0.12. Hook attempt:
"Listen to the earth ringing after an earthquake." Descriptor: `{playback, public
sensor data, audio, geoscience}`. **Gate A.** Real data, genuinely striking, and it
provides no capability anyone lacks. Seismic sonification is also long established
at observatories.

**C7 — any dataset turned into a 3D-printable object** — 2026-09-18. p≈0.08. Hook
attempt: "Turns a spreadsheet into something you can hold." Descriptor: `{batch,
tabular data, physical object, visualization}`. **Gate A and Gate E.** Data
physicalization is an established practice with existing toolchains, and the general
version collapses into "extrude a bar chart".

**C8 — navigate a codebase by ear, no screen** — 2026-09-18. p≈0.03. Hook attempt:
"Find the bug by listening to the code." Descriptor: `{live, source, audio,
developer tooling}`. **Gate A.** A constraint-injection product (sound only) that
stayed memorable and useless, which is the exact failure Gate A exists to catch.
Recorded because the constraint was worth trying even though the output failed.

**C9 — a game whose mechanic is a real algorithm** — 2026-09-18. p≈0.18. Hook
attempt: none survived. Descriptor: `{playable, —, browser, games}`. **Gate D.**
Not an idea, a wish for one: no specific algorithm, so no definition of done and no
first step. Kept as a standing prompt rather than a candidate.

**C28 — structural three-way merge driven by a format description** — 2026-09-18.
p≈0.06. Hook attempt: "Merges two edits to a binary file the way git merges text."
Descriptor: `{batch, binary files + format spec, merged file, version control}`.
**Parked, not rejected.** It is downstream of C24: it needs a format description to
exist before it can merge anything, so it cannot be the project until something
produces those descriptions. Reconsider if C24 is built.

**C29 — knitting pattern to the 3D shape the fabric actually takes** — 2026-09-18.
p≈0.03. Hook attempt: "Type a knitting pattern and watch the fabric curl into the
shape it will really have." Descriptor: `{batch, pattern text, 3D render, textiles}`.
**Parked on prior art strength, not searched to exhaustion.** This is the "more
ambitious than I am confident I can finish" candidate the rules require, and its hook
is one of the best in the pool. Known prior art before searching: Kaldor's yarn-level
cloth simulation, stitch meshes (Yuksel et al.), and Carnegie Mellon's machine-knitting
work. Not searched properly this run because it lost the pairwise comparison early;
if C24 falls, search this one first.

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

### Run of 2026-09-18 — candidates killed by prior art

Each entry below was searched this run. The searches are recorded so no future run
repeats them.

**C10 — an input where two versions of a function disagree** — p≈0.15. Hook attempt:
"Change a function and it hands you the exact input where the new version disagrees
with the old one." Descriptor: `{batch, two functions, witness input, testing}`.
Prior art: [CrossHair](https://github.com/pschanely/CrossHair)'s `diffbehavior`
command does exactly this for Python, by symbolic execution. Materially equivalent:
same problem, same user, same workflow, same output.

**C11 — the oldest surviving sentence in a Wikipedia article** — p≈0.10. Hook
attempt: "Shows you the words in an article nobody has touched in nineteen years."
Descriptor: `{batch, public dump, heat map, history}`. Prior art:
[WikiWho](https://www.wikiwho.net/) provides token-level authorship and survival for
Wikipedia revisions, and WikiBlame finds when text was introduced. The dataset work
is done; a renderer on top would be a front end for someone else's result.

**C12 — a three-way merge for spreadsheets that survives a column insert** — p≈0.12.
Hook attempt: "Merges two people's edits to the same spreadsheet without destroying
either." Prior art: [daff](https://github.com/paulfitz/daff) diffs and merges tables
with column reordering and insertion. Materially equivalent.

**C13 — time-travel debugging for Python** — p≈0.15. Hook attempt: "Step backwards
through a program that has already crashed." Prior art: rr, PyTrace, and
[Python Tutor](https://pythontutor.com/) for the teaching case. Crowded.

**C14 — an explorable explanation of floating point** — p≈0.15. Hook attempt: "Drag
a number and watch the bits that represent it fight over it." Prior art:
[float.exposed](https://float.exposed/), float-toy, and a large body of explorable
float explanations. Materially equivalent.

**C15 — a compressor for screenshots that knows they are mostly text** — p≈0.05.
Hook attempt: "Shrinks a screenshot tenfold by noticing it is full of letters."
Prior art: JBIG2 and DjVu already compress text images by building a dictionary of
repeated glyph shapes — the same mechanism, standardised decades ago.

**C16 — a file that is simultaneously valid in several formats** — p≈0.04. Hook
attempt: "One file that is a picture, an archive and a document at the same time."
Prior art: [mitra](https://github.com/corkami/mitra) generates polyglots
systematically, and PoC||GTFO shipped them as a running joke for years.

**C17 — a small language for rhythm that compiles to MIDI** — p≈0.08. Prior art:
TidalCycles and [Strudel](https://strudel.cc/). Materially equivalent, and better.

**C18 — data transmitted as sound between two devices** — p≈0.06. Hook attempt:
"Sends a file across a room using only a speaker." Prior art:
[ggwave](https://github.com/ggerganov/ggwave), chirp.io, and a long history of
acoustic modems.

**C19 — the smallest edit that makes broken input parse** — p≈0.08. Hook attempt:
"Paste something broken and it shows the smallest possible change that makes it
valid." Prior art: Aho and Peterson's minimum-distance error-correcting parser
(SIAM J. Comput. 1972) is the algorithm, with a substantial later literature on
language edit distance; `jsonrepair` and friends cover the practical JSON case.
Building it would be an implementation of a known result, which Gate E rejects. Kept
in mind as a *component* — it is a plausible internal piece of C24.

**C20 — jq, but for binary data** — p≈0.07. Prior art:
[fq](https://github.com/wader/fq) is literally this, is mature, and is excellent.

**C21 — a solver that explains its answer the way a person would** — p≈0.09. Hook
attempt: "Solves the puzzle and then shows you the reasoning you could have found
yourself." Prior art: Demystify (Espasa, Gent, Miguel et al.) auto-generates
human-interpretable explanations from constraint models; Sudoku Explainer does the
narrow case. Materially equivalent. This kill is what reduced C26 to its generation
half.

**C22 — a city's transit system rendered as one live picture** — p≈0.12. Hook
attempt: "Watch every bus in a city breathe." Prior art: many live GTFS-RT
visualisations exist for individual cities and several general ones. Crowded.

**C23 — Pebble Evolve (owner's idea)** — see section 0 for the full verdict and the
searches. Passed on this run: the whole-projects gap is now claimed by EvoLattice,
CodeEvolve and DEI among others, and the part that remains unclaimed needs owner
taste data that does not exist yet.

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

### Run of 2026-09-18 — two candidates that are re-dressings of existing projects

**C2 — backfire's retry amplification, made visual** — p≈0.30. Hook attempt: "Watch
one click fan out into thirty requests across your call graph." Not a new candidate:
it is the "what would make it hyped" note already recorded under `backfire` below,
and selecting it would be re-building this repository's own work rather than going
somewhere new. Available as a re-scope of `backfire`; not available as a selection.

**C3 — orbiter's unit inference, live as you type** — p≈0.25. Hook attempt: "Watch
milliseconds turn into seconds as you type the expression." Same status as C2: it is
the note already recorded under `orbiter` below.

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

## 5. Under deliberation — shortlisted, decision not yet made

Candidates that cleared the gates far enough to be scored, but whose selection is
not settled. Nothing is built from this section. An entry leaves it in one
direction or the other as soon as its open question is answered, and the answer is
written into the entry.

The rule that a shortlist must survive a re-read at the start of the next run
applies here: these four were generated, searched and scored on 2026-09-18, and
**must not be implemented in the same run that produced them.**

### Scores, 2026-09-18

1-5 on hook strength, reach, demo-ability, originality, difficulty-worth-it,
monetizability. Originality is scored against what the searches this run actually
turned up, not against how the idea felt.

| Candidate | Hook | Reach | Demo | Orig. | Diff. | Money | Total |
|---|---|---|---|---|---|---|---|
| C24 every byte explained | 4 | 5 | 4 | 2.5 | 4 | 3 | 22.5 |
| C25 code you can misread aloud | 4 | 3 | 4 | 4 | 3 | 2 | 20 |
| C26 puzzles with a certified solving path | 3.5 | 3.5 | 5 | 3 | 4 | 3 | 22 |
| C27 dates that are only approximately known | 3 | 3 | 3 | 3 | 3 | 2 | 17 |

The totals are deliberately not the decision — they are close enough to each other
to be noise, which is the point of the pairwise comparison below.

### Pairwise: which would I be more upset to see someone else ship first?

* C24 vs C25 → **C24.** Someone shipping "point it at files nobody documented and it
  explains every byte" would take something I want to exist. C25 is charming; I would
  read the write-up and feel fine.
* C24 vs C26 → **C24**, but less comfortably. C26 has the better demo, because it is
  playable in a browser and C24 is a rendered picture of a file. What decides it is
  reach: C24 makes a class of later projects possible, C26 makes puzzles.
* C25 vs C26 → **C26**, on demo and on the fact that its problem is real to someone.

**Provisional leader: C24**, subject to the open question below, which is capable of
killing it outright. If C24 dies, the order behind it is C26, then C25, then C27, and
C29 gets searched properly before any of them are started.

---

### C24 — every byte of an undocumented file, explained and proven
2026-09-18. p≈0.08. Working name: `grain` (not settled).

**Hook attempt:** "Give it a pile of files in a format nobody documented, and it
hands back a parser that rebuilds every one of them byte for byte — and a picture of
what every byte means."

Descriptor: `{batch analysis, corpora of binary files, generated parser + rendered
field map, reverse engineering}`. That is a different cell from the three existing
projects, whose data source is Python source and whose medium is printed warnings.

**Why it might be the one.** The correctness criterion is unusually honest: a
description of a format is right if, and only if, parsing every file in the corpus
and re-serialising it reproduces the original bytes exactly. That is checkable
without a human ground truth, it cannot be fudged, and it produces the number the
README would live on — how many of the corpus files round-trip, and what fraction of
their bytes the description accounts for. It also answers *what becomes buildable
that wasn't*: lossless converters and viewers for files from dead software, a
format-aware fuzzer, a structural diff, and C28's merge.

**What the search found (2026-09-18).** Queries run: "infer binary file format
structure automatically from corpus of sample files field inference tool"; "Netzob
NEMESYS BinaryInferno automatic message format inference reverse engineering unknown
protocol"; "grammar induction file format learn parser from examples lossless
round-trip re-serialize byte identical validation"; "automatically generate Kaitai
Struct spec from sample files infer unknown format github tool"; "'file format'
reverse engineering tool infers structure from many samples annotated hex view
differential analysis open source"; "github infer binary format from multiple sample
files automatic structure discovery length field checksum detection".

The field is much more crowded than it looks from the outside, and one finding is
close enough to be dangerous:

* [BinaryInferno](https://github.com/binaryinferno/binaryinferno) (NDSS 2023) infers
  fields in binary *messages* from a corpus, using entropy-based boundary detection
  plus targeted detectors for lengths, floats and timestamps. Inspected directly: it
  takes hex messages on stdin and emits a flat field map. It does not do nesting,
  pointers, checksums, or re-serialisation. NEMESYS, Netzob, NETPLIER, FieldHunter
  and AWRE occupy the same space, and BinaryInferno reports beating them.
* [RL-GRIT](https://arxiv.org/pdf/2105.13114) (arXiv 2105.13114) takes a corpus of
  files, infers a grammar and a parser, **and already uses round-trip
  re-serialisation as its correctness criterion.** This is the single most important
  thing found this run: the criterion I thought was the distinguishing idea is not
  new. It reports limits on deeply nested and irregular structures.
* Saggitarius (arXiv 2308.12329) and the Interval Parsing Grammars work (PLDI/OOPSLA)
  are about *writing* format specifications well, not inferring them — but the
  Saggitarius paper's own framing, that existing grammar induction tools "require
  large volumes of examples, are specialized to particular tasks, and/or don't scale
  well", is the honest state of the art.
* imHex, Hexinator, Synalyze It!, 010 Editor templates and Kaitai Struct all require
  a human to write the grammar. binwalk and polyfile are signature-based.
* `jbirby/binary-format-reverser` appears in search results with a description that
  overlaps this candidate substantially — sample comparison, brute-forced offsets and
  types, emitting a runnable Python parser and a format specification for
  record-based formats. **It could not be verified.** `github.com/jbirby/binary-format-reverser`
  returned 404, and so did the raw README on both `main` and `master`, on 2026-09-18.
  Repository deleted, renamed, private, or the search index is wrong; unresolved.

**The open question that decides it.** After the searches above, what is left
unclaimed is *not* "infer a format from a corpus" and *not* "verify by round-trip" —
both are taken. What is left is the part every one of these stops at: files whose
structure is a graph rather than a sequence. Offset tables that point elsewhere in
the file, nested containers, back-references, checksums computed over byte ranges,
and the discipline of accounting for every byte rather than labelling some of them.
That is where real proprietary formats live, and it is also the hard part. So the
question for the next run is narrow and answerable:

> Does any existing tool or paper infer *pointer and container structure* — offsets
> resolved as edges, nesting recovered, coverage of the whole file reported — from a
> corpus of files, as opposed to flat field boundaries within a message?

Searches to run: "pointer inference binary format offset table recovery corpus";
"hierarchical structure inference file format nested chunks"; "byte coverage
complete parse unknown format"; plus a direct look at NETPLIER and at the
`jbirby` repository if it can be made to resolve. If the answer is yes, C24 drops to
section 2 and C26 is promoted. If the answer is no, C24 needs a milestone ladder
whose first rung is the pointer case done badly end to end — **not** the flat-record
case, which is taken.

**Partial answer to that question, same run (2026-09-18).** Three of the four searches
were run before stopping, because resolving prior art is a factual matter that the
sleep-on-it gap does not protect against — only implementation was withheld. Results:

* Hierarchical format inference **does** now exist for network protocols: "Scalable
  hierarchical protocol format inference via feature-heuristic message delimiter"
  (Empirical Software Engineering, 2026,
  [link](https://link.springer.com/article/10.1007/s10664-026-10814-6)). Still
  messages, still no pointers into the artifact, still no re-serialisation.
* Pointer and structure recovery **does** exist from program binaries — OSPREY
  ([S&P 2021](https://yonghwi-kwon.github.io/data/osprey_sp21.pdf)) recovers variables
  and data structures by probabilistic analysis of memory accesses, and there is a
  large type-inference-from-stripped-binaries literature. Different input entirely:
  these need the *program*, and the premise of C24 is that you have only the files.
* [NetPlier](https://github.com/netplier-tool/NetPlier) (NDSS 2021) aligns messages by
  multiple sequence alignment and infers the keyword field probabilistically. Flat,
  message-level, no nesting or pointers.
* No match found for inferring **offset-as-edge structure and whole-file byte coverage
  from a corpus of files**. Searched: "pointer inference binary file format offset
  table recovery hierarchical nested structure from sample corpus automatic";
  "NETPLIER probabilistic field inference nested structure limitations"; "'byte
  coverage' OR 'explain every byte' unknown file format inference complete parse
  unclaimed bytes tool". Absence of evidence after three query formulations is weak
  evidence of absence, and this is recorded as a partial answer, not a verdict.

**On the unreachable repository.** `github.com/jbirby/binary-format-reverser` is
probably a genuine 404 rather than an access restriction: `WebFetch` read
`github.com/binaryinferno/binaryinferno` successfully in the same run, so GitHub
project pages are reachable from here. A `curl` cross-check is not available — this
environment's proxy binds raw GitHub access to `guthib241/pebble` and returns 403 for
anything else, which is worth knowing for every future prior-art search: GitHub can be
read through `WebFetch`, not through `curl`. The repository may have been deleted,
renamed or made private after being indexed. Still unresolved, still the largest gap.

**Red team, written before any decision.**

* *The closest existing thing.* RL-GRIT, and whatever `jbirby/binary-format-reverser`
  turns out to be. A reader who knows the protocol-RE literature will say this is
  BinaryInferno pointed at files. The answer has to be the pointer graph and the
  coverage guarantee, demonstrated, or there is no answer.
* *Why a stranger would shrug.* Because most people have never had an undocumented
  file they needed to open, and the ones who have reach for a hex editor and a
  weekend. The demo has to show a file from software that no longer exists, opening.
* *The part only interesting to its author.* The round-trip proof. It is the most
  satisfying property of the design and, now that RL-GRIT has it, the least novel
  thing about it. Do not build the README around it.
* *Unanswered.* Whether the pointer-graph case can be made to work at all on a real
  format inside a handful of runs. This is the one that could end the project, and
  the vertical slice exists to find out early and cheaply.
* *Shape-ban risk.* Real. Run a command, read a spec is one rename away from run a
  command, read a report. The mitigation is that the primary artifact is a generated
  parser plus a rendered field map, not prose — and if that stops being true, the
  candidate has drifted back into the banned shape and should be dropped.

### C25 — a code you can read aloud badly and still get right
2026-09-18. p≈0.05.

**Hook attempt:** "Read the code down a bad phone line, let the other person mishear
a syllable, and it still decodes to the right thing."

Descriptor: `{interactive, none (pure algorithm), spoken audio + web page, encoding}`.

An encoding whose error model is *human mishearing* rather than bit flips: build the
channel from published phoneme confusion data (Miller and Nicely 1955 is public, and
modern ASR confusion matrices exist), then design a code over words whose distance
metric is confusability rather than Hamming distance, so that one misheard syllable
is corrected rather than merely detected. Prior art found this run is about
*distinctness*, not correction: the NATO alphabet, the PGP/biometric word list,
Proquint, Crockford base32, BIP39 checksums. Searching also surfaced a large ASR
error-correction literature, which is a different problem — correcting a recogniser's
output using language context, not designing a code with a guaranteed correction
property.

**Open question:** whether a real correction guarantee survives contact with a real
confusion matrix, or whether the achievable code is so long that nobody would read it
aloud. That is answerable cheaply with a simulation before committing.

**Why it is not the leader:** reach. It is one sharp primitive with a delightful demo
and a small blast radius.

### C26 — puzzles that come with a proof of how they must be solved
2026-09-18. p≈0.07.

**Hook attempt:** "Generates a puzzle and proves it can be solved with exactly the
three techniques you have taught — and never a guess."

Descriptor: `{playable, generated, browser, games and teaching}`.

Difficulty as a proof object: the generator does not rate a puzzle after the fact, it
constructs one whose certified solving trace uses a chosen set of deduction rules and
no others. Demystify (section 2, C21) already covers *explaining* a solution, which
is why this is scoped to generation. Best demo in the shortlist — it is playable, and
the proof can be shown beside the puzzle.

**Open question:** whether "requires exactly these techniques" can be certified
rather than merely observed, for more than one puzzle family, and whether existing
per-puzzle generators (Simon Tatham's collection rates difficulty by technique
already) leave enough room. Not yet searched properly.

### C27 — dates that are only approximately known
2026-09-18. p≈0.06.

**Hook attempt:** "Give it a family tree full of 'about 1850' and it tells you which
of those dates are impossible."

Descriptor: `{batch, archival records, timeline render, history and genealogy}`.

Interval constraint propagation over uncertain dates, with provenance: narrow every
date to its tightest defensible range and report contradictions. Searched: the
conceptual foundations are well covered (fuzzy temporal intervals, Allen's interval
algebra, EDTF as a notation, archaeological uncertainty frameworks), while usable
tooling is thin and genealogy software does only shallow consistency checks.

**Why it is not the leader:** the hook is good but the result is a narrower timeline,
and the originality is in the engineering rather than the idea.
