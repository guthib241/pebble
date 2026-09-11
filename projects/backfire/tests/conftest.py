import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backfire import graph, parse  # noqa: E402
from backfire.analyze import Options, analyze  # noqa: E402


def fixture_path(name: str) -> str:
    return os.path.join(FIXTURES, name)


def analyze_fixture(name: str, options: Options | None = None, resolve_by_name: bool = False):
    modules = parse.parse_project([fixture_path(name)])
    call_graph = graph.build(modules, resolve_by_name=resolve_by_name)
    return analyze(call_graph, options)


def parse_source(source: str, module: str = "sample", path: str = "sample.py"):
    return parse.parse_module(path, module, source)


def graph_of(sources: dict):
    modules = [parse_source(text, module=name, path=f"{name}.py") for name, text in sources.items()]
    return graph.build(modules)


@pytest.fixture
def layered():
    return analyze_fixture("layered")
