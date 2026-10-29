# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains code for creating environment modules, which can
include Tcl or Lua modules, and others.
"""

import warnings
from typing import Dict, List, Optional, Sequence, Set, Tuple, Type

import spack.config
import spack.error
import spack.repo
import spack.spec
import spack.store
from spack.util import tty

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


def _enabled_module_types() -> List[Tuple[str, str]]:
    """Returns the (module set name, module type) pairs enabled by the configuration, or no
    pair, with a warning, when the modules configuration is not valid."""
    try:
        return [
            (name, module_type)
            for name, module_set in spack.config.CONFIG.get("modules", {}).items()
            for module_type in module_set.get("enable") or []
        ]
    except spack.error.ConfigError as e:
        warnings.warn(
            "module files are not updated, as the modules configuration is not valid: "
            f"{e}. Fix it, then run 'spack module <type> refresh'"
        )
        return []


def _read_database() -> Optional[common.ModuleConfigurationCache]:
    """Returns a cache holding what the database records, or None, with a warning, when the
    database cannot be read."""
    cache = common.ModuleConfigurationCache()
    try:
        cache.read_database()
    except Exception as e:
        warnings.warn(
            "module files are not updated, as the database cannot be read "
            f"[{type(e).__name__}: {e}]"
        )
        return None
    return cache


def write_module_files(specs: Sequence[spack.spec.Spec]) -> None:
    """Writes the module files of installations recorded in the database, for every module set
    and type enabled by the configuration.

    A module file folding several of them is written once, since writing it for any one of
    them lists them all.
    """
    if not specs:
        return
    enabled = _enabled_module_types()
    cache = _read_database() if enabled else None
    if cache is None:
        return
    for name, module_type in enabled:
        written_filenames: Set[str] = set()
        for spec in specs:
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
    if not specs:
        return
    enabled = _enabled_module_types()
    cache = _read_database() if enabled else None
    if cache is None:
        return
    removed_specs = frozenset(specs)
    for name, module_type in enabled:
        updated_filenames: Set[str] = set()
        for spec in specs:
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
