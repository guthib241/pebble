# cutline evidence run

- Date (UTC): 2026-09-12 22:47:01
- Commit: c155a84
- Python: 3.11.15 (CPython)
- Platform: Linux-6.18.44-fc-v24-x86_64-with-glibc2.39
- Command: `python3 evidence/run_evidence.py`

## Scenarios

Each file in `evidence/scenarios/` states its expected outcome on a `# expect:` line: whether the plan fits, which tasks the cheapest cut drops, or that no cut can fix it.

- Scenarios: 10
- Outcome matched the expectation: 10
- Mismatches: 0

## Control checks

1. **Two independent feasibility methods.** On 500 random plans the window condition and the earliest-deadline-first schedule agreed 500 times and disagreed 0 times (293 of the instances fit, 207 did not). The two methods share no code beyond the calendar, so agreement is a real check rather than a restatement.

2. **Optimality against exhaustive enumeration.** On 200 random plans (92 of them infeasible) the branch-and-bound cut matched the minimum-weight cut found by enumerating every subset in 200 cases.

3. **Invariance controls.** Two changes that cannot affect the answer: reordering the task list, and moving the whole plan forward by exactly one week. Over 200 random plans the verdict and the cut were unchanged in 200 reorderings and 200 week shifts.

4. **Determinism.** Each of the 10 scenarios was run twice through the command line; 10 produced byte-identical output.

## Timing

One full analysis (feasibility, certificate, cut search, deferral advice) per row:

| Plan shape | Tasks | Wall clock | Search nodes | Outcome | Proven minimal |
| --- | --- | --- | --- | --- | --- |
| overloaded by 20% | 10 | 0.002 s | 2 | cut 2 | yes |
| overloaded by 20% | 20 | 0.005 s | 10 | cut 3 | yes |
| overloaded by 20% | 40 | 0.035 s | 234 | cut 6 | yes |
| overloaded by 20% | 80 | 1.968 s | 10427 | cut 10 | yes |
| identical tasks, one deadline | 12 | 0.010 s | 299 | cut 4 | yes |
| identical tasks, one deadline | 20 | 7.323 s | 200000 | cut 12 | no |

The first rows use plans deliberately overloaded by 20% so that a cut is needed and the search runs; the last rows use the worst case for the search, many identical tasks sharing one deadline. Generators are seeded, so the numbers are reproducible on the same machine, and they describe these instances only. Where a plan exhausts the node budget the tool says so instead of claiming minimality.
