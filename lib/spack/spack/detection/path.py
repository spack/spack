# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detection of software installed in the system based on paths inspections
and running executables.
"""
import collections
import os
import os.path
import re
import sys
import warnings

import llnl.util.filesystem
import llnl.util.tty

import spack.operating_systems.windows_os as winOs
import spack.util.environment

from .common import (
    DetectedPackage,
    _convert_to_iterable,
    compute_windows_program_path_for_package,
    executable_prefix,
    find_win32_additional_install_paths,
    library_prefix,
    is_executable,
    is_readable,
    library_prefix,
)


def executables_in_path(path_hints=None):
    """Get the paths of all executables available from the current PATH.

    For convenience, this is constructed as a dictionary where the keys are
    the executable paths and the values are the names of the executables
    (i.e. the basename of the executable path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the executable.

    Args:
        path_hints (list): list of paths to be searched. If None the list will be
            constructed based on the PATH environment variable.
    """
    # If we're on a Windows box, run vswhere,
    # steal the installationPath using windows_os.py logic,
    # construct paths to CMake and Ninja, add to PATH
    path_hints = path_hints or spack.util.environment.get_path('PATH')
    if sys.platform == 'win32':
        msvc_paths = list(winOs.WindowsOs.vs_install_paths)
        msvc_cmake_paths = [
            os.path.join(path, "Common7", "IDE", "CommonExtensions", "Microsoft",
                         "CMake", "CMake", "bin")
            for path in msvc_paths]
        path_hints = msvc_cmake_paths + path_hints
        msvc_ninja_paths = [
            os.path.join(path, "Common7", "IDE", "CommonExtensions", "Microsoft",
                         "CMake", "Ninja")
            for path in msvc_paths]
        path_hints = msvc_ninja_paths + path_hints
        path_hints.extend(find_win32_additional_install_paths())
    search_paths = llnl.util.filesystem.search_paths_for_executables(*path_hints)

    path_to_exe = {}
    # Reverse order of search directories so that an exe in the first PATH
    # entry overrides later entries
    for search_path in reversed(search_paths):
        for exe in os.listdir(search_path):
            exe_path = os.path.join(search_path, exe)
            if is_executable(exe_path):
                path_to_exe[exe_path] = exe
    return path_to_exe


def libraries_in_ld_library_path(path_hints=None):
    """Get the paths of all libraries available from LD_LIBRARY_PATH.

    For convenience, this is constructed as a dictionary where the keys are
    the library paths and the values are the names of the libraries
    (i.e. the basename of the library path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the library.

    Args:
        path_hints (list): list of paths to be searched. If None the list will be
            constructed based on the LD_LIBRARY_PATH environment variable.
    """
    path_hints = path_hints or spack.util.environment.get_path('LD_LIBRARY_PATH')
    search_paths = llnl.util.filesystem.search_paths_for_libraries(*path_hints)

    path_to_lib = {}
    # Reverse order of search directories so that a lib in the first PATH
    # entry overrides later entries
    for search_path in reversed(search_paths):
        for lib in os.listdir(search_path):
            lib_path = os.path.join(search_path, lib)
            if is_readable(lib_path):
                path_to_lib[lib_path] = lib
    return path_to_lib


def _group_by_prefix(paths):
    groups = collections.defaultdict(set)
    for p in paths:
        groups[os.path.dirname(p)].add(p)
    return groups.items()


def by_library(packages_to_check, path_hints=None):
    # Techniques for finding libraries is determined on a per recipe basis in
    # the determine_version class method. Some packages will extract the
    # version number from a shared libraries filename.
    # Other libraries could use the strings function to extract it as described
    # in https://unix.stackexchange.com/questions/58846/viewing-linux-library-executable-version-info
    """Return the list of packages that have been detected on the system,
    searching by LD_LIBRARY_PATH.

    Args:
        packages_to_check (list): list of packages to be detected
        path_hints (list): list of paths to be searched. If None the list will be
            constructed based on the LD_LIBRARY_PATH environment variable.
    """
    path_to_lib_name = libraries_in_ld_library_path(path_hints=path_hints)
    lib_pattern_to_pkgs = collections.defaultdict(list)
    for pkg in packages_to_check:
        if hasattr(pkg, 'libraries'):
            for lib in pkg.libraries:
                lib_pattern_to_pkgs[lib].append(pkg)

    pkg_to_found_libs = collections.defaultdict(set)
    for lib_pattern, pkgs in lib_pattern_to_pkgs.items():
        compiled_re = re.compile(lib_pattern)
        for path, lib in path_to_lib_name.items():
            if compiled_re.search(lib):
                for pkg in pkgs:
                    pkg_to_found_libs[pkg].add(path)

    pkg_to_entries = collections.defaultdict(list)
    resolved_specs = {}  # spec -> lib found for the spec

    for pkg, libs in pkg_to_found_libs.items():
        if not hasattr(pkg, 'determine_spec_details'):
            llnl.util.tty.warn(
                "{0} must define 'determine_spec_details' in order"
                " for Spack to detect externally-provided instances"
                " of the package.".format(pkg.name))
            continue

        for prefix, libs_in_prefix in sorted(_group_by_prefix(libs)):
            # TODO: multiple instances of a package can live in the same
            # prefix, and a package implementation can return multiple specs
            # for one prefix, but without additional details (e.g. about the
            # naming scheme which differentiates them), the spec won't be
            # usable.
            try:
                specs = _convert_to_iterable(
                    pkg.determine_spec_details(prefix, libs_in_prefix)
                )
            except Exception as e:
                specs = []
                msg = 'error detecting "{0}" from prefix {1} [{2}]'
                warnings.warn(msg.format(pkg.name, prefix, str(e)))

            if not specs:
                llnl.util.tty.debug(
                    'The following libraries in {0} were decidedly not '
                    'part of the package {1}: {2}'
                    .format(prefix, pkg.name, ', '.join(
                        _convert_to_iterable(libs_in_prefix)))
                )

            for spec in specs:
                pkg_prefix = library_prefix(prefix)

                if not pkg_prefix:
                    msg = "no lib/ or lib64/ dir found in {0}. Cannot "
                    "add it as a Spack package"
                    llnl.util.tty.debug(msg.format(prefix))
                    continue

                if spec in resolved_specs:
                    prior_prefix = ', '.join(
                        _convert_to_iterable(resolved_specs[spec]))

                    llnl.util.tty.debug(
                        "Libraries in {0} and {1} are both associated"
                        " with the same spec {2}"
                        .format(prefix, prior_prefix, str(spec)))
                    continue
                else:
                    resolved_specs[spec] = prefix

                try:
                    spec.validate_detection()
                except Exception as e:
                    msg = ('"{0}" has been detected on the system but will '
                           'not be added to packages.yaml [reason={1}]')
                    llnl.util.tty.warn(msg.format(spec, str(e)))
                    continue

                if spec.external_path:
                    pkg_prefix = spec.external_path

                pkg_to_entries[pkg.name].append(
                    DetectedPackage(spec=spec, prefix=pkg_prefix)
                )

    return pkg_to_entries


def by_executable(packages_to_check, path_hints=None):
    """Return the list of packages that have been detected on the system,
    searching by path.

    Args:
        packages_to_check (list): list of packages to be detected
        path_hints (list): list of paths to be searched. If None the list will be
            constructed based on the PATH environment variable.
    """
    path_hints = [] if path_hints is None else path_hints
    exe_pattern_to_pkgs = collections.defaultdict(list)
    for pkg in packages_to_check:
        if hasattr(pkg, 'executables'):
            for exe in pkg.platform_executables:
                exe_pattern_to_pkgs[exe].append(pkg)
        # Add Windows specific, package related paths to the search paths
        path_hints.extend(compute_windows_program_path_for_package(pkg))

    path_to_exe_name = executables_in_path(path_hints=path_hints)
    pkg_to_found_exes = collections.defaultdict(set)
    for exe_pattern, pkgs in exe_pattern_to_pkgs.items():
        compiled_re = re.compile(exe_pattern)
        for path, exe in path_to_exe_name.items():
            if compiled_re.search(exe):
                for pkg in pkgs:
                    pkg_to_found_exes[pkg].add(path)

    pkg_to_entries = collections.defaultdict(list)
    resolved_specs = {}  # spec -> exe found for the spec

    for pkg, exes in pkg_to_found_exes.items():
        if not hasattr(pkg, 'determine_spec_details'):
            llnl.util.tty.warn(
                "{0} must define 'determine_spec_details' in order"
                " for Spack to detect externally-provided instances"
                " of the package.".format(pkg.name))
            continue

        for prefix, exes_in_prefix in sorted(_group_by_prefix(exes)):
            # TODO: multiple instances of a package can live in the same
            # prefix, and a package implementation can return multiple specs
            # for one prefix, but without additional details (e.g. about the
            # naming scheme which differentiates them), the spec won't be
            # usable.
            try:
                specs = _convert_to_iterable(
                    pkg.determine_spec_details(prefix, exes_in_prefix)
                )
            except Exception as e:
                specs = []
                msg = 'error detecting "{0}" from prefix {1} [{2}]'
                warnings.warn(msg.format(pkg.name, prefix, str(e)))

            if not specs:
                llnl.util.tty.debug(
                    'The following executables in {0} were decidedly not '
                    'part of the package {1}: {2}'
                    .format(prefix, pkg.name, ', '.join(
                        _convert_to_iterable(exes_in_prefix)))
                )

            for spec in specs:
                pkg_prefix = executable_prefix(prefix)

                if not pkg_prefix:
                    msg = "no bin/ dir found in {0}. Cannot add it as a Spack package"
                    llnl.util.tty.debug(msg.format(prefix))
                    continue

                if spec in resolved_specs:
                    prior_prefix = ', '.join(
                        _convert_to_iterable(resolved_specs[spec]))

                    llnl.util.tty.debug(
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
                           'not be added to packages.yaml [reason={1}]')
                    llnl.util.tty.warn(msg.format(spec, str(e)))
                    continue

                if spec.external_path:
                    pkg_prefix = spec.external_path

                pkg_to_entries[pkg.name].append(
                    DetectedPackage(spec=spec, prefix=pkg_prefix)
                )

    return pkg_to_entries
