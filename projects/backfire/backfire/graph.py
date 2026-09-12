"""Best-effort call graph over the functions found in a project."""

from __future__ import annotations

from dataclasses import dataclass, field

from .model import CallSite, ClassInfo, FunctionInfo, ModuleInfo


@dataclass
class CallGraph:
    modules: dict[str, ModuleInfo] = field(default_factory=dict)
    functions: dict[str, FunctionInfo] = field(default_factory=dict)
    classes: dict[str, ClassInfo] = field(default_factory=dict)
    edges: dict[str, list[tuple[CallSite, str]]] = field(default_factory=dict)
    callers: dict[str, set[str]] = field(default_factory=dict)
    unresolved: int = 0
    resolved: int = 0

    def roots(self) -> list[str]:
        """Functions nothing else in the project calls."""
        return sorted(name for name in self.functions if not self.callers.get(name))


def build(modules: list[ModuleInfo], resolve_by_name: bool = False) -> CallGraph:
    graph = CallGraph()
    for module in modules:
        graph.modules[module.name] = module
        graph.functions.update(module.functions)
        for info in module.classes.values():
            graph.classes[info.qualname] = info

    by_short_name: dict[str, list[str]] = {}
    for qualname in graph.functions:
        short = qualname.split(":", 1)[1].rsplit(".", 1)[-1]
        by_short_name.setdefault(short, []).append(qualname)

    resolver = _Resolver(graph, by_short_name, resolve_by_name)
    for qualname, info in graph.functions.items():
        edges: list[tuple[CallSite, str]] = []
        for call in info.calls:
            target = resolver.resolve(call, info)
            call.target = target
            if target is None or target == qualname:
                graph.unresolved += 1
                continue
            graph.resolved += 1
            edges.append((call, target))
            graph.callers.setdefault(target, set()).add(qualname)
        graph.edges[qualname] = edges
    return graph


class _Resolver:
    def __init__(self, graph: CallGraph, by_short_name: dict[str, list[str]], resolve_by_name: bool):
        self.graph = graph
        self.by_short_name = by_short_name
        self.resolve_by_name = resolve_by_name

    # -- public ----------------------------------------------------------
    def resolve(self, call: CallSite, caller: FunctionInfo) -> str | None:
        module = self.graph.modules.get(caller.module)
        if module is None:
            return None
        parts = call.raw.split(".")

        if parts[0] in {"self", "cls"} and caller.cls:
            owner = f"{caller.module}.{caller.cls}"
            if len(parts) == 1:  # self(...) on a callable object
                return self.lookup_method(owner, "__call__")
            if len(parts) == 2:
                return self.lookup_method(owner, parts[1])
            attribute_type = self._attr_type(owner, parts[1])
            if attribute_type:
                target_class = self.resolve_class(attribute_type, caller.module)
                if target_class:
                    return self.lookup_method(target_class, parts[-1])
            return None

        if call.hint and len(parts) >= 2:
            target_class = self.resolve_class(call.hint, caller.module)
            if target_class:
                found = self.lookup_method(target_class, parts[-1])
                if found:
                    return found

        dotted = self._expand(call.raw, module)
        found = self.resolve_dotted(dotted)
        if found:
            return found

        if len(parts) == 1:
            local = f"{caller.module}:{parts[0]}"
            if local in self.graph.functions:
                return local
            owner = f"{caller.module}.{parts[0]}"
            if owner in self.graph.classes:
                return self.lookup_method(owner, "__init__")

        if self.resolve_by_name:
            candidates = self.by_short_name.get(parts[-1], [])
            if len(candidates) == 1:
                return candidates[0]
        return None

    # -- helpers ---------------------------------------------------------
    def _expand(self, raw: str, module: ModuleInfo) -> str:
        parts = raw.split(".")
        binding = module.imports.get(parts[0])
        if binding:
            return ".".join([binding] + parts[1:])
        return f"{module.name}.{raw}"

    def _attr_type(self, class_qualname: str, attribute: str) -> str | None:
        info = self.graph.classes.get(class_qualname)
        if info is None:
            return None
        if attribute in info.attr_types:
            return info.attr_types[attribute]
        for base in info.bases:
            resolved = self.resolve_class(base, info.module)
            if resolved and resolved != class_qualname:
                found = self._attr_type(resolved, attribute)
                if found:
                    return found
        return None

    def resolve_class(self, dotted: str, from_module: str) -> str | None:
        if dotted in self.graph.classes:
            return dotted
        module = self.graph.modules.get(from_module)
        if module is not None:
            expanded = self._expand(dotted, module)
            if expanded in self.graph.classes:
                return expanded
            local = f"{from_module}.{dotted}"
            if local in self.graph.classes:
                return local
        parts = dotted.split(".")
        for index in range(len(parts) - 1, 0, -1):
            candidate = ".".join(parts[:index]) + "." + parts[index]
            if candidate in self.graph.classes:
                return candidate
        return None

    def lookup_method(self, class_qualname: str, method: str) -> str | None:
        seen: set[str] = set()
        stack = [class_qualname]
        while stack:
            current = stack.pop(0)
            if current in seen:
                continue
            seen.add(current)
            info = self.graph.classes.get(current)
            if info is None:
                continue
            if method in info.methods:
                return info.methods[method]
            for base in info.bases:
                resolved = self.resolve_class(base, info.module)
                if resolved:
                    stack.append(resolved)
        return None

    def resolve_dotted(self, dotted: str) -> str | None:
        parts = dotted.split(".")
        for index in range(len(parts) - 1, 0, -1):
            module_name = ".".join(parts[:index])
            rest = ".".join(parts[index:])
            if module_name not in self.graph.modules:
                continue
            qualname = f"{module_name}:{rest}"
            if qualname in self.graph.functions:
                return qualname
            head, _, tail = rest.partition(".")
            owner = f"{module_name}.{head}"
            if owner in self.graph.classes:
                return self.lookup_method(owner, tail or "__init__")
        return None
