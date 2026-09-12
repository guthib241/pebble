"""Static unit-consistency analysis of Python source.

Two passes. The first indexes every function definition in the files under analysis
so that call sites can be checked against parameter units. The second walks each
module, inferring a unit for every expression it can and reporting inconsistencies.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

from .config import Config, load_config
from .knowledge import (
    ATTRIBUTES,
    CONSTANTS,
    METHODS,
    PASSTHROUGH_CALLS,
    UNIFYING_CALLS,
    KnownSignature,
)
from .units import (
    RATIO,
    factor_from_name,
    Quantity,
    Scalar,
    Unit,
    conversion_hint,
    divide_quantity_by_constant,
    lookup_label,
    matches,
    quantities_match,
    scale_quantity_by_constant,
    unit_for_scale,
    unit_from_name,
)

Inferred = Union[Quantity, Scalar, None]

SKIP_DIRECTORIES = frozenset(
    {
        ".git", ".hg", ".svn", ".tox", ".nox", ".venv", "venv", "env",
        "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
        "node_modules", "build", "dist", ".eggs", "site-packages",
    }
)

_NOQA_RE = re.compile(r"#\s*noqa\b(?::\s*(?P<codes>[A-Za-z0-9,\s]+))?", re.IGNORECASE)
_PRAGMA_RE = re.compile(r"#\s*orbiter\s*:\s*(?P<body>[A-Za-z0-9,\s]+)", re.IGNORECASE)
_CODE_RE = re.compile(r"[A-Za-z]+[0-9]+")


@dataclass(frozen=True)
class Diagnostic:
    path: str
    line: int
    column: int
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}:{self.column}: {self.code} {self.message}"

    def as_dict(self) -> Dict[str, object]:
        return {
            "path": self.path,
            "line": self.line,
            "column": self.column,
            "code": self.code,
            "message": self.message,
        }


@dataclass(frozen=True)
class AnalysisError:
    path: str
    line: Optional[int]
    message: str

    def __str__(self) -> str:
        where = f"{self.path}:{self.line}" if self.line else self.path
        return f"{where}: error: {self.message}"

    def as_dict(self) -> Dict[str, object]:
        return {"path": self.path, "line": self.line, "message": self.message}


@dataclass
class FunctionInfo:
    """Indexed signature of a function definition found in the analysed files."""

    name: str
    path: str
    lineno: int
    positional: List[Tuple[str, Optional[Unit]]] = field(default_factory=list)
    by_name: Dict[str, Optional[Unit]] = field(default_factory=dict)
    return_unit: Optional[Unit] = None
    declared_return_unit: Optional[Unit] = None
    is_method: bool = False

    def positional_unit(self, index: int) -> Optional[Unit]:
        if 0 <= index < len(self.positional):
            return self.positional[index][1]
        return None

    def has_position(self, index: int) -> bool:
        return 0 <= index < len(self.positional)


class SymbolTable:
    """Function definitions indexed by name, with conservative merging."""

    def __init__(self) -> None:
        self.functions: Dict[str, List[FunctionInfo]] = {}

    def add(self, info: FunctionInfo) -> None:
        self.functions.setdefault(info.name, []).append(info)

    def signature(self, name: str) -> Optional[KnownSignature]:
        """Merged signature for ``name``, keeping only unambiguous units.

        When several definitions share a name, a parameter slot is used only if
        every definition agrees on its unit. This keeps overloaded or shadowed
        names from producing wrong expectations.
        """
        infos = self.functions.get(name)
        if not infos:
            return None
        params: Dict[Union[str, int], Unit] = {}
        widest = max(len(info.positional) for info in infos)
        for index in range(widest):
            units = [info.positional_unit(index) for info in infos]
            if all(info.has_position(index) for info in infos) and _all_same_unit(units):
                assert units[0] is not None
                params[index] = units[0]
        names = set()
        for info in infos:
            names.update(info.by_name)
        for param_name in names:
            if not all(param_name in info.by_name for info in infos):
                continue
            units = [info.by_name[param_name] for info in infos]
            if _all_same_unit(units):
                assert units[0] is not None
                params[param_name] = units[0]
        returns = [info.return_unit for info in infos]
        return_unit = returns[0] if _all_same_unit(returns) else None
        if not params and return_unit is None:
            return None
        return KnownSignature(params=params, returns=return_unit)


def _all_same_unit(units: Sequence[Optional[Unit]]) -> bool:
    if not units or any(unit is None for unit in units):
        return False
    first = units[0]
    return all(unit == first for unit in units)


def unit_from_annotation(
    node: Optional[ast.AST], lexicon: Dict[str, Unit]
) -> Optional[Unit]:
    """Read a unit out of ``Annotated[..., "ms"]``, if present."""
    if not isinstance(node, ast.Subscript):
        return None
    base = node.value
    base_name = (
        base.attr if isinstance(base, ast.Attribute)
        else base.id if isinstance(base, ast.Name)
        else None
    )
    if base_name != "Annotated":
        return None
    slice_node = node.slice
    elements = slice_node.elts if isinstance(slice_node, ast.Tuple) else [slice_node]
    for element in elements[1:]:
        if isinstance(element, ast.Constant) and isinstance(element.value, str):
            unit = lookup_label(element.value, lexicon)
            if unit is not None:
                return unit
    return None


class ModuleAnalyzer:
    """Infers units within one module and records inconsistencies."""

    def __init__(
        self,
        path: str,
        tree: ast.Module,
        config: Config,
        symbols: SymbolTable,
        record: bool = True,
    ) -> None:
        self.path = path
        self.tree = tree
        self.config = config
        self.symbols = symbols
        self.record = record
        self.diagnostics: List[Diagnostic] = []
        self._memo: Dict[int, Inferred] = {}
        self.aliases: Dict[str, str] = {}
        self.module_constants: Dict[str, float] = {}

    # ---------------------------------------------------------------- helpers

    def report(self, node: ast.AST, code: str, message: str) -> None:
        if not self.record or not self.config.enabled(code):
            return
        self.diagnostics.append(
            Diagnostic(
                path=self.path,
                line=getattr(node, "lineno", 0),
                column=getattr(node, "col_offset", 0) + 1,
                code=code,
                message=message,
            )
        )

    def name_unit(self, name: str, suffix_only: bool = False) -> Optional[Unit]:
        return unit_from_name(name, self.config.lexicon, suffix_only=suffix_only)

    def constant_factor(self, name: str) -> Optional[float]:
        """Value of an upper-case conversion constant such as ``MS_PER_SECOND``."""
        if not name.isupper():
            return None
        return factor_from_name(name, self.config.lexicon)

    def _dotted(self, node: ast.AST) -> Optional[str]:
        """Resolve an attribute chain to a dotted path, applying import aliases."""
        parts: List[str] = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if not isinstance(current, ast.Name):
            return None
        parts.append(current.id)
        parts.reverse()
        head = self.aliases.get(parts[0])
        if head is not None:
            parts = head.split(".") + parts[1:]
        return ".".join(parts)

    # --------------------------------------------------------------- prepass

    def collect_imports_and_constants(self, body: Iterable[ast.stmt]) -> None:
        for node in body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.asname:
                        self.aliases[alias.asname] = alias.name
                    else:
                        root = alias.name.split(".")[0]
                        self.aliases.setdefault(root, root)
            elif isinstance(node, ast.ImportFrom):
                if node.level or not node.module:
                    continue
                for alias in node.names:
                    local = alias.asname or alias.name
                    self.aliases[local] = f"{node.module}.{alias.name}"
            elif isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                value = _literal_number(node.value)
                if isinstance(target, ast.Name) and value is not None:
                    self.module_constants[target.id] = value
            elif isinstance(node, (ast.If, ast.Try)):
                self.collect_imports_and_constants(node.body)
                self.collect_imports_and_constants(node.orelse)
                for handler in getattr(node, "handlers", []):
                    self.collect_imports_and_constants(handler.body)
                self.collect_imports_and_constants(getattr(node, "finalbody", []))

    # ----------------------------------------------------------------- driver

    def run(self) -> List[Diagnostic]:
        self.collect_imports_and_constants(self.tree.body)
        self.visit_body(self.tree.body, {}, None)
        return self.diagnostics

    # ------------------------------------------------------------- statements

    def visit_body(
        self,
        body: Iterable[ast.stmt],
        env: Dict[str, Optional[Quantity]],
        declared_return: Optional[Unit],
    ) -> None:
        for statement in body:
            self.visit_statement(statement, env, declared_return)

    def visit_statement(
        self,
        node: ast.stmt,
        env: Dict[str, Optional[Quantity]],
        declared_return: Optional[Unit],
    ) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self.visit_function(node, env)
        elif isinstance(node, ast.ClassDef):
            for decorator in node.decorator_list:
                self.infer(decorator, env)
            self.visit_body(node.body, dict(env), None)
        elif isinstance(node, ast.Assign):
            value = self.infer(node.value, env)
            for target in node.targets:
                self.bind_target(target, node.value, value, env)
        elif isinstance(node, ast.AnnAssign):
            declared = unit_from_annotation(node.annotation, self.config.lexicon)
            value = self.infer(node.value, env) if node.value is not None else None
            self.bind_target(node.target, node.value, value, env, declared=declared)
        elif isinstance(node, ast.AugAssign):
            value = self.infer(node.value, env)
            target = self.infer(node.target, env)
            if isinstance(node.op, (ast.Add, ast.Sub)):
                self.check_pair(node, target, value, "combined with")
            if isinstance(node.target, ast.Name) and isinstance(target, Quantity):
                env.setdefault(node.target.id, target)
        elif isinstance(node, ast.Return):
            value = self.infer(node.value, env) if node.value is not None else None
            if (
                declared_return is not None
                and isinstance(value, Quantity)
                and not matches(value, declared_return, self.config.strict_binary_prefixes)
            ):
                self.report(
                    node,
                    "ORB004",
                    _mismatch_message(
                        "returned value", value, declared_return
                    ),
                )
        elif isinstance(node, ast.For) or isinstance(node, ast.AsyncFor):
            self.infer(node.iter, env)
            self.bind_loop_target(node.target, env)
            self.visit_body(node.body, env, declared_return)
            self.visit_body(node.orelse, env, declared_return)
        elif isinstance(node, ast.While):
            self.infer(node.test, env)
            self.visit_body(node.body, env, declared_return)
            self.visit_body(node.orelse, env, declared_return)
        elif isinstance(node, ast.If):
            self.infer(node.test, env)
            self.visit_body(node.body, env, declared_return)
            self.visit_body(node.orelse, env, declared_return)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                value = self.infer(item.context_expr, env)
                if item.optional_vars is not None:
                    self.bind_target(item.optional_vars, None, value, env)
            self.visit_body(node.body, env, declared_return)
        elif isinstance(node, ast.Try):
            self.visit_body(node.body, env, declared_return)
            for handler in node.handlers:
                self.visit_body(handler.body, env, declared_return)
            self.visit_body(node.orelse, env, declared_return)
            self.visit_body(node.finalbody, env, declared_return)
        elif isinstance(node, ast.Expr):
            self.infer(node.value, env)
        else:
            self.generic_statement(node, env, declared_return)

    def generic_statement(
        self,
        node: ast.stmt,
        env: Dict[str, Optional[Quantity]],
        declared_return: Optional[Unit],
    ) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.expr):
                self.infer(child, env)
            elif isinstance(child, ast.stmt):
                self.visit_statement(child, env, declared_return)
            else:
                for grandchild in ast.iter_child_nodes(child):
                    if isinstance(grandchild, ast.expr):
                        self.infer(grandchild, env)
                    elif isinstance(grandchild, ast.stmt):
                        self.visit_statement(grandchild, env, declared_return)

    def visit_function(
        self,
        node: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        env: Dict[str, Optional[Quantity]],
    ) -> None:
        for decorator in node.decorator_list:
            self.infer(decorator, env)
        for default in list(node.args.defaults) + [
            d for d in node.args.kw_defaults if d is not None
        ]:
            self.infer(default, env)
        child_env: Dict[str, Optional[Quantity]] = dict(env)
        for argument, unit in self.parameter_units(node):
            child_env[argument] = Quantity(unit) if unit is not None else None
        declared = unit_from_annotation(node.returns, self.config.lexicon)
        if declared is None:
            declared = self.name_unit(node.name, suffix_only=True)
        self.visit_body(node.body, child_env, declared)

    def parameter_units(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> List[Tuple[str, Optional[Unit]]]:
        arguments = list(node.args.posonlyargs) + list(node.args.args)
        arguments += list(node.args.kwonlyargs)
        for extra in (node.args.vararg, node.args.kwarg):
            if extra is not None:
                arguments.append(extra)
        result: List[Tuple[str, Optional[Unit]]] = []
        for argument in arguments:
            unit = unit_from_annotation(argument.annotation, self.config.lexicon)
            if unit is None:
                unit = self.name_unit(argument.arg)
            result.append((argument.arg, unit))
        return result

    def bind_loop_target(
        self, target: ast.expr, env: Dict[str, Optional[Quantity]]
    ) -> None:
        for name in _target_names(target):
            unit = self.name_unit(name)
            env[name] = Quantity(unit) if unit is not None else None

    def bind_target(
        self,
        target: ast.expr,
        value_node: Optional[ast.expr],
        value: Inferred,
        env: Dict[str, Optional[Quantity]],
        declared: Optional[Unit] = None,
    ) -> None:
        if isinstance(target, (ast.Tuple, ast.List)):
            items = (
                value_node.elts
                if isinstance(value_node, (ast.Tuple, ast.List))
                and len(value_node.elts) == len(target.elts)
                else [None] * len(target.elts)
            )
            for element, item in zip(target.elts, items):
                item_value = self.infer(item, env) if item is not None else None
                self.bind_target(element, item, item_value, env)
            return

        expected = declared
        name = _assignment_name(target)
        if expected is None and name is not None:
            expected = self.name_unit(name)

        if (
            expected is not None
            and isinstance(value, Quantity)
            and value_node is not None
            and not matches(value, expected, self.config.strict_binary_prefixes)
        ):
            label = f"assignment to {name!r}" if name else "assignment"
            self.report(value_node, "ORB003", _mismatch_message(label, value, expected))

        if isinstance(target, ast.Name):
            if expected is not None:
                env[target.id] = Quantity(expected)
            elif isinstance(value, Quantity):
                env[target.id] = value
            else:
                env[target.id] = None
        elif isinstance(target, ast.Starred):
            self.bind_target(target.value, None, None, env)

    # ------------------------------------------------------------ expressions

    def infer(self, node: Optional[ast.expr], env: Dict[str, Optional[Quantity]]) -> Inferred:
        if node is None:
            return None
        key = id(node)
        if key in self._memo:
            return self._memo[key]
        method = getattr(self, f"_infer_{type(node).__name__}", None)
        result = method(node, env) if method is not None else self._infer_children(node, env)
        self._memo[key] = result
        return result

    def _infer_children(self, node: ast.AST, env: Dict[str, Optional[Quantity]]) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.expr):
                self.infer(child, env)
            else:
                self._infer_children(child, env)
        return None

    def _infer_Constant(self, node: ast.Constant, env) -> Inferred:
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            return None
        return Scalar(float(node.value))

    def _infer_Name(self, node: ast.Name, env) -> Inferred:
        if node.id in env:
            return env[node.id]
        dotted = self.aliases.get(node.id, node.id)
        if dotted in CONSTANTS:
            return Scalar(CONSTANTS[dotted])
        if node.id in self.module_constants:
            return Scalar(self.module_constants[node.id])
        factor = self.constant_factor(node.id)
        if factor is not None:
            return Scalar(factor)
        unit = self.name_unit(node.id)
        return Quantity(unit) if unit is not None else None

    def _infer_Attribute(self, node: ast.Attribute, env) -> Inferred:
        self.infer(node.value, env)
        dotted = self._dotted(node)
        if dotted is not None and dotted in CONSTANTS:
            return Scalar(CONSTANTS[dotted])
        if node.attr in ATTRIBUTES:
            return Quantity(ATTRIBUTES[node.attr])
        factor = self.constant_factor(node.attr)
        if factor is not None:
            return Scalar(factor)
        unit = self.name_unit(node.attr)
        return Quantity(unit) if unit is not None else None

    def _infer_Subscript(self, node: ast.Subscript, env) -> Inferred:
        self.infer(node.value, env)
        key = node.slice
        if isinstance(key, ast.Constant) and isinstance(key.value, str):
            unit = self.name_unit(key.value)
            return Quantity(unit) if unit is not None else None
        self.infer(key, env)
        return None

    def _infer_UnaryOp(self, node: ast.UnaryOp, env) -> Inferred:
        operand = self.infer(node.operand, env)
        if isinstance(node.op, (ast.UAdd, ast.USub)):
            if isinstance(operand, Scalar) and operand.value is not None:
                sign = -1.0 if isinstance(node.op, ast.USub) else 1.0
                return Scalar(sign * operand.value)
            return operand
        return None

    def _infer_BinOp(self, node: ast.BinOp, env) -> Inferred:
        left = self.infer(node.left, env)
        right = self.infer(node.right, env)
        operator = node.op

        if isinstance(operator, (ast.Add, ast.Sub)):
            verb = "added to" if isinstance(operator, ast.Add) else "subtracted from"
            self.check_pair(node, left, right, verb)
            if isinstance(left, Quantity):
                return left
            if isinstance(right, Quantity):
                return right
            return _fold_scalars(left, right, operator)

        if isinstance(operator, ast.Mult):
            return self._multiply(left, right)

        if isinstance(operator, (ast.Div, ast.FloorDiv)):
            return self._divide(left, right)

        if isinstance(operator, ast.Mod):
            if isinstance(left, Quantity):
                return left
            return None

        if isinstance(operator, ast.Pow):
            return _fold_scalars(left, right, operator)

        return None

    def _multiply(self, left: Inferred, right: Inferred) -> Inferred:
        if isinstance(left, Quantity) and isinstance(right, Quantity):
            return _apply_ratio(left, right)
        quantity, other = (
            (left, right) if isinstance(left, Quantity) else (right, left)
        )
        if not isinstance(quantity, Quantity):
            return _fold_scalars(left, right, ast.Mult())
        if isinstance(other, Scalar) and other.value is not None:
            return scale_quantity_by_constant(quantity, other.value)
        return replace(quantity, unknown_factor=True)

    def _divide(self, left: Inferred, right: Inferred) -> Inferred:
        if isinstance(left, Quantity) and isinstance(right, Quantity):
            if left.dimension != right.dimension:
                return None
            if left.unknown_factor or right.unknown_factor or right.effective_scale == 0:
                return None
            ratio = left.effective_scale / right.effective_scale
            return Quantity(base=self.config.lexicon["fraction"], literal_factor=ratio)
        if isinstance(left, Quantity):
            if isinstance(right, Scalar) and right.value is not None:
                return divide_quantity_by_constant(left, right.value)
            return replace(left, unknown_factor=True)
        if isinstance(right, Quantity):
            return None
        return _fold_scalars(left, right, ast.Div())

    def _infer_BoolOp(self, node: ast.BoolOp, env) -> Inferred:
        results = [self.infer(value, env) for value in node.values]
        for result in results:
            if isinstance(result, Quantity):
                return result
        return None

    def _infer_IfExp(self, node: ast.IfExp, env) -> Inferred:
        self.infer(node.test, env)
        body = self.infer(node.body, env)
        orelse = self.infer(node.orelse, env)
        self.check_pair(node, body, orelse, "used in the same conditional as")
        return body if isinstance(body, Quantity) else orelse

    def _infer_Compare(self, node: ast.Compare, env) -> Inferred:
        left = self.infer(node.left, env)
        for comparator in node.comparators:
            right = self.infer(comparator, env)
            self.check_pair(node, left, right, "compared with")
            left = right if isinstance(right, Quantity) else left
        return None

    def _infer_Starred(self, node: ast.Starred, env) -> Inferred:
        self.infer(node.value, env)
        return None

    def _infer_Lambda(self, node: ast.Lambda, env) -> Inferred:
        child_env = dict(env)
        for argument in (
            list(node.args.posonlyargs) + list(node.args.args) + list(node.args.kwonlyargs)
        ):
            unit = self.name_unit(argument.arg)
            child_env[argument.arg] = Quantity(unit) if unit is not None else None
        self.infer(node.body, child_env)
        return None

    def _infer_comprehension(self, node: ast.expr, env) -> Inferred:
        child_env = dict(env)
        for generator in node.generators:  # type: ignore[attr-defined]
            self.infer(generator.iter, child_env)
            self.bind_loop_target(generator.target, child_env)
            for condition in generator.ifs:
                self.infer(condition, child_env)
        for field_name in ("elt", "key", "value"):
            element = getattr(node, field_name, None)
            if isinstance(element, ast.expr):
                self.infer(element, child_env)
        return None

    _infer_ListComp = _infer_comprehension
    _infer_SetComp = _infer_comprehension
    _infer_GeneratorExp = _infer_comprehension
    _infer_DictComp = _infer_comprehension

    def _infer_Call(self, node: ast.Call, env) -> Inferred:
        dotted = self._dotted(node.func)
        bare = (
            node.func.attr if isinstance(node.func, ast.Attribute)
            else node.func.id if isinstance(node.func, ast.Name)
            else None
        )
        if not isinstance(node.func, (ast.Name, ast.Attribute)):
            self.infer(node.func, env)

        positional = [self.infer(argument, env) for argument in node.args]
        keywords = [(keyword.arg, self.infer(keyword.value, env)) for keyword in node.keywords]

        if dotted in PASSTHROUGH_CALLS or (
            isinstance(node.func, ast.Name) and bare in PASSTHROUGH_CALLS
        ):
            return positional[0] if positional and isinstance(positional[0], Quantity) else None

        if isinstance(node.func, ast.Name) and bare in UNIFYING_CALLS:
            quantities = [value for value in positional if isinstance(value, Quantity)]
            for other in quantities[1:]:
                self.check_pair(node, quantities[0], other, "combined with")
            return quantities[0] if quantities else None

        signature = self.resolve_signature(dotted, bare, node)
        if signature is None:
            return None

        self.check_arguments(node, signature, positional, keywords, dotted or bare or "call")
        return Quantity(signature.returns) if signature.returns is not None else None

    def resolve_signature(
        self, dotted: Optional[str], bare: Optional[str], node: ast.Call
    ) -> Optional[KnownSignature]:
        if dotted is not None:
            signature = self.config.functions.get(dotted)
            if signature is not None:
                return signature
        if bare is None:
            return None
        if isinstance(node.func, ast.Attribute) and bare in METHODS:
            return METHODS[bare]
        return self.symbols.signature(bare)

    def check_arguments(
        self,
        node: ast.Call,
        signature: KnownSignature,
        positional: Sequence[Inferred],
        keywords: Sequence[Tuple[Optional[str], Inferred]],
        callee: str,
    ) -> None:
        saw_star = any(isinstance(argument, ast.Starred) for argument in node.args)
        for index, value in enumerate(positional):
            if saw_star:
                break
            expected = signature.params.get(index)
            if expected is None or not isinstance(value, Quantity):
                continue
            if not matches(value, expected, self.config.strict_binary_prefixes):
                self.report(
                    node.args[index],
                    "ORB001",
                    _mismatch_message(
                        f"argument {index + 1} of {callee}()", value, expected
                    ),
                )
        for position, (name, value) in enumerate(keywords):
            if name is None:
                continue
            expected = signature.params.get(name)
            if expected is None or not isinstance(value, Quantity):
                continue
            if not matches(value, expected, self.config.strict_binary_prefixes):
                self.report(
                    node.keywords[position].value,
                    "ORB001",
                    _mismatch_message(
                        f"argument {name!r} of {callee}()", value, expected
                    ),
                )

    def check_pair(
        self, node: ast.AST, left: Inferred, right: Inferred, verb: str
    ) -> None:
        if not isinstance(left, Quantity) or not isinstance(right, Quantity):
            return
        if quantities_match(left, right, self.config.strict_binary_prefixes):
            return
        self.report(
            node,
            "ORB002",
            f"{left.describe()} {verb} {right.describe()}",
        )


def _apply_ratio(left: Quantity, right: Quantity) -> Inferred:
    """Multiplication where one operand is a ratio (percentage, fraction)."""
    if left.dimension == RATIO and right.dimension != RATIO:
        ratio, other = left, right
    elif right.dimension == RATIO and left.dimension != RATIO:
        ratio, other = right, left
    elif left.dimension == RATIO and right.dimension == RATIO:
        ratio, other = left, right
    else:
        return None
    if ratio.unknown_factor:
        return replace(other, unknown_factor=True)
    return replace(other, ratio_factor=other.ratio_factor * ratio.effective_scale)


def _fold_scalars(left: Inferred, right: Inferred, operator: ast.operator) -> Inferred:
    if not isinstance(left, Scalar) or not isinstance(right, Scalar):
        return None
    if left.value is None or right.value is None:
        return Scalar(None)
    try:
        if isinstance(operator, ast.Add):
            return Scalar(left.value + right.value)
        if isinstance(operator, ast.Sub):
            return Scalar(left.value - right.value)
        if isinstance(operator, ast.Mult):
            return Scalar(left.value * right.value)
        if isinstance(operator, ast.Div):
            return Scalar(left.value / right.value)
        if isinstance(operator, ast.Pow):
            return Scalar(left.value**right.value)
    except (ZeroDivisionError, OverflowError, ValueError):
        return Scalar(None)
    return Scalar(None)


def _mismatch_message(subject: str, found: Quantity, expected: Unit) -> str:
    if found.dimension != expected.dimension:
        return (
            f"{subject} expects {expected.label} ({expected.dimension}), "
            f"got {found.describe()} ({found.dimension})"
        )
    hint = conversion_hint(found, expected)
    suffix = f" ({hint})" if hint else ""
    return f"{subject} expects {expected.label}, got {found.describe()}{suffix}"


def _literal_number(node: ast.expr) -> Optional[float]:
    """Value of a numeric literal expression, folding simple arithmetic."""
    try:
        value = ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _assignment_name(target: ast.expr) -> Optional[str]:
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    if isinstance(target, ast.Subscript):
        key = target.slice
        if isinstance(key, ast.Constant) and isinstance(key.value, str):
            return key.value
    return None


def _target_names(target: ast.expr) -> List[str]:
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        names: List[str] = []
        for element in target.elts:
            names.extend(_target_names(element))
        return names
    if isinstance(target, ast.Starred):
        return _target_names(target.value)
    return []


# --------------------------------------------------------------------- indexing


def index_module(
    path: str, tree: ast.Module, config: Config
) -> List[FunctionInfo]:
    """Index every function definition in a module."""
    infos: List[FunctionInfo] = []
    analyzer = ModuleAnalyzer(path, tree, config, SymbolTable(), record=False)
    analyzer.collect_imports_and_constants(tree.body)

    def walk(body: Iterable[ast.stmt], in_class: bool) -> None:
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                infos.append(_index_function(node, path, config, analyzer, in_class))
                walk(node.body, False)
            elif isinstance(node, ast.ClassDef):
                walk(node.body, True)
            elif isinstance(node, (ast.If, ast.Try, ast.While, ast.For, ast.With)):
                walk(getattr(node, "body", []), in_class)
                walk(getattr(node, "orelse", []), in_class)
                walk(getattr(node, "finalbody", []), in_class)
                for handler in getattr(node, "handlers", []):
                    walk(handler.body, in_class)

    walk(tree.body, False)
    return infos


def _index_function(
    node: Union[ast.FunctionDef, ast.AsyncFunctionDef],
    path: str,
    config: Config,
    analyzer: ModuleAnalyzer,
    in_class: bool,
) -> FunctionInfo:
    parameters = analyzer.parameter_units(node)
    is_method = in_class and bool(parameters) and parameters[0][0] in {"self", "cls"}
    positional = list(node.args.posonlyargs) + list(node.args.args)
    positional_names = [argument.arg for argument in positional]
    by_name = dict(parameters)
    ordered = [(name, by_name.get(name)) for name in positional_names]
    if is_method:
        ordered = ordered[1:]
    declared = unit_from_annotation(node.returns, config.lexicon)
    if declared is None:
        declared = unit_from_name(node.name, config.lexicon, suffix_only=True)
    return_unit = unit_from_annotation(node.returns, config.lexicon)
    if return_unit is None:
        return_unit = _infer_return_unit(node, config, analyzer, declared)
    return FunctionInfo(
        name=node.name,
        path=path,
        lineno=node.lineno,
        positional=ordered,
        by_name=by_name,
        return_unit=return_unit,
        declared_return_unit=declared,
        is_method=is_method,
    )


def _infer_return_unit(
    node: Union[ast.FunctionDef, ast.AsyncFunctionDef],
    config: Config,
    analyzer: ModuleAnalyzer,
    declared: Optional[Unit],
) -> Optional[Unit]:
    """Infer a function's return unit from its return statements, then its name."""
    returns: List[ast.Return] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Return) and child.value is not None:
            if isinstance(child.value, ast.Constant) and child.value.value is None:
                continue
            returns.append(child)
    if not returns:
        return None
    local = ModuleAnalyzer(analyzer.path, ast.Module(body=[], type_ignores=[]),
                           config, SymbolTable(), record=False)
    local.aliases = analyzer.aliases
    local.module_constants = analyzer.module_constants
    env: Dict[str, Optional[Quantity]] = {}
    for name, unit in analyzer.parameter_units(node):
        env[name] = Quantity(unit) if unit is not None else None
    inferred: List[Quantity] = []
    for statement in returns:
        value = local.infer(statement.value, dict(env))
        if isinstance(value, Quantity):
            inferred.append(value)
        else:
            return declared
    first = inferred[0]
    for other in inferred[1:]:
        if not quantities_match(first, other, config.strict_binary_prefixes):
            return None
    if first.unknown_factor:
        return first.base
    return unit_for_scale(first.dimension, first.effective_scale) or first.base


# ---------------------------------------------------------------------- runner


def collect_python_files(paths: Iterable[Union[str, Path]]) -> Tuple[List[Path], List[AnalysisError]]:
    """Expand paths into Python files, skipping virtualenvs and caches."""
    files: List[Path] = []
    errors: List[AnalysisError] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for candidate in sorted(path.rglob("*.py")):
                if any(part in SKIP_DIRECTORIES for part in candidate.parts):
                    continue
                files.append(candidate)
        elif path.is_file():
            files.append(path)
        else:
            errors.append(AnalysisError(str(path), None, "no such file or directory"))
    unique: List[Path] = []
    seen = set()
    for path in files:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique, errors


def _parse(path: Path) -> Tuple[Optional[ast.Module], Optional[str], Optional[AnalysisError]]:
    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return None, None, AnalysisError(str(path), None, f"not valid UTF-8: {exc.reason}")
    except OSError as exc:
        return None, None, AnalysisError(str(path), None, f"cannot read file: {exc.strerror}")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return None, None, AnalysisError(str(path), exc.lineno, f"syntax error: {exc.msg}")
    except (ValueError, RecursionError) as exc:
        return None, None, AnalysisError(str(path), None, f"cannot parse file: {exc}")
    return tree, source, None


def suppressed_codes(source: str) -> Dict[int, Optional[frozenset]]:
    """Map line numbers to the codes suppressed on that line.

    ``# noqa`` and ``# orbiter: ignore`` suppress every code on the line, recorded
    as ``None``. ``# noqa: ORB001`` and ``# orbiter: ignore ORB001`` suppress only
    the codes listed.
    """
    result: Dict[int, Optional[frozenset]] = {}

    def record(number: int, codes: frozenset) -> None:
        if codes:
            existing = result.get(number, frozenset())
            if existing is None:
                return
            result[number] = frozenset(existing | codes)
        else:
            result[number] = None

    for number, line in enumerate(source.splitlines(), start=1):
        if "#" not in line:
            continue
        for match in _NOQA_RE.finditer(line):
            text = (match.group("codes") or "").strip()
            record(number, frozenset(code.upper() for code in _CODE_RE.findall(text)))
        for match in _PRAGMA_RE.finditer(line):
            tokens = [token for token in re.split(r"[,\s]+", match.group("body")) if token]
            if not tokens or tokens[0].lower() not in {"ignore", "noqa", "skip"}:
                continue
            record(
                number,
                frozenset(
                    token.upper() for token in tokens[1:] if _CODE_RE.fullmatch(token)
                ),
            )
    return result


def _apply_suppressions(
    diagnostics: Iterable[Diagnostic], suppressions: Dict[int, Optional[frozenset]]
) -> List[Diagnostic]:
    kept = []
    for diagnostic in diagnostics:
        entry = suppressions.get(diagnostic.line, frozenset())
        if entry is None or (entry and diagnostic.code in entry):
            continue
        kept.append(diagnostic)
    return kept


def analyze_paths(
    paths: Iterable[Union[str, Path]], config: Optional[Config] = None
) -> Tuple[List[Diagnostic], List[AnalysisError]]:
    """Analyse files and directories, returning diagnostics and errors."""
    config = config or load_config()
    files, errors = collect_python_files(paths)
    parsed: List[Tuple[Path, ast.Module, str]] = []
    for path in files:
        tree, source, error = _parse(path)
        if error is not None:
            errors.append(error)
            continue
        assert tree is not None and source is not None
        parsed.append((path, tree, source))

    symbols = SymbolTable()
    for path, tree, _ in parsed:
        for info in index_module(str(path), tree, config):
            symbols.add(info)

    diagnostics: List[Diagnostic] = []
    for path, tree, source in parsed:
        analyzer = ModuleAnalyzer(str(path), tree, config, symbols)
        found = analyzer.run()
        diagnostics.extend(_apply_suppressions(found, suppressed_codes(source)))
    diagnostics.sort(key=lambda item: (item.path, item.line, item.column, item.code))
    return diagnostics, errors
