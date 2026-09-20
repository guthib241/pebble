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

### (add yours below)

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

