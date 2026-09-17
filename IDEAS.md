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

### Pebble Evolve — considered 2026-09-17, passed over for this cycle
Owner: here is the reasoning you asked for, in short. Two of its three parts cannot be
built honestly today. The taste signal needs a corpus of your own delight ratings and
none exists, so it would have to be faked or silently dropped. The remaining claim —
evolution over *whole projects* rather than single functions — is exactly the claim
that needs a full prior-art search against AlphaEvolve, OpenEvolve and ShinkaEvolve,
and that search is a run's work on its own rather than something to wave through.

What did happen instead: the generation mechanics it motivated are now in force, and
this run is the first to use them. It produced **28 candidates** against the three or
four that earlier runs managed, sampled deliberately from the tails, tagged with
behaviour descriptors, scored, compared pairwise and red-teamed. That was the part of
the proposal with immediate value, and it has been taken.

If you would rather see it built as a project than absorbed into the rules, add a line
here and it goes to the top of the next run's list, prior-art search and all.

### (add yours below)

---

## 1. Rejected — failed the rules

Ideas that failed a gate for reasons other than prior art: not feasible here, no
definition of done, no first step, no real problem, inside the shape ban, or
memorable but useless.

Format: **name** — date. Hook attempt. Which gate failed and exactly why.

### Run of 2026-09-17 — the five mode candidates, rejected on sight
The rules require the first idea to be rejected as a final answer and recorded. These
five arrived first, in order, and every one of them is what any agent would produce
given this repository. Recorded so no future run mistakes them for inspiration.

* **C1 retry-fanout animation** (p≈0.45) — "watch one click become thirty requests."
  A visual front end for `projects/backfire/`. Rejected: it is a re-render of work
  already here, not a project. Descriptor `{batch, own repo, animation, dev tooling}`.
* **C2 an explorable explanation of an algorithm** (p≈0.40) — rejected: names a shelf,
  not a thing. Gate F, category label. Which algorithm, and why, was never answered.
* **C3 a live dashboard of some public data feed** (p≈0.35) — rejected: Gate A. No
  concrete capability, and the hook is "look, numbers move."
* **C4 regex visualiser** (p≈0.50) — see section 2, settled on prior art.
* **C5 commit-history visualiser** (p≈0.40) — see section 2, settled on prior art.

### C6 decay — a file format that loses fidelity every time it is copied
2026-09-17. Hook attempt: "every copy of this file is slightly worse than the last,
like a photocopy of a photocopy." Descriptor `{batch, any file, file format, art}`.
Rejected on **Gate A**: generation loss as a medium is an art piece, not a capability.
Memorable and useless still fails. Kept because the inverse — deliberate, controlled
degradation with a guarantee about what survives — is the useful half, and it survives
as C24 below.

### C7 link-only multiplayer — a game whose entire state is the URL you send
2026-09-17. Hook attempt: "no server, no account, no save file — the game is the link."
Descriptor `{turn-based, none, browser, games}`. Rejected on **Gate A and E**: URL-state
games exist (play-by-email and fragment-encoded puzzles), and the interesting part is a
constraint, not a capability. Worth revisiting only attached to a game worth playing.

### C8 matte — a CPU-only video keyer with a new non-learned mechanism
2026-09-17. Hook attempt: "pulls a clean key off a badly lit green screen without a
model or a GPU." Descriptor `{batch, video, visual, VFX}`. This was the deliberately
over-ambitious candidate the protocol requires. Rejected on **Gate B**, with the
reasoning recorded so the next run does not redo it: video decode is reachable here
(`pip install` works, `imageio-ffmpeg`/`PyAV` bundle their own binaries; there is no
system `ffmpeg`), but there is no GPU and no model weights, and the honest bar for a
keyer is the learned matting work it would be compared against. A slower, worse keyer
is not a result worth months. **What would have to be true**: a genuinely new mechanism
that does not need learned priors — a temporal or geometric one — identified *before*
starting, not discovered at milestone four. The owner's `REFERENCES.md` entry on
Corridor's keying work means this direction has real taste behind it; it deserves a
proper attempt when there is a mechanism to attempt, not an attempt in search of one.

### C9 open-problem-arcade — a browser game whose levels are open problems
2026-09-17. Hook attempt: "every level is a problem nobody has solved, and beating one
sets a record." Descriptor `{playable, open problems, browser, games/math}`. Scored as
a finalist (see 3.5) and then rejected on **Gate A**: the value is realised only if
strangers play it, and this repository cannot supply players. A citizen-science game
with no citizens is a husk, however good the verifier is. **What would make it live**:
a problem class where a single strong solution is itself the result, so that one player
— me — beating the record is already the deliverable. That version is worth generating
properly next time the pool is refilled.

### C10 map-elites-for-ideas — a visual archive of this repository's own idea space
2026-09-17. Hook attempt: "a grid of everything this repository could have built, with
the built ones lit up." Descriptor `{interactive, own repo, visual, meta}`. Bounded
slice of the owner's Pebble Evolve. Rejected on **Gate A** for strangers: it is
infrastructure for one repository's decision-making. Its useful core — behaviour
descriptors making repeated cells visible — is already in `AGENT_RULES.md` and used
above, which is the right place for it.

### C11 cutline-engine — re-ship the minimal-cut solver as a standalone primitive
2026-09-17. Hook attempt: "proves your plan is impossible, then names the cheapest
thing to drop." Descriptor `{batch, plans, text report, planning}`. `PROGRESS.md`
flags this as a strong starting point and it is a real, verified engine. Rejected for
**this** cycle on the shape ban: extracted as-is it is still "run a command, read a
report", and re-scoping it is re-publishing work already here rather than going
somewhere new. It stays a legitimate future project, and the right version of it is
visual — a certificate you can *see* being violated — not a library with a nicer API.

### C12 units-live — orbiter's unit inference propagating as you type
2026-09-17. Hook attempt: "watch milliseconds turn into seconds as you type the
division." Descriptor `{live editor, source, visual, dev tooling}`. Suggested by
section 3 of this file. Rejected on **Gate E** for now: the inference engine is
`projects/orbiter/`, and a new interaction on top of an existing project here is a
re-skin of this repository's own work. Genuinely better than orbiter's CLI, and a good
candidate the moment the repository wants a second pass at an old project rather than a
new one.

### C13 stitch — optimal line breaking transplanted from typesetting to subtitles
2026-09-17. Hook attempt: "breaks subtitles where a reader would breathe." Descriptor
`{batch, subtitle files, text, media}`. A clean cross-domain transplant (Knuth–Plass
into subtitle segmentation) and probably a real improvement. Rejected on **Gate F**:
the hook needs a paragraph about why greedy breaking is bad before it becomes
interesting, and nothing about it is visible in ten seconds.

### C14 repo-lod — a codebase you can zoom out of, semantically
2026-09-17. Hook attempt: "zoom out of a repository and watch the code turn into its
own summary." Descriptor `{interactive, source, visual, dev tooling}`. Held, not
rejected: it is the same primitive as C24 pointed at source instead of prose, and prior
art is heavier here (semantic zoom for source code is patented — US8561015 — and Code
Bubbles and Software Cartography cover the interaction). It belongs as a *demo* of the
primitive if C24 proceeds, never as the project.

### C15 svg-by-hand — a better representation for hand-authored vector graphics
2026-09-17. Hook attempt: "draw by writing, and edit by dragging, without the two
fighting." Descriptor `{editor, drawings, visual, design}`. Real demand: the top answer
in the Hacker News "what do you still do manually" thread (item 48045237, read this
run) is drawing vector graphics, described as sitting at the worst of both worlds
between generation and code. Not rejected on the problem — rejected because every
version I could write down is a DSL that compiles to SVG, and Penrose, TikZ and Vega
already occupy that ground. **What would have to be true**: an idea about the
round-trip (drag the picture, the source edits itself, legibly) rather than another
source language. Worth returning to with that constraint imposed.

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

### C4 regex visualiser — rejected (2026-09-17)
Hook attempt: "shows you what your regex actually matches." Prior art:
[regex101](https://regex101.com), [Regexper](https://regexper.com) and Debuggex —
same problem, same user, same workflow, all mature. Also a category label, so it fails
Gate F independently. Prior-art names recalled, not re-verified this run; the rejection
does not depend on the detail, only on the field being crowded and well known.

### C5 commit-history visualiser — rejected (2026-09-17)
Hook attempt: "watch your repository grow." Prior art: Gource and git-of-theseus.
Materially equivalent, and the result is decorative rather than a capability. Prior-art
names recalled, not re-verified this run.

### C16 pdf-rewind — earlier drafts recovered from a PDF's own incremental saves
2026-09-17. Hook attempt: "shows you what the document said before it was edited."
Descriptor `{batch, PDF bytes, visual/text, forensics}`. Genuinely surprising mechanism
— PDFs keep their previous revisions inside the file — but materially equivalent work
exists and is packaged everywhere: **pdfresurrect**
([source](https://github.com/enferex/pdfresurrect),
[man page](https://manpages.ubuntu.com/manpages/bionic/man1/pdfresurrect.1.html),
in Fedora, MacPorts and FreeBSD ports) extracts all previous versions and summarises
the changes between them. PyMuPDF has the same capability
([discussion](https://github.com/pymupdf/PyMuPDF/discussions/3096)). Verified this run.
Settled. Note also that the natural demo — revealing what a redaction covered — is a
disclosure tool pointed at other people's documents, which is a reason to leave it
alone beyond the prior art.

### C17 glyph-space — a shape space learned from thousands of open fonts
2026-09-17. Hook attempt: "morph any letter into any other letter, in any font."
Descriptor `{interactive, font corpus, visual, typography}`. Rejected: Campbell and
Kautz, **"Learning a Manifold of Fonts"**, SIGGRAPH 2014
([SIGGRAPH history](https://history.siggraph.org/learning/learning-a-manifold-of-fonts-by-campbell-and-kautz/),
[project page](http://vecg.cs.ucl.ac.uk/Projects/projects_fonts/projects_fonts.html))
is the same capability — a generative manifold where every point is a novel typeface —
and the field has moved on since ([Learning Perceptual Manifold of Fonts,
arXiv:2106.09198](https://arxiv.org/pdf/2106.09198); [Attribute2Font,
arXiv:2005.07865](https://arxiv.org/pdf/2005.07865)). Variable fonts ship the
interpolation idea to every browser. Verified this run. Settled.

### C18 hint-machine — a step debugger for TrueType hinting bytecode
2026-09-17. Hook attempt: "watch a letter argue with the pixel grid, one instruction at
a time." Descriptor `{interactive, font binaries, visual, typography}`. A good
reverse-engineering target — the bytecode is real, lawfully inspectable, and poorly
documented outside the specification. Rejected on Gate E: **Microsoft Visual TrueType**
is exactly this tool, graphical and professional, and is still maintained
([Microsoft Learn](https://learn.microsoft.com/en-us/typography/tools/vtt/),
[source](https://github.com/microsoft/VisualTrueType),
[hinting variable fonts guide](https://googlefonts.github.io/how-to-hint-variable-fonts/)).
FontForge ships a hinting debugger too. Verified this run. Settled.

### C19 merge-by-intent — a merge that understands structure rather than lines
2026-09-17. Hook attempt: "merges the change, not the lines." Prior art: **Mergiraf**
([mergiraf.org](https://mergiraf.org/), syntax-aware Git merge driver over tree-sitter)
and **difftastic** ([difftastic.wilfred.me.uk](https://difftastic.wilfred.me.uk/)),
plus a decade of semantic-merge products before them. Mergiraf even publishes a
[related-work page](https://mergiraf.org/related-work.html) covering the rest of the
field. Verified this run. Materially equivalent. Settled.

### C20 fountain-archive — an archive where any sufficient fraction of bytes restores it
2026-09-17. Hook attempt: "lose a third of the file and it still opens." Descriptor
`{batch, any file, file format, storage}`. Rejected: this is Parchive/PAR2 and the
erasure-coding family ([par2cmdline](https://github.com/parchive/par2cmdline),
[Parchive on Wikipedia](https://en.wikipedia.org/wiki/Parchive)), Reed–Solomon
recovery blocks over arbitrary files, used at scale for decades. Verified this run.
Note the distinction from C24, which is not about recovering the whole file from part
of it but about a prefix being a *deliberately shorter* file — different guarantee,
different mechanism.

### C21 paper-sound — print a sound as an image and play it back from the paper
2026-09-17. Hook attempt: "photograph this square of noise and hear what it says."
Descriptor `{live, audio, printed image, music}`. Rejected: **PhonoPaper**
([warmplace.ru](https://www.warmplace.ru/soft/phonopaper/),
[App Store](https://apps.apple.com/us/app/phonopaper/id865947553),
[coverage from 2014](https://www.synthtopia.com/content/2014/04/28/phonopaper-for-ios-lets-you-print-audio-play-it-back-from-paper/))
does exactly this, generator and real-time camera reader, and optical sound on film
([VisualAudio](https://en.wikipedia.org/wiki/VisualAudio)) is a century of prior art
underneath it. Verified this run. Settled.

### C22 hexplore — a hex editor you can search structurally
2026-09-17. Hook attempt: "find me the header where the third field is bigger than the
fourth." Descriptor `{interactive, binaries, visual, reverse engineering}`. Real
demand — asked for directly in the Hacker News "what developer tool do you wish
existed" thread (item 46345827, read this run). Rejected on prior art: **Kaitai
Struct** ([kaitai.io](https://kaitai.io/), a declarative binary format language with a
[format gallery](https://formats.kaitai.io/)) and **ImHex**
([imhex.werwolv.net](https://imhex.werwolv.net/), whose
[Pattern Language](https://github.com/WerWolv/PatternLanguage) does exactly the
structural description asked for), plus 010 Editor's binary templates. Verified this
run. The unclaimed sliver is the *fuzzy* search over an unknown format rather than
parsing a known one, which is a real gap but a thin one.

### C23 cache-thrash — see your loop miss the cache
2026-09-17. Hook attempt: "watch your array traversal fall off a cliff." Prior art:
cachegrind and kcachegrind, perf, and a large body of teaching animations. Materially
equivalent as an idea and better served by existing profilers. Prior-art names
recalled, not re-verified this run.

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

### C26 slider-bug — delta debugging you drive with your hand (2026-09-17)
Hook attempts: "drag a slider and watch your bug disappear"; "shrink the input until
only the broken part is left." Descriptor `{interactive, failing inputs, visual, dev
tooling}`. Passes Gate A (minimising a failing input is real, constant work) and Gate B
easily. Fails Gate F on **originality of mechanism**: the mechanism is ddmin and
C-Reduce, and the contribution would be the slider. That is a legitimate contribution
in the Bret Victor sense, which is why it is here rather than in section 2. **What
would make it hyped**: an interaction that shows the *search* rather than the result —
the space of reduced inputs as a landscape you move through, where you can see which
parts of your input are load-bearing and which are decoration. That is a different and
better idea than a slider over ddmin's output, and it is worth generating properly.

### C27 why-this-number — every number in a report carries its own derivation
2026-09-17. Hook attempts: "hover any number in the report and watch the arithmetic that
produced it unfold"; "a number that remembers where it came from." Descriptor
`{interactive, computations, visual, data}`. Real problem: nobody can audit a figure in
a report without rebuilding the pipeline. Fails Gate F for now because the hook needs
a setup sentence before it lands, and because the honest version is a provenance
library plus a viewer, which is two projects. Prior art to search properly if revived:
spreadsheet trace-precedents, and the data-provenance literature (provenance semirings
and the `uncertainties` package are the two to start from; both recalled, unverified).
**What would make it hyped**: making the provenance *the document* rather than an
annotation on it — a report whose every figure can be expanded in place until you reach
raw data, with no separate tool.

### C28 clipped — make a truncated email end coherently
2026-09-17. Hook attempt: "your newsletter gets cut off at 102KB; this makes the cut
land somewhere sensible." Descriptor `{batch, HTML email, rendered page, publishing}`.
Not rejected — **absorbed**. It is one concrete application of C24 in section 3.5, and
`AGENT_RULES.md` is explicit that when a general engine sits inside a specific
application, the engine is the project and the application is one demo of it. Recorded
separately so the demo is not forgotten, and so that if C24 fails, this smaller, real
pain is still on the list.

---

## 3.5 Shortlisted — passed the gates, awaiting the sleep-on-it re-read

Candidates that cleared Gate F and the other gates on the run that generated them, but
have **not** been selected, because `AGENT_RULES.md` requires a shortlist to survive
being re-read at the start of the following run before any implementation begins. An
entry here is a proposal, not a decision. It moves to section 4 only after that
re-read, and only after a full prior-art search to `NOVELTY_REPORT.md` standard.

### C24 taper — a file that is every length at once (leading candidate, 2026-09-17)

**Hook sentence (verbatim, to be tested again next run):**

> Cut this file off anywhere you like and it still opens — as a shorter version of the
> same document.

Descriptor `{batch tool producing a rendered artifact, any structured document,
file format + browser page, publishing/infrastructure}` — an empty cell for this
repository, whose three projects all sit in `{batch, source files, text, dev tooling}`.

**The mechanism**, stated plainly enough to be attacked:

1. A document is split into blocks that carry a **dependency partial order** — a
   paragraph needs its heading, a row needs its header, a sentence needs the sentence
   its pronoun points at.
2. An **importance order** is any linear extension of that partial order. Because it is
   a linear extension, every prefix of it is downward-closed: nothing appears without
   its prerequisites. That is the whole formal content, and it is what makes the
   shorter versions readable instead of merely shorter.
3. The blocks are written into one self-contained HTML file **in importance order**,
   each carrying its reading-order index in a CSS `order` property inside a flex
   column. The browser puts them back into reading order for display, so byte order
   and reading order are decoupled.
4. Truncating the file drops the least important tail. Browsers close dangling markup
   themselves, so the truncated file is still a page — and by (2) it is still a
   coherent document.

So `head -c 3000 doc.html` is a three-kilobyte document, `head -c 40000 doc.html` is a
forty-kilobyte document, and the untruncated file is the whole thing. One file, every
length, no decoder, no model, no server.

**If this works, what becomes buildable that wasn't:** previews with no preview
pipeline (the first N bytes *are* the preview); newsletters that survive Gmail's 102KB
clip with an ending instead of a severed sentence (C28); range requests that return a
summary rather than a fragment; logs and archives that degrade instead of corrupt;
documents trimmed to fit a model's context window without a summarisation pass. The
answer is a list rather than one use case, which is the signal `AGENT_RULES.md` asks
for.

**Scores** (hook / reach / demo-ability / originality / difficulty-worth-it /
monetizability): **5 / 5 / 5 / 4 / 4 / 3**. Originality is 4 not 5 because the idea is
a transplant — progressive JPEG and progressive meshes are the same move in other
media — and the transplant is the contribution rather than the mechanism.

**Demo, pictured before building** (the protocol requires being able to picture it):
three screenshots of *the same file* at 2KB, 20KB and 200KB, side by side, each a
well-formed document, with the `head -c` command printed above each one. Then a slider
that is doing nothing but moving a byte offset.

**Red team, written in bad faith as required:**

* *"It's a summariser with extra steps."* The closest honest answer: no. Nothing is
  recomputed at read time, there is no model at read time, and there is no viewer — the
  shortening is `head -c`, a byte-count truncation any tool on any machine can do. What
  it shares with summarisation is the ordering step, which happens once, at write time.
* *"Progressive JPEG already exists, and so do progressive meshes."* True, and they are
  the closest prior art, and they will be named at the top of the README. The claim is
  the transplant to documents plus the prefix-closure guarantee, not the invention of
  progressive encoding.
* *"Nobody truncates files."* The weakest objection: Gmail clips at 102KB, range
  requests return prefixes, log rotation cuts mid-line, and every model context window
  is a truncation. But this is the objection to keep testing, because if the answer is
  really "only in contrived cases" the project is a toy.
* *"The only interesting part is interesting to the author."* Partly fair. The
  linear-extension framing is the author's pleasure; the stranger's pleasure is the
  three screenshots. That is an argument for leading with the demo, which the rules
  require anyway.
* *"CSS `order` divorces visual order from DOM order, which is an accessibility
  failure."* **This objection is not yet answered, and it is the serious one.** Screen
  readers and tab order follow the DOM. A document whose DOM order is importance order
  is a document a screen-reader user hears in the wrong sequence. Possible answers to
  test: emit in waves so order diverges only between detail levels, ship a decoder mode
  that restores true order, or accept and document the trade-off loudly. It must be
  measured, not argued, before this is built — and if it cannot be answered, that is a
  real reason to drop the candidate or change its shape.

**What was searched this run** (not yet to `NOVELTY_REPORT.md` standard):
progressive/prefix-decodable document encodings; truncation-tolerant document formats;
semantic zoom; progressive summarisation; out-of-order HTML flushing. Found and to be
compared properly: progressive meshes and progressive JPEG (the same move in other
media); Facebook's **BigPipe** pagelet flushing
([engineering.fb.com](https://engineering.fb.com/2010/06/04/web/bigpipe-pipelining-web-pages-for-high-performance/),
which decouples byte order from display order for latency, reordering with JavaScript
placeholders, not for truncation); **semantic zoom** as a UI technique, including for
source code (patent [US8561015](https://patents.google.com/patent/US8561015)) and a
patent on documents carrying per-element detail levels
([US10713433](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10713433));
Tiago Forte's **progressive summarisation**
([Forte Labs](https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/),
a note-taking practice, not a format); truncated-JSON *repair* libraries such as
[truncate-json](https://github.com/ehmicky/truncate-json) and
[truncjson](https://pypi.org/project/truncjson/1.2.6) (repairing an accidental cut, the
opposite of designing for one). No materially equivalent artifact surfaced, but the
search is incomplete and the confidence stays unstated until it is done.

**Open questions that must be resolved before a line of code is written:**

1. The accessibility objection above.
2. Does a truncation landing *inside* a tag or attribute break the block it lands in,
   in real browsers? Needs an empirical answer in Chromium, not a guess. Mitigation if
   so: block-aligned padding or a sentinel.
3. Where the dependency order comes from. Start only where it is derivable rather than
   guessed — headings, lists, tables, reference structure — not from pronoun resolution
   in free prose, which needs a model and would make the guarantee a bluff.
4. Format-first (a container plus decoder, HTML as one target) or HTML-first (the trick
   above, no decoder at all)? The second is the better demo; the first is the better
   primitive. Milestone 1 should be the second, to find out fast whether it is real.
5. The full prior-art search, properly, across the ecosystems Section 6 lists.

**Control check planned** (so the property is demonstrated, not asserted): render the
same document under a *random* block order rather than a linear extension, and show
that truncation then produces orphaned content — establishing that the coherence comes
from the ordering and not from the browser's error tolerance.

Name is provisional. `taper` is short, lowercase, easy to say, and describes the thing.

### C25 decoder-drift — the same image, decoded five ways, is five pictures (runner-up)

2026-09-17. Hook attempt: "this one file is a different picture depending on who opens
it." Descriptor `{batch + visual, image bytes, rendered grid, security/testing}`.
Decoders disagree — on truncated chunks, exotic colour profiles, animation disposal,
undefined corners of the spec — and a corpus that *provokes* the disagreements, shown
as a grid of renderings, is both a striking artifact and a real differential-testing
asset. Scores **4 / 3 / 5 / 4 / 3 / 2**.

Held rather than selected for two reasons. First, taper beat it in the pairwise
comparison below. Second, and recorded so it is weighed honestly next time rather than
rediscovered: the natural output of this project is *a file that looks like one thing
to a moderation preview and another to a human*, which is a known attack pattern. There
is a defensible version — a fixed corpus, published as test material, framed for people
who maintain decoders — and an indefensible one, which is a generator aimed at
pipelines. If this is ever selected, that boundary is decided in writing before
implementation, not afterwards.

### Pairwise comparisons, 2026-09-17

The question, per `AGENT_RULES.md`: *which of these two would I be more upset to see
someone else ship first?*

| A | B | Winner | Why |
| --- | --- | --- | --- |
| C24 taper | C25 decoder-drift | **taper** | decoder-drift is a thing I would enjoy reading about once. taper changes what a file *is*, and I would be annoyed for a year. |
| C24 taper | C9 open-problem-arcade | **taper** | the arcade is the bigger swing, but its value needs players this repository cannot supply. taper's value does not depend on an audience arriving. |
| C25 decoder-drift | C9 open-problem-arcade | **arcade** | between two I am not building, the more ambitious one is the bigger loss. |
| C24 taper | C27 why-this-number | **taper** | provenance is the more useful capability and the less surprising one; it needs a paragraph before it lands. |

Winner: **C24 taper**, pending the sleep-on-it re-read.

**Calibration against `REFERENCES.md`** — *is this idea in that company?* Partly, and
the honest read is worth recording. It has the jq property (small, sharp, composable)
and the Mother-of-all-Demos property (the demo is the contribution). It does **not**
have the Corridor property: this is not a pain I feel daily, it is a mechanism I found
attractive, and that is the weakest thing about it. That weakness is the specific thing
the next run's re-read should push on.

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
