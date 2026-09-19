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
* **Section 5 holds candidates still under consideration** when a run ends mid-decision,
  which the protocol allows and the sleep-on-it rule effectively requires. An entry there
  is not a selection. Re-read section 5 at the start of the next run, before anything is
  built, and move each entry out of it once it is settled.

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

### Pebble Evolve — considered 2026-09-19, passed on for now

Read first this run, as required. Passing, with reasons, so the owner can push back.

**Why not this run.** Two of the four concerns recorded above are still true and neither
is a matter of effort. (1) The taste model needs a body of the owner's own delight
ratings, and there are none — that component cannot be built honestly today, and the
system without it is generic interestingness search, which is exactly the crowded part.
(2) The remaining unclaimed slice — evolution at the level of whole user-facing projects
rather than single functions — is meta-work about this repository's own process, not a
project a stranger could look at for ten seconds and understand. It would also be graded
by the thing it is trying to improve, which is a weak evaluation loop.

**What would change the answer.** Either the owner starts recording delight ratings on
real candidates (even twenty would make the taste signal buildable and would itself be a
dataset nobody has), or the idea gets re-scoped to something with an external result —
the archive of behaviour descriptors applied to a domain outside this repository, where
coverage of the space can be shown as a picture rather than asserted.

**Not re-searched this run.** The prior art recorded above (AlphaEvolve, FunSearch,
OpenEvolve, ShinkaEvolve, MAP-Elites, novelty search, OMNI/OMNI-EPIC) was taken as
given, not re-verified. A future run that reconsiders this should check whether the
project-level framing has since been published.

### (add yours below)

---

## 1. Rejected — failed the rules

Ideas that failed a gate for reasons other than prior art: not feasible here, no
definition of done, no first step, no real problem, inside the shape ban, or
memorable but useless.

Format: **name** — date. Hook attempt. Which gate failed and exactly why.

### semantic diff and merge for binary formats — rejected as this run's first idea (2026-09-19)
Hook attempt: "Diff two save files and read 'gold: 400 → 1200' instead of a hex dump."
Descriptor: `{reads binary files, grammar-driven, developer tooling, library}`.
If it works: version control for save games, firmware configs, project files — anything
with a grammar. Rejected under the generation rule that **the first idea is not the final
answer**: it is the statistical mode for an agent sitting in a repository full of
developer tooling, and it arrived instantly, which is the tell. Also partly served
already: DFDL/Daffodil parses binary to XML and existing XML diffs handle the rest, and
Kaitai Struct supplies grammars.
**The live remnant, not yet searched:** three-way *merge* that writes a valid binary file
back out is a materially harder problem than diff, and searching for it was deliberately
left undone rather than done badly. A future run may take this up as its own candidate —
but as a merge primitive, not as a diff viewer.

### FCC device-authorization internal photo archive — held, feasibility unverified (2026-09-19)
Hook attempt: "A search engine for the insides of every wireless device sold in America."
Descriptor: `{bulk public archive, image search, hardware, web}`.
If it works: a visual history of consumer hardware internals; component-level lookup.
Not rejected on merit — held because Gate B is unverified in the direction that matters:
bulk retrieval volume, the terms attached to the archive, and whether the internal photos
are reachable without scraping behaviour the rules forbid. **Do not start this without
settling that first**, and record what is found either way.

### patent-drawing archive, searchable by shape — held, unsearched (2026-09-19)
Hook attempt: "Draw a shape and see every patent drawing that looks like it."
Descriptor: `{bulk public archive, shape retrieval, invention history, web}`.
If it works: a visual index into a century of public-domain technical drawing.
Held, not searched: patent-image retrieval is an active research area and prior art is
likely dense. Search it properly before reconsidering.

### historical ship-logbook weather reconstruction — rejected on redundancy (2026-09-19)
Hook attempt: "Reconstructs storms from what sailors wrote down two centuries ago."
Descriptor: `{archival scans, climate reconstruction, science, data}`.
The digitisation and reconstruction have both been done at scale by oldWeather and the
ICOADS/ERA reanalysis programmes. Entering behind that with less data and no domain
review is not a contribution. Recorded rather than searched exhaustively; if revisited,
the question is whether any *specific* unexploited logbook corpus remains.

### a game whose mechanic is a real algorithm — no hook yet (2026-09-19)
Hook attempt: "A puzzle game where you play the part of the cache." Flat, and the shape is
crowded by the Zachtronics family. Kept as a direction rather than a candidate: the
mechanic has to come from an algorithm whose *failure modes are fun*, and none of the
candidates considered had that property. Revisit only with a specific algorithm in hand.


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

### shadow art — a sculpture whose shadows are three different pictures — rejected (2026-09-19)
Hook attempt: "One lump of plastic that throws three different pictures on three walls."
Descriptor: `{3D geometry, optimization, sculpture/fabrication, visual}`.
Searched: "shadow art 3D object multiple shadows optimization open source implementation
github". Prior art: Mitra & Pauly, *Shadow Art* (SIGGRAPH Asia 2009);
[ShadowArt-Revisited](https://github.com/kaustubh-sadekar/ShadowArt-Revisited)
(differentiable-rendering implementation, PyTorch3D, [arXiv:2107.14539](https://arxiv.org/pdf/2107.14539));
[ShadowDraw](https://github.com/Red-Fairy/ShadowDraw) (CVPR 2026). Same problem, same
mechanism, same output, already implemented in the open. Materially equivalent.

### automatic un-shredding of documents — rejected (2026-09-19)
Hook attempt: "Photograph a bin of shredded paper and get the page back."
Descriptor: `{photo input, combinatorial reassembly, forensics, visual}`.
Searched: "automatic reassembly shredded torn document software open source unshredding".
Prior art: [RazvanRanca/UnShredder](https://github.com/RazvanRanca/UnShredder) (strip and
cross-cut, probabilistic scoring, open source); [JigsawNet](https://arxiv.org/pdf/1809.04137);
[PairingNet](https://arxiv.org/pdf/2312.08704); commercial
[Unshredder](https://www.unshredder.com/document-reconstruction-software-process); and the
DARPA Shredder Challenge behind much of it. Crowded across research and open source.

### barrier-grid / scanimation compiler — rejected (2026-09-19)
Hook attempt: "Print two sheets, slide one over the other, and the picture walks."
Descriptor: `{image sequence, optical interference, print/physical, visual}`.
Searched: "barrier grid scanimation moiré animation generator open source". Prior art:
[animbar](http://animbar.mnim.org/) (exactly this, cross-platform, open source);
[jthawme/kinegram](https://github.com/jthawme/kinegram);
[guevaracodina/barrier_grid_animation](https://github.com/guevaracodina/barrier_grid_animation);
and MIT's [FabObscura](https://vis.csail.mit.edu/pubs/fabobscura.pdf) (2025), which
generalises barrier-grid design to arbitrary pattern functions. Nothing material left.

### linkage synthesis from a drawn curve — rejected (2026-09-19)
Hook attempt: "Draw a squiggle and get a cardboard machine that draws it for you."
Descriptor: `{drawn curve, mechanism synthesis, fabrication, interactive}`.
This was the strongest candidate of the run on hook alone, and it is taken. Searched:
"four-bar linkage path synthesis Fourier descriptors open source" and "linkage synthesis
web app traces arbitrary curve github". Prior art:
[Pyslvs-UI](https://github.com/KmolYuan/Pyslvs-UI) (open-source planar linkage simulation
*and* synthesis); [pylinkage-editor](https://github.com/HugoFara/pylinkage-editor)
(interactive canvas, synthesises four-bars for path generation, runs in the browser via
Pyodide); [LInK](https://github.com/ahnobari/LInK) and the
[LINKS](https://arxiv.org/pdf/2208.14567) hundred-million-mechanism dataset; plus an
open-source four-bar path-synthesis tool using Fourier descriptors and a trained network.
Same input (a curve), same output (a mechanism), same workflow.

### transit-network fragility map from GTFS — rejected (2026-09-19)
Hook attempt: "Shows the two minutes of the day the whole network depends on."
Descriptor: `{public feed, graph analysis, transit, map}`.
Searched: "GTFS transit network fragility critical transfer single point of failure
visualization". Prior art: G2Viz; [GTFS2STN](https://arxiv.org/pdf/2405.02760); a
graph-oriented GTFS transit analysis literature with centrality-based critical-node
identification already standard. Entering an active academic field with the obvious
metric is not a contribution.

### caustic surface that projects a photograph — rejected on known prior art (2026-09-19)
Hook attempt: "A blank sheet of acrylic that throws your face onto the wall in light."
Descriptor: `{image input, inverse optics, fabrication, visual}`.
Not deeply searched — rejected on prior art already known to be dense: Schwartzburg et al.,
*High-contrast Computational Caustic Design* (SIGGRAPH 2014), the Rayform commercialisation
of it, and Matt Ferraro's widely-read open write-up and code for caustics engineering. If
ever revisited, record a real search; this entry is an informed rejection, not a searched one.

### spreadsheet that propagates uncertainty instead of point values — rejected (2026-09-19)
Hook attempt: "A spreadsheet where every number carries how sure you are."
Descriptor: `{tabular input, distribution arithmetic, estimation, interactive}`.
Prior art known without searching: Guesstimate, the Squiggle language, and Causal all do
distribution-valued cells. Materially equivalent.

### a font that renders numbers as charts — rejected (2026-09-19)
Hook attempt: "A font that turns any column of numbers into a chart, with no tooling."
Descriptor: `{text, font shaping, data display, typography}`.
Prior art: the Sparks font (After the Flood) and FF Chartwell do exactly this with
OpenType features. Settled.

### CRDT / mergeable format for structured documents — rejected (2026-09-19)
Hook attempt: "Two people edit the same file offline and it just merges."
Prior art: Yjs, Automerge, Loro. One of the most crowded areas in open source.

### paper as storage — print data, scan it back — rejected (2026-09-19)
Hook attempt: "Print your files as pages and read them back with a scanner."
Descriptor: `{arbitrary bytes, error correction, print/physical, archival}`.
Prior art: PaperBack, Optar, Colorsafe, and the many QR-archive variants. Settled.

### Wang-tile / wave-function-collapse pattern language — rejected (2026-09-19)
Hook attempt: "A tiny language for patterns that never repeat."
Prior art: the WFC ecosystem after mxgmn's original is very large. Settled.

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

### cache that reports its own regret — no demo (2026-09-19)
Hook attempt: "Shows you which of your cache's evictions were mistakes, while it runs."
Descriptor: `{live event stream, online vs offline-optimal comparison, systems, report}`.
If it works: any cache could report distance-from-optimal instead of a hit rate, which
would make eviction-policy tuning empirical rather than folkloric. Real and, as far as
considered, unshipped as a live component — but its output is a report, which puts it
inside the shape ban, and the ten-second artifact does not exist. What would make it
hyped: the comparison against the oracle shown as something you *watch* — the moment the
policy diverges from optimal, visible as it happens, not summarised afterwards.

### file birth certificate — which program produced this file (2026-09-19)
Hook attempt: "Tells you which program made a file, from the bytes nobody looks at."
Descriptor: `{file bytes, structural fingerprinting, forensics, report}`.
Producer-specific quirks in ZIP-family containers (ordering, alignment, compression
settings, timestamps, extra fields) do identify the writing tool, and the systematic
cross-producer fingerprint table would be a real dataset. Fails Gate F as scoped: it is
drag a file, read a verdict — the banned shape with a nicer surface. What would make it
hyped: the fingerprints themselves rendered as a visible signature per producer, so the
differences can be seen rather than reported.

### interval algebra with uncertain endpoints (2026-09-19)
Hook attempt: "Reason about events when you do not know exactly when they happened."
Descriptor: `{timestamps, algebra, formal groundwork, library}`.
If it works: log correlation, historical timelines, and sensor fusion could all state
what is *provable* from imprecise times rather than pretending to precision. A legitimate
primitive under the upstream rule, and formal groundwork is explicitly allowed. Fails
Gate F on demo: nothing to look at in ten seconds. Held here until someone can picture
the picture.

### program sonification (2026-09-19)
Hook attempt: "Listen to your program run." Flat, and the field has decades of research
behind it. Recorded to stop it being regenerated as though it were fresh.

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

## 5. Under consideration — carried to the next run

Live candidates that survived this run's gates but have **not** been selected. The
sleep-on-it rule means the shortlist must be re-read at the start of the next run before
anything is built, so this section is where a run in progress leaves its state.

**Honest status as of 2026-09-19: none of these yet clears the bar.** The standard is a
candidate I would be genuinely disappointed to see someone else ship first, and the
strongest one here fails its own red team. Recorded so the next run starts from the
finding rather than the feeling.

### Scores (1-5: hook, reach, demo-ability, originality, difficulty-worth-it, monetizability)

| Candidate | Hook | Reach | Demo | Orig. | Diff. | Money | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Any-fragment image format | 5 | 3 | 5 | 3 | 4 | 2 | 22 |
| Pop-up compiler from a 3D model | 4 | 3 | 5 | 2 | 4 | 3 | 21 |
| Shape-aware line breaking | 2 | 4 | 3 | 3 | 3 | 2 | 17 |
| PDF revision time machine | 4 | 2 | 4 | 2 | 2 | 2 | 16 |

**Pairwise — which would I be more upset to see someone else ship first?**
Any-fragment vs pop-up: any-fragment. Any-fragment vs shape-aware line breaking:
any-fragment. So the leader is the any-fragment format — and then it loses to its own
red team, below.

### F1. Any-fragment image format — leader, and failing its red team
Hook attempt: "Throw away any 40% of the file, at random, and the picture still appears —
just softer."
Descriptor: `{file bytes, rateless coding, image/codec, format + viewer}`.
If it works: archival media that degrades like paper instead of failing like a checksum;
partial-transfer previews; print/scan storage that tolerates damage.
Searched: fountain/LT/Raptor codes, unequal loss protection, progressive rateless codes,
FLIF and JPEG XL progressive decoding. Found: no shipped image *format* recovers
proportionally from an **arbitrary** subset of bytes — FLIF and JPEG XL degrade on a
truncated *prefix*, and fountain codes recover all-or-nothing at a threshold rather than
proportionally.
**Red team (written before any build, per the rules):**
*Closest existing thing* — unequal loss protection (Mohr et al., 2000) and progressive
rateless codes ([arXiv:1204.3391](https://arxiv.org/pdf/1204.3391)) already combine a
multi-resolution image with stronger protection on the important layers, which is exactly
the mechanism that would make this work. PAR2 parity archives already give arbitrary-block
recovery for damaged files.
*Why a stranger shrugs* — "that is unequal loss protection, published twenty-six years
ago, plus a file extension."
*The part only interesting to its author* — the elegance of the container.
*Answer attempted* — the honest answer is that the contribution would be packaging and a
demo, not a mechanism. That is not enough for Gate E, and the hook is doing work the
originality cannot support. **Not selected.** It stays here rather than moving to section
2 only because one question is genuinely open: whether any shipped artifact actually
delivers smooth proportional degradation under arbitrary loss, or whether that remains
purely a literature result. Settle that first; if it has shipped, move this to section 2.

### F2. Pop-up compiler — a printable sheet that folds into a 3D shape
Hook attempt: "Feed it a 3D model, print one sheet, and fold it into the thing."
Descriptor: `{3D mesh, geometric decomposition, paper/fabrication, printable artifact}`.
If it works: a geometry primitive for self-erecting paper structures — pop-up books,
packaging, deployable structures, kirigami toys — with the card as one demo of it.
Searched: "computational kirigami pop-up design open source", "pop-up card generator from
3D model", "Popup Li et al implementation github". Found: Mitani & Suzuki's voxel-based
90-degree origamic architecture work, shipped free as
[Pop Up Block Card](https://mitani.cs.tsukuba.ac.jp/ja/software/popup_card/) and
commercialised as Tama Software's Pop-Up Card Designer;
[Li et al., *Popup: Automatic Paper Architectures from 3D Models*](https://www.cse.wustl.edu/~taoju/research/popup_final.pdf)
(SIGGRAPH 2010) and the 2011 v-style extension — **no public implementation found**;
[Abel, Demaine et al., *Algorithms for Designing Pop-Up Cards*](https://erikdemaine.org/papers/Popups_STACS2013/paper.pdf)
(STACS 2013, theory); Okamura & Igarashi's interactive design assistant (2009).
**Open question for the next run:** a faithful reimplementation of a 2010 paper is the
missing reference implementation — which `AGENT_RULES.md` explicitly counts as a
contribution — but Gate E asks for something materially new about the *idea*, not just
the execution. So the question to settle is what the authors did not build and whether
that extension is the actual project. Do not start this until that answer is written down.

### F3. Shape-aware line breaking as a primitive — unsearched
Hook attempt: "Text that flows around any shape as well as a typesetter would set it."
Descriptor: `{text + shape, optimal line breaking, typography, library}`.
If it works: magazine-quality layout becomes available to anything that can draw a
boundary. Knuth-Plass optimises line breaks against a rectangle; extending the badness
model to arbitrary boundaries is a real generalisation. **Not searched at all** — CSS
Shapes, existing Knuth-Plass ports and commercial layout engines must be checked before
this is taken seriously. Weak hook as written.

### F4. PDF revision time machine — unsearched
Hook attempt: "Shows you the earlier drafts still sitting inside a PDF someone sent you."
Descriptor: `{file bytes, incremental-update recovery, document forensics, visual}`.
PDFs keep prior revisions in the file when saved incrementally, so earlier states —
including content later covered over — can be rendered rather than merely reported.
**Not searched**: PDF forensics is an established area (pdf-parser and similar), and the
mechanism is standard, so this likely fails Gate E even though the hook is strong. The
differentiator would be experience only, which the rules say is not enough on its own.

### Carried over from section 1
The three-way **merge** for binary formats (writing a valid file back out, not just
diffing) is noted in section 1 as the live remnant of this run's rejected first idea. It
was deliberately not searched. It is a harder and more primitive-shaped problem than the
diff, and a future run may take it up on those terms.
