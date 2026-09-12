"""Tests for the unit model, the lexicon and name inference."""

from __future__ import annotations

import math
import unittest

from orbiter.units import (
    LEXICON,
    Quantity,
    Unit,
    conversion_hint,
    divide_quantity_by_constant,
    format_scale,
    lookup_label,
    matches,
    quantities_match,
    scale_quantity_by_constant,
    scales_compatible,
    split_identifier,
    unit_for_scale,
    unit_from_name,
)

MS = LEXICON["ms"]
SECONDS = LEXICON["seconds"]
BYTES = LEXICON["bytes"]
KIB = LEXICON["kib"]
KB = LEXICON["kb"]
PERCENT = LEXICON["pct"]
FRACTION = LEXICON["fraction"]
DEGREES = LEXICON["deg"]
RADIANS = LEXICON["rad"]


class SplitIdentifierTest(unittest.TestCase):
    def test_snake_case(self):
        self.assertEqual(split_identifier("read_timeout_ms"), ["read", "timeout", "ms"])

    def test_camel_case(self):
        self.assertEqual(split_identifier("readTimeoutMs"), ["read", "timeout", "ms"])

    def test_acronym_run(self):
        self.assertEqual(split_identifier("httpTimeoutMS"), ["http", "timeout", "ms"])

    def test_pascal_case_and_digits(self):
        self.assertEqual(split_identifier("Timeout2Ms"), ["timeout", "2", "ms"])

    def test_punctuation_and_dunder(self):
        self.assertEqual(split_identifier("__size.bytes__"), ["size", "bytes"])

    def test_empty(self):
        self.assertEqual(split_identifier(""), [])
        self.assertEqual(split_identifier("___"), [])


class UnitFromNameTest(unittest.TestCase):
    def test_suffix_match(self):
        self.assertEqual(unit_from_name("timeout_ms"), MS)
        self.assertEqual(unit_from_name("sizeBytes"), BYTES)
        self.assertEqual(unit_from_name("angle_deg"), DEGREES)

    def test_prefix_match_on_multi_token_name(self):
        self.assertEqual(unit_from_name("ms_timeout"), MS)
        self.assertEqual(unit_from_name("bytes_written"), BYTES)

    def test_suffix_only_rejects_leading_token(self):
        self.assertIsNone(unit_from_name("second_largest", suffix_only=True))
        self.assertEqual(unit_from_name("get_timeout_ms", suffix_only=True), MS)

    def test_unit_token_in_the_middle_is_not_used(self):
        self.assertIsNone(unit_from_name("timeout_ms_default"))

    def test_two_different_units_is_ambiguous(self):
        self.assertIsNone(unit_from_name("ms_to_seconds"))
        self.assertIsNone(unit_from_name("MS_PER_SECOND"))

    def test_same_unit_twice_is_not_ambiguous(self):
        self.assertEqual(unit_from_name("ms_timeout_ms"), MS)

    def test_no_unit_token(self):
        self.assertIsNone(unit_from_name("timeout"))
        self.assertIsNone(unit_from_name("params"))
        self.assertIsNone(unit_from_name("buffer_size"))

    def test_short_token_requires_suffix_position(self):
        self.assertEqual(unit_from_name("timeout_s"), SECONDS)
        self.assertIsNone(unit_from_name("s"))
        self.assertIsNone(unit_from_name("s_timeout"))

    def test_lone_unit_name(self):
        self.assertEqual(unit_from_name("seconds"), SECONDS)

    def test_ambiguous_tokens_absent_from_lexicon(self):
        for token in ("m", "min", "h", "d", "w", "nm", "bps"):
            self.assertNotIn(token, LEXICON, token)

    def test_custom_lexicon(self):
        custom = dict(LEXICON)
        custom["tmo"] = SECONDS
        self.assertEqual(unit_from_name("tmo", custom), SECONDS)
        self.assertIsNone(unit_from_name("tmo"))


class LookupLabelTest(unittest.TestCase):
    def test_known_labels(self):
        self.assertEqual(lookup_label("ms"), MS)
        self.assertEqual(lookup_label("milliseconds"), MS)
        self.assertEqual(lookup_label(" MS "), MS)

    def test_unknown_label(self):
        self.assertIsNone(lookup_label("parsecs"))
        self.assertIsNone(lookup_label("ms per second"))


class ScaleTest(unittest.TestCase):
    def test_scales_compatible_exact(self):
        self.assertTrue(scales_compatible("time", 1.0, 1.0))
        self.assertFalse(scales_compatible("time", 1.0, 1e-3))

    def test_binary_and_decimal_byte_prefixes_are_compatible_by_default(self):
        self.assertTrue(scales_compatible("data", 1000.0, 1024.0))
        self.assertTrue(scales_compatible("data", 1e6, float(2**20)))
        self.assertFalse(scales_compatible("data", 1000.0, 1024.0, strict_binary=True))

    def test_unrelated_data_scales_are_not_compatible(self):
        self.assertFalse(scales_compatible("data", 1.0, 1000.0))

    def test_unit_for_scale(self):
        self.assertEqual(unit_for_scale("time", 1e-3), MS)
        self.assertIsNone(unit_for_scale("time", 1.7e-4))

    def test_format_scale(self):
        self.assertEqual(format_scale(1000.0), "1000")
        self.assertEqual(format_scale(0.001), "0.001")


class QuantityTest(unittest.TestCase):
    def test_constant_multiplication_converts(self):
        quantity = scale_quantity_by_constant(Quantity(SECONDS), 1000.0)
        self.assertAlmostEqual(quantity.effective_scale, 1e-3)
        self.assertTrue(matches(quantity, MS))

    def test_constant_division_converts(self):
        quantity = divide_quantity_by_constant(Quantity(MS), 1000.0)
        self.assertAlmostEqual(quantity.effective_scale, 1.0)
        self.assertTrue(matches(quantity, SECONDS))

    def test_magnitude_factor_keeps_the_unit(self):
        doubled = scale_quantity_by_constant(Quantity(MS), 2.0)
        self.assertTrue(matches(doubled, MS))
        self.assertFalse(matches(doubled, SECONDS))

    def test_zero_factor_is_unknown(self):
        quantity = scale_quantity_by_constant(Quantity(MS), 0.0)
        self.assertTrue(quantity.unknown_factor)
        self.assertTrue(matches(quantity, SECONDS))

    def test_dimension_mismatch_is_never_accepted(self):
        unknown = Quantity(MS, unknown_factor=True)
        self.assertFalse(matches(unknown, BYTES))

    def test_quantities_match(self):
        self.assertTrue(quantities_match(Quantity(MS), Quantity(MS)))
        self.assertFalse(quantities_match(Quantity(MS), Quantity(SECONDS)))
        self.assertFalse(quantities_match(Quantity(MS), Quantity(BYTES)))

    def test_describe(self):
        self.assertEqual(Quantity(MS).describe(), "milliseconds")
        self.assertEqual(
            divide_quantity_by_constant(Quantity(MS), 1000.0).describe(), "seconds"
        )
        odd = divide_quantity_by_constant(Quantity(SECONDS), 7.0)
        self.assertEqual(odd.describe(), "a unit of 7 seconds")
        self.assertIn("unknown factor", Quantity(MS, unknown_factor=True).describe())

    def test_ratio_factor_is_not_forgiven(self):
        percent_scaled = Quantity(LEXICON["usd"], ratio_factor=0.01)
        self.assertFalse(matches(percent_scaled, LEXICON["usd"]))
        corrected = divide_quantity_by_constant(percent_scaled, 100.0)
        self.assertTrue(matches(corrected, LEXICON["usd"]))


class ConversionHintTest(unittest.TestCase):
    def test_hint_direction_ms_to_seconds(self):
        self.assertEqual(conversion_hint(Quantity(MS), SECONDS), "divide by 1000")

    def test_hint_direction_seconds_to_ms(self):
        self.assertEqual(conversion_hint(Quantity(SECONDS), MS), "multiply by 1000")

    def test_no_hint_when_scales_agree(self):
        self.assertEqual(conversion_hint(Quantity(MS), MS), "")

    def test_no_hint_across_dimensions(self):
        self.assertEqual(conversion_hint(Quantity(MS), BYTES), "")

    def test_percent_hint(self):
        self.assertEqual(conversion_hint(Quantity(FRACTION), PERCENT), "multiply by 100")

    def test_degree_hint_is_the_radian_factor(self):
        hint = conversion_hint(Quantity(DEGREES), RADIANS)
        self.assertTrue(hint.startswith("divide by"))
        self.assertAlmostEqual(float(hint.split()[-1]), 180 / math.pi, places=3)


class LexiconIntegrityTest(unittest.TestCase):
    def test_every_entry_is_a_unit_with_a_positive_scale(self):
        for token, unit in LEXICON.items():
            self.assertIsInstance(unit, Unit, token)
            self.assertGreater(unit.scale, 0.0, token)

    def test_base_unit_exists_for_every_dimension(self):
        dimensions = {unit.dimension for unit in LEXICON.values()}
        for dimension in dimensions:
            self.assertIsNotNone(unit_for_scale(dimension, 1.0), dimension)

    def test_scales_within_a_dimension_are_distinct_enough(self):
        # Two lexicon units of the same dimension must not collide under the
        # comparison tolerance, or a real mismatch would be silently accepted.
        by_dimension = {}
        for unit in LEXICON.values():
            by_dimension.setdefault(unit.dimension, set()).add((unit.label, unit.scale))
        for dimension, units in by_dimension.items():
            ordered = sorted(units, key=lambda item: item[1])
            for (left_label, left), (right_label, right) in zip(ordered, ordered[1:]):
                if left_label == right_label:
                    continue
                self.assertFalse(
                    math.isclose(left, right, rel_tol=1e-9),
                    f"{dimension}: {left_label} and {right_label} have equal scales",
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
