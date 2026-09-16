# Progress

Status: no project in progress. Three projects complete. Selection is under way and
deliberately unfinished: this run generated and searched a candidate pool and
produced one leading candidate, which is held for the mandatory cold re-read.
Last updated: 2026-09-16

**Where this run's work lives:** branch `claude/intelligent-mendel-knoq8x`, not
`main`. The session was assigned that branch. It should be merged into `main` so
the next run's intake sees it — the consolidation note below is about exactly the
cost of leaving run state stranded on a branch.

## Read this first

The rules changed substantially on 2026-09-12, after these three projects were
built. Read `AGENT_RULES.md` and the execution protocol completely before acting —
they are not what the earlier runs operated under. The main changes: projects may
now span many runs and take as long as they need, selection is not time-boxed, a
hook sentence and a ten-second demo are required before building, there is a
temporary ban on the shape all three existing projects share, and every candidate
idea must be recorded in `IDEAS.md`.

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

## Run of 2026-09-16 — selection only, no implementation (Outcome E)

This run produced no code, by design. Under the selection rules that is a complete
run, and it is recorded as one rather than dressed up or apologised for.

**What was done**

* Full Phase 1 intake of all five control files; `TASKS.json` parsed and valid.
* Phase 1.5: `current_project` was null and all three completed projects are
  published, so Section 4 selection was the job.
* The owner's idea in section 0 of `IDEAS.md` (Pebble Evolve) was considered first,
  as the rules require, and passed on for this cycle with the reasons written into
  its entry — along with the one thing the owner could supply that would change the
  answer (roughly 50 personal 1-5 delight ratings on candidates from `IDEAS.md`).
* 26 candidates generated and recorded in `IDEAS.md` section 5, with probabilities,
  behaviour descriptors and outcomes. The cell all three existing projects occupy
  was excluded by hand.
* This run's first idea (PDF draft time-lapse) was rejected as a final answer, as
  required, and then died independently on prior art.
* Prior art searched across web search, GitHub and PyPI, plus search-result
  summaries of the Blender developer tracker and community forums — a direct fetch
  of `projects.blender.org` returned HTTP 403 here, so that source is second-hand
  and is labelled as such in `IDEAS.md`. Four candidates were killed outright, each
  recorded with links: regex delta (greenery, interegular, RegexSolver), PDF
  time-lapse (pdfresurrect), barrier-grid animation (animbar, Mightool), and — on
  feasibility here rather than prior art — the green-screen keyer.
* Two finalists scored, compared pairwise, and the leader red-teamed in writing.

**Leading candidate: `dovetail` — a three-way merge for Blender `.blend` files**

Proposed hook: *"Two artists edited the same 3D file at the same time — this merges
both of their changes into one file that opens in Blender."*

It is a leading candidate, **not a selection**. It has not been entered in section 4
of `IDEAS.md` and `current_project` remains null.

**Feasibility verified this run, not assumed:** `pip install bpy` gives Blender
5.0.1 importable in this environment; a script authored, saved, re-opened and
CPU-rendered a `.blend` successfully. Two facts worth inheriting: rendering must use
Cycles on CPU (`BLENDER_WORKBENCH` fails — no `libEGL.so.1`), and a saved `.blend`
starts with `28 b5 2f fd`, i.e. Zstandard, so a parser must decompress before it
will find the `SDNA` block. Blender itself is therefore available as an independent
oracle for every merged file.

## What the next run must do first

1. **Do not start implementing on sight.** The sleep-on-it rule exists precisely for
   this state: re-read `IDEAS.md` section 5 cold, before anything else, and ask
   whether `dovetail` still reads better the second time. If it does not, say so and
   go back to the pool — that is a successful outcome too.
2. **Read Blender PR #151266 directly if you can.** The quote that anchors
   `dovetail`'s prior-art case came from a search-result summary; `projects.blender.org`
   returned 403 to a direct fetch this run. Try an alternative route and confirm it.
3. **Close the one open prior-art question.** Search the model-driven engineering
   literature on three-way merging of graph-structured models — EMF Compare, EMF
   Diff/Merge, and the academic work on model merging. Nothing has been searched
   there yet, and it is the only search that could still materially overlap
   `dovetail`'s algorithm. Record the result either way.
4. **Settle one design question before milestone 1:** merge by operating on the file
   structure directly (primitive, uses `bpy` only to verify) or by appending through
   `bpy` (a script, not a primitive). The rules point at the first; confirm it is
   achievable with a short spike that decompresses a real `.blend` and reads its
   `SDNA` block.
5. **Only then** write the definition of done and the milestone ladder into
   `TASKS.json`, set `current_project`, and build milestone 1 as a vertical slice:
   one real merge of two real edits, verified by re-opening and rendering in
   Blender, with the three-render demo.
6. If `dovetail` falls, `driftwood` is the recorded fallback and half its search is
   already done. Its honest weakness is written down: originality 2, because the
   theory is 25 years old.

## Standing notes for every run

1. **Selection is not time-boxed.** A run whose entire output is a documented search
   and one excellent decision is a successful run. Do not implement something to
   make a run look productive.
2. **All three existing projects are the same shape** — a Python static analyzer
   that reads source files, prints findings and returns an exit code. That shape is
   banned for now. So is anything whose primary interface is "run a command, read a
   report". See the shape ban in `AGENT_RULES.md`.
3. **Check `IDEAS.md` before generating candidates.** The cron linter, the
   swapped-argument detector, the CSV anti-join tool, and now the regex delta, the
   PDF time-lapse and the barrier-grid generator are settled rejections with
   prior-art links. Do not re-search them. Section 5 holds 19 parked candidates that
   were generated but not gated — start a pool from those rather than from nothing.
4. **There is an unshipped primitive already in this repository.** `cutline`
   contains an engine that proves a set of commitments cannot all be met, emits a
   checkable certificate, and computes the provably cheapest subset to drop,
   verified against exhaustive enumeration. It shipped inside a day planner. It
   generalises to sprints, cloud budgets, timetables and CI minutes. It is parked as
   candidate 17 rather than chosen, because it re-occupies the cell this repository
   already over-uses — but it stays available.
