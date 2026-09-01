# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Low-level wrappers around clingo API and other basic functionality related to ASP"""

from typing import Any, Dict, NamedTuple, Optional, Tuple

from spack.util import lang

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
        return AspFunction(self.name, args if not self.args else self.args + args)

    def __str__(self) -> str:
        return self.to_str({})

    def to_str(self, quoted: "QuotedStrings") -> str:
        """The ASP representation of this function, reusing the literals in ``quoted``."""
        return f"{self.name}({','.join([asp_argument(arg, quoted) for arg in self.args])})"

    def args_str(self, quoted: "QuotedStrings") -> str:
        """The arguments as they appear between the parentheses of this function.

        The trigger and effect rules write the arguments of a clause out under a head of
        their own, which is what needs this separately from :meth:`to_str`.
        """
        return ",".join([asp_argument(arg, quoted) for arg in self.args])

    def __repr__(self) -> str:
        return str(self)


#: ASP literals of the strings that have been written out, by string. String arguments are
#: package, variant, version, ... names, of which a solve writes the same handful out over and
#: over, and escaping one means scanning it three times. A problem instance owns one of these,
#: so that the literals it collects are released together with it.
QuotedStrings = Dict[str, str]


def quote(arg: str, quoted: QuotedStrings) -> str:
    """The ASP literal for the string ``arg``: escaped, in double quotes, and kept for reuse.

    Use :func:`quote_once` for the strings that are written out once, such as the messages that
    explain a condition, so that they do not fill ``quoted``.
    """
    return quoted.get(arg) or _quote(arg, quoted)


def quote_once(arg: str) -> str:
    """The ASP literal for a string that is not expected to come up again."""
    return '"' + arg.replace("\\", r"\\").replace("\n", r"\n").replace('"', r"\"") + '"'


def _quote(arg: str, quoted: QuotedStrings) -> str:
    """Compute and keep the ASP literal for ``arg``; see :func:`quote`."""
    result = quoted[arg] = quote_once(arg)
    return result


def asp_argument(arg: Any, quoted: QuotedStrings) -> str:
    """The ASP representation of a single argument of a function."""
    # exact type checks first, ordered by frequency
    if type(arg) is str:
        return quoted.get(arg) or _quote(arg, quoted)
    if type(arg) is AspFunction:
        return arg.to_str(quoted)
    if type(arg) is int or type(arg) is AspVar:
        return str(arg)
    # subclasses miss the checks above: config values are syaml_str / syaml_int. bool is
    # an int subclass, but is not a number in ASP, so it is quoted below.
    if isinstance(arg, int) and not isinstance(arg, bool):
        return str(arg)
    if isinstance(arg, str):
        return quoted.get(arg) or _quote(arg, quoted)
    return f'"{arg}"'


class _AspFunctionBuilder:
    def __getattr__(self, name: str) -> AspFunction:
        # Writing to __dict__ directly caches the result so repeated access to the
        # same name bypasses __getattr__ and hits the instance dict instead.
        # Safe because AspFunction objects are never mutated.
        f = AspFunction(name)
        self.__dict__[name] = f
        return f


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
    with ``SpecClauseGenerator.spec_clauses``).

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
