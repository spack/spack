# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
from collections import defaultdict, namedtuple
import os
import re
import six

import spack
import llnl.util.tty as tty
import spack.util.spack_yaml as syaml
import spack.util.environment
import llnl.util.filesystem

description = "add external packages to Spack configuration"
section = "config"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='external_command')

    sp.add_parser('find', help=external_find.__doc__)


def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


def _get_system_executables():
    """Get the paths of all executables available from the current PATH.

    For convenience, this is constructed as a dictionary where the keys are
    the executable paths and the values are the names of the executables
    (i.e. the basename of the executable path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the executable.
    """
    path_hints = spack.util.environment.get_path('PATH')
    search_paths = llnl.util.filesystem.search_paths_for_executables(
        *path_hints)

    path_to_exe = {}
    # Reverse order of search directories so that an exe in the first PATH
    # entry overrides later entries
    for search_path in reversed(search_paths):
        for exe in os.listdir(search_path):
            exe_path = os.path.join(search_path, exe)
            if is_executable(exe_path):
                path_to_exe[exe_path] = exe
    return path_to_exe


ExternalPackageEntry = namedtuple(
    'ExternalPackageEntry',
    ['spec', 'base_dir'])


def _pkg_yaml_template(pkg_name, external_pkg_entries):
    """Generate config according to the packages.yaml schema for a single
    package.

    This does not generate the entire packages.yaml.
    """
    paths_dict = syaml.syaml_dict()
    for e in external_pkg_entries:
        paths_dict[str(e.spec)] = e.base_dir
    pkg_dict = syaml.syaml_dict()
    pkg_dict['paths'] = paths_dict

    pkgs_dict = syaml.syaml_dict()
    pkgs_dict[pkg_name] = pkg_dict

    return pkgs_dict


def external_find(args):
    _get_external_packages(TestRepo())


def _group_by_prefix(paths):
    groups = defaultdict(set)
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
    assert os.path.isdir(prefix)
    if os.path.basename(prefix) == 'bin':
        return os.path.dirname(prefix)


def _get_external_packages(repo, system_path_to_exe=None):
    if not system_path_to_exe:
        system_path_to_exe = _get_system_executables()

    exe_pattern_to_pkgs = defaultdict(list)
    for pkg in repo.all_packages():
        if hasattr(pkg, 'executables'):
            for exe in pkg.executables:
                exe_pattern_to_pkgs[exe].append(pkg)

    pkg_to_found_exes = defaultdict(set)
    for path, exe in system_path_to_exe.items():
        for exe_pattern, pkgs in exe_pattern_to_pkgs.items():
            if re.search(exe_pattern, exe):
                for pkg in pkgs:
                    pkg_to_found_exes[pkg].add(path)

    pkg_to_entries = defaultdict(list)
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
                pkg.determine_spec_details(prefix, exes_in_prefix))

            for spec in specs:
                pkg_prefix = _determine_base_dir(prefix)

                if not pkg_prefix:
                    tty.debug("{0} does not end with a 'bin/' directory: it"
                              " cannot be added as a Spack package"
                              .format(prefix))
                    continue

                if spec in resolved_specs:
                    prior_prefix = ', '.join(resolved_specs[spec])

                    tty.debug(
                        "Executables in {0} and {1} are both associated"
                        " with the same spec {2}"
                        .format(prefix, prior_prefix, str(spec)))
                    continue
                else:
                    resolved_specs[spec] = prefix

                pkg_to_entries[pkg.name].append(
                    ExternalPackageEntry(spec=spec, base_dir=pkg_prefix))
            else:
                tty.debug(
                    'The following executables in {0} were decidedly not'
                    'part of the package {1}: {2}'
                    .format(prefix, pkg.name, ', '.join(exes_in_prefix))
                )

    pkg_to_template = {}
    for pkg_name, ext_pkg_entries in pkg_to_entries.items():
        pkg_to_template[pkg_name] = _pkg_yaml_template(
            pkg.name, ext_pkg_entries)

    for config in pkg_to_template.values():
        print(syaml.dump_config(pkg_to_template[pkg_name]))


class TestRepo(object):
    def all_packages(self):
        test_pkgs = ['cmake']
        return list(spack.repo.path.get(x) for x in test_pkgs)

    def get(self, pkg_name):
        return spack.repo.path.get(pkg_name)


def external(parser, args):
    action = {'find': external_find}

    action[args.external_command](args)
