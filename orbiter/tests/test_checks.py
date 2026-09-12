"""Tests for the four checks, over real source files."""

from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from orbiter.analyze import Diagnostic, analyze_paths
from orbiter.config import Config, load_config


class CheckCase(unittest.TestCase):
    """Runs the analyzer over source written to a temporary directory."""

    def analyze(
        self,
        source: str,
        config: Optional[Config] = None,
        extra: Optional[Dict[str, str]] = None,
    ) -> List[Diagnostic]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "module.py").write_text(textwrap.dedent(source), encoding="utf-8")
            for name, text in (extra or {}).items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(textwrap.dedent(text), encoding="utf-8")
            diagnostics, errors = analyze_paths([root], config or load_config())
            self.assertEqual(errors, [], f"unexpected errors: {errors}")
            return diagnostics

    def codes(self, source: str, **kwargs) -> List[str]:
        return [diagnostic.code for diagnostic in self.analyze(source, **kwargs)]

    def assertClean(self, source: str, **kwargs) -> None:
        diagnostics = self.analyze(source, **kwargs)
        self.assertEqual(
            [str(diagnostic) for diagnostic in diagnostics], [], "expected no findings"
        )

    def assertCodes(self, source: str, expected: Sequence[str], **kwargs) -> None:
        self.assertEqual(self.codes(source, **kwargs), list(expected))


class ArgumentCheckTest(CheckCase):
    def test_milliseconds_passed_to_sleep(self):
        diagnostics = self.analyze(
            """
            import time

            def wait(timeout_ms):
                time.sleep(timeout_ms)
            """
        )
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, "ORB001")
        self.assertEqual(diagnostics[0].line, 5)
        self.assertIn("expects seconds", diagnostics[0].message)
        self.assertIn("divide by 1000", diagnostics[0].message)

    def test_explicit_conversion_is_accepted(self):
        self.assertClean(
            """
            import time

            def wait(timeout_ms):
                time.sleep(timeout_ms / 1000)
            """
        )

    def test_conversion_through_a_module_constant(self):
        self.assertClean(
            """
            import time

            MS_PER_SECOND = 1000

            def wait(timeout_ms):
                time.sleep(timeout_ms / MS_PER_SECOND)
            """
        )

    def test_magnitude_arithmetic_is_not_a_conversion(self):
        self.assertCodes(
            """
            import time

            def wait(timeout_ms):
                time.sleep(timeout_ms * 2)
            """,
            ["ORB001"],
        )

    def test_from_import_alias(self):
        self.assertCodes(
            """
            from time import sleep

            def wait(delay_ms):
                sleep(delay_ms)
            """,
            ["ORB001"],
        )

    def test_module_alias(self):
        self.assertCodes(
            """
            import time as clock

            def wait(delay_ms):
                clock.sleep(delay_ms)
            """,
            ["ORB001"],
        )

    def test_keyword_argument(self):
        self.assertCodes(
            """
            import subprocess

            def run(command, timeout_ms):
                return subprocess.run(command, timeout=timeout_ms)
            """,
            ["ORB001"],
        )

    def test_radians_expected_by_math(self):
        self.assertCodes(
            """
            import math

            def wave(angle_deg):
                return math.sin(angle_deg)
            """,
            ["ORB001"],
        )

    def test_degree_conversion_is_accepted(self):
        self.assertClean(
            """
            import math

            def wave(angle_deg):
                return math.sin(angle_deg * math.pi / 180)
            """
        )

    def test_radians_helper_is_accepted(self):
        self.assertClean(
            """
            import math

            def wave(angle_deg):
                return math.sin(math.radians(angle_deg))
            """
        )

    def test_math_degrees_expects_radians(self):
        self.assertCodes(
            """
            import math

            def show(angle_deg):
                return math.degrees(angle_deg)
            """,
            ["ORB001"],
        )

    def test_method_known_by_name(self):
        self.assertCodes(
            """
            def configure(sock, timeout_ms):
                sock.settimeout(timeout_ms)
            """,
            ["ORB001"],
        )

    def test_project_function_positional(self):
        self.assertCodes(
            """
            def schedule(delay_ms, label):
                return (delay_ms, label)

            def caller(wait_seconds):
                return schedule(wait_seconds, "x")
            """,
            ["ORB001"],
        )

    def test_project_function_keyword(self):
        self.assertCodes(
            """
            def schedule(delay_ms=0):
                return delay_ms

            def caller(wait_seconds):
                return schedule(delay_ms=wait_seconds)
            """,
            ["ORB001"],
        )

    def test_project_function_across_files(self):
        self.assertCodes(
            """
            from helper import schedule

            def caller(wait_seconds):
                return schedule(wait_seconds)
            """,
            ["ORB001"],
            extra={"helper.py": "def schedule(delay_ms):\n    return delay_ms\n"},
        )

    def test_method_call_skips_self_parameter(self):
        self.assertCodes(
            """
            class Client:
                def wait(self, timeout_ms):
                    return timeout_ms

            def caller(client, delay_seconds):
                client.wait(delay_seconds)
            """,
            ["ORB001"],
        )

    def test_ambiguous_definitions_are_not_resolved(self):
        self.assertClean(
            """
            def schedule(delay_ms):
                return delay_ms

            class Other:
                def schedule(self, delay_seconds):
                    return delay_seconds

            def caller(value_seconds):
                return schedule(value_seconds)
            """
        )

    def test_annotated_parameter_unit(self):
        self.assertCodes(
            """
            from typing import Annotated

            def schedule(delay: Annotated[float, "ms"]):
                return delay

            def caller(wait_seconds):
                return schedule(wait_seconds)
            """,
            ["ORB001"],
        )

    def test_starred_arguments_are_skipped(self):
        self.assertClean(
            """
            import time

            def wait(values_ms):
                time.sleep(*values_ms)
            """
        )

    def test_return_unit_of_a_project_function_reaches_the_call_site(self):
        self.assertCodes(
            """
            import time

            def get_timeout_ms():
                return 250

            def wait():
                time.sleep(get_timeout_ms())
            """,
            ["ORB001"],
        )

    def test_unknown_scaling_factor_suppresses_the_finding(self):
        self.assertClean(
            """
            import time

            def wait(timeout_ms, factor):
                time.sleep(timeout_ms / factor)
            """
        )

    def test_bytes_expected_by_bytearray(self):
        self.assertCodes(
            """
            def buffer(size_kb):
                return bytearray(size_kb)
            """,
            ["ORB001"],
        )

    def test_dimension_mismatch_message_names_both_dimensions(self):
        diagnostics = self.analyze(
            """
            import time

            def wait(size_bytes):
                time.sleep(size_bytes)
            """
        )
        self.assertEqual(len(diagnostics), 1)
        self.assertIn("(time)", diagnostics[0].message)
        self.assertIn("(data)", diagnostics[0].message)


class ArithmeticCheckTest(CheckCase):
    def test_addition_of_different_scales(self):
        diagnostics = self.analyze(
            """
            def total(elapsed_ms, budget_seconds):
                return elapsed_ms + budget_seconds
            """
        )
        self.assertEqual([d.code for d in diagnostics], ["ORB002"])
        self.assertIn("milliseconds added to seconds", diagnostics[0].message)

    def test_subtraction_of_different_dimensions(self):
        self.assertCodes(
            """
            def total(size_bytes, elapsed_ms):
                return size_bytes - elapsed_ms
            """,
            ["ORB002"],
        )

    def test_comparison(self):
        self.assertCodes(
            """
            def over(latency_ms, threshold_seconds):
                return latency_ms > threshold_seconds
            """,
            ["ORB002"],
        )

    def test_chained_comparison(self):
        self.assertCodes(
            """
            def within(low_ms, value_ms, high_seconds):
                return low_ms < value_ms < high_seconds
            """,
            ["ORB002"],
        )

    def test_augmented_assignment(self):
        self.assertCodes(
            """
            def accumulate(total_ms, step_seconds):
                total_ms += step_seconds
                return total_ms
            """,
            ["ORB002"],
        )

    def test_min_and_max_unify_arguments(self):
        self.assertCodes(
            """
            def clamp(timeout_ms, ceiling_seconds):
                return min(timeout_ms, ceiling_seconds)
            """,
            ["ORB002"],
        )

    def test_conditional_expression_branches(self):
        self.assertCodes(
            """
            def pick(flag, timeout_ms, fallback_seconds):
                return timeout_ms if flag else fallback_seconds
            """,
            ["ORB002"],
        )

    def test_same_unit_arithmetic_is_clean(self):
        self.assertClean(
            """
            def total(elapsed_ms, budget_ms):
                return elapsed_ms + budget_ms * 2
            """
        )

    def test_literal_operand_is_clean(self):
        self.assertClean(
            """
            def bump(elapsed_ms):
                return elapsed_ms + 5
            """
        )

    def test_converted_operand_is_clean(self):
        self.assertClean(
            """
            def total(elapsed_ms, budget_seconds):
                return elapsed_ms / 1000 + budget_seconds
            """
        )

    def test_modulo_keeps_the_unit(self):
        self.assertClean(
            """
            def remainder(elapsed_ms, other_ms):
                return elapsed_ms % 1000 + other_ms
            """
        )

    def test_ratio_multiplier_keeps_dimension(self):
        self.assertClean(
            """
            def scaled(size_bytes, compression_ratio, other_bytes):
                return size_bytes * compression_ratio + other_bytes
            """
        )


class AssignmentCheckTest(CheckCase):
    def test_assignment_scale_mismatch(self):
        diagnostics = self.analyze(
            """
            def convert(read_timeout_ms):
                timeout_seconds = read_timeout_ms
                return timeout_seconds
            """
        )
        self.assertEqual([d.code for d in diagnostics], ["ORB003"])
        self.assertIn("assignment to 'timeout_seconds'", diagnostics[0].message)

    def test_inverted_conversion_is_reported(self):
        diagnostics = self.analyze(
            """
            def convert(duration_seconds):
                duration_ms = duration_seconds / 1000
                return duration_ms
            """
        )
        self.assertEqual([d.code for d in diagnostics], ["ORB003"])
        self.assertIn("multiply by 1000000", diagnostics[0].message)

    def test_correct_conversion_is_clean(self):
        self.assertClean(
            """
            def convert(duration_seconds):
                duration_ms = duration_seconds * 1000
                return duration_ms
            """
        )

    def test_attribute_assignment(self):
        self.assertCodes(
            """
            class Client:
                def configure(self, delay_seconds):
                    self.timeout_ms = delay_seconds
            """,
            ["ORB003"],
        )

    def test_subscript_assignment_with_string_key(self):
        self.assertCodes(
            """
            def configure(config, delay_seconds):
                config["timeout_ms"] = delay_seconds
            """,
            ["ORB003"],
        )

    def test_annotated_target(self):
        self.assertCodes(
            """
            from typing import Annotated

            def convert(delay_seconds):
                value: Annotated[float, "ms"] = delay_seconds
                return value
            """,
            ["ORB003"],
        )

    def test_percentage_used_as_a_plain_multiplier(self):
        diagnostics = self.analyze(
            """
            def discounted(price_usd, discount_pct):
                total_usd = price_usd * discount_pct
                return total_usd
            """
        )
        self.assertEqual([d.code for d in diagnostics], ["ORB003"])
        self.assertIn("divide by 100", diagnostics[0].message)

    def test_percentage_with_division_is_clean(self):
        self.assertClean(
            """
            def discounted(price_usd, discount_pct):
                total_usd = price_usd * discount_pct / 100
                return total_usd
            """
        )

    def test_fraction_assigned_to_a_percent_name(self):
        self.assertCodes(
            """
            def usage(used_bytes, total_bytes):
                used_pct = used_bytes / total_bytes
                return used_pct
            """,
            ["ORB003"],
        )

    def test_fraction_scaled_to_percent_is_clean(self):
        self.assertClean(
            """
            def usage(used_bytes, total_bytes):
                used_pct = used_bytes / total_bytes * 100
                return used_pct
            """
        )

    def test_variable_unit_propagates_without_a_unit_name(self):
        self.assertCodes(
            """
            import time

            def wait(timeout_ms):
                value = timeout_ms
                time.sleep(value)
            """,
            ["ORB001"],
        )

    def test_for_loop_target_carries_its_name_unit(self):
        self.assertCodes(
            """
            import time

            def wait(values):
                for delay_ms in values:
                    time.sleep(delay_ms)
            """,
            ["ORB001"],
        )

    def test_with_statement_target(self):
        self.assertClean(
            """
            import time

            def wait(source):
                with source as handle:
                    time.sleep(handle)
            """
        )

    def test_tuple_unpacking_uses_target_names(self):
        self.assertCodes(
            """
            import time

            def wait(pair):
                first_ms, later_ms = pair
                time.sleep(first_ms)
            """,
            ["ORB001"],
        )

    def test_tuple_assignment_reports_each_element_once(self):
        self.assertCodes(
            """
            def convert(delay_seconds, other_seconds):
                first_ms, later_ms = delay_seconds, other_seconds
                return first_ms, later_ms
            """,
            ["ORB003", "ORB003"],
        )

    def test_file_size_attribute(self):
        self.assertCodes(
            """
            import os

            def check(path, limit_kb):
                return os.stat(path).st_size > limit_kb
            """,
            ["ORB002"],
            config=load_config(strict_binary_prefixes=True),
        )

    def test_comprehension_target(self):
        self.assertCodes(
            """
            def convert(values):
                return [value_ms + 1.5 for value_ms in values] + [total_seconds for total_seconds in values]
            """,
            [],
        )

    def test_comprehension_element_is_checked(self):
        self.assertCodes(
            """
            def convert(values, budget_seconds):
                return [value_ms + budget_seconds for value_ms in values]
            """,
            ["ORB002"],
        )

    def test_lambda_parameters(self):
        self.assertCodes(
            """
            import time

            handler = lambda delay_ms: time.sleep(delay_ms)
            """,
            ["ORB001"],
        )


class ReturnCheckTest(CheckCase):
    def test_return_unit_mismatch_from_function_name(self):
        diagnostics = self.analyze(
            """
            def get_timeout_ms(delay_seconds):
                return delay_seconds
            """
        )
        self.assertEqual([d.code for d in diagnostics], ["ORB004"])
        self.assertIn("returned value expects milliseconds", diagnostics[0].message)

    def test_return_annotation_unit(self):
        self.assertCodes(
            """
            from typing import Annotated

            def timeout(delay_seconds) -> Annotated[float, "ms"]:
                return delay_seconds
            """,
            ["ORB004"],
        )

    def test_correct_return_is_clean(self):
        self.assertClean(
            """
            def get_timeout_ms(delay_seconds):
                return delay_seconds * 1000
            """
        )

    def test_leading_unit_word_in_a_function_name_is_ignored(self):
        self.assertClean(
            """
            def second_largest(values_bytes):
                return sorted(values_bytes)[-2]
            """
        )

    def test_percent_named_function_does_not_type_its_return(self):
        self.assertClean(
            """
            def percent_of(price_usd, other_usd):
                return price_usd + other_usd
            """
        )


class BytePrefixTest(CheckCase):
    source = """
        def copy(size_kb, other_kib):
            return size_kb + other_kib
    """

    def test_decimal_and_binary_prefixes_compatible_by_default(self):
        self.assertClean(self.source)

    def test_strict_mode_reports_them(self):
        self.assertCodes(
            self.source, ["ORB002"], config=load_config(strict_binary_prefixes=True)
        )


class SuppressionTest(CheckCase):
    def test_bare_noqa(self):
        self.assertClean(
            """
            import time

            def wait(timeout_ms):
                time.sleep(timeout_ms)  # noqa
            """
        )

    def test_noqa_with_matching_code(self):
        self.assertClean(
            """
            import time

            def wait(timeout_ms):
                time.sleep(timeout_ms)  # noqa: ORB001
            """
        )

    def test_noqa_with_other_code_does_not_suppress(self):
        self.assertCodes(
            """
            import time

            def wait(timeout_ms):
                time.sleep(timeout_ms)  # noqa: ORB003
            """,
            ["ORB001"],
        )

    def test_orbiter_pragma(self):
        self.assertClean(
            """
            import time

            def wait(timeout_ms):
                time.sleep(timeout_ms)  # orbiter: ignore
            """
        )

    def test_orbiter_pragma_with_code(self):
        self.assertCodes(
            """
            import time

            def wait(timeout_ms):
                time.sleep(timeout_ms)  # orbiter: ignore ORB003
            """,
            ["ORB001"],
        )

    def test_mentioning_orbiter_in_prose_does_not_suppress(self):
        self.assertCodes(
            """
            import time

            def wait(timeout_ms):
                time.sleep(timeout_ms)  # orbiter finds this
            """,
            ["ORB001"],
        )

    def test_disabled_check(self):
        self.assertClean(
            """
            import time

            def wait(timeout_ms):
                time.sleep(timeout_ms)
            """,
            config=load_config(disable=frozenset({"ORB001"})),
        )


class RobustnessTest(CheckCase):
    def test_empty_module(self):
        self.assertClean("")

    def test_class_body_and_nested_functions(self):
        self.assertCodes(
            """
            import time

            class Runner:
                interval_ms = 500

                def start(self, budget_seconds):
                    def inner(delay_ms):
                        time.sleep(delay_ms / 1000)
                    inner(budget_seconds * 1000)
                    time.sleep(self.interval_ms)
            """,
            ["ORB001"],
        )

    def test_match_statement_is_walked(self):
        self.assertCodes(
            """
            import time

            def wait(kind, timeout_ms):
                match kind:
                    case "fast":
                        time.sleep(timeout_ms)
                    case _:
                        pass
            """,
            ["ORB001"],
        )

    def test_decorators_and_defaults_are_walked(self):
        self.assertCodes(
            """
            import time

            def register(value):
                return value

            @register(1)
            def wait(timeout_ms=5, other=time.sleep(5)):
                return timeout_ms
            """,
            [],
        )

    def test_async_function(self):
        self.assertCodes(
            """
            import asyncio

            async def wait(timeout_ms):
                await asyncio.sleep(timeout_ms)
            """,
            ["ORB001"],
        )

    def test_try_and_while_bodies(self):
        self.assertCodes(
            """
            import time

            def wait(timeout_ms):
                while True:
                    try:
                        time.sleep(timeout_ms)
                    except OSError:
                        time.sleep(timeout_ms)
                    finally:
                        time.sleep(timeout_ms)
            """,
            ["ORB001", "ORB001", "ORB001"],
        )

    def test_walrus_and_fstrings_do_not_crash(self):
        self.assertCodes(
            """
            import time

            def wait(values):
                if (delay_ms := values[0]) > 0:
                    time.sleep(delay_ms)
                return f"waited {delay_ms}"
            """,
            ["ORB001"],
        )

    def test_deeply_nested_expression(self):
        self.assertCodes(
            """
            import time

            def wait(timeout_ms):
                time.sleep(((timeout_ms)))
            """,
            ["ORB001"],
        )

    def test_findings_are_sorted_by_position(self):
        diagnostics = self.analyze(
            """
            import time

            def wait(timeout_ms, other_ms):
                time.sleep(other_ms)
                time.sleep(timeout_ms)
            """
        )
        self.assertEqual([d.line for d in diagnostics], [5, 6])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
