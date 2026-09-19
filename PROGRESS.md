# Progress

Status: **selection in progress, no project selected.** Three projects complete. The
2026-09-19 run generated and searched candidates and deliberately produced no code — a
documented search and no decision yet, which the rules count as a successful run.
Last updated: 2026-09-19

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

## Run 2026-09-19 — selection only, nothing built (Outcome E)

No hook sentence for the run, because no project was selected. That is the finding, not
an omission.

**What was done.** Full intake of all five control files. `current_project` was null, so
Phase 1.5 sent this run to Section 4. Twenty-five candidates were generated and every one
was written into `IDEAS.md` under the heading matching its outcome. The generation rules
were followed as written: the run's first idea (semantic diff and merge for binary
formats) was rejected as a final answer and recorded as such; candidates were sampled
from the tails rather than the obvious centre; the pool spans formats, fabrication,
optics, data, typography, games and formal groundwork rather than five command-line
tools; the owner's Pebble Evolve idea was read and considered first.

**What was searched.** Web search across research literature, GitHub, open-source tools
and product pages, using multiple query formulations per candidate. Six candidates were
killed on directly inspected prior art and are now settled — do not re-search them:

* shadow art — Mitra & Pauly 2009, ShadowArt-Revisited, ShadowDraw (CVPR 2026)
* document un-shredding — RazvanRanca/UnShredder, JigsawNet, PairingNet, commercial Unshredder
* barrier-grid / scanimation — animbar, kinegram, MIT FabObscura (2025)
* linkage synthesis from a drawn curve — Pyslvs-UI, pylinkage-editor, LInK, LINKS
* GTFS transit fragility — G2Viz, GTFS2STN, the graph-oriented GTFS literature
* caustic projection — Schwartzburg et al. 2014, Rayform, Ferraro's open implementation

Four more were settled on prior art already known without a fresh search (uncertainty
spreadsheets, chart fonts, CRDTs, paper-as-storage, WFC pattern languages), and are
recorded as informed rejections rather than searched ones, which `IDEAS.md` says plainly.

**Where the decision stands.** Four candidates survived into `IDEAS.md` section 5, with
scores and a pairwise comparison. The leader — an image format that degrades
proportionally when an arbitrary fraction of its bytes is lost — was red-teamed in
writing before any build, and **it failed its own red team**: the mechanism is unequal
loss protection and progressive rateless coding, both published, so the contribution
would be packaging plus a demo. The hook was stronger than the originality, which is
exactly the trap `AGENT_RULES.md` warns about.

**Honest conclusion: nothing on the list yet reaches the bar** — a candidate I would be
genuinely disappointed to see someone else ship first. Per the rules, that means the list
is too short, not that the standard should drop. No implementation was produced and none
should have been.

**The open question blocking the choice.** Every surviving candidate is either a
packaging exercise over a published mechanism (F1, F4), a reimplementation of a paper
whose idea is not itself new (F2), or has no hook yet (F3). What is missing from the pool
is a candidate whose *mechanism* is the contribution, not its presentation.

**Next concrete steps, in order, for the next run:**

1. Re-read `IDEAS.md` section 5 first, before anything else — the sleep-on-it gate. A
   candidate that reads worse the second time is dead; say so and move it out of section 5.
2. Settle F2's open question in writing: what did Li et al. (2010) not build, and is that
   extension the actual project? If the answer is only "a reference implementation," it
   fails Gate E — record that and move it out of section 5.
3. Generate a second pool from the sources this run did not reach: future-work sections of
   recent papers, GitHub issues with many reactions and no pull request, and unexploited
   public datasets. This run drew mostly on cross-domain transplants and constraint
   injection, and those two veins are now thin.
4. Settle F1's one open question — whether any shipped artifact delivers smooth
   proportional degradation under arbitrary byte loss, or whether that is purely a
   literature result. If it has shipped, move F1 to section 2.

**What this run did not do**, stated plainly: it did not select a project, did not write
a `NOVELTY_REPORT.md` (none is due — that is a per-project document, required before
implementation of a selected project), and did not write any code.

## What the next run should know

1. **No project is in progress.** `current_project` is null. Selection is the job, and
   it is already underway — start from `IDEAS.md` section 5 and the four next steps
   above, not from a blank page.
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
