"""Turn a directory of Python source into modules, functions and retry sites."""

from __future__ import annotations

import ast
import os
import re
from dataclasses import dataclass, field

from . import detect
from .model import (
    UNBOUNDED,
    BlockingCall,
    CallSite,
    ClassInfo,
    Deadline,
    FunctionInfo,
    Location,
    ModuleInfo,
    RetryPolicy,
    RetrySite,
)

DEFAULT_EXCLUDES = (
    ".git",
    ".hg",
    ".svn",
    ".tox",
    ".nox",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    "build",
    "dist",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "site-packages",
)

ASSUMED_ATTEMPTS = 3.0


def discover(paths, excludes=DEFAULT_EXCLUDES, root=None):
    """Yield (absolute path, relative path, module name) for each Python file."""
    excludes = set(excludes)
    seen = set()
    for raw in paths:
        target = os.path.abspath(raw)
        base = os.path.abspath(root) if root else (target if os.path.isdir(target) else os.path.dirname(target))
        if os.path.isfile(target):
            files = [target]
        else:
            files = []
            for dirpath, dirnames, filenames in os.walk(target):
                dirnames[:] = sorted(
                    name for name in dirnames if name not in excludes and not name.startswith(".")
                )
                for filename in sorted(filenames):
                    if filename.endswith(".py"):
                        files.append(os.path.join(dirpath, filename))
        for path in files:
            if path in seen:
                continue
            seen.add(path)
            relative = os.path.relpath(path, base)
            yield path, relative, module_name_for(relative)


def module_name_for(relative_path: str) -> str:
    parts = relative_path.replace(os.sep, "/").split("/")
    if parts and parts[0] in {"src", "lib"}:
        parts = parts[1:]
    if not parts:
        return "?"
    parts[-1] = parts[-1][:-3] if parts[-1].endswith(".py") else parts[-1]
    if parts[-1] == "__init__":
        parts = parts[:-1] or ["__init__"]
    return ".".join(parts)


def _is_true(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is True


def _range_attempts(node: ast.AST) -> tuple[float, bool] | None:
    call = node if isinstance(node, ast.Call) else None
    if call is None or detect._last(detect.dotted_name(call.func) or "") != "range":
        return None
    values = [detect.number(arg) for arg in call.args]
    if not values or any(value is None for value in values):
        return ASSUMED_ATTEMPTS, False
    if len(values) == 1:
        return max(values[0], 0.0), True
    span = values[1] - values[0]
    step = values[2] if len(values) > 2 and values[2] else 1.0
    return max(span / step, 0.0), True


def _scoped_nodes(node: ast.AST):
    """Yield nodes inside a loop without descending into nested loops or functions."""
    stack = list(ast.iter_child_nodes(node))
    while stack:
        current = stack.pop()
        yield current
        if isinstance(
            current,
            (ast.For, ast.AsyncFor, ast.While, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
        ):
            continue
        stack.extend(ast.iter_child_nodes(current))


TIMEOUT_EXCEPTIONS = {"TimeoutError", "CancelledError", "Exception", "BaseException"}


def _catches_timeout(node: ast.Try) -> bool:
    """True when a try block handles the timeout it is about to impose."""
    for handler in node.handlers:
        if handler.type is None:
            return True
        types = handler.type.elts if isinstance(handler.type, ast.Tuple) else [handler.type]
        for item in types:
            if detect._last(detect.dotted_name(item) or "") in TIMEOUT_EXCEPTIONS:
                return True
    return False


def _is_sleep_call(node: ast.AST) -> bool:
    return isinstance(node, ast.Call) and detect.is_sleep(detect.dotted_name(node.func) or "")


def loop_retry_policy(node: ast.AST) -> RetryPolicy | None:
    """Recognise a hand-rolled retry loop."""
    if isinstance(node, ast.For) or isinstance(node, ast.AsyncFor):
        counted = _range_attempts(node.iter)
        if counted is None:
            return None
        attempts, attempts_known = counted
        detail = f"for-loop over {ast.unparse(node.iter)}"
    elif isinstance(node, ast.While):
        if not _is_true(node.test):
            return None
        attempts, attempts_known = UNBOUNDED, True
        detail = "while True retry loop with no attempt cap"
    else:
        return None

    scoped = list(_scoped_nodes(node))
    tries = [child for child in scoped if isinstance(child, ast.Try) and child.handlers]
    if not tries:
        return None
    # A retry loop leaves the loop on success (break/return in a try body) or loops
    # again on failure (continue or a sleep in a handler). Anything else is an
    # ordinary loop that happens to catch an exception.
    succeeds = any(
        isinstance(child, (ast.Break, ast.Return))
        for block in tries
        for statement in block.body
        for child in ast.walk(statement)
    )
    retries = any(
        isinstance(child, ast.Continue) or _is_sleep_call(child)
        for block in tries
        for handler in block.handlers
        for child in ast.walk(handler)
    )
    has_backoff = any(_is_sleep_call(child) for child in scoped)
    if not (succeeds or retries):
        return None
    return RetryPolicy(
        source="loop",
        attempts=attempts,
        attempts_known=attempts_known,
        backoff=has_backoff,
        wait_total=0.0,  # sleeps inside the loop are counted as blocking items
        wait_known=True,
        detail=detail,
    )


@dataclass
class _Scope:
    """Mutable state while walking one function body."""

    var_types: dict[str, str] = field(default_factory=dict)
    var_transports: dict[str, RetryPolicy] = field(default_factory=dict)
    var_timeouts: dict[str, float] = field(default_factory=dict)


class ModuleParser:
    def __init__(self, module: str, relative_path: str, tree: ast.Module):
        self.module = module
        self.path = relative_path
        self.tree = tree
        self.info = ModuleInfo(name=module, path=relative_path)
        self.module_scope = _Scope()

    # -- helpers ---------------------------------------------------------
    def loc(self, node: ast.AST) -> Location:
        return Location(self.path, getattr(node, "lineno", 0))

    def parse(self) -> ModuleInfo:
        self._collect_imports(self.tree)
        with detect.constant_scope(self._collect_constants(self.tree)):
            self._walk_toplevel(self.tree.body, cls=None, prefix="")
        return self.info

    def _collect_constants(self, tree: ast.Module) -> dict:
        """Module-level literals, so ``stop_after_attempt(MAX_TRIES)`` can be read."""
        constants: dict = {}
        for node in tree.body:
            if isinstance(node, ast.Assign):
                value = detect.literal(node.value)
                if value is None:
                    continue
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        constants[target.id] = value
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                value = detect.literal(node.value)
                if value is not None:
                    constants[node.target.id] = value
        return constants

    def _collect_imports(self, tree: ast.Module) -> None:
        package = self.module.rsplit(".", 1)[0] if "." in self.module else ""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.info.imports[alias.asname or alias.name.split(".")[0]] = (
                        alias.name if alias.asname else alias.name.split(".")[0]
                    )
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level:
                    parent = package
                    for _ in range(node.level - 1):
                        parent = parent.rsplit(".", 1)[0] if "." in parent else ""
                    base = f"{parent}.{base}".strip(".") if base else parent
                for alias in node.names:
                    target = f"{base}.{alias.name}" if base else alias.name
                    self.info.imports[alias.asname or alias.name] = target

    def _walk_toplevel(self, body, cls: ClassInfo | None, prefix: str) -> None:
        for node in body:
            if isinstance(node, ast.Assign):
                # Module-level singletons (``client = ApiClient()``) are common,
                # so their types and transports are tracked for the whole module.
                self._record_assignment(node, None, self.module_scope, None)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._parse_function(node, cls, prefix)
            elif isinstance(node, ast.ClassDef):
                info = ClassInfo(
                    name=node.name,
                    module=self.module,
                    bases=[name for name in (detect.dotted_name(base) for base in node.bases) if name],
                )
                self.info.classes[node.name] = info
                methods = [
                    child
                    for child in node.body
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                methods.sort(key=lambda child: child.name != "__init__")
                for method in methods:
                    info.methods[method.name] = f"{self.module}:{node.name}.{method.name}"
                    self._parse_function(method, info, f"{node.name}.")

    # -- functions -------------------------------------------------------
    def _parse_function(self, node, cls: ClassInfo | None, prefix: str) -> FunctionInfo:
        qualname = f"{self.module}:{prefix}{node.name}"
        info = FunctionInfo(
            qualname=qualname,
            location=self.loc(node),
            module=self.module,
            cls=cls.name if cls else None,
            is_async=isinstance(node, ast.AsyncFunctionDef),
        )
        for decorator in node.decorator_list:
            policy = detect.decorator_policy(decorator)
            if policy is not None:
                info.entry_sites.append(
                    RetrySite(
                        policy=policy,
                        location=self.loc(decorator),
                        kind="decorator",
                        start_line=node.lineno,
                        end_line=getattr(node, "end_lineno", node.lineno),
                    )
                )
        self.info.functions[qualname] = info
        scope = _Scope()
        self._walk_body(node.body, info, scope, cls, (), f"{prefix}{node.name}.")
        return info

    def _walk_body(self, body, info, scope, cls, scopes, prefix, handled=False) -> None:
        for node in body:
            self._walk_node(node, info, scope, cls, scopes, prefix, handled)

    def _walk_node(self, node, info, scope, cls, scopes, prefix, handled=False) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self._parse_function(node, cls, prefix)
            return
        if isinstance(node, ast.ClassDef):
            return
        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            policy = loop_retry_policy(node)
            if policy is not None:
                site = RetrySite(
                    policy=policy,
                    location=self.loc(node),
                    kind="loop",
                    start_line=node.lineno,
                    end_line=getattr(node, "end_lineno", node.lineno),
                )
                info.block_scopes.append(site)
                scopes = scopes + (len(info.block_scopes) - 1,)
        if isinstance(node, ast.Try):
            catches = _catches_timeout(node)
            self._walk_body(node.body, info, scope, cls, scopes, prefix, handled or catches)
            for child in list(node.handlers) + list(node.orelse) + list(node.finalbody):
                self._walk_node(child, info, scope, cls, scopes, prefix, handled)
            return
        if isinstance(node, ast.Assign):
            self._record_assignment(node, info, scope, cls)
        if isinstance(node, ast.Call):
            self._record_call(node, info, scope, cls, scopes, handled)
        for child in ast.iter_child_nodes(node):
            self._walk_node(child, info, scope, cls, scopes, prefix, handled)

    # -- assignments -----------------------------------------------------
    def _record_assignment(self, node: ast.Assign, info, scope, cls) -> None:
        if not isinstance(node.value, ast.Call):
            return
        call = node.value
        constructed = detect.dotted_name(call.func) or ""
        policy = detect.transport_policy(call)
        timeout, timeout_known = detect.timeout_seconds(call)
        transport_node = detect.kwarg(call, "transport")
        if policy is None and isinstance(transport_node, ast.Call):
            policy = detect.transport_policy(transport_node)
        elif policy is None and isinstance(transport_node, ast.Name):
            policy = scope.var_transports.get(transport_node.id)
        for target in node.targets:
            name = detect.dotted_name(target)
            if not name:
                continue
            if name.startswith("self.") and cls is not None:
                attribute = name.split(".", 1)[1]
                if constructed:
                    cls.attr_types[attribute] = constructed
                if policy is not None:
                    cls.attr_transports[attribute] = policy
                if timeout_known and timeout != UNBOUNDED:
                    cls.attr_timeouts[attribute] = timeout
            elif "." not in name:
                if constructed:
                    scope.var_types[name] = constructed
                if policy is not None:
                    scope.var_transports[name] = policy
                if timeout_known and timeout != UNBOUNDED:
                    scope.var_timeouts[name] = timeout

    # -- calls -----------------------------------------------------------
    def _lookup_transport(self, receiver: str, scope, cls) -> RetryPolicy | None:
        if receiver.startswith("self.") and cls is not None:
            return cls.attr_transports.get(receiver.split(".", 1)[1])
        return scope.var_transports.get(receiver) or self.module_scope.var_transports.get(receiver)

    def _lookup_timeout(self, receiver: str, scope, cls) -> float | None:
        if receiver.startswith("self.") and cls is not None:
            return cls.attr_timeouts.get(receiver.split(".", 1)[1])
        value = scope.var_timeouts.get(receiver)
        return value if value is not None else self.module_scope.var_timeouts.get(receiver)

    def _mount_adapter(self, call: ast.Call, raw: str, scope, cls) -> bool:
        """Handle session.mount(prefix, HTTPAdapter(...))."""
        if not raw.endswith(".mount"):
            return False
        receiver = raw[: -len(".mount")]
        policy = None
        for argument in list(call.args) + [keyword.value for keyword in call.keywords]:
            if isinstance(argument, ast.Call):
                policy = detect.transport_policy(argument) or policy
            elif isinstance(argument, ast.Name):
                policy = scope.var_transports.get(argument.id) or policy
        if policy is None:
            return True
        if receiver.startswith("self.") and cls is not None:
            cls.attr_transports[receiver.split(".", 1)[1]] = policy
        else:
            scope.var_transports[receiver] = policy
        return True

    def _record_call(self, call: ast.Call, info, scope, cls, scopes, handled=False) -> None:
        raw = detect.dotted_name(call.func)
        if raw is None:
            return
        location = self.loc(call)
        if self._mount_adapter(call, raw, scope, cls):
            return

        deadline = detect.wait_for_deadline(call)
        if deadline is not None:
            info.deadlines.append(
                Deadline(
                    seconds=deadline,
                    location=location,
                    start_line=call.lineno,
                    end_line=getattr(call, "end_lineno", call.lineno),
                    detail=ast.unparse(call.func),
                    handled=handled,
                )
            )

        receiver, _, attribute = raw.rpartition(".")
        timeout, timeout_known = detect.timeout_seconds(call)
        transport = self._lookup_transport(receiver, scope, cls) if receiver else None
        kind = None
        if detect.is_sleep(raw):
            seconds, known = detect.sleep_seconds(call)
            info.blocking.append(
                BlockingCall(
                    location=location,
                    kind="sleep",
                    timeout=seconds,
                    timeout_known=known,
                    detail=f"{raw}()",
                    scopes=scopes,
                )
            )
            return
        if detect.is_http_module_call(raw) or detect.is_urlopen(raw):
            kind = "http"
        elif detect.is_subprocess(raw):
            kind = "subprocess"
        elif detect.is_socket_connect(raw):
            kind = "socket"
        elif attribute in detect.HTTP_METHODS and receiver:
            client = self._receiver_type(receiver, scope, cls)
            if client and any(token in client for token in ("Session", "Client", "httpx", "requests")):
                kind = "http"
            elif transport is not None:
                kind = "http"
        if kind is not None:
            if timeout == UNBOUNDED and timeout_known and receiver:
                default = self._lookup_timeout(receiver, scope, cls)
                if default is not None:
                    timeout = default
            info.blocking.append(
                BlockingCall(
                    location=location,
                    kind=kind,
                    timeout=timeout,
                    timeout_known=timeout_known,
                    detail=f"{raw}()",
                    scopes=scopes,
                    transport=transport,
                )
            )
        hint = self._receiver_type(receiver, scope, cls) if receiver else None
        info.calls.append(CallSite(raw=raw, location=location, scopes=scopes, hint=hint))

    def _receiver_type(self, receiver: str, scope, cls) -> str | None:
        if receiver.startswith("self.") and cls is not None:
            return cls.attr_types.get(receiver.split(".", 1)[1])
        return scope.var_types.get(receiver) or self.module_scope.var_types.get(receiver)


SUPPRESSION = re.compile(r"#\s*backfire:\s*ignore(?:\[([^\]]*)\])?")


def find_suppressions(source: str) -> dict[int, set[str] | None]:
    """Lines carrying '# backfire: ignore' or '# backfire: ignore[BF001,BF003]'."""
    found: dict[int, set[str] | None] = {}
    for number, line in enumerate(source.splitlines(), start=1):
        match = SUPPRESSION.search(line)
        if not match:
            continue
        rules = match.group(1)
        found[number] = {rule.strip().upper() for rule in rules.split(",") if rule.strip()} if rules else None
    return found


def parse_module(relative_path: str, module: str, source: str) -> ModuleInfo:
    try:
        tree = ast.parse(source, filename=relative_path)
    except SyntaxError as error:
        info = ModuleInfo(name=module, path=relative_path)
        info.parse_error = f"{error.msg} (line {error.lineno})"
        return info
    info = ModuleParser(module, relative_path, tree).parse()
    info.suppressions = find_suppressions(source)
    return info


def parse_project(paths, excludes=DEFAULT_EXCLUDES, root=None) -> list[ModuleInfo]:
    modules: list[ModuleInfo] = []
    for absolute, relative, module in discover(paths, excludes=excludes, root=root):
        try:
            source = open(absolute, "r", encoding="utf-8", errors="replace").read()
        except OSError as error:
            info = ModuleInfo(name=module, path=relative)
            info.parse_error = str(error)
            modules.append(info)
            continue
        modules.append(parse_module(relative, module, source))
    return modules
