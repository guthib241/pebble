# Progress

Status: `cutline` is complete and pushed. No project in progress.
Current project: none (see `TASKS.json`)

## Completed projects

### orbiter (folder `orbiter/`)

Flags Python code that mixes units, like milliseconds passed as seconds. A static
analyzer over the `ast` module, standard library only, Python 3.11 or newer.

It infers a unit and a numeric scale for expressions from identifier names,
`typing.Annotated` metadata, and a table of standard-library call conventions, then
reports mismatches in call arguments (ORB001), arithmetic and comparisons (ORB002),
assignments (ORB003) and return values (ORB004). Constant factors are read as
conversions when they land on a real unit, so `time.sleep(timeout_ms / 1000)` is
accepted while `time.sleep(timeout_ms)` is reported.

State: finished. 151 tests pass. README, novelty report, license and reproducible
evidence are in the folder.

### cutline (folder `cutline/`)

Decides whether your task list fits its deadlines, and what to cut. A command-line
tool over one plain-text plan file, standard library only, Python 3.11 or newer.

It builds a capacity calendar from working hours minus appointments and days off, then
decides feasibility exactly for divisible work by two independent methods (preemptive
earliest-deadline-first, and the window condition). When a plan does not fit it prints
the over-subscribed window as a checkable certificate, the cheapest set of tasks to cut
found by branch and bound over violated windows, and for each cut task the earliest
deadline that would let it stay. Also answers "how much more can I take on by this
deadline" and "can I accept this new commitment".

State: finished. 120 tests pass. README, novelty report, license and reproducible
evidence are in the folder.

## Run log

### 2026-09-12 (run 1) — orbiter

Intake: read `AGENT_RULES.md`, `PROGRESS.md`, `TASKS.json`. `current_project` was null
and the repository held no project folders, so a new project was selected.

Prior-art search across GitHub repository pages, PyPI, the flake8 plugin index,
academic sources (arXiv, ACM DL, ScienceDirect, Semantic Scholar), tool documentation
and forum results. Full record in `orbiter/NOVELTY_REPORT.md`.

- Candidate 1, a cron DST hazard auditor: **rejected**. `cronkit` provides CLI crontab
  linting with overlap detection and schedule projection, and several DST-focused cron
  timezone checkers exist, so the capability overlapped materially.
- Candidate 2, a Python swapped-argument detector: **set aside**. The capability
  already exists for Python as a research artefact (the DeepBugs IntelliJ plugin;
  `eth-sri/learning-real-bug-detector` has an argument-swap task).
- Candidate 3, `orbiter`: **selected**, novelty confidence Medium. Closest prior art is
  Phys / Phriky-Units, which do annotation-free unit inconsistency detection for ROS
  C++; no Python equivalent was found.

Findings worth carrying forward:

- The first corpus run over `/usr/lib/python3.11` produced 9 findings, **all false
  positives**, from two lexicon problems: `mm` (millimetre or minute) and the singular
  calendar words `second`, `minute`, `hour`, `day`, `week`, which in real code name an
  index rather than a duration. Those entries were removed, singular `bit` with them.
  Re-running the same corpus gave 0 findings. Regression tests pin the exclusions.
- Removing singular `second` broke conversion constants such as `MS_PER_SECOND`, so
  names containing a `per` token are now handled separately: upper-case ones resolve to
  a numeric factor from the lexicon, lower-case ones (rates like `bytes_per_second`)
  are treated as unknown.

### 2026-09-12 (run 2) — cutline

Intake confirmed `current_project: null` and `orbiter/` complete, so Section 4 applied:
a new project, deliberately outside static analysis to avoid clustering.

- Candidate 1, a join-diagnosis tool for CSV files (discover join keys, explain why a
  join loses rows, name the normalisation that would fix it): **rejected on material
  equivalence**. Apify's "CSV Anti-Join Finder" advertises exactly that capability, and
  `joinspy` (R), `Prism EDA` and `FDTool` cover neighbouring parts of it.
- Candidate 2, `cutline`: **selected**, novelty confidence Medium. The closest tool,
  `taskcheck`, was fetched and read: it schedules Taskwarrior tasks against working
  hours and iCal availability and warns when a deadline will be missed, but responds by
  adjusting urgency and explicitly does not compute what to drop. Super Productivity
  warns about overload; the commercial auto-schedulers do not document their methods.
  The academic work that does compute removal sets (Lauffer and Topcu 2019, minimal
  unsatisfiable sets for resource-constrained scheduling) is a research framework, not
  a planning tool.

Findings worth carrying forward:

- A property test comparing the two feasibility methods found a real disagreement on
  the fifteenth random instance: a task whose earliest start was after its own deadline.
  EDF called it infeasible, the window condition called it feasible. The parser already
  rejects such plans, but the window method now reports an empty-window certificate so
  the two methods agree on every input, not only on valid ones.
- The first timing table was measuring the wrong code path: random plans with required
  tasks hit the "required work alone does not fit" early exit, so the cut search never
  ran and every row showed zero search nodes. The timing generators were replaced with
  plans deliberately overloaded by 20% and a worst case of identical tasks sharing one
  deadline. That worst case (20 tasks) exhausts the node budget, and the recorded
  result says "not proven minimal" rather than overstating it.
- Controls chosen for this project are invariances rather than a scenario suite alone:
  reordering the task list, shifting the whole plan by exactly one week, re-running the
  same scenario, and comparing the branch-and-bound cut against exhaustive enumeration.

Next action: `TASKS.json` has `current_project: null`, so the next run performs idea
generation and a fresh prior-art search under Section 4 of the execution protocol. The
search must treat both `orbiter/` and `cutline/` as prior art for any new candidate,
and both existing projects are command-line developer or productivity tools, so the
next candidate should look to a different category (data or visualisation work, a game
or playful tool, a reproduction of a published method, or something monetisable).
