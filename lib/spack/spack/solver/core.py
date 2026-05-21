# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Low-level wrappers around clingo API and other basic functionality related to ASP"""

from typing import Any, NamedTuple, Optional, Tuple

import spack.platforms
from spack.llnl.util import lang

from .compat import symbol_name, symbol_string


class AspVar:
    """Represents a variable in an ASP rule, allows for conditionally generating
    rules"""

    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return str(self.name)


@lang.key_ordering
class AspFunction:
    """A term in the ASP logic program"""

    __slots__ = ("name", "args")

    def __init__(self, name: str, args: Tuple[Any, ...] = ()) -> None:
        self.name = name
        self.args = args

    def _cmp_key(self) -> Tuple[str, Tuple[Any, ...]]:
        return self.name, self.args

    def __call__(self, *args: Any) -> "AspFunction":
        """Return a new instance of this function with added arguments.

        Note that calls are additive, so you can do things like::

            >>> attr = AspFunction("attr")
            attr()

            >>> attr("version")
            attr("version")

            >>> attr("version")("foo")
            attr("version", "foo")

            >>> v = AspFunction("attr", "version")
            attr("version")

            >>> v("foo", "bar")
            attr("version", "foo", "bar")

        """
        return AspFunction(self.name, self.args + args)

    def __str__(self) -> str:
        parts = []
        for arg in self.args:
            if type(arg) is str:
                arg = arg.replace("\\", r"\\").replace("\n", r"\n").replace('"', r"\"")
                parts.append(f'"{arg}"')
            elif type(arg) is AspFunction or type(arg) is int or type(arg) is AspVar:
                parts.append(str(arg))
            else:
                parts.append(f'"{arg}"')
        return f"{self.name}({','.join(parts)})"

    def __repr__(self) -> str:
        return str(self)


class _AspFunctionBuilder:
    def __getattr__(self, name: str) -> AspFunction:
        return AspFunction(name)


#: Global AspFunction builder
fn = _AspFunctionBuilder()


class NodeId(NamedTuple):
    """Represents a node in the DAG"""

    id: str
    pkg: str


class NodeFlag(NamedTuple):
    flag_type: str
    flag: str
    flag_group: str
    source: str


def intermediate_repr(sym):
    """Returns an intermediate representation of clingo models for Spack's spec builder.

    Currently, transforms symbols from clingo models either to strings or to NodeId objects.

    Returns:
        This will turn a ``clingo.Symbol`` into a string or NodeId, or a sequence of
        ``clingo.Symbol`` objects into a tuple of those objects.
    """
    if isinstance(sym, (list, tuple)):
        return tuple(intermediate_repr(a) for a in sym)

    name = symbol_name(sym)
    if name == "node":
        return NodeId(
            id=intermediate_repr(sym.arguments[0]), pkg=intermediate_repr(sym.arguments[1])
        )
    if name == "node_flag":
        return NodeFlag(
            flag_type=intermediate_repr(sym.arguments[0]),
            flag=intermediate_repr(sym.arguments[1]),
            flag_group=intermediate_repr(sym.arguments[2]),
            source=intermediate_repr(sym.arguments[3]),
        )
    return symbol_string(sym)


def extract_args(model, predicate_name):
    """Extract the arguments to predicates with the provided name from a model.

    Pull out all the predicates with name ``predicate_name`` from the model, and
    return their intermediate representation.
    """
    return [
        intermediate_repr(sym.arguments) for sym in model if symbol_name(sym) == predicate_name
    ]


class SourceContext:
    """Tracks context in which a Spec's clause-set is generated (i.e.
    with ``SpackSolverSetup.spec_clauses``).

    Facts generated for the spec may include this context.
    """

    def __init__(self, *, source: Optional[str] = None):
        # This can be "literal" for constraints that come from a user
        # spec (e.g. from the command line); it can be the output of
        # `ConstraintOrigin.append_type_suffix`; the default is "none"
        # (which means it isn't important to keep track of the source
        # in that case).
        self.source = "none" if source is None else source
        self.wrap_node_requirement: Optional[bool] = None


def using_libc_compatibility() -> bool:
    """Returns True if we are currently using libc compatibility"""
    return spack.platforms.host().name == "linux"
