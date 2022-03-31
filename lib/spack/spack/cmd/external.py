# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import argparse
import sys

import llnl.util.tty as tty
import llnl.util.tty.colify as colify

import spack
import spack.cmd
import spack.cmd.common.arguments
import spack.detection
import spack.error
import spack.util.environment

description = "manage external packages in Spack configuration"
section = "config"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='external_command')

    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    find_parser = sp.add_parser(
        'find', help='add external packages to packages.yaml'
    )
    find_parser.add_argument(
        '--not-buildable', action='store_true', default=False,
        help="packages with detected externals won't be built with Spack")
    find_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope('packages'),
        help="configuration scope to modify")
    find_parser.add_argument(
        '--all', action='store_true',
        help="search for all packages that Spack knows about"
    )
    spack.cmd.common.arguments.add_common_arguments(find_parser, ['tags'])
    find_parser.add_argument('packages', nargs=argparse.REMAINDER)
    find_parser.epilog = (
        'The search is by default on packages tagged with the "build-tools" or '
        '"core-packages" tags. Use the --all option to search for every possible '
        'package Spack knows how to find.'
    )

    sp.add_parser(
        'list', help='list detectable packages, by repository and name'
    )


def external_find(args):
    # If the user didn't specify anything, search for build tools by default
    if not args.tags and not args.all and not args.packages:
        args.tags = ['core-packages', 'build-tools']

    # If the user specified both --all and --tag, then --all has precedence
    if args.all and args.tags:
        args.tags = []

    # Construct the list of possible packages to be detected
    packages_to_check = []

    # Add the packages that have been required explicitly
    if args.packages:
        packages_to_check = list(spack.repo.get(pkg) for pkg in args.packages)
        if args.tags:
            allowed = set(spack.repo.path.packages_with_tags(*args.tags))
            packages_to_check = [x for x in packages_to_check if x in allowed]

    if args.tags and not packages_to_check:
        # If we arrived here we didn't have any explicit package passed
        # as argument, which means to search all packages.
        # Since tags are cached it's much faster to construct what we need
        # to search directly, rather than filtering after the fact
        packages_to_check = [
            spack.repo.get(pkg) for tag in args.tags for pkg in
            spack.repo.path.packages_with_tags(tag)
        ]
        packages_to_check = list(set(packages_to_check))

    # If the list of packages is empty, search for every possible package
    detected_packages = spack.detection.by_executable(
        packages_to_check
        if packages_to_check
        else spack.repo.path.all_packages())

    def filter_packages(package_list, names):
        for pkg in package_list:
            if pkg.name not in names:
                yield pkg

    detected_packages.update(
        spack.detection.by_pkgconfig(
            filter_packages(packages_to_check if packages_to_check
                            else spack.repo.path.all_packages(),
                            detected_packages.keys())
        ))

    new_entries = spack.detection.update_configuration(
        detected_packages, scope=args.scope, buildable=not args.not_buildable
    )
    if new_entries:
        path = spack.config.config.get_config_filename(args.scope, 'packages')
        msg = ('The following specs have been detected on this system '
               'and added to {0}')
        tty.msg(msg.format(path))
        spack.cmd.display_specs(new_entries)
    else:
        tty.msg('No new external packages detected')


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
