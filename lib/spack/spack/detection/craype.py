# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import re

import llnl.util.tty as tty
import spack.architecture
import spack.detection.path
import spack.operating_systems.cray_frontend as cray_frontend
import spack.util.module_cmd


def detect(packages_to_check, system_path_to_exe=None):
    """Detect software in a Cray Programming Environment.

    This function will detect first the system software on the
    front-end and then it will look for modules in the Cray
    Programming environment to add software for both the frontend
    and the backend.

    Args:
        packages_to_check (list): list of packages to be searched for
        system_path_to_exe (dict): dictionary mapping an absolute path
            to an executable to its basename

    Returns:
        Dictionary mapping a package name to the list of specs that were
        detected for it.
    """
    # Assert the system is a Cray
    p = spack.architecture.platform()
    error_message = "the --craype option can be used only on Cray platforms"
    assert str(p) == 'cray', error_message

    # Front-end goes through the usual detection mechanism, but before that
    # we need to temporarily unload module files
    tty.debug("[CRAY] Detecting front-end software")
    with cray_frontend.unload_programming_environment():
        pkg_to_entries = spack.detection.path.detect(
            packages_to_check, system_path_to_exe
        )

    # Annotate the OS in the extra attributes for later reuse
    for pkg, entries in pkg_to_entries.items():
        for entry in entries:
            entry.spec.constrain('os={0}'.format(p.front_os))

    # Back-end uses module detection
    tty.debug("[CRAY] Detecting back-end software")
    be_pkg_to_entries = _detect_from_craype_modules(packages_to_check)
    # Add the modules just detected to the list of entries
    for name, entries in be_pkg_to_entries.items():
        pkg_to_entries[name].extend(entries)

    return pkg_to_entries


def _detect_from_craype_modules(packages_to_check):
    module = spack.util.module_cmd.module
    p = spack.architecture.platform()
    spec_os, pkg_to_entries = p.back_os, collections.defaultdict(list)
    for pkg in packages_to_check:
        # The PrgEnv module needs to be loaded before the compiler module
        if not hasattr(pkg, 'cray_prgenv'):
            continue
        # Compiler module to be loaded
        if not hasattr(pkg, 'cray_module_name'):
            continue

        # Inspect the output of module avail and extract version
        # information from there
        output = module('avail', pkg.cray_module_name)
        version_regex = r'({0})/([\d\.]+[\d][-]?[\w]*)'.format(
            pkg.cray_module_name
        )
        matches = re.findall(version_regex, output)

        extract_path_re = re.compile(r'prepend-path[\s]*PATH[\s]*([/\w\.:-]*)')
        module_versions = [version for _, version in matches]
        version_fn = getattr(pkg, 'cray_spec_version', lambda x: x)
        for module_version in module_versions:
            # Check which spec version corresponds to a Cray module version.
            # If this function returns None it means to discard this module.
            version = version_fn(module_version)
            if not version:
                continue

            extra_attributes = getattr(pkg, 'cray_extra_attributes', {})
            spec_str_format = '{0}@{1} os={2}'
            spec = spack.spec.Spec.from_detection(
                spec_str=spec_str_format.format(pkg.name, version, spec_os),
                external_modules=[
                    pkg.cray_prgenv,
                    '{0}/{1}'.format(pkg.cray_module_name, module_version)
                ],
                extra_attributes=extra_attributes
            )
            # Add back-end compiler
            pkg_to_entries[pkg.name].append(spec)
            msg = "[CRAY BE] Detected BE compiler [name={0}, version={1}]"
            tty.debug(msg.format(pkg.name, version))

            # Detect front-end compilers from module
            fe_pkg_to_entries = {}
            try:
                current_module = pkg.cray_module_name + '/' + version
                out = module('show', current_module)
                match = extract_path_re.search(out)
                path_hints = match.group(1).split(':')
                system_path_to_exe = spack.detection.path.system_executables(
                    path_hints
                )
                fe_pkg_to_entries = spack.detection.path.detect(
                    [pkg], system_path_to_exe
                )
            except Exception as e:
                msg = ("[CRAY FE] An unexpected error occurred while "
                       "detecting FE compiler [compiler={0}, "
                       " version={1}, error={2}]")
                tty.debug(msg.format(pkg.name, version, str(e)))

            msg = "[CRAY FE] Detected FE compiler [name={0}, version={1}]"
            tty.debug(msg.format(pkg.name, version))

            for name, entries in fe_pkg_to_entries.items():
                for entry in entries:
                    entry.spec.constrain('os={0}'.format(p.front_os))
                    entry.modules.extend([
                        '{0}/{1}'.format(pkg.cray_module_name, module_version)
                    ])

                pkg_to_entries[name].extend(entries)

    return pkg_to_entries
