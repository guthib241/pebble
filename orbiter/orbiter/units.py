"""Unit vocabulary and inference of units from identifier names.

A unit is a dimension plus a numeric ``scale`` relative to that dimension's base
unit. ``scale`` is the multiplier that converts a numeric value in this unit to the
base unit: a value in milliseconds times ``0.001`` is a value in seconds.

Only dimensions whose conversions are a single multiplication are modelled.
Temperature (Celsius, Fahrenheit) is deliberately excluded because those
conversions are affine, not multiplicative.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, replace
from typing import Dict, List, Optional, Tuple

# Relative tolerance used when comparing scales. Scales are stored as floats, so
# comparisons are made with a tolerance rather than exact equality.
REL_TOL = 1e-9

TIME = "time"
DATA = "data"
ANGLE = "angle"
RATIO = "ratio"
FREQUENCY = "frequency"
LENGTH = "length"
MONEY = "money"

BASE_UNIT_NAME = {
    TIME: "seconds",
    DATA: "bytes",
    ANGLE: "radians",
    RATIO: "fraction",
    FREQUENCY: "hertz",
    LENGTH: "meters",
    MONEY: "major currency units",
}


@dataclass(frozen=True)
class Unit:
    """A unit: a dimension, a scale relative to the dimension's base unit."""

    dimension: str
    scale: float
    label: str
    # Byte-size prefix level (1=kilo, 2=mega, 3=giga, 4=tera); 0 for everything else.
    prefix_level: int = 0
    # True for binary byte prefixes (KiB, MiB, ...).
    binary_prefix: bool = False

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.label


@dataclass(frozen=True)
class Scalar:
    """A dimensionless value. ``value`` is set when it is a known constant."""

    value: Optional[float] = None


@dataclass(frozen=True)
class Quantity:
    """An inferred quantity.

    ``base`` is the unit implied by a name, annotation or known signature.
    ``literal_factor`` accumulates multiplication or division by *constant*
    numbers, which in real code is how unit conversions are written.
    ``ratio_factor`` accumulates multiplication by ratio-dimension quantities
    (such as a percentage), which changes the scale of the result.
    ``unknown_factor`` records that the expression was scaled by something whose
    value is not known, in which case no conclusion is drawn about scale.
    """

    base: Unit
    literal_factor: float = 1.0
    ratio_factor: float = 1.0
    unknown_factor: bool = False

    @property
    def dimension(self) -> str:
        return self.base.dimension

    @property
    def effective_scale(self) -> float:
        """Scale of the expression, reading constant factors as conversions."""
        return self.base.scale * self.literal_factor * self.ratio_factor

    @property
    def lenient_scale(self) -> float:
        """Scale ignoring constant factors, reading them as magnitude changes."""
        return self.base.scale * self.ratio_factor

    @property
    def converted(self) -> bool:
        return self.literal_factor != 1.0

    def describe(self) -> str:
        """Human-readable description of the inferred unit."""
        if self.unknown_factor:
            return f"{self.base.label} scaled by an unknown factor"
        if not self.converted and self.ratio_factor == 1.0:
            return self.base.label
        eff = self.effective_scale
        named = unit_for_scale(self.dimension, eff)
        if named is not None:
            return named.label
        return f"a unit of {format_scale(eff)} {BASE_UNIT_NAME[self.dimension]}"


def format_scale(scale: float) -> str:
    """Format a scale factor compactly."""
    if scale == int(scale) and abs(scale) < 1e15:
        return str(int(scale))
    return f"{scale:g}"


def _u(
    dimension: str,
    scale: float,
    label: str,
    prefix_level: int = 0,
    binary_prefix: bool = False,
) -> Unit:
    return Unit(dimension, scale, label, prefix_level, binary_prefix)


_SECOND = _u(TIME, 1.0, "seconds")
_MS = _u(TIME, 1e-3, "milliseconds")
_US = _u(TIME, 1e-6, "microseconds")
_NS = _u(TIME, 1e-9, "nanoseconds")
_MINUTE = _u(TIME, 60.0, "minutes")
_HOUR = _u(TIME, 3600.0, "hours")
_DAY = _u(TIME, 86400.0, "days")
_WEEK = _u(TIME, 604800.0, "weeks")

_BIT = _u(DATA, 0.125, "bits")
_BYTE = _u(DATA, 1.0, "bytes")
_KB = _u(DATA, 1e3, "kilobytes", 1, False)
_KIB = _u(DATA, 1024.0, "kibibytes", 1, True)
_MB = _u(DATA, 1e6, "megabytes", 2, False)
_MIB = _u(DATA, float(2**20), "mebibytes", 2, True)
_GB = _u(DATA, 1e9, "gigabytes", 3, False)
_GIB = _u(DATA, float(2**30), "gibibytes", 3, True)
_TB = _u(DATA, 1e12, "terabytes", 4, False)
_TIB = _u(DATA, float(2**40), "tebibytes", 4, True)

_RADIAN = _u(ANGLE, 1.0, "radians")
_DEGREE = _u(ANGLE, math.pi / 180.0, "degrees")

_FRACTION = _u(RATIO, 1.0, "fraction")
_PERCENT = _u(RATIO, 0.01, "percent")
_PERMILLE = _u(RATIO, 1e-3, "permille")

_HERTZ = _u(FREQUENCY, 1.0, "hertz")
_KHZ = _u(FREQUENCY, 1e3, "kilohertz")
_MHZ = _u(FREQUENCY, 1e6, "megahertz")
_GHZ = _u(FREQUENCY, 1e9, "gigahertz")
_RPM = _u(FREQUENCY, 1.0 / 60.0, "revolutions per minute")

_METER = _u(LENGTH, 1.0, "meters")
_KM = _u(LENGTH, 1e3, "kilometers")
_CM = _u(LENGTH, 1e-2, "centimeters")
_MM = _u(LENGTH, 1e-3, "millimeters")
_MILE = _u(LENGTH, 1609.344, "miles")
_FOOT = _u(LENGTH, 0.3048, "feet")
_INCH = _u(LENGTH, 0.0254, "inches")
_YARD = _u(LENGTH, 0.9144, "yards")

_CENT = _u(MONEY, 0.01, "cents")
_MAJOR = _u(MONEY, 1.0, "dollars")

#: Identifier tokens that name a unit. Tokens are matched whole, after splitting an
#: identifier on underscores and camel-case boundaries, so ``params`` never matches
#: the ``ms`` entry.
#:
#: Deliberately absent because they are ambiguous in real code: ``m`` (metre or
#: minute), ``min`` (minute or minimum), ``h``/``d``/``w`` (single letters),
#: ``us`` is kept but ``nm`` (nanometre or nautical mile) and ``bps`` (bits per
#: second or basis points) are not.
LEXICON: Dict[str, Unit] = {
    # time
    "ns": _NS, "nsec": _NS, "nsecs": _NS, "nanos": _NS,
    "nanosecond": _NS, "nanoseconds": _NS,
    "us": _US, "usec": _US, "usecs": _US, "micros": _US,
    "microsecond": _US, "microseconds": _US,
    "ms": _MS, "msec": _MS, "msecs": _MS, "millis": _MS,
    "millisecond": _MS, "milliseconds": _MS,
    "s": _SECOND, "sec": _SECOND, "secs": _SECOND,
    "second": _SECOND, "seconds": _SECOND,
    "minutes": _MINUTE, "mins": _MINUTE, "minute": _MINUTE,
    "hours": _HOUR, "hrs": _HOUR, "hour": _HOUR,
    "days": _DAY, "day": _DAY,
    "weeks": _WEEK, "week": _WEEK,
    # data size
    "bit": _BIT, "bits": _BIT,
    "byte": _BYTE, "bytes": _BYTE,
    "kb": _KB, "kbytes": _KB, "kilobyte": _KB, "kilobytes": _KB,
    "kib": _KIB, "kibibytes": _KIB,
    "mb": _MB, "mbytes": _MB, "megabyte": _MB, "megabytes": _MB,
    "mib": _MIB, "mebibytes": _MIB,
    "gb": _GB, "gbytes": _GB, "gigabyte": _GB, "gigabytes": _GB,
    "gib": _GIB, "gibibytes": _GIB,
    "tb": _TB, "terabyte": _TB, "terabytes": _TB,
    "tib": _TIB, "tebibytes": _TIB,
    # angle
    "rad": _RADIAN, "rads": _RADIAN, "radian": _RADIAN, "radians": _RADIAN,
    "deg": _DEGREE, "degs": _DEGREE, "degree": _DEGREE, "degrees": _DEGREE,
    # ratio
    "fraction": _FRACTION, "ratio": _FRACTION,
    "pct": _PERCENT, "percent": _PERCENT, "percentage": _PERCENT,
    "permille": _PERMILLE,
    # frequency
    "hz": _HERTZ, "hertz": _HERTZ,
    "khz": _KHZ, "mhz": _MHZ, "ghz": _GHZ, "rpm": _RPM,
    # length
    "meter": _METER, "meters": _METER, "metre": _METER, "metres": _METER,
    "km": _KM, "kilometers": _KM, "kilometres": _KM,
    "cm": _CM, "centimeters": _CM, "centimetres": _CM,
    "mm": _MM, "millimeters": _MM, "millimetres": _MM,
    "mile": _MILE, "miles": _MILE,
    "foot": _FOOT, "feet": _FOOT,
    "inch": _INCH, "inches": _INCH,
    "yard": _YARD, "yards": _YARD,
    # money, single currency
    "cent": _CENT, "cents": _CENT,
    "dollar": _MAJOR, "dollars": _MAJOR, "usd": _MAJOR,
}

#: Tokens that are only trusted as the final token of a multi-token identifier,
#: because on their own they are too short to be a reliable signal.
SHORT_TOKENS = frozenset({"s"})

#: Byte-size ratios between a decimal prefix and the binary prefix at the same
#: level. Code uses "KB" for 1024 bytes routinely, so these are treated as
#: compatible unless strict checking is requested.
_BINARY_DECIMAL_RATIOS = (1.024, 1.048576, 1.073741824, 1.099511627776)

_TOKEN_RE = re.compile(r"[A-Z]+(?![a-z])|[A-Z][a-z0-9]*|[a-z0-9]+")


def split_identifier(name: str) -> List[str]:
    """Split an identifier into lowercase word tokens.

    >>> split_identifier("read_timeout_ms")
    ['read', 'timeout', 'ms']
    >>> split_identifier("httpTimeoutMS")
    ['http', 'timeout', 'ms']
    """
    tokens: List[str] = []
    for chunk in re.split(r"[^0-9A-Za-z]+", name):
        if not chunk:
            continue
        tokens.extend(match.group(0).lower() for match in _TOKEN_RE.finditer(chunk))
    return tokens


def scales_compatible(
    dimension: str, left: float, right: float, strict_binary: bool = False
) -> bool:
    """Whether two scales of the same dimension should be treated as equal."""
    if math.isclose(left, right, rel_tol=REL_TOL):
        return True
    if dimension == DATA and not strict_binary:
        if left == 0 or right == 0:
            return False
        ratio = max(left, right) / min(left, right)
        return any(
            math.isclose(ratio, candidate, rel_tol=1e-9)
            for candidate in _BINARY_DECIMAL_RATIOS
        )
    return False


def unit_for_scale(dimension: str, scale: float) -> Optional[Unit]:
    """The lexicon unit matching ``scale`` in ``dimension``, if there is one."""
    best: Optional[Unit] = None
    for unit in LEXICON.values():
        if unit.dimension != dimension:
            continue
        if math.isclose(unit.scale, scale, rel_tol=REL_TOL):
            if best is None or len(unit.label) < len(best.label):
                best = unit
    return best


def lookup_label(label: str, lexicon: Optional[Dict[str, Unit]] = None) -> Optional[Unit]:
    """Look up a unit by an explicit label, as used in annotations and config."""
    table = LEXICON if lexicon is None else lexicon
    key = label.strip().lower()
    unit = table.get(key)
    if unit is not None:
        return unit
    tokens = split_identifier(key)
    if len(tokens) == 1:
        return table.get(tokens[0])
    return None


def unit_from_name(
    name: str,
    lexicon: Optional[Dict[str, Unit]] = None,
    suffix_only: bool = False,
) -> Optional[Unit]:
    """Infer a unit from an identifier, or return ``None``.

    A unit token is accepted in the last position, or in the first position of a
    multi-token identifier (``ms_timeout``). An identifier naming two different
    units (``timeout_ms_to_seconds``) is treated as unknown.

    ``suffix_only`` drops the first-position rule. It is used for function names,
    which read as verb phrases where a leading unit word is usually a modifier
    rather than the unit of the result: ``second_largest`` is not seconds.
    """
    table = LEXICON if lexicon is None else lexicon
    tokens = split_identifier(name)
    if not tokens:
        return None
    hits: List[Tuple[int, Unit]] = [
        (index, table[token]) for index, token in enumerate(tokens) if token in table
    ]
    if not hits:
        return None
    if len({unit.label for _, unit in hits}) > 1:
        return None
    index, unit = hits[0]
    token = tokens[index]
    last = len(tokens) - 1
    if token in SHORT_TOKENS:
        return unit if (index == last and len(tokens) > 1) else None
    if index == last:
        return unit
    if index == 0 and len(tokens) > 1 and not suffix_only:
        return unit
    return None


def quantity_from_unit(unit: Unit) -> Quantity:
    return Quantity(base=unit)


def scale_quantity_by_constant(quantity: Quantity, factor: float) -> Quantity:
    """Apply multiplication by a known constant (``factor`` divides the scale)."""
    if factor == 0:
        return replace(quantity, unknown_factor=True)
    return replace(quantity, literal_factor=quantity.literal_factor / factor)


def divide_quantity_by_constant(quantity: Quantity, factor: float) -> Quantity:
    """Apply division by a known constant (``factor`` multiplies the scale)."""
    if factor == 0:
        return replace(quantity, unknown_factor=True)
    return replace(quantity, literal_factor=quantity.literal_factor * factor)


def matches(
    found: Quantity, expected: Unit, strict_binary: bool = False
) -> bool:
    """Whether ``found`` is an acceptable value for a slot expecting ``expected``.

    Two readings are accepted: the expression's scale after treating constant
    factors as conversions, and its scale ignoring those factors, which covers
    plain magnitude arithmetic such as ``base_delay_ms * 2``.
    """
    if found.dimension != expected.dimension:
        return False
    if found.unknown_factor:
        return True
    if scales_compatible(
        expected.dimension, found.effective_scale, expected.scale, strict_binary
    ):
        return True
    return scales_compatible(
        expected.dimension, found.lenient_scale, expected.scale, strict_binary
    )


def quantities_match(
    left: Quantity, right: Quantity, strict_binary: bool = False
) -> bool:
    """Whether two quantities can be added, subtracted or compared."""
    if left.dimension != right.dimension:
        return False
    if left.unknown_factor or right.unknown_factor:
        return True
    if scales_compatible(
        left.dimension, left.effective_scale, right.effective_scale, strict_binary
    ):
        return True
    return scales_compatible(
        left.dimension, left.lenient_scale, right.lenient_scale, strict_binary
    )


def conversion_hint(found: Quantity, expected: Unit) -> str:
    """A hint naming the factor that would fix a scale mismatch."""
    if found.dimension != expected.dimension:
        return ""
    found_scale = found.effective_scale
    if found_scale == 0 or expected.scale == 0:
        return ""
    # The numeric value must be multiplied by found/expected to be expressed in
    # the expected unit, so the fix is stated the other way round.
    factor = expected.scale / found_scale
    if math.isclose(factor, 1.0, rel_tol=REL_TOL):
        return ""
    if factor > 1:
        return f"divide by {format_scale(factor)}"
    return f"multiply by {format_scale(1.0 / factor)}"
