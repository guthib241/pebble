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

**Status: considered first on 2026-09-16, passed on for now — see the decision note
at the end of this entry.** It has not been through the full gates and must not be
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

**Decision note, 2026-09-16 (run: selection).** Considered first, as required, and
passed on for this cycle. The reasons, so the owner can push back:

1. *The one component that would make it distinctive cannot be built yet.* The
   taste signal is what separates this from AlphaEvolve / FunSearch / OpenEvolve /
   ShinkaEvolve, and it needs a body of the owner's own delight ratings. There are
   none. Building the loop without it produces a generic evolutionary code search,
   which fails Gate E against a crowded, well-funded field.
2. *It has no ten-second demo at milestone 1.* What you would show a stranger is an
   archive of candidate descriptions — text about projects, not a project. Gate F.
3. *It is a process, not an artifact.* The useful parts of it (tail sampling, first-
   idea rejection, behaviour descriptors, pairwise comparison, red-teaming) are
   already adopted into `AGENT_RULES.md` and were used to produce this run's pool.
   The remaining delta is the automation, which is the least interesting part.

**What would move it:** the owner rating ~50 candidates from this file 1-5 on
personal delight. That single artifact turns the taste model from unbuildable into
buildable, and it is the cheapest thing the owner could contribute. Section 5's
pool is a ready-made source of candidates to rate.

### (add yours below)

---

## 1. Rejected — failed the rules

Ideas that failed a gate for reasons other than prior art: not feasible here, no
definition of done, no first step, no real problem, inside the shape ban, or
memorable but useless.

Format: **name** — date. Hook attempt. Which gate failed and exactly why.

### explorable explanation "of something" — 2026-09-16
Hook attempt: none possible. Descriptor: `{reader manipulates, varies, web, varies}`.
Generated as a candidate and rejected immediately: it names a *form*, not an idea.
There is no subject, so there is nothing to search and nothing to build. Recorded
because the temptation to write "a Bret Victor style explorable of X" and call it a
candidate will recur, and it is not one until X is chosen. Gate A and Gate D.

### despill and edge-detail keyer (green screen, classical, no ML) — 2026-09-16
Hook attempt: "pulls a clean key off a cheap green screen without eating the hair."
Descriptor: `{filter, video frames, video, GUI/plugin}`. Aligned with the owner's
Corridor reference in `REFERENCES.md`, which is why it was generated. Failed Gate B
here: the version that would beat what exists is learned matting, and this
environment has no GPU and no matting training data, while the classical version
sits inside mature prior art (every compositor ships despill — Nuke, Fusion, After
Effects, OBS). Not searched exhaustively; if a future run revisits it, search
learned matting (RVM, BiMatting) and classical despill algorithms first. Recorded
so the owner's reference is not mistaken for an unexamined direction — it was
examined, and the environment is the blocker, not the idea.

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

### regex delta — which strings your edit started or stopped matching — rejected (2026-09-16)
Hook attempt: "change a regex and it shows you the exact strings that used to match
and don't any more." Descriptor: `{live editor, pair of regexes, text, web}`.
A genuinely good hook, killed by the engine already existing as a library.
Prior art: [greenery](https://github.com/qntm/greenery) (regex → FSM, difference,
intersection, complement, and enumeration of matching strings, plus FSM → regex
reconstruction), [interegular](https://github.com/MegaIng/interegular) (same
operations, tuned for Python `re` syntax), and
[RegexSolver](https://regexsolver.com/) (commercial engine and
[online demo](https://regexsolver.com/demo) doing intersection, subtraction,
complement, comparison and enumeration, with open-source clients in several
languages). Subtract-two-regexes-and-enumerate-the-difference is the documented
core of all three. What is left for this candidate is a front end over someone
else's primitive, which is the wrapper failure in `AGENT_RULES.md`, not a project.
**Partially settled.** The unclaimed remainder, if a future run wants it: the same
question for *real* regex features that automata cannot express — backreferences,
lookaround, lazy quantifiers — where witness generation needs a solver rather than
a difference automaton. That is a research-scale problem and was not searched.

### PDF draft time-lapse — replaying a document's own edit history — rejected (2026-09-16)
Hook attempt: "every PDF quietly carries its own earlier drafts — this plays them
back like a time-lapse." Descriptor: `{player, PDF internal revisions, document,
web}`. **This was this run's first idea, and is recorded as rejected on both
counts:** as the first idea it was rejected as a final answer per the generation
rules, and it then died independently on prior art.
Prior art: [pdfresurrect](https://github.com/enferex/pdfresurrect) — extracts every
previous version retained by a PDF's incremental updates and produces a summary of
changes between versions; packaged in Fedora, Ubuntu, MacPorts and FreeBSD ports.
The extraction and the version summary are the whole mechanism; rendering the
extracted versions as an animation is a presentation layer on top of a solved
problem. Section 10 material equivalence.

### barrier-grid / scanimation generator — rejected (2026-09-16)
Hook attempt: "print two sheets, slide one over the other, and the picture moves."
Descriptor: `{generator, image sequence, print + transparency, desktop}`. Delightful,
and thoroughly occupied. Prior art:
[animbar](http://animbar.mnim.org/) (takes a set of input images, emits the paper
sheet and the transparency), the
[Mightool scanimation generator](https://www.mightool.com/scanimation) (free, web,
emits composite plus grating), and
[guevaracodina/barrier_grid_animation](https://github.com/guevaracodina/barrier_grid_animation).
The technique itself dates to the 1890s and was commercialised as Scanimation books
from 2007. Same inputs, same mechanism, same outputs.

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

_As of 2026-09-16 there is a leading candidate — `dovetail` — which is **not** yet
selected. It is held in section 5 until it survives the cold re-read required by the
sleep-on-it rule and two named prior-art searches are closed. Do not move it here
until both are done._


---

## 5. Candidate pools, by run

The generation record. Every candidate produced in a run is listed here with its
rough probability at generation time, its behaviour descriptor, and where it ended
up. Entries that reached an outcome have their substantive record under the matching
heading above; entries marked *parked* were generated but not carried through the
gates this run, and are honest about not having been searched.

Parked is not rejected. A parked candidate is inventory: the next run that needs a
pool starts from these instead of from nothing.

### Run of 2026-09-16 — 26 candidates, selection only, no implementation

Existing projects all occupy one cell — `{reads source files, prints text,
developer tooling, local CLI}`. That cell was excluded by hand from this pool.

| # | Candidate | p | Descriptor `{interaction, data, medium, domain}` | Outcome |
|---|-----------|---|--------------------------------|---------|
| 1 | **dovetail** — three-way merge for Blender `.blend` files | 0.03 | `{merge driver, binary scene graph, 3D files, library + CLI}` | **Shortlist — leading candidate** (below) |
| 2 | **driftwood** — image format that survives random byte loss | 0.05 | `{file format, image bytes, image, format + web demo}` | **Shortlist — runner-up** (below) |
| 3 | regex delta witnesses | 0.08 | `{live editor, regex pair, text, web}` | Rejected, prior art → §2 |
| 4 | PDF draft time-lapse | 0.06 | `{player, PDF revisions, document, web}` | Rejected — first idea, and prior art → §2 |
| 5 | barrier-grid / scanimation generator | 0.04 | `{generator, image sequence, print, desktop}` | Rejected, prior art → §2 |
| 6 | explorable explanation "of something" | 0.20 | `{reader manipulates, —, web, —}` | Rejected, not an idea → §1 |
| 7 | despill / edge-detail green-screen keyer | 0.07 | `{filter, video frames, video, GUI}` | Rejected, Gate B here → §1 |
| 8 | merge for DAW projects (Ableton `.als`, MIDI) | 0.03 | `{merge driver, gzipped XML project, music, CLI}` | Parked — sibling of #1; the natural second format for testing #1's primitive claim. Prior art to search: Splice Studio (versioning, discontinued), `git-lfs` workflows. Not searched. |
| 9 | scan diff — align two scans of one printed page, glow what changed | 0.08 | `{viewer, scanned images, documents, web}` | Parked, not searched. Expect prior art in DiffPDF/Draftable for text PDFs; the warp-invariant *scan* case looked thinner. |
| 10 | recurrence algebra with a visual calendar | 0.15 | `{library + viz, schedule expressions, time, web}` | Parked. Expect material prior art: Fowler's temporal expressions (1997), `dateutil.rrule`, `ice_cube`. Near the mode. |
| 11 | Knuth-Plass global line-breaking for subtitles | 0.05 | `{batch processor, subtitle files, video text, CLI}` | Parked. Real and probably unclaimed, but the hook is weak and the output is a file nobody looks at. |
| 12 | sonification of live buoy / lightning feeds | 0.12 | `{audio stream, public sensor feed, sound, web}` | Parked. Crowded genre; "data sonification" has a decade of art projects. |
| 13 | GTFS day-of-transit animation | 0.20 | `{animation, transit feed, motion, web}` | Parked as a recognised mode — many "a day of transit" visualisations exist. |
| 14 | whole spreadsheet encoded in a URL | 0.10 | `{app, URL payload, web, productivity}` | Parked. Prior art: itty.bitty.site, urlpages. |
| 15 | knitting as a compile target | 0.04 | `{compiler, pattern source, textile, physical}` | Parked. Prior art: CMU knitout / KnitScript. |
| 16 | structural diff+merge for SVG artwork | 0.09 | `{merge driver, vector XML, illustration, CLI}` | Parked — sibling of #1, weaker because SVG is text and partially merge-able already. |
| 17 | extract `cutline`'s minimal-cut engine as a standalone primitive | 0.30 | `{solver, constraint sets, scheduling, library}` | Parked. `PROGRESS.md` flags it, and it is real — but it is a second bite at an occupied cell and the mode of this repository's own history. Do it when nothing better is on the list, not now. |
| 18 | halftone descreening of scanned print | 0.06 | `{filter, scanned images, image, desktop}` | Parked. Prior art: Sattva Descreen and similar. |
| 19 | automatic letterfitting / kerning by simulated physics | 0.07 | `{generator, font outlines, typography, library}` | Parked. Prior art: kernagic, autokern. |
| 20 | time-travel program state visualiser | 0.15 | `{scrubber, execution trace, code, web}` | Parked. Crowded: Python Tutor, rr, replay debuggers. |
| 21 | sketch-to-shape search over patent drawings | 0.08 | `{search, patent image corpus, drawings, web}` | Parked. Google Patents image search is close. |
| 22 | visual atlas of the shape space of every free font | 0.10 | `{map, font binaries, typography, web}` | Parked. Prior art: Google Font Map (t-SNE of fonts). |
| 23 | sync two amateur recordings of one event by audio fingerprint | 0.10 | `{aligner, audio tracks, video, CLI}` | Parked. Built into NLEs (PluralEyes, Premiere, Resolve). |
| 24 | paper data format that survives photocopying | 0.05 | `{codec, arbitrary bytes, print, CLI}` | Parked. Prior art: Optar, PaperBack, colorsafe. |
| 25 | teletext recovery from off-air recordings | 0.04 | `{decoder, VHS captures, broadcast data, CLI}` | Parked. The `vhs-teletext` project occupies this. |
| 26 | corpus-specific compressor (chess / GPS / sheet music) | 0.20 | `{codec, domain corpus, files, library}` | Parked as a recognised mode; every one of these has specialist prior art. |

**Constraint injection, as required.** Two constraints were forced onto candidates
mid-generation and both changed the pool: *"assume the file is damaged"* turned a
dull image-format idea into #2, and *"the result must be verifiable by a tool that
is not mine"* turned #1 from a scripting exercise into a project with an
independent oracle (Blender itself re-opening and rendering the merged file). That
oracle is now part of #1's design rather than an afterthought.

---

### Shortlist detail

#### 1. dovetail — three-way merge for Blender `.blend` files

*Proposed hook sentence (Gate F, written before any implementation):*

> **Two artists edited the same 3D file at the same time — this merges both of
> their changes into one file that opens in Blender.**

*Proposed demo (ten seconds, no install):* three rendered frames side by side —
what A changed, what B changed, and the merged file with both, rendered from the
merge output by Blender itself rather than by anything this project wrote.

*Why it is not inside the shape ban:* the output is a working file, not a report.
Nothing about it is "run a command, read warnings, check the exit code".

*What becomes buildable that wasn't:* code review, branching and pull requests for
3D scenes — the same workflow programmers have had for twenty years and 3D artists
have not. Underneath the application it is a structural three-way merge over a
self-describing binary object graph, which is the part that generalises (see #8
and #16 for the two formats that would test that claim).

**Prior art found, 2026-09-16.** Search scope, stated precisely: web search across
several query formulations, GitHub, PyPI, and search-result summaries of the Blender
developer tracker and Blender Artists forum threads. A direct fetch of
`projects.blender.org` returned HTTP 403 from this environment, so **the PR contents
below come from search-result summaries and have not been read firsthand** — the
next run should try to read PR #151266 directly before relying on it further:

| Dimension | dovetail | `blend_diff` (Blender PR #151266) | `blendiff` (PyPI) | `ifcmerge` | UnityYAMLMerge |
|---|---|---|---|---|---|
| Problem | two artists' edits collide | reviewing a change | reviewing a change | merging BIM models | merging Unity scenes |
| Output | a merged `.blend` | textual diff | textual diff | merged IFC | merged YAML |
| Applies changes? | yes | **no** | no | yes | yes |
| Format | compressed binary heap, pointer identity | same | same | text-ish IFC | YAML with stable file IDs |

The decisive line is upstream Blender's own, on PR #151266 — as reported in a
search-result summary rather than read directly, per the scope note above: the diff
tool *"only allows seeing what has changed and does not allow applying or merging
diffs, which is a significantly more complex problem in general."* Treat it as
strong but unverified until the page is read. Demand is documented on the
Blender Artists forum and in collaboration guides, which uniformly answer "you
cannot merge `.blend` files". Closest true prior art is `ifcmerge` — three-way
merge, different format, and it requires all authoring to happen in a native-IFC
application.

*Not yet searched, and required before selection is final:* the model-driven
engineering literature on three-way model merging (EMF Compare, EMF Diff/Merge,
and the academic work on merging graph-structured models). That field has solved
adjacent problems and could materially overlap the *algorithm* even though it has
never been applied to `.blend`. This is the single largest open novelty question.

**Feasibility, verified this run (not asserted):** `pip install bpy` gives Blender
5.0.1 as an importable module in this environment; a script authored a cube, a sun
and a camera, saved a `.blend`, re-opened it and rendered a 160×160 PNG with Cycles
on CPU (GPU/EGL paths are unavailable, so `BLENDER_WORKBENCH` fails and Cycles-CPU
is the render path to use). The saved file begins `28 b5 2f fd` — Zstandard, not
`BLENDER`: Blender 3.0+ compresses saves by default, so any parser must decompress
before it will find the `SDNA` block. Gate B is therefore satisfied *and* the
independent verification oracle exists: every merged file can be proved to open and
render by Blender itself.

**Scores (1-5):** hook 4 · reach 5 · demo-ability 4 · originality 4 ·
difficulty-worth-it 5 · monetizability 4.

#### 2. driftwood — an image format that degrades instead of dying

*Proposed hook sentence:*

> **Delete a third of this file at random and the photograph is still there — just
> softer.**

*Proposed demo:* a slider that destroys N% of the bytes, with driftwood on one side
getting gradually blurrier and a JPEG on the other side turning to garbage at 1%.

**Prior art found, 2026-09-16:** the *theory* is old and thoroughly published —
joint source-channel coding, fountain/rateless codes (RaptorQ, RFC 6330, with
mature implementations such as OpenRQ and `cberner/raptorq`), and JPEG 2000's
error-resilience tools plus JPWL (Part 11), which exists precisely to make images
survive lossy channels. PAR2 protects files against bit rot but as *separate*
recovery volumes, not as part of the image. What the searches did not surface is a
usable single-file format where arbitrary byte loss costs resolution rather than
the file — and note the honest wrinkle found while searching: RaptorQ repairs
*erasures at known symbol positions*, so making it work on a file that has simply
lost bytes requires self-locating symbols, which is a real design problem rather
than a library call.

**Scores (1-5):** hook 5 · reach 3 · demo-ability 5 · originality 2 ·
difficulty-worth-it 3 · monetizability 2.

The 2 on originality is the honest score and it is what settles the comparison.
The contribution would be packaging 25-year-old theory into something usable, and
the README would have to say exactly that.

#### Pairwise: which would I be more upset to see someone else ship first?

**dovetail wins.** If someone shipped driftwood tomorrow, the reaction is "nice
demo of known theory" — JPWL has existed since 2004. If someone shipped dovetail
tomorrow, the reaction is that they solved the thing an entire community has been
told is unsolvable, on a format whose own maintainers describe merging as
significantly harder than the diff they are still building. That asymmetry is
larger than the gap in hook strength, which is the one dimension driftwood wins.

driftwood stays on the shortlist rather than being rejected: if dovetail's
remaining prior-art search turns up a materially equivalent merge algorithm,
driftwood is the fallback and its own search is already half done.

#### Red team of the leader, in bad faith, before anything is built

1. **"This is UnityYAMLMerge for Blender."** The closest real objection. Answer:
   Unity scenes are YAML text carrying stable file IDs that survive saves — the
   format was designed to be merged, and the merge is a structural three-way diff
   over labelled nodes. A `.blend` is a compressed dump of C structs whose identity
   is a raw 64-bit memory address from the authoring session, which does not
   survive a save, let alone two independent ones. Establishing identity across two
   saves *is* the problem, and it is not the problem Unity solved. If that turns
   out to be easy, the project is much smaller than it looks and should be dropped.
2. **"A stranger who doesn't use Blender shrugs."** Fair, and it caps the hook at
   4. Mitigation is the demo carrying the explanation: three renders, and anyone
   who has shared a file with a colleague understands the problem instantly.
3. **"The part you find interesting — SDNA parsing — is the part nobody cares
   about."** Correct, and it is a documentation rule, not an argument: the README
   leads with the render, and the format archaeology goes below the fold.
4. **"It will silently corrupt files, which is worse than not existing."** The
   strongest objection and it shapes the design. The answer is refusal: merge only
   what can be proved safe, refuse the rest loudly, and verify every output by
   re-opening and rendering it in Blender before claiming success. A tool that
   merges the easy 80% and declines the rest honestly is useful; one that produces
   plausible-looking corruption is not.
5. **"If you merge by appending through `bpy`, it is a script, not a primitive."**
   Also correct. The primitive version works on the file structure directly — as
   upstream's diff deliberately does — and uses `bpy` only as an independent
   oracle. That distinction must be settled before milestone 1, not during it.

**Objection 1 is not fully answered until the model-merging literature is
searched.** That is why this is a leading candidate and not a selection.
