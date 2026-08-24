# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Basic data structures used to build Spack's ASP program"""

from typing import Any, NamedTuple, Optional, Tuple

from spack.util import lang


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
        parts = []
        for arg in self.args:
            # exact type checks first, ordered by frequency
            if type(arg) is str:
                arg = arg.replace("\\", r"\\").replace("\n", r"\n").replace('"', r"\"")
                parts.append(f'"{arg}"')
            elif type(arg) is AspFunction or type(arg) is int or type(arg) is AspVar:
                parts.append(str(arg))
            # subclasses miss the checks above: config values are syaml_str / syaml_int. bool is
            # an int subclass, but is not a number in ASP, so it is quoted below.
            elif isinstance(arg, int) and not isinstance(arg, bool):
                parts.append(str(arg))
            elif isinstance(arg, str):
                arg = arg.replace("\\", r"\\").replace("\n", r"\n").replace('"', r"\"")
                parts.append(f'"{arg}"')
            else:
                parts.append(f'"{arg}"')
        return f"{self.name}({','.join(parts)})"

    def __repr__(self) -> str:
        return str(self)


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


def min_dupe_node(*, pkg: str) -> NodeId:
    """Given a package name, returns the "min_dupe_id" node in the ASP encoding.

    Args:
        pkg: name of a package
    """
    return NodeId(id="0", pkg=pkg)


class NodeFlag(NamedTuple):
    flag_type: str
    flag: str
    flag_group: str
    source: str


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
