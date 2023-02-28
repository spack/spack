# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys
from collections import defaultdict
from enum import Flag, auto

import spack.build_environment
import spack.config
import spack.util.environment as environment
import spack.util.prefix as prefix
from spack import traverse

#: Environment variable name Spack uses to track individually loaded packages
spack_loaded_hashes_var = "SPACK_LOADED_HASHES"


def prefix_inspections(platform):
    """Get list of prefix inspections for platform

    Arguments:
        platform (str): the name of the platform to consider. The platform
            determines what environment variables Spack will use for some
            inspections.

    Returns:
        A dictionary mapping subdirectory names to lists of environment
            variables to modify with that directory if it exists.
    """
    inspections = spack.config.get("modules:prefix_inspections")
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


def environment_modifications_for_spec(spec, view=None, set_package_py_globals=True):
    """List of environment (shell) modifications to be processed for spec.

    This list is specific to the location of the spec or its projection in
    the view.

    Args:
        spec (spack.spec.Spec): spec for which to list the environment modifications
        view: view associated with the spec passed as first argument
        set_package_py_globals (bool): whether or not to set the global variables in the
            package.py files (this may be problematic when using buildcaches that have
            been built on a different but compatible OS)
    """
    spec = spec.copy()
    if view and not spec.external:
        spec.prefix = prefix.Prefix(view.get_projection_for_spec(spec))

    # generic environment modifications determined by inspecting the spec
    # prefix
    env = environment.inspect_path(
        spec.prefix, prefix_inspections(spec.platform), exclude=environment.is_system_path
    )

    # Let the extendee/dependency modify their extensions/dependents
    # before asking for package-specific modifications
    env.extend(
        spack.build_environment.modifications_from_dependencies(
            spec, context="run", set_package_py_globals=set_package_py_globals
        )
    )

    if set_package_py_globals:
        spack.build_environment.set_module_variables_for_package(spec.package)

    spec.package.setup_run_environment(env)

    return env


class EnvironmentVisitor:
    def __init__(self, roots: list, context: str):
        # For the roots (well, marked specs) we follow different edges
        # than for their deps, depending on the context.
        self.root_hashes = set(s.dag_hash() for s in roots)

        if context == "build":
            # Drop direct run deps in build context
            # We don't really distinguish between install and build time test deps,
            # so we include them here as build-time test deps.
            self.root_deptypes = ["build", "test", "link"]
        elif context == "test":
            # This is more of an extended run environment
            self.root_deptypes = ["test", "run", "link"]
        elif context == "run":
            self.root_deptypes = ["run", "link"]
        else:
            raise ValueError(f"Unknown context {context}. Should be one of build, test, run")

    def neighbors(self, item):
        spec = item.edge.spec
        if spec.dag_hash() in self.root_hashes:
            deptype = self.root_deptypes
        else:
            deptype = ("link", "run")
        return traverse.sort_edges(spec.edges_to_dependencies(deptype=deptype))


class Mode(Flag):
    # Entrypoint spec (a spec to be built; an env root, etc)
    ROOT = auto()

    # A spec used at runtime, but no executables in PATH
    RUNTIME = auto()

    # A spec used at runtime, with executables in PATH
    RUNTIME_EXECUTABLE = auto()

    # A spec that's a direct build or test dep
    BUILDTIME_DIRECT = auto()

    # A spec that should be visible in search paths in a build env.
    BUILDTIME = auto()

    # Flag is set when the (node, mode) is finalized
    ADDED = auto()


def effective_deptypes(specs: list, context="build"):
    """
    Given a list of input specs and a context, return a list of tuples of
    all specs that contribute to (environment) modifications, together with
    a flag specifying in what way they do so. The list is ordered topologically
    from root to leaf, meaning that environment modifications should be applied
    in reverse so that dependents override dependencies, not the other way around.
    """
    assert context in ("build", "run", "test")

    visitor = traverse.TopoVisitor(
        EnvironmentVisitor(specs, context), key=lambda x: x.dag_hash(), root=True, all_edges=True
    )
    traverse.traverse_depth_first_with_visitor(traverse.with_artificial_edges(specs), visitor)

    modes = defaultdict(lambda: Mode(0))
    nodes_with_type = []

    for edge in visitor.edges:
        key = edge.spec

        # Mark the starting point
        if edge.parent is None:
            modes[key] = Mode.ROOT
            continue

        mode = modes[edge.parent]

        # Nothing to propagate.
        if not mode:
            continue

        # Dependending on the context, include particular deps from the root.
        if Mode.ROOT in mode:
            if context == "build":
                if "build" in edge.deptypes or "test" in edge.deptypes:
                    modes[key] |= Mode.BUILDTIME_DIRECT
                if "link" in edge.deptypes:
                    modes[key] |= Mode.BUILDTIME

            elif context == "test":
                if "run" in edge.deptypes or "test" in edge.deptypes:
                    modes[key] |= Mode.RUNTIME_EXECUTABLE
                elif "link" in edge.deptypes:
                    modes[key] |= Mode.RUNTIME

            elif context == "run":
                if "run" in edge.deptypes:
                    modes[key] |= Mode.RUNTIME_EXECUTABLE
                elif "link" in edge.deptypes:
                    modes[key] |= Mode.RUNTIME

        # Propagate RUNTIME and RUNTIME_EXECUTABLE through link and run deps.
        if (Mode.RUNTIME | Mode.RUNTIME_EXECUTABLE | Mode.BUILDTIME_DIRECT) & mode:
            if "link" in edge.deptypes:
                modes[key] |= Mode.RUNTIME
            if "run" in edge.deptypes:
                modes[key] |= Mode.RUNTIME_EXECUTABLE

        # Propagate BUILDTIME through link deps.
        if Mode.BUILDTIME in mode:
            if "link" in edge.deptypes:
                modes[key] |= Mode.BUILDTIME

        # Finalize the spec; the invariant is that all in-edges are processed
        # before out-edges, meaning that edge.parent is done.
        if Mode.ADDED not in mode:
            modes[edge.parent] |= Mode.ADDED
            nodes_with_type.append((edge.parent, mode))

    # Attach the leaf nodes, since we only added nodes
    # with out-edges. Can this be improved?
    for spec, mode in modes.items():
        if mode and Mode.ADDED not in mode:
            nodes_with_type.append((spec, mode))

    return nodes_with_type
