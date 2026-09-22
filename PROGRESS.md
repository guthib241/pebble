# Progress

Status: **selection run.** No project is in progress and none was started, which is
the intended outcome of this run, not a shortfall: selection is not time-boxed and
the sleep-on-it rule requires a shortlist to survive a gap before anything is built.
Outcome E under Section 29.
Last updated: 2026-09-22

## Run 2026-09-22 — what happened

Intake, then Section 4 selection from a pool of 24 candidates. Five were searched:
three were rejected on prior art with links, one was filed as not hyped, and one was
provisionally selected, red-teamed, and then corrected after its closest prior art was
read in full. Everything is recorded in `IDEAS.md`: the
full pool with probabilities and behaviour descriptors is section 5, and every
candidate with a settled outcome also has a full entry in sections 1 to 4.

**Provisional hook sentence for the selected candidate:**

> *"Lays out a book so no figure drifts away from the sentence that mentions it, and
> proves no other arrangement scores better under the rules you set."*

**The candidate:** a standalone engine that decides every page break and float
placement in a document globally — minimising figure-to-mention distance, widows,
orphans, page fill and spread balance under a stated, editable cost model — where
every shipping system does it greedily, page by page. The engine is the project; a
book renderer and an interactive page grid you can drag and pin figures in are its
demos. Full entry, scores, pairwise result and red team: `IDEAS.md` section 4.

Why it survived: the method is published (Mittelbach's globally optimised pagination,
DocEng 2016 best paper, extended 2019) and, by the author's own statement, has never
left prototype stage — a published method with no public implementation, which
`AGENT_RULES.md` names as legitimate and valuable work. The demand is public and
unmet (Typst issues #5558, #3967, #6392; Quarto discussion #8801: "figures get pushed
quite far from where they are first mentioned"). It is outside the shape ban, it has
a ten-second visual demo, and it is an upstream primitive rather than an application.

**It is provisional on purpose.** Nothing was implemented and nothing should have
been.

## What the next run must do, in this order

1. **Re-read `IDEAS.md` section 4 first, before anything else.** That is the
   sleep-on-it gate. If the idea reads flat after the gap, return it to the pool and
   keep searching — that is a correct outcome, not a wasted run.
2. **Close the open searches** listed at the bottom of that entry: PyPI, npm,
   crates.io, CTAN and GitHub code search; direct inspection of the Mittelbach 2019
   and Brüggemann-Klein papers; whether Mittelbach's prototype has been released since;
   and what Patoline, SILE, Typst and Vivliostyle actually do at page-break time, read
   from source or docs rather than assumed.
3. **Write `NOVELTY_REPORT.md`** with the full Section 12 contents. Confidence is
   capped at Medium: the optimisation method is published and credited.
4. **Fix the name** (`quire`, `galley`, `forme`, `signature` are the shortlist) and
   write the definition of done plus the milestone ladder into `TASKS.json` — Gate D
   requires both before any code.
5. **Then build milestone 1 as a vertical slice**: one real document, crude but end to
   end, global page breaking with float placement, rendered to a page-thumbnail grid,
   with the greedy baseline rendered beside it and exactness checked against exhaustive
   enumeration on small instances. Not a parser, not a config system.

## Searches performed 2026-09-22 — do not repeat these

* retroactive data structures, implementations and libraries → several public
  implementations exist (csvoss, 6851-2021 x2, chshersh, panwaria) → rejected.
* linkage path synthesis from a drawn curve → MotionGen, SALAR, Kempe literature →
  rejected.
* reverse / reversible sound change appliers → rsca does exactly this; Lexurgy covers
  forward application → rejected.
* dynamic graph layout stability and mental-map preservation → large literature,
  incremental modes already in webcola/ELK → hook too weak, filed under not hyped.
* optimal pagination, float placement, NP-hardness, and whether an implementation
  exists → Mittelbach 2019, Brüggemann-Klein et al., Plass 1981; no standalone
  open-source global pagination engine surfaced.
* Typst and Quarto issue trackers for figure-placement demand → four open threads.
* registries: npm (found `paged-with-floats`, a CSS Page Floats polyfill that places a
  float on its anchor's page and defers to the next when it does not fit — greedy, and
  a good comparison target), crates.io (`rustyfi-*`, a Rust port of SATySFi), CTAN
  (local float helpers only). PyPI was only name-probed, so it stays open.
* whether Mittelbach's prototype was ever released → no evidence of a release; the
  LaTeX project's published output since 2020 is tagged PDF and accessibility work.

## Primary sources read directly this run

Both are open copies on the author's own site, and reading them changed the entry:

* `latex-project.org/publications/2019-FMi-coin12165-final.pdf` (43 pages) — the
  globally optimised pagination framework. **Its base algorithm does not handle
  floats**, which a search summary had wrongly suggested it did; the entry in `IDEAS.md`
  is corrected. Its abstract states the gap plainly: all systems to date use greedy
  pagination, and no prototype "ever made it into a generally usable and publicly
  available system."
* `latex-project.org/publications/2017-09-FMi-doceng2017-effective-floating-strategies-slides.pdf`
  — DocEng 2017, the float half, and the closer prior art of the two. It already models
  call-out/float constraints (a float must follow its call-out; same column, page or
  spread or later; confined to a subsection; visible from the call-out), absolute versus
  preference rules, and the O(n^c) candidate-placement blow-up.

Consequence: tying a figure to its mention is **not** a new idea and must never be
claimed as one. Originality for the candidate was lowered from 4 to 3 the same day, and
the open question for the next run is written at the end of the `IDEAS.md` entry: whether
the first public implementation, plus an exactness check and an interactive explainer, is
enough for Gate E. If the answer is no, the candidate returns to the pool.

## Environment facts verified this run (Gate B)

Python 3.11.15, Node 22, gcc/g++, cargo, go. `pip install` works (numpy, fontTools
4.65.0, pyphen all installed cleanly). Real font files present under
`/usr/share/fonts` (DejaVu, Liberation, Noto). Pyphen hyphenates with real
dictionaries. Chromium and ffmpeg are present under `/opt/pw-browsers`, so rendering
pages and recording animations is possible. **No TeX distribution is installed**, so
a LaTeX comparison is not available — which is the better outcome anyway: the honest
control is a greedy page breaker implemented inside the same engine, holding fonts,
line breaking and content fixed and varying only the page-break strategy.

## Completed projects

All three live in `projects/`, each self-contained with its own README,
`NOVELTY_REPORT.md`, `LICENSE.txt` and tests. All three were verified to still pass
after being consolidated here from separate branches on 2026-09-12.

### backfire — `projects/backfire/`
Finds retry amplification and timeout blowups in Python codebases. Resolves the
call graph and multiplies retry policies along each path, so three stacked layers
of reasonable-looking retries are reported as the 30 requests they actually
produce, with each contributing site named.
- 85 tests pass (`python3 -m pytest`, from `projects/backfire/`; needs pytest)
- Run against psf/requests (dae7ef6), openai/openai-python (d7c41ef),
  PrefectHQ/prefect (d82220b)
- Controls: two single-layer codebases report no amplification; repeat runs
  byte-identical
- Novelty confidence: Medium
- Built 2026-09-11 on `claude/eloquent-newton-p3qht6`

### orbiter — `projects/orbiter/`
Flags Python code that mixes units, like milliseconds passed as seconds. Infers a
unit and scale from identifier names, `typing.Annotated` metadata and standard
library conventions, and reads explicit conversions, so `time.sleep(timeout_ms /
1000)` is accepted where `time.sleep(timeout_ms)` is reported.
- 151 tests pass (`python3 -m unittest discover -s tests -t .`, from
  `projects/orbiter/`)
- Benchmark: 19 of 19 seeded mistakes detected, 0 findings on unmarked lines,
  2 documented known misses
- Controls: null control (unit tokens stripped from identifiers) gives 0 findings;
  determinism control identical across runs; paired correct/incorrect twins
- Clean on 1,748 real files (`/usr/lib/python3.11`, `/usr/lib/python3/dist-packages`)
- Reproduce evidence: `python3 evidence/run_evidence.py > evidence/results.md`
- Novelty confidence: Medium
- Built 2026-09-12 on `claude/optimistic-pasteur-metblz`

### cutline — `projects/cutline/`
Reads one plain-text plan and decides whether everything fits. When it does not, it
prints the over-subscribed window as a certificate that can be checked by hand, the
cheapest set of tasks to cut, and the earliest deadline that would let each cut task
stay.
- 120 tests pass (`python3 -m unittest discover -s tests -t .`, from
  `projects/cutline/`), including a fresh-virtualenv install check
- Controls: both feasibility methods agreed on 500 of 500 random plans; cut matched
  exhaustive enumeration 200 of 200; verdict survived task reordering and a one-week
  shift 200 of 200 each; 10 of 10 scenarios byte-identical on re-run
- Known limitation, recorded rather than hidden: the worst-case row of the timing
  table reports "not proven minimal" because it exhausts the node budget
- Novelty confidence: Medium
- Built 2026-09-12 on `claude/optimistic-pasteur-metblz`

## Consolidation, 2026-09-12

These three projects were built on three separate branches, none of which could see
the others. That directly cost usage: two runs independently generated, searched and
rejected the same cron-linter candidate, because neither knew the other had done it.
All three folders are now on `main` under `projects/`, so every future run starts
with the full back catalogue visible. The original branches are untouched and retain
the detailed per-run history, including each project's own novelty search narrative.

