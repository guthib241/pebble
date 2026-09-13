# Progress

Status: no project in progress. Three projects complete. A new project has not yet
been selected under the current rule set. Selection is **in progress and
deliberately unfinished** — see the 2026-09-13 run record below.
Last updated: 2026-09-13

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

## Run record — 2026-09-13 (Outcome E: selection only, no implementation)

This run produced no code, and should not have. Under `AGENT_RULES.md` ("a run that
produces no code and one excellent decision is a successful run") and protocol
Outcome E, that is the intended result when the bar has not been met. It has not
been met. Nothing was selected.

**Hook sentence for the run: none.** No candidate earned one that holds. Recording
the absence rather than manufacturing a sentence for a candidate I was not pulled
toward — a hook that needed several attempts and still felt flat is the first
listed sign of rushing.

### What changed in the repository

The owner supplied two documents mid-run. Both are now committed, because they
lived outside the repository where the next run could not see them:

* **`IDEA_DOMAINS.md`** (repository root) — an ideation directive. Five domains,
  seven hard rejection filters applied before scoring, and a verification bar of
  novelty ≥ 4 and verifiability ≥ 4. Read it with the other control files from now
  on. It does not replace `AGENT_RULES.md` or the protocol; it reshapes the seed
  distribution and adds filters on top.
* **`notes/2026-09-13-external-repo-analysis.md`** — a landscape survey of the 2026
  agent-loop field with ten proposed projects, preserved verbatim under a
  provenance header.

**The two documents conflict, and the conflict was resolved against the analysis.**
All ten of its proposed projects are agent-loop meta-tooling, which
`IDEA_DOMAINS.md` §0.3 puts out of scope ("Pebble builds projects; it does not
build more Pebble"). All ten are recorded as rejected in `IDEAS.md` section 1. The
survey itself is worth keeping; its project list is not actionable. If the owner
meant for those to be built, §0.3 needs changing and they should say so.

Also checked and closed: `IDEA_DOMAINS.md` §5 raises an "Action required" on
`LICENSE.txt` placeholders. It is **stale**. `[YEAR]`, `[YOUR NAME OR ORG]`,
`[YOUR NAME]` and `[YOUR EMAIL]` were filled in commit 3721576. The single
remaining `[PROJECT NAME]` sits inside clause 3's example attribution string, which
a derivative project fills in with its own name — not a blank to fill here.
Nothing is blocked; no action taken beyond verifying it.

### The search, and what it killed

36 candidates recorded in `IDEAS.md` (C1–C10 from the owner's document, P1–P26
generated here), against a quota of 20. 22 resolved, 14 standing, none selected.
Six independent web searches were run, all recorded with their query strings in
`IDEAS.md`.

Four of the strongest candidates died on prior art, which is the useful part of
the run:

* **P4, a canonical fingerprint for circuit topology** — the best candidate in the
  pool on the upstream-primitive rule, because it answered "what becomes
  buildable?" with a list. It is a mature EDA field: topology-only netlist
  normalisation is standard, subcircuit recognition as bipartite subgraph
  isomorphism underpins layout-versus-schematic checking, and it is patented.
  Building it would be re-deriving LVS.
* **P3, a semantic diff for schematics** — `AGENT_RULES.md` names "a diff strategy
  for something that currently has none" as a target, and hardware people do
  suffer here. KiHub already ships under that exact framing. Not fully settled:
  the open-source tools are image diffs, so the graph-level version is not
  entirely claimed, and the entry says what would reopen it.
* **P2, Gerber → netlist** — this run's *first* idea, rejected as a final answer per
  the rule, and then killed independently by Altium's documented CAMtastic
  workflow, a service industry, and US 5781447. Its useful residue: connectivity
  extraction is the solved part, so any survivor must start *after* the netlist and
  do the electrical interpretation, which is what `IDEA_DOMAINS.md` D3 demands.
* **P5, thermal field from Gerber copper** — occupied by commercial tools, KiCad,
  and a documented Elmer/ParaView route. The only gap is convenience, which R7
  rejects outright.

### Where it stands, precisely

The leading survivor is **P1 — recovering an unknown wire protocol from raw logic
captures and emitting a runnable decoder**. Its position is genuinely open: the
academic protocol-reverse-engineering field (Netzob, Discoverer, NetPlier, the Sija
survey) works on *already-framed byte messages*, and the blind physical-layer
literature is RF-flavoured; the wired-embedded case starting from sampled logic
levels is where the two do not meet. Its originality scores 3, not higher, because
of that RF literature. Identifying a *known* protocol from a capture is dead —
patented and implemented — so only the unknown-protocol framing survives.

**The specific open question blocking the choice: ground truth for P1.**
Synthesised captures would make the evaluation circular, and `IDEA_DOMAINS.md`
sets verifiability ≥ 4. The public sigrok-dumps archive is the obvious source and
**was not inspected this run**. The candidate stands or falls on it.

**Next concrete steps, in order:**

1. Re-read `IDEAS.md` section 5 cold, before anything else. That is the mandatory
   gap-crossing check; an entry that no longer reads well was infatuation.
2. Inspect sigrok-dumps directly — does a labelled corpus of real captures exist,
   how many, how many distinct protocols, and is it usable as scored ground truth?
   This decides P1 and is cheap.
3. Search **P7** (a representation for a partly-known circuit, with an
   evidence-combination algebra and calibrated per-net confidence). It is the
   highest-value *unsearched* entry and the only remaining candidate that answers
   "what becomes buildable?" with a list. Its known risk is collapsing into "a
   netlist with confidence floats", which would fail Gate A.
4. Search ERC formalisation for **P6/P12** (a type system for electrical
   connections), which survives only if the lattice and its soundness are the
   deliverable and the checker is one demo — otherwise it is inside the shape ban.
5. If none of these clears the bar, generate again. Do not settle.

### One structural observation for the owner

Every surviving candidate sits in electronics. That is the filters working as
written, not a preference: R1–R5 remove the conversational and wrapper shapes, R6
removes D2 and D5 because this container has no microcontroller and no instruments,
R4 plus §0.3 remove D4, and the `AGENT_RULES.md` shape ban removes the
source-reading checker the repository keeps defaulting to. What is left is D1 and
D3. Worth flagging in case that concentration was not intended — and worth saying
that **if a board and a logic analyser are on a desk somewhere, D2 and D5 reopen
immediately** and are the most interesting territory in the file.

---

## What the next run should know

1. **No project is in progress.** `current_project` is null. Selection is the job,
   and it is already underway — start from `IDEAS.md` section 5 and the numbered
   next steps in the 2026-09-13 run record above, not from a blank page.
2. **Selection is not time-boxed.** A run whose entire output is a documented search
   and one excellent decision is a successful run. Record it here and in `IDEAS.md`
   and stop. Do not implement something to make the run look productive.
3. **All three existing projects are the same shape** — a Python static analyzer
   that reads source files, prints findings and returns an exit code. That shape is
   banned for now. So is anything whose primary interface is "run a command, read a
   report". See the shape ban in `AGENT_RULES.md`.
4. **Check `IDEAS.md` before generating candidates.** The cron linter, the
   swapped-argument detector and the CSV anti-join tool are settled rejections with
   prior-art links. So are the Gerber-to-netlist recoverer, the canonical circuit
   fingerprint, the Gerber thermal solver, the probeable schematic (Falstad) and
   the firmware-blob mapper, all added 2026-09-13. Do not re-search any of them.
   `IDEA_DOMAINS.md` must also be read now — its R1-R7 filters apply before
   scoring, and its §0.3 rules out agent-loop meta-tooling as a project.
5. **There is an unshipped primitive already in this repository.** `cutline`
   contains an engine that proves a set of commitments cannot all be met, emits a
   checkable certificate, and computes the provably cheapest subset to drop,
   verified against exhaustive enumeration. It shipped inside a day planner. It
   generalises to sprints, cloud budgets, timetables and CI minutes. If a candidate
   would build on it, that is a strong starting point — and re-scoping it as the
   primitive it is would satisfy the ship-the-primitive rule.
