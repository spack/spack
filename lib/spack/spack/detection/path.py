# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import os
import os.path
import re

import six

import llnl.util.filesystem
import llnl.util.tty as tty
import spack.util.environment


def system_executables(path_hints=None):
    """Get the paths of all executables available from the current PATH.

    For convenience, this is constructed as a dictionary where the keys are
    the executable paths and the values are the names of the executables
    (i.e. the basename of the executable path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the executable.
    """
    path_hints = path_hints or spack.util.environment.get_path('PATH')
    search_paths = llnl.util.filesystem.search_paths_for_executables(
        *path_hints)

    path_to_exe = {}
    # Reverse order of search directories so that an exe in the first PATH
    # entry overrides later entries
    for search_path in reversed(search_paths):
        for exe in os.listdir(search_path):
            exe_path = os.path.join(search_path, exe)
            if llnl.util.filesystem.is_exe(exe_path):
                path_to_exe[exe_path] = exe
    return path_to_exe


def detect(packages_to_check, system_path_to_exe=None):
    """Detect external packages based on path inspection.

    Args:
        packages_to_check (list): list of packages to be searched for
        system_path_to_exe (dict): dictionary mapping an absolute path
            to an executable to its basename

    Returns:
        Dictionary mapping a package name to the list of specs that were
        detected for it.
    """
    if not system_path_to_exe:
        system_path_to_exe = system_executables()

    pkg_to_found_exes = executables_by_package(
        packages_to_check, system_path_to_exe
    )

    pkg_to_entries = collections.defaultdict(list)
    resolved_specs = {}  # spec -> exe found for the spec

    for pkg, exes in pkg_to_found_exes.items():
        if not hasattr(pkg, 'determine_spec_details'):
            tty.warn("{0} must define 'determine_spec_details' in order"
                     " for Spack to detect externally-provided instances"
                     " of the package.".format(pkg.name))
            continue

        # TODO: iterate through this in a predetermined order (e.g. by package
        # name) to get repeatable results when there are conflicts. Note that
        # if we take the prefixes returned by _group_by_prefix, then consider
        # them in the order that they appear in PATH, this should be sufficient
        # to get repeatable results.
        for prefix, exes_in_prefix in _group_by_prefix(exes):
            # TODO: multiple instances of a package can live in the same
            # prefix, and a package implementation can return multiple specs
            # for one prefix, but without additional details (e.g. about the
            # naming scheme which differentiates them), the spec won't be
            # usable.
            specs = _convert_to_iterable(
                pkg.determine_spec_details(prefix, exes_in_prefix)
            )

            if not specs:
                tty.debug(
                    'The following executables in {0} were decidedly not'
                    'part of the package {1}: {2}'
                    .format(prefix, pkg.name, ', '.join(exes_in_prefix))
                )

            for spec in specs:
                spec.external_path = (spec.external_path or
                                      _determine_base_dir(prefix))

                if not spec.external_path:
                    tty.debug('{0} does not have a "bin" directory: it'
                              ' cannot be added as a Spack package'
                              .format(prefix))
                    continue

                if spec in resolved_specs:
                    prior_prefix = resolved_specs[spec]

                    tty.debug(
                        "Executables in {0} and {1} are both associated"
                        " with the same spec {2}"
                        .format(prefix, prior_prefix, str(spec)))
                    continue
                else:
                    resolved_specs[spec] = prefix

                try:
                    spec.validate_detection()
                except Exception as e:
                    msg = ('"{0}" has been detected on the system but will '
                           'not be added to packages.yaml [{1}]')
                    tty.warn(msg.format(spec, str(e)))
                    continue
                pkg_to_entries[pkg.name].append(spec)

    return pkg_to_entries


def executables_by_package(packages_to_check, system_path_to_exe):
    """Map packages to a list of executables that might be related
    to each package.

    Args:
        packages_to_check (list): list of packages to be checked
        system_path_to_exe (dict): dictionary mapping an absolute path
            to an executable to its basename

    Returns:
        Dictionary from a package to a list of executables to be
        inspected.
    """
    exe_pattern_to_pkgs = collections.defaultdict(list)
    for pkg in packages_to_check:
        if hasattr(pkg, 'executables'):
            for exe in pkg.executables:
                exe_pattern_to_pkgs[exe].append(pkg)
    pkg_to_found_exes = collections.defaultdict(set)
    for exe_pattern, pkgs in exe_pattern_to_pkgs.items():
        compiled_re = re.compile(exe_pattern)
        for path, exe in system_path_to_exe.items():
            if compiled_re.search(exe):
                for pkg in pkgs:
                    pkg_to_found_exes[pkg].add(path)
    return pkg_to_found_exes


def _group_by_prefix(paths):
    groups = collections.defaultdict(set)
    for p in paths:
        groups[os.path.dirname(p)].add(p)
    return groups.items()


def _convert_to_iterable(single_val_or_multiple):
    x = single_val_or_multiple
    if x is None:
        return []
    elif isinstance(x, six.string_types):
        return [x]
    elif isinstance(x, spack.spec.Spec):
        # Specs are iterable, but a single spec should be converted to a list
        return [x]

    try:
        iter(x)
        return x
    except TypeError:
        return [x]


def _determine_base_dir(prefix):
    # Given a prefix where an executable is found, assuming that prefix
    # contains /bin/, strip off the 'bin' directory to get a Spack-compatible
    # prefix
    assert os.path.isdir(prefix)

    components = prefix.split(os.sep)
    if 'bin' not in components:
        return None
    idx = components.index('bin')
    return os.sep.join(components[:idx])
