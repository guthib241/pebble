import math

from conftest import parse_source

from backfire import parse


def test_module_names():
    assert parse.module_name_for("pkg/mod.py") == "pkg.mod"
    assert parse.module_name_for("src/pkg/mod.py") == "pkg.mod"
    assert parse.module_name_for("pkg/__init__.py") == "pkg"
    assert parse.module_name_for("mod.py") == "mod"


def test_syntax_error_is_reported_not_raised():
    module = parse_source("def broken(:\n    pass\n")
    assert module.parse_error is not None
    assert module.functions == {}


def test_empty_module():
    module = parse_source("")
    assert module.parse_error is None
    assert module.functions == {}


def test_imports_are_recorded():
    module = parse_source(
        "import os\n"
        "import os.path as p\n"
        "from pkg.sub import thing\n"
        "from . import sibling\n",
        module="pkg.here",
        path="pkg/here.py",
    )
    assert module.imports["os"] == "os"
    assert module.imports["p"] == "os.path"
    assert module.imports["thing"] == "pkg.sub.thing"
    assert module.imports["sibling"] == "pkg.sibling"


def test_method_attribute_types_and_transport():
    module = parse_source(
        "import requests\n"
        "from requests.adapters import HTTPAdapter\n"
        "from urllib3.util.retry import Retry\n"
        "class C:\n"
        "    def __init__(self):\n"
        "        self.session = requests.Session()\n"
        "        self.session.mount('https://', HTTPAdapter(max_retries=Retry(total=2)))\n"
        "    def go(self):\n"
        "        return self.session.get('https://x.invalid', timeout=1)\n"
    )
    info = module.classes["C"]
    assert info.attr_types["session"] == "requests.Session"
    assert info.attr_transports["session"].attempts == 3
    call = module.functions["sample:C.go"].blocking[0]
    assert call.kind == "http"
    assert call.timeout == 1
    assert call.transport.attempts == 3


def test_module_level_singleton_client():
    module = parse_source(
        "import httpx\n"
        "client = httpx.Client(timeout=4)\n"
        "def fetch():\n"
        "    return client.get('https://x.invalid')\n"
    )
    call = module.functions["sample:fetch"].blocking[0]
    assert call.kind == "http"
    assert call.timeout == 4  # inherited from the client's default timeout


def test_nested_retry_loops_stack():
    module = parse_source(
        "import time\n"
        "import requests\n"
        "def f(url):\n"
        "    for outer in range(2):\n"
        "        try:\n"
        "            for inner in range(3):\n"
        "                try:\n"
        "                    return requests.get(url, timeout=1)\n"
        "                except OSError:\n"
        "                    time.sleep(1)\n"
        "        except OSError:\n"
        "            time.sleep(1)\n"
    )
    info = module.functions["sample:f"]
    assert len(info.block_scopes) == 2
    http = [call for call in info.blocking if call.kind == "http"][0]
    assert len(http.scopes) == 2


def test_sleep_calls_are_recorded_separately():
    module = parse_source("import time\ndef f():\n    time.sleep(3)\n")
    call = module.functions["sample:f"].blocking[0]
    assert (call.kind, call.timeout) == ("sleep", 3.0)


def test_call_without_timeout_is_unbounded():
    module = parse_source("import requests\ndef f(url):\n    return requests.get(url)\n")
    call = module.functions["sample:f"].blocking[0]
    assert math.isinf(call.timeout)


def test_async_function_and_deadline():
    module = parse_source(
        "import asyncio\nasync def f(task):\n    return await asyncio.wait_for(task, timeout=2)\n"
    )
    info = module.functions["sample:f"]
    assert info.is_async is True
    assert info.deadlines[0].seconds == 2


def test_nested_function_gets_own_qualname():
    module = parse_source("def outer():\n    def inner():\n        pass\n    return inner\n")
    assert "sample:outer" in module.functions
    assert "sample:outer.inner" in module.functions


def test_discover_skips_excluded_directories(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "a.py").write_text("x = 1\n")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "b.py").write_text("x = 1\n")
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "c.py").write_text("x = 1\n")
    found = {relative for _, relative, _ in parse.discover([str(tmp_path)])}
    assert found == {"pkg/a.py"}
