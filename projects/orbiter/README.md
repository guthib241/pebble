# orbiter

Flags Python code that mixes units, like milliseconds passed as seconds.

**Closest prior art:** [Phys](https://github.com/unl-nimbus-lab/phys) and
[Phriky-Units](https://github.com/unl-nimbus-lab/phriky-units), which detect physical
unit inconsistencies in ROS C++ without annotations.
**Difference:** orbiter analyses Python source, uses a software-engineering unit
vocabulary (time, byte sizes, angles, percentages, frequency, length, single-currency
money) rather than SI robotics units, and reads explicit conversions in the code, so
`time.sleep(timeout_ms / 1000)` is accepted where `time.sleep(timeout_ms)` is
reported. The Python options found in the search either require values to be wrapped
in runtime unit objects (pint, numericalunits, astropy.units) or require distinct
declared types everywhere (mypy with `NewType`); orbiter needs no change to the code
under analysis.
**Search confidence:** Medium.
**Scope:** This assessment reflects the sources and queries documented in
[`NOVELTY_REPORT.md`](NOVELTY_REPORT.md). It states that no materially equivalent
Python tool was found in that search, not that none exists.

## Status

Working and tested. The four checks below are implemented, 151 tests pass, and the
numbers in [Validation](#validation) come from a script in this repository that
reproduces them. Requires Python 3.11 or newer and has no dependencies outside the
standard library.

## Install and run

This project lives inside the `pebble` repository at `projects/orbiter/`. Start from a
checkout:

```sh
git clone https://github.com/guthib241/pebble
cd pebble/projects/orbiter
```


No installation is needed to try it:

```sh
python3 -m orbiter path/to/your/code
```

To install the `orbiter` command:

```sh
python3 -m pip install .
orbiter path/to/your/code
```

Options:

```
--format {text,json}        output format (default: text)
--disable CODE              turn off one check, repeatable
--strict-binary-prefixes    also report kilobyte/kibibyte style mismatches
--config PATH               TOML configuration file
--list-units                print the unit lexicon and the check list
```

Exit status is 0 when nothing is found, 1 when there are findings, and 2 when a file
could not be read or parsed or the configuration is invalid.

Example, against the fixture project in this repository:

```
$ python3 -m orbiter tests/fixtures/sample_project
tests/fixtures/sample_project/scheduler.py:10:5: ORB004 returned value expects seconds, got milliseconds (divide by 1000)
tests/fixtures/sample_project/scheduler.py:15:16: ORB001 argument 1 of time.sleep() expects seconds, got milliseconds (divide by 1000)
tests/fixtures/sample_project/scheduler.py:25:12: ORB002 seconds subtracted from milliseconds
tests/fixtures/sample_project/transfer.py:6:16: ORB003 assignment to 'used_pct' expects percent, got fraction (multiply by 100)
tests/fixtures/sample_project/transfer.py:18:22: ORB001 argument 1 of bytearray() expects bytes, got megabytes (multiply by 1000000)
```

## The checks

| Code | Reports |
| --- | --- |
| ORB001 | A call argument whose unit does not match the parameter's unit |
| ORB002 | Addition, subtraction, comparison, `min`/`max` or a conditional mixing units |
| ORB003 | An assignment whose value does not match the target name's unit |
| ORB004 | A returned value that does not match the function's declared unit |

## How units are inferred

Three sources, in this order of authority:

1. **`typing.Annotated` metadata.** `def wait(delay: Annotated[float, "ms"])` declares
   milliseconds explicitly. No runtime dependency, no wrapper types.
2. **A table of standard-library call conventions.** `time.sleep` and `asyncio.sleep`
   take seconds, `time.monotonic_ns` returns nanoseconds, `math.sin` takes radians,
   `select.poll.poll` takes milliseconds, `os.stat().st_size` is bytes, and
   `requests`' `timeout` is seconds. Import aliases are followed, so
   `from time import sleep as nap` still resolves.
3. **Identifier names.** A unit token is read from the last token of a name, or from
   the first token of a multi-token name: `timeout_ms`, `readTimeoutMS`,
   `size_bytes`, `ms_timeout`, `config["timeout_ms"]`, `self.interval_ms`.

Functions defined in the files under analysis are indexed, so their parameter and
return units are known at call sites, including across files. When several functions
share a name, a parameter's unit is used only if every definition agrees.

Run `python3 -m orbiter --list-units` for the full lexicon. It covers time, byte
sizes, angles, ratios and percentages, frequency, length, and single-currency money.

## Conversions are read, not guessed

A unit is a dimension plus a scale, so conversions written in the code are followed:

```python
time.sleep(timeout_ms / 1000)            # accepted: the value is in seconds
time.sleep(timeout_ms / MS_PER_SECOND)   # accepted: the constant's name gives 1000
math.sin(angle_deg * math.pi / 180)      # accepted: the value is in radians
retry_delay_ms = base_delay_ms * 2       # accepted: 2 is not a conversion factor
time.sleep(timeout_ms * 1000)            # reported: wrong direction
duration_ms = duration_seconds / 1000    # reported: multiply by 1000000 to fix
```

A constant factor is treated as a conversion only when the result lands on a unit that
exists in the lexicon; otherwise it is read as ordinary magnitude arithmetic. That is
why doubling a delay keeps its unit while dividing by 1000 changes it.

Percentages carry their scale, so a percentage used as a plain multiplier is reported:

```python
total_usd = price_usd * discount_pct        # reported: divide by 100
total_usd = price_usd * discount_pct / 100  # accepted
used_pct = sent_bytes / total_bytes         # reported: multiply by 100
```

## Precision rules

The checker stays quiet rather than guessing:

- Both sides must have a known unit. Nothing is inferred from a name without a unit
  token.
- A value scaled by something whose value is not known (`timeout_ms / factor`) is not
  judged on scale, only on dimension.
- A name containing two different unit tokens (`ms_to_seconds`) is treated as unknown.
- A name containing a `per` token is a rate or a conversion factor, not a quantity:
  `bytes_per_second` is left alone, and an upper-case `MS_PER_SECOND` is read as the
  number 1000.
- Singular calendar words (`second`, `minute`, `hour`, `day`, `week`) and singular
  `bit` are not in the lexicon, because in real code they name an index more often than
  a duration or a size. `day_1` and `week1monday` are positions, not durations. Plural
  and abbreviated forms (`seconds`, `ms`, `hrs`, `days`, `bits`) are used. Short or
  overloaded tokens (`m`, `min`, `h`, `mm`, `nm`, `bps`) are left out for the same
  reason.
- A function name contributes a return unit only from its last token, since a leading
  unit word is usually a modifier: `second_largest` is not seconds.
- Kilobyte and kibibyte are treated as compatible by default, because code uses "KB"
  for 1024 bytes routinely. `--strict-binary-prefixes` reports those mismatches too.

Suppress a finding with `# noqa`, `# noqa: ORB001`, `# orbiter: ignore`, or
`# orbiter: ignore ORB001`.

## Limitations

- Rates are not modelled. Dividing one dimension by another (bytes per second, degrees
  per second) yields no unit, so mistakes in rate handling are not reported.
- Temperature is excluded on purpose: Celsius and Fahrenheit conversions are affine,
  not a single multiplication, and the model only handles multiplicative scales.
- Money is treated as one currency with a major and a minor unit. Cross-currency
  mistakes are not detectable, since exchange rates are not constants.
- Analysis is intra-procedural for local variables and flow-insensitive within a
  function. A variable assigned different units on different branches keeps the unit
  its name implies, or the last one inferred.
- Calls are resolved by name, not by type. A method call resolves through the indexed
  definitions or the built-in table, so a third-party function sharing a name with a
  local one can be resolved to the local signature.
- Findings depend on identifier names. Code that names no units gets no findings, which
  the null control below demonstrates.

## Configuration

An optional TOML file extends the vocabulary:

```toml
[orbiter]
disable = ["ORB002"]
strict_binary_prefixes = false

[orbiter.aliases]
tmo = "ms"            # this codebase writes tmo for a millisecond timeout

[orbiter.functions."mylib.pause"]
params = { 0 = "seconds", timeout = "seconds" }
returns = "ms"
```

Pass it with `--config orbiter.toml`.

## Validation

Test suite (151 tests, standard library `unittest`, no plugins):

```sh
python3 -m unittest discover -s tests -t .
```

It covers name inference and the lexicon, the scale algebra, each check with paired
correct and incorrect inputs, suppression, configuration errors, file discovery,
syntax errors, non-UTF-8 files, missing paths, an end-to-end run over the fixture
project, a self-analysis run (orbiter's own source produces no findings), and an
install check that builds this package into a fresh virtualenv and runs the installed
`orbiter` command.

Measured results, all produced by one script:

```sh
python3 evidence/run_evidence.py > evidence/results.md
```

| Measurement | Result |
| --- | --- |
| Seeded mistakes in `evidence/benchmark/` (6 files) | 19 |
| Seeded mistakes reported | 19 |
| Findings on lines with no seeded mistake | 0 |
| Documented known misses that stayed missed | 2 of 2 |
| Findings on `/usr/lib/python3.11` (669 files) | 0 |
| Findings on `/usr/lib/python3/dist-packages` (1079 files) | 0 |
| Wall clock, 669-file corpus | 9.8 s |
| Wall clock, 1079-file corpus | 12.5 s |

Environment for those timings: CPython 3.11.15 on Linux 6.18.44 x86-64. The full run
record, including the commit analysed, is in
[`evidence/results.md`](evidence/results.md).

Three control checks run in the same script:

1. **Null control.** The benchmark files with every unit token in every identifier
   replaced by a neutral word, nothing else changed: 0 findings. Findings come from
   unit evidence in names, not from code shape.
2. **Determinism control.** Two consecutive runs over the benchmark produce identical
   output.
3. **Paired-variant control.** Every seeded mistake in the benchmark sits beside a
   corrected twin function that differs only in the conversion. All 19 findings land on
   the seeded lines and none on the twins.

The benchmark was written by the same author as the checker, which limits what the
19-of-19 figure establishes: it shows the checks fire on the patterns they target and
stay silent on their corrected forms, not a detection rate on defects found in the
wild. The two corpus runs measure how often the checker speaks up on ordinary code;
they do not establish how many real unit defects those corpora contain. An earlier run
of the same corpora reported 9 findings, all false positives from ambiguous lexicon
entries; those entries were removed and the reasoning is recorded in
`orbiter/units.py` and in the precision rules above.

## License

See [`LICENSE.txt`](LICENSE.txt). This repository's owner has chosen a single custom
license for everything built here, which permits non-commercial use with attribution
and requires contact for commercial use.
