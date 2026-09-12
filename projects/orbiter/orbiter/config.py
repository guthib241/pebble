"""Configuration: extra unit aliases, extra known signatures, disabled checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, FrozenSet, Optional, Union

from .knowledge import FUNCTIONS, KnownSignature
from .units import LEXICON, Unit, lookup_label

CODES = {
    "ORB001": "call argument unit mismatch",
    "ORB002": "mixed units in arithmetic or comparison",
    "ORB003": "assignment unit mismatch",
    "ORB004": "return value unit mismatch",
}


class ConfigError(Exception):
    """Raised when a configuration file cannot be used."""


@dataclass(frozen=True)
class Config:
    disabled: FrozenSet[str] = frozenset()
    strict_binary_prefixes: bool = False
    lexicon: Dict[str, Unit] = field(default_factory=lambda: dict(LEXICON))
    functions: Dict[str, KnownSignature] = field(default_factory=lambda: dict(FUNCTIONS))

    def enabled(self, code: str) -> bool:
        return code not in self.disabled


def _parse_unit(label: str, where: str, lexicon: Dict[str, Unit]) -> Unit:
    unit = lookup_label(label, lexicon)
    if unit is None:
        raise ConfigError(f"{where}: unknown unit {label!r}")
    return unit


def load_config(
    path: Optional[Union[str, Path]] = None,
    disable: FrozenSet[str] = frozenset(),
    strict_binary_prefixes: bool = False,
) -> Config:
    """Build a :class:`Config`, optionally reading a TOML file.

    The file may define ``disable``, ``strict_binary_prefixes``, ``[orbiter.aliases]``
    (identifier token to unit label) and ``[orbiter.functions."pkg.func"]`` tables
    with ``params`` and ``returns``.
    """
    lexicon = dict(LEXICON)
    functions = dict(FUNCTIONS)
    disabled = set(disable)
    strict = strict_binary_prefixes

    if path is not None:
        try:
            import tomllib
        except ModuleNotFoundError as exc:  # pragma: no cover - 3.11+ in practice
            raise ConfigError(
                "reading a config file requires Python 3.11 or newer (tomllib)"
            ) from exc
        file_path = Path(path)
        try:
            raw = tomllib.loads(file_path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise ConfigError(f"cannot read config {file_path}: {exc}") from exc
        except tomllib.TOMLDecodeError as exc:
            raise ConfigError(f"invalid TOML in {file_path}: {exc}") from exc

        section = raw.get("orbiter", raw)
        if not isinstance(section, dict):
            raise ConfigError(f"{file_path}: [orbiter] must be a table")

        for code in section.get("disable", []) or []:
            if code not in CODES:
                raise ConfigError(f"{file_path}: unknown check code {code!r}")
            disabled.add(code)

        if "strict_binary_prefixes" in section:
            value = section["strict_binary_prefixes"]
            if not isinstance(value, bool):
                raise ConfigError(f"{file_path}: strict_binary_prefixes must be a bool")
            strict = strict or value

        aliases = section.get("aliases", {}) or {}
        if not isinstance(aliases, dict):
            raise ConfigError(f"{file_path}: [orbiter.aliases] must be a table")
        for token, label in aliases.items():
            if not isinstance(label, str):
                raise ConfigError(f"{file_path}: alias {token!r} must map to a string")
            lexicon[token.lower()] = _parse_unit(
                label, f"{file_path}: alias {token!r}", lexicon
            )

        extra_functions = section.get("functions", {}) or {}
        if not isinstance(extra_functions, dict):
            raise ConfigError(f"{file_path}: [orbiter.functions] must be a table")
        for dotted, spec in extra_functions.items():
            if not isinstance(spec, dict):
                raise ConfigError(f"{file_path}: function {dotted!r} must be a table")
            params: Dict[Union[str, int], Unit] = {}
            for key, label in (spec.get("params", {}) or {}).items():
                if not isinstance(label, str):
                    raise ConfigError(
                        f"{file_path}: {dotted}.params.{key} must be a unit label"
                    )
                unit = _parse_unit(label, f"{file_path}: {dotted}.params.{key}", lexicon)
                params[int(key) if str(key).isdigit() else str(key)] = unit
            returns = spec.get("returns")
            return_unit = (
                _parse_unit(returns, f"{file_path}: {dotted}.returns", lexicon)
                if isinstance(returns, str)
                else None
            )
            functions[dotted] = KnownSignature(params=params, returns=return_unit)

    return Config(
        disabled=frozenset(disabled),
        strict_binary_prefixes=strict,
        lexicon=lexicon,
        functions=functions,
    )
