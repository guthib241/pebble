# cutline

Decides whether your task list fits its deadlines, and what to cut.

**Closest prior art:** [taskcheck](https://github.com/00sapo/taskcheck), a non-AI
automatic scheduler for Taskwarrior that fits tasks into working hours and calendar
availability and warns when a task will miss its due date. Also
[Super Productivity](https://super-productivity.com/use-cases/schedule-planner/), whose
schedule view shows overload warnings, and the commercial auto-schedulers (Motion,
Reclaim, SkedPal, FlowSavvy, TimeHero, Trevor).
**Difference:** those tools place work and warn. cutline decides. It gives an exact
feasibility verdict, a checkable certificate naming the over-subscribed window and its
deficit in minutes, the cheapest set of tasks to cut with that cut proven minimal, and
for each cut task the earliest deadline that would let it stay. taskcheck responds to
unmeetable deadlines by adjusting task urgency and explicitly does not compute what to
drop; cutline needs no Taskwarrior database, no calendar service and no dependencies.
**Search confidence:** Medium.
**Scope:** This assessment reflects the sources and queries documented in
[`NOVELTY_REPORT.md`](NOVELTY_REPORT.md). It states that no materially equivalent tool
was found in that search, not that none exists.

## Status

Working and tested. 120 tests pass, and every number in
[Validation](#validation) comes from a script in this repository that reproduces it.
Requires Python 3.11 or newer; nothing outside the standard library.

## Install and run

No installation needed to try it:

```sh
python3 -m cutline --example > week.txt
python3 -m cutline week.txt
```

To install the `cutline` command:

```sh
python3 -m pip install .
cutline week.txt
```

Exit status is 0 when the plan fits, 1 when it does not, and 2 when the plan file or the
arguments cannot be used.

## The plan file

One plain-text file says when you can work and what you have promised:

```
now: 2026-09-14 09:00

hours:
  mon-fri: 09:00-12:30, 13:30-17:30
  sat: 10:00-13:00

off: 2026-09-16

busy:
  2026-09-14 11:00-12:00  standup
  2026-09-15 14:00-15:30  dentist

tasks:
  spec draft        6h    due 2026-09-15 12:00  weight 3
  migration script  5h    due 2026-09-15 17:30  required
  code review       2h    due 2026-09-14 17:30  earliest 2026-09-14 13:30
  slides            3h    due 2026-09-15 17:30  weight 0.5
```

* `hours` gives working windows per weekday; `mon-fri`, `mon,wed,fri` and single days all
  work. Time outside those windows does not exist as far as cutline is concerned.
* `busy` blocks and `off` days are subtracted from that capacity.
* A task needs an estimate and a `due`. A bare date as a deadline means the end of that
  day. `earliest` says the work cannot start before some moment, `weight` says how much
  cutting it would cost (default 1), and `required` means never cut it.
* Durations are written `45m`, `2h` or `6h30m`. All times are naive local times.

Problems are reported together, with line numbers, rather than one per run:

```
$ cutline broken.txt
cutline: line 7: task 'review' is due at or before 'now' (2026-09-13 17:00 <= 2026-09-14 09:00)
cutline: line 8: task name 'review' already used on line 7
cutline: line 9: task 'write up' cannot start after its deadline
```

Syntax problems are reported before the checks that need a complete plan, so a file with
both kinds takes two passes to clear.

## What it tells you

```
$ cutline evidence/scenarios/one-cut.txt
plan: evidence/scenarios/one-cut.txt
now: Mon 2026-09-14 09:00    last deadline: Mon 2026-09-14 17:30
capacity until then: 7h30m free, committed 9h across 3 task(s)

VERDICT: does not fit, 1h30m too much work

over-subscribed window
  Mon 2026-09-14 09:00 -> Mon 2026-09-14 17:30
  capacity 7h30m, committed 9h, short 1h30m
  tasks that must run inside it: customer reply, incident writeup, slides

cheapest cut (proven minimal, total weight 1, 1 search node(s))
  cut slides  2h  weight 1  due Mon 2026-09-14 17:30
      keep it by moving its deadline to Mon 2026-09-21 10:30 (6 days 17h later)
  after the cut the plan fits, tightest deadline Mon 2026-09-14 17:30 with 30m spare
```

The window is a certificate you can check by hand: those three tasks can only run inside
that interval, the interval holds 7h30m, and they need 9h.

Other things it answers:

```sh
cutline week.txt --schedule                      # the block-by-block plan
cutline week.txt --slack                         # how much new work each deadline can take
cutline week.txt --accept "review:90m@2026-09-18 17:00"   # can I take this on?
cutline week.txt --now "2026-09-14 16:00"        # re-decide later in the day
cutline week.txt --json                          # the whole analysis, machine readable
```

## How the decision is made

Work is treated as divisible: a task can be split across any number of free blocks, with
a minute as the smallest unit. Under that assumption the verdict is exact, and it is
computed twice by methods that share no code beyond the calendar:

1. **Preemptive earliest-deadline-first** over the free intervals. EDF is optimal for one
   resource with release times, so a task that finishes late means no schedule exists.
2. **The window condition.** For every interval bounded by a release time and a deadline,
   the work that can only run inside it must not exceed its capacity. A violated window
   is the certificate printed above.

If the two ever disagree, that is a bug, and the tool says so in its output rather than
picking one. The control checks below run both on hundreds of random plans.

The cut search uses one fact: every task in an over-subscribed window cannot fit, so any
fix must cut at least one of them. Branching over the tasks of one violated window is
therefore complete, and with cost-based pruning the search returns a minimum-weight cut.
A greedy pass in the spirit of the Moore-Hodgson rule (discard the longest job when a
deadline breaks) supplies the starting bound. When the search hits its node budget,
output says `NOT proven minimal` instead of claiming optimality.

## Limitations

* Tasks are divisible. A task that must run in one unbroken block is not expressible, and
  such a plan could be reported as fitting when in practice it does not.
* One resource. cutline plans one person's time; it does not assign work across people.
* No dependencies between tasks: "B after A" cannot be stated.
* Estimates are taken at face value. Nothing here corrects optimistic estimates.
* Naive local times only. No time zones, and no daylight-saving arithmetic.
* Deferral advice moves one deadline at a time, holding the rest of the cut in place.
* Minimising the weighted number of late tasks with release times is a hard problem in
  general. The search is exhaustive with pruning and is honest when its budget runs out;
  no complexity claim is made.

## Validation

```sh
python3 -m unittest discover -s tests -t .      # 120 tests
python3 evidence/run_evidence.py > evidence/results.md
```

The test suite covers the parser and its error reporting, interval and capacity
arithmetic, both feasibility methods, schedule validity (no overlaps, inside free time,
inside each task's own window, every minute of every estimate placed), slack tightness,
deferral advice, the cut search against exhaustive enumeration, the CLI including error
paths, and an install check that builds this package into a fresh virtualenv and runs the
installed `cutline` command.

Measured results, all produced by the evidence script and recorded in
[`evidence/results.md`](evidence/results.md):

| Measurement | Result |
| --- | --- |
| Scenario files in `evidence/scenarios/` | 10 |
| Scenarios whose outcome matched the expectation written in the file | 10 |
| Random plans where both feasibility methods agreed | 500 of 500 |
| Of those, plans that fit / did not fit | 293 / 207 |
| Random plans where the cut matched exhaustive enumeration | 200 of 200 |
| Random plans whose verdict and cut survived reordering the task list | 200 of 200 |
| Random plans whose verdict and cut survived shifting the plan one week | 200 of 200 |
| Scenarios producing byte-identical output on a second run | 10 of 10 |

Timing from the same run, on CPython 3.11.15, Linux 6.18.44 x86-64. Search-node counts
are deterministic; wall clock varies between runs on the same machine.

| Plan shape | Tasks | Wall clock | Search nodes | Proven minimal |
| --- | --- | --- | --- | --- |
| overloaded by 20% | 40 | 0.035 s | 234 | yes |
| overloaded by 20% | 80 | 1.968 s | 10427 | yes |
| identical tasks, one deadline | 12 | 0.010 s | 299 | yes |
| identical tasks, one deadline | 20 | 7.323 s | 200000 | no |

The last row is the worst case for the search and is included deliberately: twenty
interchangeable tasks sharing one deadline exhaust the default node budget, and the tool
reports the cut it found as not proven minimal rather than overstating it.

Four control checks run in the same script. Three are invariance controls in the strict
sense, comparing inputs that cannot change the answer: the same plan with its task list
reordered, the same plan shifted forward by exactly one week, and the same scenario run
twice. The fourth compares two independent implementations of the same decision. A
scenario suite alone would only show that the tool agrees with its author; these compare
the tool against itself under changes that must not matter, and against exhaustive
enumeration where that is affordable.

The scenarios were written by the same author as the tool, which limits what "10 of 10"
establishes: it shows the documented behaviour holds on the cases it targets, not
accuracy on plans from the wild. No claim is made about how cutline compares to any other
scheduler's output, because no controlled comparison was run.

## License

See [`LICENSE.txt`](LICENSE.txt). This repository's owner has chosen a single custom
license for everything built here, which permits non-commercial use with attribution and
requires contact for commercial use.
