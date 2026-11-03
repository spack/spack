# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains code for creating environment modules, which can
include Tcl or Lua modules, and others.
"""

import collections
import os
import warnings
from typing import Callable, Dict, List, Optional, Sequence, Set, Tuple, Type

import spack.config
import spack.error
import spack.repo
import spack.spec
import spack.store
from spack.util import tty
from spack.util.lang import dedupe

from . import common
from .common import BaseModuleFileWriter, disable_modules
from .error import ModuleNotFoundError
from .lmod import LmodModulefileWriter
from .tcl import TclModulefileWriter

__all__ = ["TclModulefileWriter", "LmodModulefileWriter", "disable_modules"]

module_types: Dict[str, Type[BaseModuleFileWriter]] = {
    "tcl": TclModulefileWriter,
    "lmod": LmodModulefileWriter,
}


def get_module(
    module_type: str,
    spec: spack.spec.Spec,
    get_full_path: bool,
    module_set_name: str = "default",
    required: bool = True,
    *,
    cache: Optional[common.ModuleConfigurationCache] = None,
) -> Optional[str]:
    """Retrieve the module file for a given spec and module type.

    Retrieve the module file for the given spec if it is available. If the
    module is not available, this will raise an exception unless the module
    is excluded or if the spec is installed upstream.

    Args:
        module_type: the type of module we want to retrieve (e.g. lmod)
        spec: refers to the installed package that we want to retrieve a module
            for
        required: if the module is required but excluded, this function will
            print a debug message. If a module is missing but not excluded,
            then an exception is raised (regardless of whether it is required)
        get_full_path: if ``True``, this returns the full path to the module.
            Otherwise, this returns the module name.
        module_set_name: the named module configuration set from modules.yaml
            for which to retrieve the module.
        cache: optional per-operation configuration cache, shared across a batch of specs to
            avoid recomputing configuration objects for shared dependencies.

    Returns:
        The module name or path. May return ``None`` if the module is not
        available.
    """
    try:
        upstream = spack.store.STORE.db.installed_upstream(spec)
    except spack.repo.UnknownPackageError:
        upstream, record = spack.store.STORE.db.query_by_spec_hash(spec.dag_hash())
    if upstream:
        module = common.upstream_module_index.upstream_module(spec, module_type)
        if not module:
            return None

        if get_full_path:
            return module.path
        else:
            return module.use_name
    else:
        writer = module_types[module_type].from_spec(spec, module_set_name, cache=cache)
        if not writer.has_installation:
            fmt_str = "{name}{@version}{/hash:7}"
            if not writer.conf.excluded:
                raise ModuleNotFoundError(
                    "The module for package {} should be at {}, but it does not exist".format(
                        spec.format(fmt_str), writer.layout.filename
                    )
                )
            elif required:
                tty.debug(
                    "The module configuration has excluded {}: omitting it".format(
                        spec.format(fmt_str)
                    )
                )
            else:
                return None

        if get_full_path:
            return writer.layout.filename
        else:
            return writer.layout.use_name


def _enabled_module_roots() -> Dict[str, List[Tuple[str, str]]]:
    """Returns the enabled (module set name, module type) pairs grouped by the real path of their
    module root, or an empty dict, with a warning, when the modules configuration is not
    valid.
    """
    by_root: Dict[str, List[Tuple[str, str]]] = collections.defaultdict(list)
    try:
        for name, module_set in spack.config.CONFIG.get("modules", {}).items():
            for module_type in module_set.get("enable") or []:
                by_root[os.path.realpath(common.root_path(module_type, name))].append(
                    (name, module_type)
                )
    except spack.error.ConfigError as e:
        warnings.warn(
            "module files are not updated, as the modules configuration is not valid: "
            f"{e}. Fix it, then run 'spack module <type> refresh'"
        )
        return {}
    return by_root


def _update_module_roots(specs: Sequence[spack.spec.Spec], update: Callable[..., None]) -> None:
    """Calls ``update`` for each enabled module root, holding the lock of the root."""
    if not specs:
        return

    for root, enabled in _enabled_module_roots().items():
        try:
            with common.module_root_transaction(root) as cache:
                update(specs, enabled, cache)
        except Exception as e:
            refresh = " or ".join(
                f"'spack module {t} refresh'" for t in dedupe(t for _, t in enabled)
            )
            warnings.warn(
                f"module files under {root} are not updated [{type(e).__name__}: {e}]. "
                f"Run {refresh} once the cause is fixed"
            )


def write_module_files(specs: Sequence[spack.spec.Spec]) -> None:
    """Writes the module files of the specs, for every enabled module set and type.

    Specs that the database does not record as installed are skipped. A module file shared by
    several specs is written only once, since it lists all of them.
    """
    _update_module_roots(specs, _write_module_files)


def _write_module_files(
    specs: Sequence[spack.spec.Spec],
    enabled: List[Tuple[str, str]],
    cache: common.ModuleConfigurationCache,
) -> None:
    installed = [s for s in specs if cache.installed(s)]
    for name, module_type in enabled:
        written_filenames: Set[str] = set()
        for spec in installed:
            try:
                writer = module_types[module_type].from_spec(spec, name, cache=cache)
                # An excluded installation does not write the module file of its siblings
                if writer.conf.excluded:
                    continue
                filename = writer.layout.filename
                if filename in written_filenames and writer.has_other_installations:
                    continue
                writer.write()
                written_filenames.add(filename)
            except Exception as e:
                warnings.warn(
                    f"cannot write the {module_type} module file of "
                    f"{spec.format('{name}{@version}{/hash:7}')} in module set '{name}' "
                    f"[{type(e).__name__}: {e}]"
                )


def remove_module_files(specs: Sequence[spack.spec.Spec]) -> None:
    """Removes installations removed from the database from their module files, for every
    module set and type enabled by the configuration.

    A module file holding several of them is updated once.
    """
    _update_module_roots(specs, _remove_module_files)


def _remove_module_files(
    specs: Sequence[spack.spec.Spec],
    enabled: List[Tuple[str, str]],
    cache: common.ModuleConfigurationCache,
) -> None:
    removed = [s for s in specs if not cache.installed(s)]
    removed_specs = frozenset(removed)
    for name, module_type in enabled:
        updated_filenames: Set[str] = set()
        for spec in removed:
            try:
                writer = module_types[module_type].from_spec(
                    spec, name, removed_specs=removed_specs, cache=cache
                )
                filename = writer.layout.filename
                if filename in updated_filenames:
                    continue
                writer.remove_installation()
                updated_filenames.add(filename)
            except Exception as e:
                warnings.warn(
                    f"cannot remove {spec.format('{name}{@version}{/hash:7}')} from its "
                    f"{module_type} module file in module set '{name}' "
                    f"[{type(e).__name__}: {e}]"
                )
