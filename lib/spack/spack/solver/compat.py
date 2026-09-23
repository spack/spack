# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Loads clingo and abstracts over the differences between its Python API variants.

Spack supports three clingo Python APIs: the pre-CFFI API, the CFFI-based API, and the clingo 6
rewrite, which moved everything into ``clingo.*`` submodules, replaced the top-level ``Control``
constructor with one that takes a shared ``Library`` plus CLI options, renamed backend methods
(``add_atom``/``add_rule`` to ``atom``/``rule``), and made statistics a lazy view that must be
``nestify()``-ed.

This module bootstraps/imports the right clingo and exposes a single uniform interface (a
legacy-shaped ``Control`` plus ``symbol_name`` / ``symbol_string`` helpers) so the rest of Spack
does not have to branch on the flavor in use.
"""

import enum
import functools
import importlib
import pathlib
from types import ModuleType
from typing import Any, Optional, Tuple

#: Process-global cache of the lazily-imported clingo module.
_CLINGO_MODULE: Optional[ModuleType] = None


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
    """Cache the lazily-imported clingo module."""
    global _CLINGO_MODULE
    importlib.import_module("clingo.ast")
    _CLINGO_MODULE = clingo_mod
    return clingo_mod


def _ensure_clingo_or_raise(clingo_mod: ModuleType) -> None:
    """Ensures the clingo module can access expected attributes, otherwise raises an error."""
    # These are imports that may be problematic at top level (circular imports). They are used
    # only to provide exhaustive details when erroring due to a broken clingo module.
    import spack.config
    import spack.paths as sp

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
                spack.config.canonicalize_path(
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


def _bootstrap_clingo() -> ModuleType:
    """Bootstraps the clingo module and returns it"""
    import spack.bootstrap

    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_clingo_importable_or_raise()
        clingo_mod = importlib.import_module("clingo")

    return clingo_mod


class ClingoFlavor(enum.Enum):
    """The clingo Python API variant in use.

    Spack supports three: the legacy pre-CFFI API, the CFFI-based API (clingo ``@5.5:5``), and the
    clingo 6 rewrite, which restructured everything into submodules ``clingo.*``."""

    LEGACY = enum.auto()
    CFFI = enum.auto()
    V6 = enum.auto()


def _detect_clingo_flavor(clingo_mod: ModuleType) -> ClingoFlavor:
    """Determine which of the three supported clingo Python APIs is in use."""
    if not hasattr(clingo_mod, "Control"):
        # clingo 6 dropped the top-level Control/Symbol.
        return ClingoFlavor.V6
    if hasattr(getattr(clingo_mod, "Symbol", None), "_rep"):
        return ClingoFlavor.CFFI
    return ClingoFlavor.LEGACY


@functools.lru_cache(maxsize=None)
def clingo_flavor() -> ClingoFlavor:
    """Return the :class:`ClingoFlavor` of the loaded clingo module (detected once)."""
    return _detect_clingo_flavor(clingo())


@functools.lru_cache(maxsize=None)
def clingo_library() -> Any:
    """Return a process-global ``clingo.core.Library`` (clingo 6 only).

    A single shared library lets symbols produced by one control object be reused by another
    (e.g. when ``raise_if_errors`` feeds a model from the main solve into a second control).
    """
    clingo()  # ensure the clingo module is importable / bootstrapped
    return importlib.import_module("clingo.core").Library()


def symbol_name(sym: Any) -> Optional[str]:
    """Return ``sym.name`` if ``sym`` is a function symbol, otherwise ``None``.

    Non-function symbols raise ``RuntimeError`` on clingo+CFFI and ``ValueError`` on clingo 6;
    legacy clingo returns an empty string.
    """
    try:
        return sym.name or None
    except (RuntimeError, ValueError):
        return None


def symbol_string(sym: Any) -> str:
    """Return ``sym.string`` for a string symbol, otherwise ``str(sym)``."""
    if clingo_flavor() is ClingoFlavor.CFFI:
        # CFFI throws RuntimeError on ".string" for non-string symbols.
        try:
            return sym.string
        except RuntimeError:
            return str(sym)
    # Legacy returns "" for non-string symbols; clingo 6 raises ValueError.
    try:
        return sym.string or str(sym)
    except (RuntimeError, ValueError):
        return str(sym)


class _ClingoBackend:
    """Context manager adapting the clingo 6 backend to the legacy interface."""

    __slots__ = ("_manager", "_backend")

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
    """Adapter exposing the legacy clingo ``Control`` interface on top of the restructured clingo
    6 Python API. Only the subset of the API used by Spack's solver is implemented; instantiate
    via :func:`default_clingo_control` / :func:`make_error_control`."""

    __slots__ = ("_control",)

    def __init__(self, options: Tuple[str, ...] = ()) -> None:
        control_mod = importlib.import_module("clingo.control")
        self._control = control_mod.Control(clingo_library(), list(options))

    def add(self, name: str, parameters: Tuple[str, ...], program: str) -> None:
        # Spack only ever adds the implicit "base" part without parameters.
        self._control.parse_string(program)

    def load(self, path: str) -> None:
        self._control.parse_files([path])

    def ground(self, parts: Any) -> None:
        self._control.ground([(name, list(args)) for name, args in parts])

    def solve(self, on_model: Any = None, async_: bool = False) -> Any:
        if async_:
            return self._control.start_solve(on_model=on_model, async_=True)
        return self._control.solve(on_model=on_model)

    def backend(self) -> _ClingoBackend:
        return _ClingoBackend(self._control.backend)

    @property
    def statistics(self) -> Any:
        # clingo 6 returns a lazy StatsView; nestify() yields the plain dict older versions did.
        return self._control.stats.nestify()


def default_clingo_control() -> Any:
    """Return a control object configured with Spack's default solver settings."""
    if clingo_flavor() is ClingoFlavor.V6:
        # clingo 6 has no `.configuration` API; pass equivalents as CLI options.
        return _ClingoV6Control(
            ("--configuration=tweety", "--heuristic=Domain", "--opt-strategy=usc")
        )
    control = clingo().Control()
    control.configuration.configuration = "tweety"
    control.configuration.solver.heuristic = "Domain"
    control.configuration.solver.opt_strategy = "usc"
    return control


def make_error_control() -> Any:
    """Return a plain control object, used to derive error causation on unsat."""
    if clingo_flavor() is ClingoFlavor.V6:
        return _ClingoV6Control()
    return clingo().Control()
