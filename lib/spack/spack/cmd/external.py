# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
from collections import defaultdict
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

    # Find
    sp.add_parser('find', help=external_find.__doc__)


def _get_system_executables():
    path = os.getenv('PATH')
    search_paths = path.split(os.pathsep)
    exe_to_path = {}
    # Reverse order of search directories so that an exe in the first PATH
    # entry overrides later entries
    for search_path in reversed(search_paths):
        for exe in os.listdir(search_path):
            exe_to_path[exe] = os.path.join(search_path, exe)
    return exe_to_path


def _pkg_yaml_template(name, spec, path):
    template = """\
{name}:
  paths:
    {spec}: {path}"""
    return template.format(name=name, spec=spec, path=path)


def external_find(args):
    _get_external_packages(TestRepo())


def _get_external_packages(repo):
    system_exe_to_path = _get_system_executables()

    exe_pattern_to_pkgs = defaultdict(list)
    for pkg in repo.all_packages():
        if hasattr(pkg, 'executables'):
            for exe in pkg.executables:
                exe_pattern_to_pkgs[exe].append(pkg)

    pkg_to_found_exes = defaultdict(set)
    found_exe_to_pkgs = defaultdict(set)
    for exe in system_exe_to_path:
        for exe_pattern, pkgs in exe_pattern_to_pkgs.items():
            if re.search(exe_pattern, exe):
                for pkg in pkgs:
                    pkg_to_found_exes[pkg].add(exe)
                found_exe_to_pkgs[exe].update(pkgs)
    # Sort to get repeatable results
    found_exe_to_pkgs = dict(
        (x, list(sorted(y, key=lambda p: p.name)))
        for x, y in found_exe_to_pkgs.items())
    pkg_to_found_exes = dict(
        (x, list(sorted(y)))
        for x, y in pkg_to_found_exes.items())

    exe_to_usable_packages = defaultdict(list)
    pkg_to_template = {}
    resolved_pkgs = set()
    for exe in sorted(found_exe_to_pkgs):
        associated_packages = found_exe_to_pkgs[exe]
        for pkg in associated_packages:
            if pkg.name in resolved_pkgs:
                # The package was already considered as part of examining a
                # different exe. It does not need to be reexamined.
                continue
            resolved_pkgs.add(pkg.name)

            found_pkg_exes = pkg_to_found_exes[pkg]

            if hasattr(pkg, 'determine_spec_details'):
                spec_str = pkg.determine_spec_details(found_pkg_exes)
            else:
                spec_str = pkg_name

            if not spec_str:
                tty.msg("{0} detected that the following executables are"
                        " associated with a different package: {1}"
                        .format(pkg.name, ", ".join(found_pkg_exes)))
                continue

            paths = list(system_exe_to_path[x] for x in found_pkg_exes)
            bin_dirs = set(os.path.dirname(x) for x in paths)
            if len(bin_dirs) > 1:
                tty.warn("{0} has executables in separate locations: {1}"
                         .format(pkg.name, ", ".join(bin_dirs)))
            bin_dir = list(bin_dirs)[0]
            base_dir = os.path.dirname(bin_dir)

            for exe in found_pkg_exes:
                exe_to_usable_packages[exe].append(pkg)

            pkg_to_template[pkg.name] = _pkg_yaml_template(
                pkg.name, spec_str, base_dir)

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
