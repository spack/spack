##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from __future__ import print_function

import argparse

import llnl.util.tty as tty
import spack
import spack.cmd
import spack.repository
from spack.cmd.find import display_specs

description = "Remove an installed package"

error_message = """You can either:
    a) Use a more specific spec, or
    b) use spack uninstall -a to uninstall ALL matching specs.
"""


def ask_for_confirmation(message):
    while True:
        tty.msg(message + '[y/n]')
        choice = raw_input().lower()
        if choice == 'y':
            break
        elif choice == 'n':
            raise SystemExit('Operation aborted')
        tty.warn('Please reply either "y" or "n"')


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="Remove regardless of whether other packages depend on this one.")
    subparser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="USE CAREFULLY. Remove ALL installed packages that match each " +
             "supplied spec. i.e., if you say uninstall libelf, ALL versions of " +
             "libelf are uninstalled. This is both useful and dangerous, like rm -r.")
    subparser.add_argument(
        '-d', '--dependents', action='store_true', dest='dependents',
        help='Also uninstall any packages that depend on the ones given via command line.'
    )
    subparser.add_argument(
        '-y', '--yes-to-all', action='store_true', dest='yes_to_all',
        help='Assume "yes" is the answer to every confirmation asked to the user.'

    )
    subparser.add_argument('packages', nargs=argparse.REMAINDER, help="specs of packages to uninstall")


def concretize_specs(specs, allow_multiple_matches=False, force=False):
    """
    Returns a list of specs matching the non necessarily concretized specs given from cli

    Args:
        specs: list of specs to be matched against installed packages
        allow_multiple_matches : boolean (if True multiple matches for each item in specs are admitted)

    Return:
        list of specs
    """
    specs_from_cli = []  # List of specs that match expressions given via command line
    has_errors = False
    for spec in specs:
        matching = spack.installed_db.query(spec)
        # For each spec provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matching) > 1:
            tty.error("%s matches multiple packages:" % spec)
            print()
            display_specs(matching, long=True)
            print()
            has_errors = True

        # No installed package matches the query
        if len(matching) == 0 and not force:
            tty.error("%s does not match any installed packages." % spec)
            has_errors = True

        specs_from_cli.extend(matching)
    if has_errors:
        tty.die(error_message)

    return specs_from_cli


def installed_dependents(specs):
    """
    Returns a dictionary that maps a spec with a list of its installed dependents

    Args:
        specs: list of specs to be checked for dependents

    Returns:
        dictionary of installed dependents
    """
    dependents = {}
    for item in specs:
        lst = [x for x in item.package.installed_dependents if x not in specs]
        if lst:
            lst = list(set(lst))
            dependents[item] = lst
    return dependents


def do_uninstall(specs, force):
    """
    Uninstalls all the specs in a list.

    Args:
        specs: list of specs to be uninstalled
        force: force uninstallation (boolean)
    """
    packages = []
    for item in specs:
        try:
            # should work if package is known to spack
            packages.append(item.package)
        except spack.repository.UnknownPackageError as e:
            # The package.py file has gone away -- but still
            # want to uninstall.
            spack.Package(item).do_uninstall(force=True)

    # Sort packages to be uninstalled by the number of installed dependents
    # This ensures we do things in the right order
    def num_installed_deps(pkg):
        return len(pkg.installed_dependents)

    packages.sort(key=num_installed_deps)
    for item in packages:
        item.do_uninstall(force=force)


def uninstall(parser, args):
    if not args.packages:
        tty.die("uninstall requires at least one package argument.")

    with spack.installed_db.write_transaction():
        specs = spack.cmd.parse_specs(args.packages)
        # Gets the list of installed specs that match the ones give via cli
        uninstall_list = concretize_specs(specs, args.all, args.force)  # takes care of '-a' is given in the cli
        dependent_list = installed_dependents(uninstall_list)  # takes care of '-d'

        # Process dependent_list and update uninstall_list
        has_error = False
        if dependent_list and not args.dependents and not args.force:
            for spec, lst in dependent_list.items():
                tty.error("Will not uninstall %s" % spec.format("$_$@$%@$#", color=True))
                print('')
                print("The following packages depend on it:")
                display_specs(lst, long=True)
                print('')
                has_error = True
        elif args.dependents:
            for key, lst in dependent_list.items():
                uninstall_list.extend(lst)
            uninstall_list = list(set(uninstall_list))

        if has_error:
            tty.die('You can use spack uninstall --dependents to uninstall these dependencies as well')

        if not args.yes_to_all:
            tty.msg("The following packages will be uninstalled : ")
            print('')
            display_specs(uninstall_list, long=True)
            print('')
            ask_for_confirmation('Do you want to proceed ? ')

        # Uninstall everything on the list
        do_uninstall(uninstall_list, args.force)
