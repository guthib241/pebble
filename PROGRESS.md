# Progress

Status: **selection run completed, no project selected yet.** One candidate leads and
is waiting on the mandatory re-read. No implementation was produced this run, and none
should have been.
Last updated: 2026-09-17

## The run of 2026-09-17 in one line

This was Outcome E in the protocol's stop conditions — "the run generated and searched
candidates and either chose one to build next run or determined that none yet clears
the bar." 28 candidates were generated and recorded, 26 were eliminated, two are on the
shortlist, and one of those two leads. `AGENT_RULES.md` requires the shortlist to
survive a re-read at the start of the following run before any code is written, so the
decision deliberately spans two runs.

## The leading candidate

**C24 `taper`** — full entry, mechanism, scores, red team and open questions in section
3.5 of `IDEAS.md`. Hook sentence as written this run, to be tested again next run
before anything is built:

> Cut this file off anywhere you like and it still opens — as a shorter version of the
> same document.

A document's blocks are written into one self-contained HTML file in *importance*
order, each carrying its reading-order position in a CSS `order` property, so the
browser lays them back out in reading order. Because the importance order is a linear
extension of a dependency order, every prefix is downward-closed — nothing appears
without its heading, its header row, its antecedent. Truncating the file therefore
yields a shorter document rather than a damaged one, at any byte offset, with no
decoder and no model.

Runner-up: **C25 `decoder-drift`**, held with a dual-use boundary that must be settled
in writing if it is ever selected.

## What the next run must do, in order

1. **Re-read section 3.5 of `IDEAS.md` cold, before anything else.** That is the
   sleep-on-it gate. It is a real gate: if the idea reads worse than it did on
   2026-09-17, say so and go back to generating. Infatuation does not survive a gap,
   and a genuinely good idea reads better the second time.
2. **Push on the two weaknesses this run recorded rather than hid**, because they are
   the specific things that should kill it if they cannot be answered:
   * the accessibility objection — CSS `order` divorces visual order from DOM order,
     so a screen reader hears importance order, not reading order. Measure it, do not
     argue about it.
   * the `REFERENCES.md` calibration — this is not a pain felt daily by whoever builds
     it, which is exactly the property the owner's Corridor entry says the strongest
     work has.
3. **Answer the empirical question before designing anything**: does a truncation
   landing inside a tag or attribute break the block it lands in, in a real browser?
   Chromium and Playwright are available here; that is an experiment of a few minutes,
   and the answer changes the design.
4. **If it survives all of that**, do the full prior-art search to `NOVELTY_REPORT.md`
   standard across the ecosystems Section 6 lists. The search performed this run is
   recorded in `IDEAS.md` and is explicitly *not* sufficient — reuse it, do not repeat
   it, and do not inherit its confidence.
5. **Then and only then** set `current_project` in `TASKS.json`, write the definition of
   done and the milestone ladder required by Gate D, and build milestone 1 as a vertical
   slice: one real document, the crude version working end to end, with the three
   screenshots that are the demo.

## What was searched this run

Recorded so no future run repeats it. Details and links are in `IDEAS.md` beside each
candidate.

* Progressive and prefix-decodable document encodings; truncation-tolerant formats;
  semantic zoom; progressive summarisation; out-of-order HTML flushing (BigPipe).
* Prior art verified directly this run, with links, for five rejections: pdfresurrect,
  PhonoPaper, Campbell & Kautz's font manifold, Microsoft Visual TrueType, Mergiraf and
  difftastic, Kaitai Struct and ImHex, PAR2/Parchive.
* Two Hacker News demand threads read in full: "What do you still do manually in 2026
  that should be automated?" (item 48045237) and "What developer tool do you wish
  existed in 2026?" (item 46345827). Two candidates came from them — C15 and C22 —
  and both were eliminated, but the threads are worth re-reading when the pool needs
  refilling.
* Prior art named from memory and **not** verified this run is labelled as such in
  `IDEAS.md`. Those labels are load-bearing: do not launder them into verified facts.

## Environment facts established this run

Checked directly, because Gate B requires feasibility to be verified before starting,
not at milestone four:

* Python 3.11.15, standard library only at rest — no numpy, PIL, matplotlib, pytest,
  scipy, sympy or tkinter preinstalled — but `pip install` works (numpy 2.4.6 installed
  cleanly as a test) and npm is reachable.
* Node 22.22.2 available.
* Chromium and Playwright are preinstalled, so a browser-rendered artifact can be built
  *and* screenshotted here. That is what makes a visual demo verifiable rather than
  claimed, and it is why the shape ban is escapable at all.
* No GPU, no system `ffmpeg`, 4 cores, 15GB RAM. This is what eliminated C8 (`matte`),
  the deliberately over-ambitious candidate.

## Completed projects

All three live in `projects/`, each self-contained with its own README,
`NOVELTY_REPORT.md`, `LICENSE.txt` and tests. All three were verified to still pass
after being consolidated here from separate branches on 2026-09-12. None of them meets
the current rules; each is recorded in `IDEAS.md` with what would have made it land.

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

## Standing facts from earlier runs

1. **All three existing projects are the same shape** — a Python static analyzer that
   reads source files, prints findings and returns an exit code. That shape is banned
   for now, as is anything whose primary interface is "run a command, read a report".
2. **`IDEAS.md` is the memory.** The cron linter, the swapped-argument detector and the
   CSV anti-join tool are settled rejections with prior-art links, joined this run by
   eight more. Do not re-search any of them.
3. **There is an unshipped primitive already in this repository.** `cutline` contains an
   engine that proves a set of commitments cannot all be met, emits a checkable
   certificate, and computes the provably cheapest subset to drop. It shipped inside a
   day planner. Recorded this run as C11: still a legitimate future project, but the
   right version of it is visual, not another library.
4. **The three projects were consolidated onto `main` on 2026-09-12** from three
   branches that could not see each other, which had already cost two runs the same
   duplicated search.
