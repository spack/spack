# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
from collections import defaultdict, namedtuple
import os
import re

import spack
import llnl.util.tty as tty

description = "add external packages to Spack configuration"
section = "config"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='external_command')

    sp.add_parser('find', help=external_find.__doc__)


def _get_system_executables():
    path = os.getenv('PATH')
    search_paths = list(p for p in path.split(os.pathsep) if os.path.isdir(p))
    path_to_exe = {}
    # Reverse order of search directories so that an exe in the first PATH
    # entry overrides later entries
    for search_path in reversed(search_paths):
        for exe in os.listdir(search_path):
            path_to_exe[os.path.join(search_path, exe)] = exe
    return path_to_exe


ExternalPackageEntry = namedtuple(
    'ExternalPackageEntry',
    ['spec', 'base_dir'])


def _pkg_yaml_template(pkg_name, external_pkg_entries):
    template = """\
{name}:
  paths:
    {path_entries_block}"""

    entry_template = "{spec}: {path}"
    path_entries_block = "\n    ".join(
        entry_template.format(spec=str(e.spec), path=e.base_dir)
        for e in external_pkg_entries)

    return template.format(
        name=pkg_name, path_entries_block=path_entries_block)


def external_find(args):
    _get_external_packages(TestRepo())


def _get_external_packages(repo, system_path_to_exe=None):
    if not system_path_to_exe:
        system_path_to_exe = _get_system_executables()

    exe_pattern_to_pkgs = defaultdict(list)
    for pkg in repo.all_packages():
        if hasattr(pkg, 'executables'):
            for exe in pkg.executables:
                exe_pattern_to_pkgs[exe].append(pkg)

    pkg_to_found_exes = defaultdict(set)
    found_exe_to_pkgs = defaultdict(set)
    for path, exe in system_path_to_exe.items():
        for exe_pattern, pkgs in exe_pattern_to_pkgs.items():
            if re.search(exe_pattern, exe):
                for pkg in pkgs:
                    pkg_to_found_exes[pkg].add(path)
                found_exe_to_pkgs[path].update(pkgs)
    # Sort to get repeatable results
    found_exe_to_pkgs = dict(
        (x, list(sorted(y, key=lambda p: p.name)))
        for x, y in found_exe_to_pkgs.items())
    pkg_to_found_exes = dict(
        (x, list(sorted(y)))
        for x, y in pkg_to_found_exes.items())

    exe_to_usable_packages = defaultdict(list)
    pkg_to_entries = defaultdict(list)
    resolved_specs = {}  # spec -> exe found for the spec
    for exe in sorted(found_exe_to_pkgs):
        associated_packages = found_exe_to_pkgs[exe]
        for pkg in associated_packages:
            found_pkg_exes = pkg_to_found_exes[pkg]

            if hasattr(pkg, 'determine_spec_details'):
                spec_str = pkg.determine_spec_details(exe, found_pkg_exes)
            else:
                spec_str = pkg.name

            if not spec_str:
                tty.msg("{0} detected that the following executables are"
                        " associated with a different package: {1}"
                        .format(pkg.name, ", ".join(found_pkg_exes)))
                continue

            spec = spack.spec.Spec(spec_str)
            if spec in resolved_specs:
                prior_associated_exe = resolved_specs[spec]
                tty.debug("Executables {0} and {1} are both associated with"
                          " the same spec {2}"
                          .format(exe, prior_associated_exe, str(spec)))
                continue
            else:
                resolved_specs[spec] = exe

            bin_dir = os.path.dirname(exe)
            base_dir = os.path.dirname(bin_dir)

            exe_to_usable_packages[exe].append(pkg)

            pkg_to_entries[pkg.name].append(
                ExternalPackageEntry(spec=spec, base_dir=base_dir))

    pkg_to_template = {}
    for pkg_name, ext_pkg_entries in pkg_to_entries.items():
        pkg_to_template[pkg_name] = _pkg_yaml_template(
            pkg.name, ext_pkg_entries)

    used_packages = set()
    for exe, pkgs in exe_to_usable_packages.items():
        if len(pkgs) > 1:
            tty.warn("The following packages all use {0}: {1}"
                     .format(exe, ", ".join(p.name for p in pkgs)))

        # If some package that uses this exe was already selected, then omit
        # this executable from consideration
        if used_packages & set(p.name for p in pkgs):
            continue

        used_packages.add(pkgs[0].name)

    for pkg_name in used_packages:
        print(pkg_to_template[pkg_name])


class TestRepo(object):
    def all_packages(self):
        test_pkgs = ['cmake']
        return list(spack.repo.path.get(x) for x in test_pkgs)

    def get(self, pkg_name):
        return spack.repo.path.get(pkg_name)


def external(parser, args):
    action = {'find': external_find}

    action[args.external_command](args)
