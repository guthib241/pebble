# Progress

Status: **selection in progress, deliberately unfinished.** No project is being built.
This run generated and searched a pool of 29 candidates and produced a scored
shortlist with a provisional leader. Per the sleep-on-it rule, the shortlist must be
re-read at the start of the next run before anything is implemented.
Last updated: 2026-09-18

## Run of 2026-09-18 — outcome E (selection only)

No code was written, and none should have been. The run's output is the candidate
pool, the searches behind it, and one decision that is not yet final. What follows is
everything the next run needs.

### 1. The owner's idea was evaluated first, and passed on

`Pebble Evolve` (section 0 of `IDEAS.md`) had never been through the gates. It has now
been, and it was passed on for this run, with the reasoning written into its entry so
the owner can push back. Short version: the gap the owner's note identified — evolving
whole projects rather than single functions — has closed since the note was written
(EvoLattice, CodeEvolve, DEI, on top of AlphaEvolve, ShinkaEvolve and OpenEvolve), and
the part that is still unclaimed, a taste signal personal to the owner, needs owner
rating data that does not exist yet. The cheap way to unblock it is for the owner to
rate past candidates in `IDEAS.md` for delight, which would create that data.

### 2. The shortlist, and what decides it

Full scores, the pairwise comparisons and the red team are in section 5 of `IDEAS.md`.
Provisional order: **C24**, then C26, then C25, then C27.

**C24 — "Give it a pile of files in a format nobody documented, and it hands back a
parser that rebuilds every one of them byte for byte."** Infer the structure of an
undocumented binary format from a corpus of files, emit an executable description plus
a rendered map of what every byte means, and prove the description by re-serialising
the corpus byte for byte.

**This is not yet a decision, and one specific finding could kill it.** The searches
this run showed the area is far more crowded than it looks: field inference from
corpora is an active research area for network messages (BinaryInferno, NEMESYS,
Netzob, NETPLIER, FieldHunter), and RL-GRIT already infers a grammar from a corpus of
files *and already uses byte-identical round-trip re-serialisation as its correctness
criterion* — which was the property this candidate was going to be distinguished by.

### 3. The single open question the next run must answer first

> Does any existing tool or paper infer **pointer and container structure** from a
> corpus of files — offsets resolved as edges into the file, nesting recovered,
> coverage of every byte reported — as opposed to flat field boundaries within a
> message?

Everything else about C24 is settled. If the answer is yes, C24 goes to section 2 of
`IDEAS.md` as prior-art-rejected and C26 is promoted. If the answer is no, C24 is the
project, and its milestone 1 must be the pointer case done badly end to end on one
real format — **not** the flat-record case, which is taken.

Searches to run (these have not been run; do not repeat the ones in section 4 below):
"pointer inference binary format offset table recovery corpus"; "hierarchical
structure inference file format nested chunks"; "byte coverage complete parse unknown
format"; a direct look at NETPLIER; and one more attempt at
`github.com/jbirby/binary-format-reverser`, which is indexed by search engines with a
description that overlaps C24 but returned 404 on both the repository page and the raw
README on `main` and `master` on 2026-09-18. That repository is the largest unresolved
gap in this run's search, and its contents could change the verdict on their own.

### 4. Searches already performed — do not repeat these

* evolutionary search over whole software projects, LLM population, MAP-Elites, 2026
* ShinkaEvolve / OpenEvolve / AlphaEvolve evolving entire applications
* infer binary file format structure from a corpus of sample files
* Netzob / NEMESYS / BinaryInferno message format inference
* grammar induction for file formats with round-trip byte-identical validation
* automatically generating a Kaitai Struct spec from sample files
* file-format RE tools with annotated hex views and differential analysis
* GitHub: infer binary format from multiple samples, length field and checksum detection
* phonetic error-correcting codes, confusion matrices, PGP word list
* uncertain and fuzzy historical date reasoning, interval propagation, EDTF
* minimum-edit repair to a grammar, Aho-Peterson error-correcting parsers

Directly inspected: BinaryInferno's repository, the RL-GRIT paper. Attempted and
failed: `jbirby/binary-format-reverser` (404, twice, two branches).

### 5. Why no code

Because the rules say a run whose entire output is a documented search and one
excellent decision is a successful run, and because the shortlist is one unresolved
search away from changing. Building C24 this run would have meant implementing a
candidate whose closest prior art I had explicitly failed to reach. The candidate
survived the searches I could complete; it has not survived the one I could not.

## Where the work is committed

This run's changes are on branch `claude/intelligent-mendel-20xp8a`, which is
`main` plus these commits. `IDEAS.md` gained 29 candidate entries and a new section 5
for shortlisted-but-undecided candidates; `PROGRESS.md` and `TASKS.json` record the
state above. `current_project` remains null: selection is genuinely not finished, and
recording it as finished would be the exact false completion the protocol forbids.

## Read this first — standing context

The rules changed substantially on 2026-09-12, after the three existing projects were
built. Read `AGENT_RULES.md` and the execution protocol completely before acting. The
main changes: projects may span many runs and take as long as they need, selection is
not time-boxed, a hook sentence and a ten-second demo are required before building,
there is a temporary ban on the shape all three existing projects share, and every
candidate idea must be recorded in `IDEAS.md`.

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

## Standing notes for any run

1. **Check `IDEAS.md` before generating candidates.** As of 2026-09-18 it holds 29
   candidates from this run alone, most already searched, plus the earlier settled
   rejections (cron linter, swapped-argument detector, CSV anti-join). Do not
   re-search anything recorded there without a specific reason to think the landscape
   changed — and if you do, record what changed.
2. **All three existing projects are the same shape** — a Python static analyzer that
   reads source files, prints findings and returns an exit code. That shape is banned
   for now, as is anything whose primary interface is "run a command, read a report".
3. **There is an unshipped primitive already in this repository.** `cutline` contains
   an engine that proves a set of commitments cannot all be met, emits a checkable
   certificate, and computes the provably cheapest subset to drop, verified against
   exhaustive enumeration. It shipped inside a day planner. Re-scoping it around that
   engine is legitimate work — but it was rejected as *this* run's selection under the
   first-idea rule, because it is the candidate any agent reading this repository
   would produce first. See C1 in `IDEAS.md`.
