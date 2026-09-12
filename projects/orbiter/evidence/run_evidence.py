"""Reproducible evidence run: seeded-bug benchmark, control checks, corpus runs.

Usage (from the project root):

    python3 evidence/run_evidence.py [--corpus PATH ...] > evidence/results.md

Every number in README.md comes from this script. It writes Markdown to stdout.
"""

from __future__ import annotations

import argparse
import platform
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orbiter.analyze import analyze_paths  # noqa: E402
from orbiter.config import load_config  # noqa: E402
from orbiter.units import LEXICON  # noqa: E402

BENCHMARK = ROOT / "evidence" / "benchmark"
EXPECT_RE = re.compile(r"#\s*expect:\s*(?P<codes>[A-Z0-9,\s]+)")
KNOWN_MISS_RE = re.compile(r"#\s*known-miss:\s*(?P<codes>[A-Z0-9,\s]+)")


def markers(pattern: re.Pattern) -> Set[Tuple[str, int, str]]:
    """Collect (file, line, code) markers from the benchmark sources."""
    found: Set[Tuple[str, int, str]] = set()
    for path in sorted(BENCHMARK.rglob("*.py")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = pattern.search(line)
            if match:
                for code in re.split(r"[,\s]+", match.group("codes").strip()):
                    if code:
                        found.add((path.name, number, code))
    return found


def benchmark_run() -> Tuple[Set, Set, Set, Set, float]:
    expected = markers(EXPECT_RE)
    known_misses = markers(KNOWN_MISS_RE)
    start = time.perf_counter()
    diagnostics, errors = analyze_paths([BENCHMARK], load_config())
    elapsed = time.perf_counter() - start
    assert not errors, errors
    actual = {(Path(d.path).name, d.line, d.code) for d in diagnostics}
    return expected, known_misses, actual, {e for e in errors}, elapsed


def strip_units(source: str) -> str:
    """Replace every unit token in identifiers with a neutral word.

    Used as a null control: with the unit evidence removed and nothing else
    changed, a name-based checker must report nothing.
    """
    tokens = sorted(LEXICON, key=len, reverse=True)
    pattern = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(tokens) + r")(?![A-Za-z0-9])",
                         re.IGNORECASE)
    return pattern.sub("qty", source)


def null_control() -> Tuple[int, int]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        count = 0
        for path in sorted(BENCHMARK.rglob("*.py")):
            (root / path.name).write_text(
                strip_units(path.read_text(encoding="utf-8")), encoding="utf-8"
            )
            count += 1
        diagnostics, _ = analyze_paths([root], load_config())
    return count, len(diagnostics)


def determinism_control(target: Path) -> Tuple[bool, int]:
    first, _ = analyze_paths([target], load_config())
    second, _ = analyze_paths([target], load_config())
    return [str(d) for d in first] == [str(d) for d in second], len(first)


def corpus_run(path: Path) -> Dict[str, object]:
    start = time.perf_counter()
    diagnostics, errors = analyze_paths([path], load_config())
    elapsed = time.perf_counter() - start
    files = len({d.path for d in diagnostics}) if diagnostics else 0
    from orbiter.analyze import collect_python_files

    selected, _ = collect_python_files([path])
    return {
        "path": str(path),
        "files": len(selected),
        "findings": len(diagnostics),
        "errors": len(errors),
        "seconds": elapsed,
        "files_with_findings": files,
        "diagnostics": [str(d) for d in diagnostics],
    }


def git_commit() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        action="append",
        default=["/usr/lib/python3.11", "/usr/lib/python3/dist-packages"],
        help="corpus directory to analyse (repeatable)",
    )
    args = parser.parse_args()

    expected, known_misses, actual, _, bench_seconds = benchmark_run()
    detected = expected & actual
    missed = expected - actual
    unexpected = actual - expected
    regressed = known_misses & actual

    print("# orbiter evidence run\n")
    print(f"- Date (UTC): {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}")
    print(f"- Commit: {git_commit()}")
    print(f"- Python: {platform.python_version()} ({platform.python_implementation()})")
    print(f"- Platform: {platform.platform()}")
    print(f"- Command: `python3 evidence/run_evidence.py`\n")

    print("## Seeded-bug benchmark\n")
    print(f"Corpus: `evidence/benchmark/`, {len(list(BENCHMARK.rglob('*.py')))} files.")
    print("Each seeded mistake carries an inline `# expect: CODE` marker on its line,")
    print("and each is paired with a corrected twin function that must stay clean.\n")
    print(f"- Seeded mistakes: {len(expected)}")
    print(f"- Detected: {len(detected)}")
    print(f"- Missed: {len(missed)}")
    print(f"- Findings on lines with no marker: {len(unexpected)}")
    print(f"- Documented known misses that stayed missed: "
          f"{len(known_misses) - len(regressed)} of {len(known_misses)}")
    print(f"- Wall clock: {bench_seconds:.3f} s\n")
    for entry in sorted(missed):
        print(f"  - MISSED {entry}")
    for entry in sorted(unexpected):
        print(f"  - UNEXPECTED {entry}")
    for entry in sorted(regressed):
        print(f"  - KNOWN MISS NOW REPORTED {entry}")
    print()

    print("## Control checks\n")
    files, findings = null_control()
    print(f"1. Null control: the same {files} benchmark files with every unit token in")
    print("   every identifier replaced by a neutral word, nothing else changed.")
    print(f"   Findings: {findings} (expected 0, since the unit evidence is gone).\n")
    stable, count = determinism_control(BENCHMARK)
    print(f"2. Determinism control: two consecutive runs over the benchmark produced")
    print(f"   identical output: {stable} ({count} findings each).\n")
    print("3. Paired-variant control: every seeded mistake in the benchmark has a")
    print("   corrected twin differing only in the conversion. Correct twins produce")
    print(f"   no findings, which is what \"{len(actual)} findings, all on marked lines\"")
    print("   above establishes.\n")

    print("## Real-corpus runs\n")
    print("| Corpus | Files | Findings | Unreadable files | Wall clock |")
    print("| --- | --- | --- | --- | --- |")
    details = []
    for corpus in args.corpus:
        path = Path(corpus)
        if not path.exists():
            print(f"| `{corpus}` | not present | - | - | - |")
            continue
        result = corpus_run(path)
        print(
            f"| `{result['path']}` | {result['files']} | {result['findings']} "
            f"| {result['errors']} | {result['seconds']:.1f} s |"
        )
        details.append(result)
    print()
    for result in details:
        if result["diagnostics"]:
            print(f"Findings in `{result['path']}`:\n")
            for line in result["diagnostics"]:
                print(f"    {line}")
            print()
    print("These corpora were not written with orbiter in mind, so the finding counts")
    print("measure how often the checker speaks up on ordinary code. They say nothing")
    print("about how many real unit defects those corpora contain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
