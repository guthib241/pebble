# Progress

**Hook sentence for the project selected this run (Gate F, recorded before any
implementation):**

> Two people edited the same song. This works out what each of them changed, combines both,
> and plays you the one bar where they actually disagree.

Status: **selection run complete, no implementation — and that is the intended outcome**
(Outcome E in Section 29). A project has been chosen and must survive a cold re-read at the
start of the next run before a line of code is written. `current_project` is still null on
purpose.
Last updated: 2026-09-21

## Run of 2026-09-21 — what happened

Phase 1 intake was completed in full: `AGENT_RULES.md`, the execution protocol, `PROGRESS.md`,
`TASKS.json` (parsed, valid JSON) and `IDEAS.md`, plus `REFERENCES.md` for calibration.
Phase 1.5: `current_project` was null and no checklist was outstanding, so Section 4
selection was the run's job.

**32 candidates were generated and every one is recorded in `IDEAS.md`** under the heading
matching its outcome, with descriptors, hook attempts and reasons. The quota is 20. The first
idea — extracting `cutline`'s certificate engine as its own project, which the previous
`PROGRESS.md` itself recommended — was rejected as a final answer before any gate ran,
because it is the mode and because Gate E treats a near-duplicate of an existing project
folder as prior art. Finalists were scored, compared pairwise on "which would I be more upset
to see someone else ship first", and the winner was red-teamed in writing. All of that is in
`IDEAS.md` section 5.

The owner's idea in section 0 (Pebble Evolve) was read first and evaluated. It was passed
over this run, not rejected; the reasons are recorded under its own entry so the owner can
push back. The short version: its distinguishing component needs a body of the owner's own
ratings that does not exist, and the buildable remainder is a second machine for choosing
projects at a point when the object-level catalogue is three items long.

## The selection

**Proposed name: `comping`** (the studio term for assembling one good take out of several).
Name still to be confirmed next run.

A three-way merge for music, and underneath it a merge algebra for timelines. Given a common
ancestor and two edited versions, it works out each side's edits in musical terms, produces a
merged result, and flags only genuine collisions. The interesting difficulty is that edits
interact in time: inserting two bars on one side has to move the other side's later edit, and
a text or XML merge cannot know that, because it reconciles tags rather than time.

The primitive is the project; symbolic music is the first binding; the visible, audible
artifact is the deliverable. Full entry, with prior art, demand evidence and the red team, is
in `IDEAS.md` section 4.

## What was searched, so the next run does not repeat it

Sources: web search across forums and aggregators, GitHub, PyPI and npm, and academic
indexes (ACM DL, Springer, ResearchGate listings). Query formulations covered the problem
statement, the user action, the mechanism, the distinctive terminology and the synonyms:
music version control and merge, MIDI diff/merge and git merge drivers, MusicXML and MEI
diff and merge, structural and AST merge carried over to time-based media, symbolic music
alignment and edit distance (Mongeau-Sankoff, polyphonic alignment), collaborative score
editing with CRDTs, notation-software compare features, and structured merge for edit
decision lists and animation curves.

Closest prior art, inspected directly:

* **musicdiff** (github.com/gregchapman-dev/musicdiff, on PyPI) — diffs and visualises two
  scores, aimed at evaluating optical music recognition. **No merge, by design.** Closest
  match; it gets credited at the top of the README.
* **"A diff procedure for music score files"**, DLfM 2019 — the research diff.
* **Mongeau-Sankoff** melodic edit distance and later polyphonic alignment work — a
  similarity measure, not an edit script and not a merge.
* **GitDaw** — converts Ableton `.als` to JSON so git can text-merge it; no model of time.
* **CRDT collaborative score editors** — the real-time problem, a different capability from
  an ancestor-based asynchronous merge.

No materially equivalent three-way merge was found for symbolic music, and none for the
general timeline case either. That is a search-scoped finding, not a claim of universal
novelty, and it will be written up properly with confidence rating in `NOVELTY_REPORT.md`
before implementation begins.

## Next run — do these in order

1. **Re-read `IDEAS.md` section 4 cold, before anything else.** This is the sleep-on-it gate.
   Confirm the choice or record why it did not survive. Infatuation does not survive a gap;
   if it reads worse today, say so and go back to the pool, which now holds 32 candidates.
2. If confirmed: settle the name, then write `NOVELTY_REPORT.md` (Section 12 fields, using
   the searches above plus one confirming sweep for anything newer) **before** code.
3. Fill in `TASKS.json`: set `current_project`, the one-paragraph definition of done, and the
   milestone ladder. Proposed ladder, each rung a working artifact:
   * **M1 — vertical slice.** Dependency-free MIDI reader, an internal timed-event model,
     three-way merge of note additions, deletions and velocity changes where timing is
     unchanged, and one HTML page showing base / ours / theirs / merged as piano rolls with
     playback. Crude, end to end, on one real pair of files.
   * **M2 — time interaction.** Edits that insert or remove musical time and therefore move
     later material; conflict detection for overlapping regions; the conflict rendered and
     auditionable as A versus B.
   * **M3 — alignment without a trustworthy ancestor.** Recognise a moved or transposed
     section as moved rather than deleted-and-reinserted. Flagged in the red team as the
     rung most likely to fail; if it does, it is documented and the project stands on the
     others.
   * **M4 — real files.** Multiple tracks, tempo maps, controller curves, and a round-trip
     guarantee that bytes not understood are preserved.
   * **M5 — second binding.** Same core against a non-music timeline (subtitles or an edit
     decision list), which is the evidence that the primitive generalises rather than the
     claim that it does. A git merge driver is a thin adapter here, not the project.
   * **M6 — evidence pack.** Property tests, exhaustive verification on small cases,
     fuzzing against an oracle, and the controls: disjoint edits never conflict, identical
     edits never conflict, re-runs are byte-identical.
4. Hold the line the red team identified: if this ships as a command that prints a report,
   it has failed, regardless of how correct the merge is.

## Environment facts confirmed this run (Gate B)

Python 3.11.15, Node 22.22, 4 CPU cores, 15 GB RAM, ~30 GB writable disk, no GPU. Outbound
network works through the agent proxy (`pip download` verified). No numpy/scipy preinstalled.
Nothing in the selected project needs credentials, external services, or data this container
cannot reach.

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

## What the next run should know about the back catalogue

1. **All three existing projects share one shape** — a Python static analyzer that reads
   source files, prints findings and returns an exit code. That shape is banned for now, as
   is anything whose primary interface is "run a command, read a report".
2. **`IDEAS.md` is now large and is the repository's memory.** Read it before generating
   anything. The cron linter, the swapped-argument detector, the CSV anti-join tool, and ten
   more candidates as of 2026-09-21 are settled rejections with prior-art links.
3. **`cutline` still contains an unshipped primitive** — a solver that proves a set of
   commitments cannot all be met, emits a checkable certificate, and computes the cheapest
   subset to drop. It was considered again on 2026-09-21 and rejected as a standalone
   project under Gate E (near-duplicate of the existing folder). It remains a good engine to
   build *on top of*; it is not a new project by itself.
