# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import argparse
import sys

import llnl.util.tty as tty
import llnl.util.tty.colify as colify
import spack
import spack.architecture
import spack.compilers
import spack.cmd
import spack.detection.common
import spack.detection.craype
import spack.detection.path
import spack.error
import spack.util.environment
import spack.util.module_cmd
import spack.util.spack_yaml as syaml

description = "manage external packages in Spack configuration"
section = "config"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='external_command')

    find_parser = sp.add_parser(
        'find', help='add external packages to packages.yaml'
    )
    find_parser.add_argument(
        '--not-buildable', action='store_true', default=False,
        help="packages with detected externals won't be built with Spack")
    find_parser.add_argument(
        '--craype', action='store_true', default=False,
        help="detect packages using modules from the Cray PE")
    find_parser.add_argument('packages', nargs=argparse.REMAINDER)

    sp.add_parser(
        'list', help='list detectable packages, by repository and name'
    )


def _generate_pkg_config(external_pkg_entries):
    """Generate config according to the packages.yaml schema for a single
    package.

    This does not generate the entire packages.yaml. For example, given some
    external entries for the CMake package, this could return::

        {
            'externals': [{
                'spec': 'cmake@3.17.1',
                'prefix': '/opt/cmake-3.17.1/'
            }, {
                'spec': 'cmake@3.16.5',
                'prefix': '/opt/cmake-3.16.5/'
            }]
       }
    """

    pkg_dict = syaml.syaml_dict()
    pkg_dict['externals'] = []
    for e in external_pkg_entries:
        if not _spec_is_valid(e.spec):
            continue

        external_items = [('spec', str(e.spec))]
        if e.base_dir:
            external_items.append(('prefix', e.base_dir))

        if e.modules:
            external_items.append(('modules', e.modules))

        # FIXME: check how to add external modules
        if e.spec.external_modules:
            external_items.append(('modules', e.spec.external_modules))

        if e.spec.extra_attributes:
            external_items.append(
                ('extra_attributes',
                 syaml.syaml_dict(e.spec.extra_attributes.items()))
            )

        # external_items.extend(e.spec.extra_attributes.items())
        pkg_dict['externals'].append(
            syaml.syaml_dict(external_items)
        )

    return pkg_dict


def _spec_is_valid(spec):
    try:
        str(spec)
    except spack.error.SpackError:
        # It is assumed here that we can at least extract the package name from
        # the spec so we can look up the implementation of
        # determine_spec_details
        tty.warn('Constructed spec for {0} does not have a string'
                 ' representation'.format(spec.name))
        return False

    try:
        spack.spec.Spec(str(spec))
    except spack.error.SpackError:
        tty.warn('Constructed spec has a string representation but the string'
                 ' representation does not evaluate to a valid spec: {0}'
                 .format(str(spec)))
        return False

    return True


def external_find(args):
    # Select the packages to be checked for detection
    if args.packages:
        packages_to_check = list(spack.repo.get(pkg) for pkg in args.packages)
    else:
        packages_to_check = spack.repo.path.all_packages()

    if args.craype:
        # Search Cray programming environment + frontend
        tty.debug("Detecting Cray")
        pkg_to_entries = spack.detection.craype.detect(packages_to_check)
    else:
        pkg_to_entries = spack.detection.path.detect(packages_to_check)

    new_entries, write_scope = _update_pkg_config(
        pkg_to_entries, args.not_buildable
    )
    if new_entries:
        path = spack.config.config.get_config_filename(write_scope, 'packages')
        msg = ('The following specs have been detected on this system '
               'and added to {0}')
        tty.msg(msg.format(path))
        spack.cmd.display_specs(new_entries)
    else:
        tty.msg('No new external packages detected')


def _get_predefined_externals():
    # Pull from all scopes when looking for preexisting external package
    # entries
    pkg_config = spack.config.get('packages')
    already_defined_specs = set()
    for pkg_name, per_pkg_cfg in pkg_config.items():
        for item in per_pkg_cfg.get('externals', []):
            already_defined_specs.add(spack.spec.Spec(item['spec']))
    return already_defined_specs


def _update_pkg_config(pkg_to_entries, not_buildable):
    predefined_external_specs = _get_predefined_externals()

    pkg_to_cfg, all_new_specs = {}, []
    for pkg_name, ext_pkg_entries in pkg_to_entries.items():
        new_entries = list(
            e for e in ext_pkg_entries
            if (e.spec not in predefined_external_specs))

        pkg_config = _generate_pkg_config(new_entries)
        all_new_specs.extend([
            spack.spec.Spec(x['spec']) for x in pkg_config.get('externals', [])
        ])
        if not_buildable:
            pkg_config['buildable'] = False
        pkg_to_cfg[pkg_name] = pkg_config

    cfg_scope = spack.config.default_modify_scope()
    pkgs_cfg = spack.config.get('packages', scope=cfg_scope)

    spack.config.merge_yaml(pkgs_cfg, pkg_to_cfg)
    spack.config.set('packages', pkgs_cfg, scope=cfg_scope)

    return all_new_specs, cfg_scope


def external_list(args):
    # Trigger a read of all packages, might take a long time.
    list(spack.repo.path.all_packages())
    # Print all the detectable packages
    tty.msg("Detectable packages per repository")
    for namespace, pkgs in sorted(spack.package.detectable_packages.items()):
        print("Repository:", namespace)
        colify.colify(pkgs, indent=4, output=sys.stdout)


def external(parser, args):
    action = {'find': external_find, 'list': external_list}
    action[args.external_command](args)
