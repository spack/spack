# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys

import spack.build_environment
import spack.config
import spack.util.environment as environment
import spack.util.prefix as prefix

#: Environment variable name Spack uses to track individually loaded packages
spack_loaded_hashes_var = 'SPACK_LOADED_HASHES'


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
    inspections = spack.config.get('modules:prefix_inspections', {})
    if inspections:
        return inspections

    inspections = {
        'bin': ['PATH'],
        'lib': ['LD_LIBRARY_PATH', 'LIBRARY_PATH'],
        'lib64': ['LD_LIBRARY_PATH', 'LIBRARY_PATH'],
        'man': ['MANPATH'],
        'share/man': ['MANPATH'],
        'share/aclocal': ['ACLOCAL_PATH'],
        'include': ['CPATH'],
        'lib/pkgconfig': ['PKG_CONFIG_PATH'],
        'lib64/pkgconfig': ['PKG_CONFIG_PATH'],
        'share/pkgconfig': ['PKG_CONFIG_PATH'],
        '': ['CMAKE_PREFIX_PATH']
    }

    if platform == 'darwin':
        for subdir in ('lib', 'lib64'):
            inspections[subdir].append('DYLD_FALLBACK_LIBRARY_PATH')

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
        spec.prefix,
        prefix_inspections(spec.platform),
        exclude=environment.is_system_path
    )

    # Let the extendee/dependency modify their extensions/dependents
    # before asking for package-specific modifications
    env.extend(
        spack.build_environment.modifications_from_dependencies(
            spec, context='run', set_package_py_globals=set_package_py_globals
        )
    )

    if set_package_py_globals:
        spack.build_environment.set_module_variables_for_package(spec.package)

    spec.package.setup_run_environment(env)

    return env
