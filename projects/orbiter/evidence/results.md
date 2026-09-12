# orbiter evidence run

- Date (UTC): 2026-09-12 03:34:55
- Commit: 9c8af15
- Python: 3.11.15 (CPython)
- Platform: Linux-6.18.44-fc-v24-x86_64-with-glibc2.39
- Command: `python3 evidence/run_evidence.py`

## Seeded-bug benchmark

Corpus: `evidence/benchmark/`, 6 files.
Each seeded mistake carries an inline `# expect: CODE` marker on its line,
and each is paired with a corrected twin function that must stay clean.

- Seeded mistakes: 19
- Detected: 19
- Missed: 0
- Findings on lines with no marker: 0
- Documented known misses that stayed missed: 2 of 2
- Wall clock: 0.007 s


## Control checks

1. Null control: the same 6 benchmark files with every unit token in
   every identifier replaced by a neutral word, nothing else changed.
   Findings: 0 (expected 0, since the unit evidence is gone).

2. Determinism control: two consecutive runs over the benchmark produced
   identical output: True (19 findings each).

3. Paired-variant control: every seeded mistake in the benchmark has a
   corrected twin differing only in the conversion. Correct twins produce
   no findings, which is what "19 findings, all on marked lines"
   above establishes.

## Real-corpus runs

| Corpus | Files | Findings | Unreadable files | Wall clock |
| --- | --- | --- | --- | --- |
| `/usr/lib/python3.11` | 669 | 0 | 0 | 10.4 s |
| `/usr/lib/python3/dist-packages` | 1079 | 0 | 0 | 12.8 s |

These corpora were not written with orbiter in mind, so the finding counts
measure how often the checker speaks up on ordinary code. They say nothing
about how many real unit defects those corpora contain.
