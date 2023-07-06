# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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

import spack.util.environment
import spack.util.ld_so_conf

from .common import (  # find_windows_compiler_bundled_packages,
    DetectedPackage,
    WindowsCompilerExternalPaths,
    WindowsKitExternalPaths,
    _convert_to_iterable,
    compute_windows_program_path_for_package,
    compute_windows_user_path_for_package,
    executable_prefix,
    find_win32_additional_install_paths,
    library_prefix,
    path_to_dict,
)


def common_windows_package_paths():
    paths = WindowsCompilerExternalPaths.find_windows_compiler_bundled_packages()
    paths.extend(find_win32_additional_install_paths())
    paths.extend(WindowsKitExternalPaths.find_windows_kit_bin_paths())
    paths.extend(WindowsKitExternalPaths.find_windows_kit_reg_installed_roots_paths())
    paths.extend(WindowsKitExternalPaths.find_windows_kit_reg_sdk_paths())
    return paths


def executables_in_path(path_hints):
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
    if sys.platform == "win32":
        path_hints.extend(common_windows_package_paths())
    search_paths = llnl.util.filesystem.search_paths_for_executables(*path_hints)
    return path_to_dict(search_paths)


def libraries_in_ld_and_system_library_path(path_hints=None):
    """Get the paths of all libraries available from LD_LIBRARY_PATH,
    LIBRARY_PATH, DYLD_LIBRARY_PATH, DYLD_FALLBACK_LIBRARY_PATH, and
    standard system library paths.

    For convenience, this is constructed as a dictionary where the keys are
    the library paths and the values are the names of the libraries
    (i.e. the basename of the library path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the library.

    Args:
        path_hints (list): list of paths to be searched. If None the list will be
            constructed based on the set of LD_LIBRARY_PATH, LIBRARY_PATH,
            DYLD_LIBRARY_PATH, and DYLD_FALLBACK_LIBRARY_PATH environment
            variables as well as the standard system library paths.
    """
    path_hints = (
        path_hints
        or spack.util.environment.get_path("LD_LIBRARY_PATH")
        + spack.util.environment.get_path("DYLD_LIBRARY_PATH")
        + spack.util.environment.get_path("DYLD_FALLBACK_LIBRARY_PATH")
        + spack.util.ld_so_conf.host_dynamic_linker_search_paths()
    )
    search_paths = llnl.util.filesystem.search_paths_for_libraries(*path_hints)
    return path_to_dict(search_paths)


def libraries_in_windows_paths(path_hints):
    path_hints.extend(spack.util.environment.get_path("PATH"))
    search_paths = llnl.util.filesystem.search_paths_for_libraries(*path_hints)
    # on Windows, some libraries (.dlls) are found in the bin directory or sometimes
    # at the search root. Add both of those options to the search scheme
    search_paths.extend(llnl.util.filesystem.search_paths_for_executables(*path_hints))
    search_paths.extend(WindowsKitExternalPaths.find_windows_kit_lib_paths())
    search_paths.extend(WindowsKitExternalPaths.find_windows_kit_bin_paths())
    search_paths.extend(WindowsKitExternalPaths.find_windows_kit_reg_installed_roots_paths())
    search_paths.extend(WindowsKitExternalPaths.find_windows_kit_reg_sdk_paths())
    # SDK and WGL should be handled by above, however on occasion the WDK is in an atypical
    # location, so we handle that case specifically.
    search_paths.extend(WindowsKitExternalPaths.find_windows_driver_development_kit_paths())
    return path_to_dict(search_paths)


def _group_by_prefix(paths):
    groups = collections.defaultdict(set)
    for p in paths:
        groups[os.path.dirname(p)].add(p)
    return groups.items()


# TODO consolidate this with by_executable
# Packages should be able to define both .libraries and .executables in the future
# determine_spec_details should get all relevant libraries and executables in one call
def by_library(packages_to_check, path_hints=None):
    # Techniques for finding libraries is determined on a per recipe basis in
    # the determine_version class method. Some packages will extract the
    # version number from a shared libraries filename.
    # Other libraries could use the strings function to extract it as described
    # in https://unix.stackexchange.com/questions/58846/viewing-linux-library-executable-version-info
    """Return the list of packages that have been detected on the system,
    searching by LD_LIBRARY_PATH, LIBRARY_PATH, DYLD_LIBRARY_PATH,
    DYLD_FALLBACK_LIBRARY_PATH, and standard system library paths.

    Args:
        packages_to_check (list): list of packages to be detected
        path_hints (list): list of paths to be searched. If None the list will be
            constructed based on the LD_LIBRARY_PATH, LIBRARY_PATH,
            DYLD_LIBRARY_PATH, DYLD_FALLBACK_LIBRARY_PATH environment variables
            and standard system library paths.
    """
    # If no path hints from command line, intialize to empty list so
    # we can add default hints on a per package basis
    path_hints = [] if path_hints is None else path_hints

    lib_pattern_to_pkgs = collections.defaultdict(list)
    for pkg in packages_to_check:
        if hasattr(pkg, "libraries"):
            for lib in pkg.libraries:
                lib_pattern_to_pkgs[lib].append(pkg)
        path_hints.extend(compute_windows_user_path_for_package(pkg))
        path_hints.extend(compute_windows_program_path_for_package(pkg))

    path_to_lib_name = (
        libraries_in_ld_and_system_library_path(path_hints=path_hints)
        if sys.platform != "win32"
        else libraries_in_windows_paths(path_hints)
    )

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
        if not hasattr(pkg, "determine_spec_details"):
            llnl.util.tty.warn(
                "{0} must define 'determine_spec_details' in order"
                " for Spack to detect externally-provided instances"
                " of the package.".format(pkg.name)
            )
            continue

        for prefix, libs_in_prefix in sorted(_group_by_prefix(libs)):
            try:
                specs = _convert_to_iterable(pkg.determine_spec_details(prefix, libs_in_prefix))
            except Exception as e:
                specs = []
                msg = 'error detecting "{0}" from prefix {1} [{2}]'
                warnings.warn(msg.format(pkg.name, prefix, str(e)))

            if not specs:
                llnl.util.tty.debug(
                    "The following libraries in {0} were decidedly not "
                    "part of the package {1}: {2}".format(
                        prefix, pkg.name, ", ".join(_convert_to_iterable(libs_in_prefix))
                    )
                )

            for spec in specs:
                pkg_prefix = library_prefix(prefix)

                if not pkg_prefix:
                    msg = "no lib/ or lib64/ dir found in {0}. Cannot "
                    "add it as a Spack package"
                    llnl.util.tty.debug(msg.format(prefix))
                    continue

                if spec in resolved_specs:
                    prior_prefix = ", ".join(_convert_to_iterable(resolved_specs[spec]))

                    llnl.util.tty.debug(
                        "Libraries in {0} and {1} are both associated"
                        " with the same spec {2}".format(prefix, prior_prefix, str(spec))
                    )
                    continue
                else:
                    resolved_specs[spec] = prefix

                try:
                    spec.validate_detection()
                except Exception as e:
                    msg = (
                        '"{0}" has been detected on the system but will '
                        "not be added to packages.yaml [reason={1}]"
                    )
                    llnl.util.tty.warn(msg.format(spec, str(e)))
                    continue

                if spec.external_path:
                    pkg_prefix = spec.external_path

                pkg_to_entries[pkg.name].append(DetectedPackage(spec=spec, prefix=pkg_prefix))

    return pkg_to_entries


def by_executable(packages_to_check, path_hints=None):
    """Return the list of packages that have been detected on the system,
    searching by path.

    Args:
        packages_to_check (list): list of package classes to be detected
        path_hints (list): list of paths to be searched. If None the list will be
            constructed based on the PATH environment variable.
    """
    path_hints = spack.util.environment.get_path("PATH") if path_hints is None else path_hints
    exe_pattern_to_pkgs = collections.defaultdict(list)
    for pkg in packages_to_check:
        if hasattr(pkg, "executables"):
            for exe in pkg.platform_executables():
                exe_pattern_to_pkgs[exe].append(pkg)
        # Add Windows specific, package related paths to the search paths
        path_hints.extend(compute_windows_user_path_for_package(pkg))
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
        if not hasattr(pkg, "determine_spec_details"):
            llnl.util.tty.warn(
                "{0} must define 'determine_spec_details' in order"
                " for Spack to detect externally-provided instances"
                " of the package.".format(pkg.name)
            )
            continue

        for prefix, exes_in_prefix in sorted(_group_by_prefix(exes)):
            # TODO: multiple instances of a package can live in the same
            # prefix, and a package implementation can return multiple specs
            # for one prefix, but without additional details (e.g. about the
            # naming scheme which differentiates them), the spec won't be
            # usable.
            try:
                specs = _convert_to_iterable(pkg.determine_spec_details(prefix, exes_in_prefix))
            except Exception as e:
                specs = []
                msg = 'error detecting "{0}" from prefix {1} [{2}]'
                warnings.warn(msg.format(pkg.name, prefix, str(e)))

            if not specs:
                llnl.util.tty.debug(
                    "The following executables in {0} were decidedly not "
                    "part of the package {1}: {2}".format(
                        prefix, pkg.name, ", ".join(_convert_to_iterable(exes_in_prefix))
                    )
                )

            for spec in specs:
                pkg_prefix = executable_prefix(prefix)

                if not pkg_prefix:
                    msg = "no bin/ dir found in {0}. Cannot add it as a Spack package"
                    llnl.util.tty.debug(msg.format(prefix))
                    continue

                if spec in resolved_specs:
                    prior_prefix = ", ".join(_convert_to_iterable(resolved_specs[spec]))

                    llnl.util.tty.debug(
                        "Executables in {0} and {1} are both associated"
                        " with the same spec {2}".format(prefix, prior_prefix, str(spec))
                    )
                    continue
                else:
                    resolved_specs[spec] = prefix

                try:
                    spec.validate_detection()
                except Exception as e:
                    msg = (
                        '"{0}" has been detected on the system but will '
                        "not be added to packages.yaml [reason={1}]"
                    )
                    llnl.util.tty.warn(msg.format(spec, str(e)))
                    continue

                if spec.external_path:
                    pkg_prefix = spec.external_path

                pkg_to_entries[pkg.name].append(DetectedPackage(spec=spec, prefix=pkg_prefix))

    return pkg_to_entries
