# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Low-level wrappers around clingo API."""
import importlib
import pathlib
from typing import Callable, List, NamedTuple

from llnl.util import lang

import spack.config
import spack.paths as sp
import spack.util.path as sup


# backward compatibility functions for clingo ASTs
def ast_getter(*names):
    def getter(node):
        for name in names:
            result = getattr(node, name, None)
            if result:
                return result
        raise KeyError("node has no such keys: %s" % names)

    return getter


ast_type = ast_getter("ast_type", "type")
ast_sym = ast_getter("symbol", "term")


class AspObject:
    """Object representing a piece of ASP code."""


def _id(thing):
    """Quote string if needed for it to be a valid identifier."""
    if isinstance(thing, AspObject):
        return thing
    elif isinstance(thing, bool):
        return f'"{str(thing)}"'
    elif isinstance(thing, int):
        return str(thing)
    else:
        return f'"{str(thing)}"'


@lang.key_ordering
class AspFunction(AspObject):
    __slots__ = ["name", "args"]

    def __init__(self, name, args=None):
        self.name = name
        self.args = () if args is None else tuple(args)

    def _cmp_key(self):
        return self.name, self.args

    def __call__(self, *args):
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

    def argify(self, arg):
        if isinstance(arg, bool):
            return clingo().String(str(arg))
        elif isinstance(arg, int):
            return clingo().Number(arg)
        elif isinstance(arg, AspFunction):
            return clingo().Function(arg.name, [self.argify(x) for x in arg.args], positive=True)
        return clingo().String(str(arg))

    def symbol(self):
        return clingo().Function(self.name, [self.argify(arg) for arg in self.args], positive=True)

    def __str__(self):
        return f"{self.name}({', '.join(str(_id(arg)) for arg in self.args)})"

    def __repr__(self):
        return str(self)


class AspFunctionBuilder:
    def __getattr__(self, name):
        return AspFunction(name)


fn = AspFunctionBuilder()

TransformFunction = Callable[["spack.spec.Spec", List[AspFunction]], List[AspFunction]]


def clingo():
    try:
        clingo_mod = importlib.import_module("clingo")
    except ImportError:
        clingo_mod = None  # type: ignore
    except AttributeError:
        # Reaching this point indicates a broken clingo installation
        # If Spack derived clingo, suggest user re-run bootstrap
        # if non-spack, suggest user investigate installation

        # assume Spack is not responsible for broken clingo
        msg = (
            f"Clingo installation at {clingo_mod.__file__} is incomplete or invalid."
            "Please repair installation or re-install. "
            "Alternatively, consider installing clingo via Spack."
        )
        # check whether Spack is responsible
        if (
            pathlib.Path(
                sup.canonicalize_path(
                    spack.config.CONFIG.get("bootstrap:root", sp.default_user_bootstrap_path)
                )
            )
            in pathlib.Path(clingo_mod.__file__).parents
        ):
            # Spack is responsible for the broken clingo
            msg = (
                "Spack bootstrapped copy of Clingo is broken, "
                "please re-run the bootstrapping process via command `spack bootstrap now`."
                " If this issue persists, please file a bug at: github.com/spack/spack"
            )
        raise RuntimeError(
            "Clingo installation may be broken or incomplete, "
            "please verify clingo has been installed correctly"
            "\n\nClingo does not provide symbol clingo.Symbol"
            f"{msg}"
        )

    if clingo_mod:
        importlib.import_module("clingo.ast")
        return clingo_mod

    clingo_mod = _bootstrap_clingo()
    importlib.import_module("clingo.ast")
    return clingo_mod


def clingo_cffi():
    return hasattr(clingo(), "_rep")


def _bootstrap_clingo():
    import spack.bootstrap

    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_core_dependencies()
        clingo_mod = importlib.import_module("clingo")

    return clingo_mod


def parse_files(*args, **kwargs):
    clingo()
    try:
        return importlib.import_module("clingo.ast").parse_files(*args, **kwargs)
    except (ImportError, AttributeError):
        return clingo().parse_files(*args, **kwargs)


def parse_term(*args, **kwargs):
    clingo()
    try:
        return importlib.import_module("clingo.symbol").parse_term(*args, **kwargs)
    except (ImportError, AttributeError):
        return clingo().parse_term(*args, **kwargs)

    #     from clingo.ast import ASTType
    #
    #     try:
    #         from clingo.ast import parse_files
    #         from clingo.symbol import parse_term
    #     except ImportError:
    #         # older versions of clingo have this one namespace up
    #         from clingo import parse_files, parse_term
    #
    # return clingo


class NodeArgument(NamedTuple):
    id: str
    pkg: str


def intermediate_repr(sym):
    """Returns an intermediate representation of clingo models for Spack's spec builder.

    Currently, transforms symbols from clingo models either to strings or to NodeArgument objects.

    Returns:
        This will turn a ``clingo.Symbol`` into a string or NodeArgument, or a sequence of
        ``clingo.Symbol`` objects into a tuple of those objects.
    """
    # TODO: simplify this when we no longer have to support older clingo versions.
    if isinstance(sym, (list, tuple)):
        return tuple(intermediate_repr(a) for a in sym)

    try:
        if sym.name == "node":
            return NodeArgument(
                id=intermediate_repr(sym.arguments[0]), pkg=intermediate_repr(sym.arguments[1])
            )
    except RuntimeError:
        # This happens when using clingo w/ CFFI and trying to access ".name" for symbols
        # that are not functions
        pass

    if clingo_cffi():
        # Clingo w/ CFFI will throw an exception on failure
        try:
            return sym.string
        except RuntimeError:
            return str(sym)
    else:
        return sym.string or str(sym)


def extract_args(model, predicate_name):
    """Extract the arguments to predicates with the provided name from a model.

    Pull out all the predicates with name ``predicate_name`` from the model, and
    return their intermediate representation.
    """
    return [intermediate_repr(sym.arguments) for sym in model if sym.name == predicate_name]
