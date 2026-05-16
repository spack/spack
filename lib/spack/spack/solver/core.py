# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Low-level wrappers around clingo API and other basic functionality related to ASP"""

import enum
import importlib
import pathlib
from types import ModuleType
from typing import Any, NamedTuple, Optional, Tuple

import spack.platforms
from spack.llnl.util import lang


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


class ClingoFlavor(enum.Enum):
    """The clingo Python API variant in use.

    Spack supports three: the legacy pre-CFFI API, the CFFI-based API (clingo ``@5.5:5``), and the
    clingo 6 rewrite, which restructured everything into submodules ``clingo.*``."""

    LEGACY = enum.auto()
    CFFI = enum.auto()
    V6 = enum.auto()


#: Process-global clingo module and its API flavor, both set once on first import.
_CLINGO_MODULE: Optional[ModuleType] = None
_CLINGO_FLAVOR: Optional[ClingoFlavor] = None


def clingo() -> ModuleType:
    """Lazy imports the Python module for clingo, and returns it."""
    if _CLINGO_MODULE is not None:
        return _CLINGO_MODULE

    try:
        clingo_mod = importlib.import_module("clingo")
        # Make sure we didn't import an empty module
        _ensure_clingo_or_raise(clingo_mod)
    except ImportError:
        clingo_mod = None

    if clingo_mod is not None:
        return _set_clingo_module_cache(clingo_mod)

    clingo_mod = _bootstrap_clingo()
    return _set_clingo_module_cache(clingo_mod)


def _set_clingo_module_cache(clingo_mod: ModuleType) -> ModuleType:
    """Caches the lazily-imported clingo module and detects its API flavor once."""
    global _CLINGO_MODULE, _CLINGO_FLAVOR
    importlib.import_module("clingo.ast")
    _CLINGO_FLAVOR = _detect_clingo_flavor(clingo_mod)
    _CLINGO_MODULE = clingo_mod
    return clingo_mod


def _detect_clingo_flavor(clingo_mod: ModuleType) -> ClingoFlavor:
    """Determine which of the three supported clingo Python APIs is in use."""
    if not hasattr(clingo_mod, "Control"):
        # clingo 6 dropped the top-level Control/Symbol.
        return ClingoFlavor.V6
    if hasattr(getattr(clingo_mod, "Symbol", None), "_rep"):
        return ClingoFlavor.CFFI
    return ClingoFlavor.LEGACY


def _ensure_clingo_or_raise(clingo_mod: ModuleType) -> None:
    """Ensures the clingo module can access expected attributes, otherwise raises an error."""
    # These are imports that may be problematic at top level (circular imports). They are used
    # only to provide exhaustive details when erroring due to a broken clingo module.
    import spack.config
    import spack.paths as sp
    import spack.util.path as sup

    try:
        clingo_mod.Symbol
    except AttributeError:
        # clingo 6 moved Symbol into the clingo.symbol submodule
        try:
            if importlib.import_module("clingo.symbol").Symbol is not None:
                return
        except (ImportError, AttributeError):
            pass
        assert clingo_mod.__file__ is not None, "clingo installation is incomplete or invalid"
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


def clingo_flavor() -> ClingoFlavor:
    """Return the cached :class:`ClingoFlavor` of the loaded clingo module.

    The flavor is detected exactly once, when clingo is first imported; callers
    dispatch off the cached value rather than re-probing the module.
    """
    if _CLINGO_FLAVOR is None:
        clingo()  # forces the import and the one-time flavor detection
    assert _CLINGO_FLAVOR is not None, "clingo flavor was not detected"
    return _CLINGO_FLAVOR


def _bootstrap_clingo() -> ModuleType:
    """Bootstraps the clingo module and returns it"""
    import spack.bootstrap

    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_clingo_importable_or_raise()
        clingo_mod = importlib.import_module("clingo")

    return clingo_mod


#: Process-global clingo 6 library object (lazily created)
_CLINGO_LIBRARY: Optional[Any] = None


def clingo_library() -> Any:
    """Return a process-global ``clingo.core.Library`` (clingo 6 only).

    A single shared library lets symbols produced by one control object be
    reused by another (e.g. when ``raise_if_errors`` feeds a model from the
    main solve into a second control object).
    """
    global _CLINGO_LIBRARY
    if _CLINGO_LIBRARY is None:
        clingo()  # ensure the clingo module is importable
        _CLINGO_LIBRARY = importlib.import_module("clingo.core").Library()
    return _CLINGO_LIBRARY


class _ClingoBackend:
    """Context manager adapting the clingo 6 backend to the legacy interface."""

    def __init__(self, manager: Any) -> None:
        self._manager = manager
        self._backend: Any = None

    def __enter__(self) -> "_ClingoBackend":
        self._backend = self._manager.__enter__()
        return self

    def __exit__(self, *exc_info) -> Any:
        return self._manager.__exit__(*exc_info)

    def add_atom(self, symbol: Any = None) -> int:
        return self._backend.atom(symbol)

    def add_rule(self, head: Any, body: Any = (), choice: bool = False) -> None:
        self._backend.rule(head, body, choice)


class _ClingoV6Control:
    """Adapter exposing the legacy clingo ``Control`` interface on top of the restructured clingo 6
    Python API.

    Only the subset of the API used by Spack's solver is implemented. This keeps ``asp.py``
    agnostic to which clingo version is in use; it is created through
    :func:`default_clingo_control` / :func:`make_error_control` rather than directly."""

    def __init__(self, options: Optional[Tuple[str, ...]] = None) -> None:
        control_mod = importlib.import_module("clingo.control")
        # clingo 6's grounder no longer implicitly projects anonymous variables
        # that occur only in negative body literals (older gringo did). Spack's
        # logic program relies on that behavior, so request it explicitly.
        control_options = ["--project-anonymous", *(options or ())]
        self._control = control_mod.Control(clingo_library(), control_options)

    def add(self, name: str, parameters: Tuple[str, ...], program: str) -> None:
        # Spack only ever adds the implicit "base" part without parameters.
        self._control.parse_string(program)

    def load(self, path: str) -> None:
        self._control.parse_files([path])

    def ground(self, parts: Any) -> None:
        # ``parts`` looks like ``[("base", [])]``; clingo 6 expects a sequence
        # of ``(name, [symbols])`` tuples.
        self._control.ground([(name, list(args)) for name, args in parts])

    def solve(self, on_model: Any = None, async_: bool = False) -> Any:
        # The returned async handle supports timed ``wait()`` / ``get()`` /
        # ``cancel()``, matching what ``_run_clingo`` expects.
        if async_:
            return self._control.start_solve(on_model=on_model, async_=True)
        return self._control.solve(on_model=on_model)

    def backend(self) -> _ClingoBackend:
        return _ClingoBackend(self._control.backend)

    @property
    def statistics(self) -> Any:
        # clingo 6 exposes a lazy StatsView; nestify() turns it into a plain
        # nested dict, matching what older clingo versions returned.
        return self._control.stats.nestify()


def _make_control(options: Tuple[str, ...] = ()) -> Any:
    """Create a clingo control object for the loaded clingo flavor.

    For clingo 6 the result is a :class:`_ClingoV6Control` adapter; for the
    legacy/CFFI APIs it is a raw ``clingo.Control``. Both expose the subset of
    the control interface Spack's solver relies on. ``options`` (command-line
    options) only apply to clingo 6 -- legacy/CFFI configure the solver through
    the ``.configuration`` attribute instead.
    """
    if clingo_flavor() is ClingoFlavor.V6:
        return _ClingoV6Control(options)
    return clingo().Control()


def default_clingo_control() -> Any:
    """Return a control object configured with Spack's default solver settings."""
    if clingo_flavor() is ClingoFlavor.V6:
        # clingo 6 has no `configuration` API; the equivalent settings are
        # passed as command line options instead.
        return _make_control(
            ("--configuration=tweety", "--heuristic=Domain", "--opt-strategy=usc")
        )
    control = _make_control()
    control.configuration.configuration = "tweety"
    control.configuration.solver.heuristic = "Domain"
    control.configuration.solver.opt_strategy = "usc"
    return control


def make_error_control() -> Any:
    """Return a plain control object, used to derive error causation on unsat."""
    return _make_control()


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
    # TODO: simplify this when we no longer have to support older clingo versions.
    if isinstance(sym, (list, tuple)):
        return tuple(intermediate_repr(a) for a in sym)

    try:
        if sym.name == "node":
            return NodeId(
                id=intermediate_repr(sym.arguments[0]), pkg=intermediate_repr(sym.arguments[1])
            )
        elif sym.name == "node_flag":
            return NodeFlag(
                flag_type=intermediate_repr(sym.arguments[0]),
                flag=intermediate_repr(sym.arguments[1]),
                flag_group=intermediate_repr(sym.arguments[2]),
                source=intermediate_repr(sym.arguments[3]),
            )
    except (RuntimeError, ValueError):
        # Accessing ".name" on a non-function symbol raises: RuntimeError with
        # clingo+CFFI, ValueError with clingo 6.
        pass

    if clingo_flavor() is ClingoFlavor.CFFI:
        # Clingo w/ CFFI throws RuntimeError on ".string" for a non-string symbol.
        try:
            return sym.string
        except RuntimeError:
            return str(sym)
    # Legacy clingo returns "" for non-string symbols; clingo 6 raises ValueError.
    try:
        return sym.string or str(sym)
    except (RuntimeError, ValueError):
        return str(sym)


def extract_args(model, predicate_name):
    """Extract the arguments to predicates with the provided name from a model.

    Pull out all the predicates with name ``predicate_name`` from the model, and
    return their intermediate representation.
    """

    def _matches(sym):
        try:
            return sym.name == predicate_name
        except (RuntimeError, ValueError):
            # ".name" raises for non-function symbols (CFFI / clingo 6)
            return False

    return [intermediate_repr(sym.arguments) for sym in model if _matches(sym)]


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
