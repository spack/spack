# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import sys
from typing import Iterable, List, Mapping

import spack.build_environment
import spack.config
import spack.spec
import spack.util.undo_record as undo_record
from spack import traverse
from spack.enums import Context
from spack.util import environment
from spack.util.lang import dedupe

#: Environment variable name Spack uses to track individually loaded packages
spack_loaded_hashes_var = "SPACK_LOADED_HASHES"

#: Kind of the undo record units holding the changes made by loading a spec
_LOAD_KIND = "load"


def prefix_inspections(platform: str) -> dict:
    """Get list of prefix inspections for platform

    Arguments:
        platform: the name of the platform to consider. The platform determines what environment
            variables Spack will use for some inspections.

    Returns:
        A dictionary mapping subdirectory names to lists of environment variables to modify with
        that directory if it exists.
    """
    inspections = spack.config.CONFIG.get("modules:prefix_inspections")
    if isinstance(inspections, dict):
        return inspections

    inspections = {
        "bin": ["PATH"],
        "man": ["MANPATH"],
        "share/man": ["MANPATH"],
        "share/aclocal": ["ACLOCAL_PATH"],
        "lib/pkgconfig": ["PKG_CONFIG_PATH"],
        "lib64/pkgconfig": ["PKG_CONFIG_PATH"],
        "share/pkgconfig": ["PKG_CONFIG_PATH"],
        "": ["CMAKE_PREFIX_PATH"],
    }

    if platform == "darwin":
        inspections["lib"] = ["DYLD_FALLBACK_LIBRARY_PATH"]
        inspections["lib64"] = ["DYLD_FALLBACK_LIBRARY_PATH"]

    return inspections


def unconditional_environment_modifications(view):
    """List of environment (shell) modifications to be processed for view.

    This list does not depend on the specs in this environment"""
    env = environment.EnvironmentModifications()

    for subdir, vars in prefix_inspections(sys.platform).items():
        full_subdir = os.path.join(view.root, subdir)
        for var in vars:
            env.prepend_path(var, full_subdir)

    return env


def project_env_mods(
    *specs: spack.spec.Spec, view, env: environment.EnvironmentModifications
) -> None:
    """Given a list of environment modifications, project paths changes to the view."""
    prefix_to_prefix = {
        str(s.prefix): view.get_projection_for_spec(s) for s in specs if not s.external
    }
    # Avoid empty regex if all external
    if not prefix_to_prefix:
        return
    prefix_regex = re.compile("|".join(re.escape(p) for p in prefix_to_prefix.keys()))
    for mod in env.env_modifications:
        if isinstance(mod, environment.NameValueModifier):
            mod.value = prefix_regex.sub(lambda m: prefix_to_prefix[m.group(0)], mod.value)


def environment_modifications_for_specs(
    *specs: spack.spec.Spec, view=None, set_package_py_globals: bool = True
):
    """List of environment (shell) modifications to be processed for spec.

    This list is specific to the location of the spec or its projection in
    the view.

    Args:
        specs: spec(s) for which to list the environment modifications
        view: view associated with the spec passed as first argument
        set_package_py_globals: whether or not to set the global variables in the
            package.py files (this may be problematic when using buildcaches that have
            been built on a different but compatible OS)
    """
    env = environment.EnvironmentModifications()
    topo_ordered = list(
        traverse.traverse_nodes(specs, root=True, deptype=("run", "link"), order="topo")
    )

    # Static environment changes (prefix inspections)
    for s in reversed(topo_ordered):
        static = environment.inspect_path(
            s.prefix, prefix_inspections(s.platform), exclude=environment.is_system_path
        )
        env.extend(static)

    # Dynamic environment changes (setup_run_environment etc)
    setup_context = spack.build_environment.SetupContext(*specs, context=Context.RUN)
    if set_package_py_globals:
        setup_context.set_all_package_py_globals()
    env.extend(setup_context.get_env_modifications())

    # Apply view projections if any.
    if view:
        project_env_mods(*topo_ordered, view=view, env=env)

    return env


def _load_key(dag_hash: str) -> str:
    return f"{_LOAD_KIND}:{dag_hash}"


def loaded_hashes(environ: Mapping[str, str]) -> List[str]:
    """Returns the hashes of the loaded specs listed in ``environ``, most recently loaded first,
    without duplicates.
    """
    return list(dedupe(h for h in environ.get(spack_loaded_hashes_var, "").split(os.pathsep) if h))


def unloaded_keys(record: undo_record.UndoRecord, environ: Mapping[str, str]) -> List[str]:
    """Returns the keys of the load units of specs that ``environ`` does not list as loaded, which
    were unloaded outside the record.
    """
    loaded = {_load_key(h) for h in loaded_hashes(environ)}
    return [u.key for u in record.units if u.kind == _LOAD_KIND and u.key not in loaded]


def load(record: undo_record.UndoRecord, spec: spack.spec.Spec) -> None:
    """Pushes the environment modifications of ``spec`` on the undo record of the shell. A spec
    that is already loaded is moved to the top of the stack, with its modifications computed
    again.
    """
    modifications = environment_modifications_for_specs(spec)
    record.push(
        undo_record.Unit(
            _load_key(spec.dag_hash()), undo_record.ops_from_modifications(modifications)
        )
    )


def unload(record: undo_record.UndoRecord, dag_hash: str) -> bool:
    """Removes the unit of the spec with ``dag_hash`` from the undo record of the shell. Returns
    False if the spec was loaded without a record (by an older Spack, or before the shell was
    updated), so that its changes cannot be undone.
    """
    return record.remove(_load_key(dag_hash))


def shell_commands(
    record: undo_record.UndoRecord, shell: str, unloaded: Iterable[str] = ()
) -> str:
    """Returns the shell code that makes the shell environment match the record.

    The specs listed as loaded are those with a unit on the record, most recently loaded first,
    followed by those the shell lists without a unit, loaded without a record, except the hashes
    in ``unloaded``. Raises EnvironmentTooLargeError if the new environment would be too large to
    start processes.
    """
    hashes = [u.name for u in reversed(record.units) if u.kind == _LOAD_KIND]
    skip = set(hashes).union(unloaded)
    hashes.extend(h for h in loaded_hashes(record.environ) if h not in skip)
    return record.shell_commands(shell, {spack_loaded_hashes_var: os.pathsep.join(hashes) or None})
