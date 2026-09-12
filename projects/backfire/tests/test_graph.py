from conftest import graph_of


def targets(call_graph, caller):
    return {target for _, target in call_graph.edges.get(caller, [])}


def test_module_function_call_is_resolved():
    call_graph = graph_of(
        {
            "a": "from b import work\ndef top():\n    return work()\n",
            "b": "def work():\n    return 1\n",
        }
    )
    assert targets(call_graph, "a:top") == {"b:work"}


def test_module_alias_call_is_resolved():
    call_graph = graph_of(
        {
            "a": "import b\ndef top():\n    return b.work()\n",
            "b": "def work():\n    return 1\n",
        }
    )
    assert targets(call_graph, "a:top") == {"b:work"}


def test_relative_import_is_resolved():
    call_graph = graph_of(
        {
            "pkg.a": "from .b import work\ndef top():\n    return work()\n",
            "pkg.b": "def work():\n    return 1\n",
        }
    )
    assert targets(call_graph, "pkg.a:top") == {"pkg.b:work"}


def test_self_method_and_attribute_calls():
    call_graph = graph_of(
        {
            "svc": (
                "from cli import Client\n"
                "class Service:\n"
                "    def __init__(self):\n"
                "        self.client = Client()\n"
                "    def run(self):\n"
                "        self.helper()\n"
                "        return self.client.fetch()\n"
                "    def helper(self):\n"
                "        return 1\n"
            ),
            "cli": "class Client:\n    def fetch(self):\n        return 2\n",
        }
    )
    assert targets(call_graph, "svc:Service.run") == {"svc:Service.helper", "cli:Client.fetch"}


def test_local_variable_type_inference():
    call_graph = graph_of(
        {
            "a": "from cli import Client\ndef top():\n    client = Client()\n    return client.fetch()\n",
            "cli": "class Client:\n    def fetch(self):\n        return 2\n",
        }
    )
    assert "cli:Client.fetch" in targets(call_graph, "a:top")


def test_inherited_method_lookup():
    call_graph = graph_of(
        {
            "base": "class Base:\n    def fetch(self):\n        return 1\n",
            "child": (
                "from base import Base\n"
                "class Child(Base):\n"
                "    def run(self):\n"
                "        return self.fetch()\n"
            ),
        }
    )
    assert targets(call_graph, "child:Child.run") == {"base:Base.fetch"}


def test_external_calls_stay_unresolved():
    call_graph = graph_of({"a": "import requests\ndef top():\n    return requests.get('x')\n"})
    assert call_graph.edges["a:top"] == []
    assert call_graph.unresolved >= 1


def test_roots_exclude_called_functions():
    call_graph = graph_of(
        {
            "a": "from b import work\ndef top():\n    return work()\n",
            "b": "def work():\n    return 1\n",
        }
    )
    assert call_graph.roots() == ["a:top"]


def test_recursion_does_not_loop_forever():
    call_graph = graph_of({"a": "def top():\n    return top()\n"})
    assert call_graph.edges["a:top"] == []  # self-calls are dropped


def test_resolve_by_name_is_opt_in():
    sources = {
        "a": "def top():\n    return helper()\n",
        "b": "def helper():\n    return 1\n",
    }
    strict = graph_of(sources)
    assert strict.edges["a:top"] == []
    from backfire import graph, parse

    modules = [parse.parse_module(f"{name}.py", name, text) for name, text in sources.items()]
    loose = graph.build(modules, resolve_by_name=True)
    assert targets(loose, "a:top") == {"b:helper"}


def test_callable_instance_self_call():
    call_graph = graph_of(
        {
            "a": (
                "class Handler:\n"
                "    def __call__(self):\n"
                "        return 1\n"
                "    def run(self):\n"
                "        return self()\n"
            )
        }
    )
    assert targets(call_graph, "a:Handler.run") == {"a:Handler.__call__"}
