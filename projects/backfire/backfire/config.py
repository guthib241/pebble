"""Optional configuration file support (backfire.toml or pyproject.toml)."""

from __future__ import annotations

import os
import re

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - only on older interpreters
    tomllib = None  # type: ignore[assignment]

DURATION = re.compile(r"^\s*([0-9]*\.?[0-9]+)\s*(ms|s|m|h)?\s*$")
UNITS = {"ms": 0.001, "s": 1.0, "m": 60.0, "h": 3600.0, None: 1.0}

CONFIG_NAMES = ("backfire.toml", "pyproject.toml")


class ConfigError(ValueError):
    pass


def parse_duration(value) -> float:
    """Turn '30s', '1.5m', 2 or 2.0 into seconds."""
    if isinstance(value, bool):
        raise ConfigError(f"not a duration: {value!r}")
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = DURATION.match(value)
        if match:
            return float(match.group(1)) * UNITS[match.group(2)]
    raise ConfigError(f"not a duration: {value!r}")


def find_config(start: str) -> str | None:
    directory = os.path.abspath(start if os.path.isdir(start) else os.path.dirname(start))
    while True:
        for name in CONFIG_NAMES:
            candidate = os.path.join(directory, name)
            if os.path.isfile(candidate):
                if name == "pyproject.toml" and not _has_backfire_table(candidate):
                    continue
                return candidate
        parent = os.path.dirname(directory)
        if parent == directory:
            return None
        directory = parent


def _has_backfire_table(path: str) -> bool:
    data = _read(path)
    return "backfire" in data.get("tool", {})


def _read(path: str) -> dict:
    if tomllib is None:  # pragma: no cover
        raise ConfigError("reading a config file needs Python 3.11+ (tomllib)")
    with open(path, "rb") as handle:
        return tomllib.load(handle)


def load(path: str) -> dict:
    """Return the backfire settings from a config file."""
    data = _read(path)
    if os.path.basename(path) == "pyproject.toml":
        data = data.get("tool", {}).get("backfire", {})
    settings: dict = {}
    if "max_attempts" in data:
        settings["max_attempts"] = float(data["max_attempts"])
    if "max_depth" in data:
        settings["max_depth"] = int(data["max_depth"])
    if "exclude" in data:
        settings["exclude"] = list(data["exclude"])
    if "resolve_by_name" in data:
        settings["resolve_by_name"] = bool(data["resolve_by_name"])
    budgets = data.get("budgets", {})
    if budgets:
        settings["budgets"] = {key: parse_duration(value) for key, value in budgets.items()}
    return settings
