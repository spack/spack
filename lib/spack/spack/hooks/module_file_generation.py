# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import warnings
from typing import Iterator, Sequence, Set, Tuple

import spack.config
import spack.modules
import spack.modules.common
import spack.spec
from spack.util import tty


def _enabled_module_types() -> Iterator[Tuple[str, str]]:
    """Yields the (module set name, module type) pairs enabled by the configuration."""
    set_names: Set[str] = set(spack.config.CONFIG.get("modules", {}).keys())
    for name in set_names:
        enabled = spack.config.CONFIG.get(f"modules:{name}:enable")
        if not enabled:
            tty.debug("NO MODULE WRITTEN: list of enabled module files is empty")
            continue

        for module_type in enabled:
            yield name, module_type


def post_database_add(specs: Sequence[spack.spec.Spec]) -> None:
    """Writes the module files of the installations just recorded in the database. A module
    file folding several of them is written once, as it lists them all whichever is written.

    Every spec is attempted: an error raised for one of them is reported as a warning.
    """
    for name, module_type in _enabled_module_types():
        cache: spack.modules.common.ModuleConfigurationCache = {}
        written_filenames: Set[str] = set()
        for spec in specs:
            try:
                writer = spack.modules.module_types[module_type].from_spec(spec, name, cache=cache)
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


def post_database_remove(specs: Sequence[spack.spec.Spec]) -> None:
    """Removes the installations just removed from the database from their module files. A
    module file holding several of them is updated once.

    Every spec is attempted: an error raised for one of them is reported as a warning."""
    removed_specs = tuple(specs)
    for name, module_type in _enabled_module_types():
        cache: spack.modules.common.ModuleConfigurationCache = {}
        updated_filenames: Set[str] = set()
        for spec in specs:
            try:
                writer = spack.modules.module_types[module_type].from_spec(
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
