# Progress

Status: no project in progress. Three projects complete. A new project has not yet
been selected under the current rule set.
Last updated: 2026-09-12

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

## What the next run should know

1. **No project is in progress.** `current_project` is null. Selection is the job.
2. **Selection is not time-boxed.** A run whose entire output is a documented search
   and one excellent decision is a successful run. Record it here and in `IDEAS.md`
   and stop. Do not implement something to make the run look productive.
3. **All three existing projects are the same shape** — a Python static analyzer
   that reads source files, prints findings and returns an exit code. That shape is
   banned for now. So is anything whose primary interface is "run a command, read a
   report". See the shape ban in `AGENT_RULES.md`.
4. **Check `IDEAS.md` before generating candidates.** The cron linter, the
   swapped-argument detector and the CSV anti-join tool are settled rejections with
   prior-art links. Do not re-search them.
5. **There is an unshipped primitive already in this repository.** `cutline`
   contains an engine that proves a set of commitments cannot all be met, emits a
   checkable certificate, and computes the provably cheapest subset to drop,
   verified against exhaustive enumeration. It shipped inside a day planner. It
   generalises to sprints, cloud budgets, timetables and CI minutes. If a candidate
   would build on it, that is a strong starting point — and re-scoping it as the
   primitive it is would satisfy the ship-the-primitive rule.
