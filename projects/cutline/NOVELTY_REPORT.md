# Novelty Report — cutline

**Project:** `cutline`

**One-sentence description:** Decides whether your task list fits its deadlines, and what to cut.

**Date of search:** 2026-09-12

**Searcher:** autonomous agent run (see `PROGRESS.md` in the repository root)

---

## 1. Candidate under assessment

A dependency-free command-line tool that reads a plain-text plan (working hours, fixed
appointments, days off, and tasks with estimates, deadlines, earliest start times and
importance weights) and answers three questions exactly:

1. Does every task fit before its deadline in the capacity that actually exists?
2. If not, which window is over-subscribed and by how many minutes? The answer is a
   checkable certificate: a set of tasks that can only run inside one interval, plus
   the capacity of that interval.
3. What is the cheapest set of tasks to cut so the rest fits, and how much later would
   each cut task's deadline need to be for it to survive?

The decision procedure is exact for divisible work: preemptive earliest-deadline-first
scheduling decides feasibility, and the cut set is found by branch and bound over
violated-window certificates, reported as proven minimal or explicitly labelled
unproven when the search budget is exhausted.

## 2. Search scope

In scope: personal and project task schedulers that consider deadlines, duration
estimates, working hours and calendar availability; tools that warn about
overcommitment; algorithms and academic work on deadline feasibility, minimising late
jobs, and explaining scheduling infeasibility.

Out of scope: multi-resource project-management suites whose purpose is Gantt planning
across teams, calendar applications without duration estimates, and the internals of
closed commercial schedulers, which are not publicly documented.

## 3. Sources searched

| Category | Sources actually consulted |
| --- | --- |
| Public source repositories | github.com via web search; repository and package pages for `00sapo/taskcheck` (fetched and read), `linuxcaffe/taskcheck`, `Aperocky/tascli`, GitHub topic listings for `taskwarrior` and `taskscheduler` |
| Package registries | pypi.org via web search, including a `site:pypi.org` query; `taskcheck`, `tasksched`, `ccpm-scheduler`, `student-task-deadline-planner-sm`, `deadline-suggester`, `timeboard`, `dailyscheduler`, `ManHourCalendar` |
| Product documentation | Super Productivity schedule-planner pages; Taskwarrior documentation, workflow guide and FAQ |
| Academic literature | arXiv, ACM DL, ScienceDirect, OpenReview, Dagstuhl results for the Moore–Hodgson algorithm and its 2021 proof, single-machine deadline feasibility, and infeasibility explanation |
| Forums and roundups | LWN task-management article, Hacker News Taskwarrior thread, medevel roundup of 27 CLI task managers, alternativeto listings, DaniWeb and OpenGenus algorithm discussions |
| This repository | `orbiter/`, the only existing project folder, which is a Python static analyzer and shares no capability with this candidate |

## 4. Query formulations used

Recorded as issued:

1. `CLI tool check if daily task list fits deadlines durations feasibility infeasible warn overcommitted plain text offline scheduler`
2. `open source deterministic time blocking scheduler earliest deadline first personal tasks feasibility proof minimal set to drop`
3. `"Moore-Hodgson" OR "minimum number of late jobs" algorithm applied todo list personal planner app which tasks to drop optimal`
4. `taskwarrior OR todo.txt overcommitment check will I finish before deadline calendar free time simulation github tool`
5. `github "non-AI automatic scheduler" todo tasks respecting working hours calendar taskwarrior topic project name`
6. `site:pypi.org task scheduling deadlines estimates working hours plan generator CLI package feasibility`
7. `tool "which tasks to drop" deadline overcommitted minimum tasks cut optimal scheduling personal planner reddit wish existed`
8. `"infeasibility" certificate explanation scheduling personal tasks tool "minimal" set drop OR defer deadline capacity window deficit github`

Pages fetched and read directly: `github.com/00sapo/taskcheck`, `pypi.org/project/taskcheck/`.

Queries 1 and 2 of the earlier rejected candidate in this run (see Section 8) were
`tool diagnose why csv join loses rows key mismatch leading zeros whitespace case normalization data engineering CLI`
and `join key discovery tool csv candidate keys inclusion dependency detection cardinality orphan rows report python`.

## 5. Closest prior art found

**1. taskcheck** — <https://github.com/00sapo/taskcheck>, <https://pypi.org/project/taskcheck/>
The closest tool. A non-AI automatic scheduler for Taskwarrior: it fits tasks into
working-hour maps and iCal calendar availability and warns when a task will miss its
due date. On an unmeetable deadline it "auto-adjusts urgency", retrying with urgency
overrides for up to ten rounds and then once at urgency 1000; if the task is still
late it stops raising it and optimises the others. Read directly for this report: it
does not compute which tasks to drop or defer and makes no minimality or optimality
claim. It requires Taskwarrior with custom user-defined attributes.

**2. Super Productivity** — <https://super-productivity.com/use-cases/schedule-planner/>
Free desktop planner whose schedule view "shows overload warnings before you
overcommit" from per-task time estimates. A warning that the day is too full, not a
decision about what to shed, and a GUI application rather than a checkable procedure.

**3. Commercial auto-schedulers** — Motion, Reclaim.ai, SkedPal, FlowSavvy, TimeHero,
Trevor. Calendar-integrated services that place tasks automatically and re-plan when
things slip. Their internal methods are not publicly documented; none advertises a
minimum-cost set of commitments to drop with an infeasibility certificate.

**4. Lauffer and Topcu, "Human-Understandable Explanations of Infeasibility for
Resource-Constrained Scheduling Problems" (2019)** —
<https://niklaslauffer.github.io/files/explain2019.pdf>
The closest academic work: it explains infeasibility in over-constrained
resource-constrained scheduling by enumerating minimal unsatisfiable sets and
computing hitting sets whose removal restores feasibility. Research framework for the
agent resource-constrained project scheduling problem, not a tool for personal plans,
and not tied to a working-hours calendar.

**5. The Moore–Hodgson algorithm** (1968; a short proof was published in *Operations
Research Letters* in 2021, <https://arxiv.org/abs/2104.06210>)
Minimises the number of late jobs on a single machine in O(n log n) by adding jobs in
due-date order and discarding the longest job whenever a deadline breaks. A building
block for this candidate's greedy upper bound, defined for a single machine with
continuous availability, no release times, and no calendar.

**6. Smaller PyPI packages** — `student-task-deadline-planner-sm` (flags overloaded
days or weeks where several tasks are due), `tasksched` (resource-levelled work plan),
`ccpm-scheduler` (critical-chain project scheduling), `deadline-suggester` (deadline
recommendations for freelance work). Each addresses a neighbouring problem; none
decides feasibility against a capacity calendar and returns a minimal cut set.

## 6. Feature-level comparison

| Dimension | cutline (proposed) | taskcheck (closest tool) | Super Productivity | Lauffer and Topcu 2019 | Moore–Hodgson |
| --- | --- | --- | --- | --- | --- |
| Problem | Decide whether a plan fits, and what to cut when it does not | Place tasks in available time and warn about late ones | Warn that a day is overloaded | Explain why a schedule is infeasible | Minimise the count of late jobs |
| Primary output | Verdict, over-subscription certificate, minimal cut set, deadline deferrals | A schedule plus urgency adjustments | A warning banner | Minimal unsatisfiable sets and hitting sets | A set of late jobs |
| Inputs | One plain-text file: hours, busy blocks, days off, tasks with estimate, deadline, earliest start, weight | Taskwarrior database with custom attributes, iCal feeds, TOML config | Tasks with estimates inside the app | A problem instance in the paper's formalism | Processing times and due dates |
| Calendar capacity | Yes: weekday working windows minus appointments and days off | Yes: time maps and iCal | Working hours in the app | Resource availability in the model | None |
| Release times | Yes, per task | Not documented as a constraint | No | Yes | No |
| Feasibility decision | Exact for divisible work, by two independent methods that must agree | Constructive: whatever the scheduler manages | Sum of estimates against available hours | Exact via a constraint solver | Implicit in the algorithm |
| What to cut | Minimum total weight, proven minimal or labelled unproven | Not computed | Not computed | Hitting sets of constraint subsets | Minimum count, no calendar |
| Deferral advice | Earliest deadline at which each cut task would fit | No | No | No | No |
| Deployment | Standard-library CLI, no install needed, text or JSON | Python package plus Taskwarrior | Desktop application | Research code | Algorithm |
| Weights and required tasks | Yes: weights, and tasks that may never be cut | Urgency heuristics | No | Constraint priorities | Unweighted |

## 7. Material equivalence assessment

The domain is crowded: several tools and services already place personal tasks into
calendar availability and warn when deadlines will slip. The capability this candidate
adds over them is a decision rather than a placement: an exact feasibility verdict, a
checkable certificate naming the over-subscribed window and its deficit, and a
minimum-weight set of commitments to cut with per-task deferral advice.

No tool found provides that. taskcheck, the closest, was read directly and responds to
unmeetable deadlines by adjusting urgency, explicitly without computing what to drop.
The academic work that does compute removal sets (Lauffer and Topcu) is a research
framework for a different problem class and is not available as a planning tool. The
classical algorithm that minimises late jobs (Moore–Hodgson) does not model a calendar
or release times, and is used here only as an upper bound inside the exact search.

The candidate therefore passes the material equivalence test, while claiming nothing
new about the underlying algorithms, all of which are established.

## 8. Candidates rejected earlier in this run

* **A join-diagnosis tool for tabular files** (discover candidate join keys between two
  CSVs, explain why a join loses rows, and name the normalisation that would fix it).
  **Rejected on material equivalence.** Apify's "CSV Anti-Join Finder" advertises
  exactly this: it "checks whether two CSV files are safe to join by analyzing key
  coverage, null keys, duplicates, type mismatches, whitespace/case drift, cardinality,
  unmatched rows, and likely row multiplication", with composite keys and normalisation
  rules. The R package `joinspy` diagnoses join key problems before joining, `Prism EDA`
  reports candidate keys with coverage and orphan counts, and `FDTool` mines candidate
  keys. The proposed capability was materially covered.

## 9. Unresolved uncertainty

* GitHub code search and full-text package search were unavailable in this environment,
  so discovery relied on web search results. A small or unindexed project with this
  capability could exist without appearing here.
* The commercial auto-schedulers (Motion, Reclaim, SkedPal, FlowSavvy, TimeHero,
  Trevor) do not document their algorithms. One of them may compute a minimal cut set
  internally without saying so.
* Whether the exact search stays within a practical budget on plans much larger than
  the sizes measured in `README.md` is not established beyond those measurements.
* The complexity of minimising the weighted number of late jobs with release times is
  not claimed here. The implementation is an exhaustive search with pruning and reports
  honestly when its budget is exhausted rather than relying on a complexity result.

## 10. Novelty confidence

**Medium.**

Several source categories were searched with multiple query formulations, the closest
tool was fetched and read rather than judged from its description, and no materially
equivalent capability was found. The rating is not High because the surrounding space
is densely populated with schedulers that share the same inputs, because closed
commercial products in that space cannot be inspected, and because the two search
channels that would most directly refute the finding, GitHub code search and full-text
package search, were unavailable.

## 11. Scope statement

This conclusion is limited to the sources and queries documented above. It states that
no materially equivalent prior art was found within the documented search scope, and
makes no claim that none exists.
