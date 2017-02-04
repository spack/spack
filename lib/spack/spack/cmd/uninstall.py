##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from __future__ import print_function

import argparse

import llnl.util.tty as tty
import spack
import spack.cmd
import spack.store
import spack.repository

description = "remove an installed package"

error_message = """You can either:
    a) Use a more specific spec, or
    b) use spack uninstall -a to uninstall ALL matching specs.
"""

# Arguments for display_specs when we find ambiguity
display_args = {
    'long': True,
    'show_flags': True,
    'variants': True
}


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="remove regardless of whether other packages depend on this one")

    subparser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="USE CAREFULLY. remove ALL installed packages that match each "
             "supplied spec. i.e., if you say uninstall `libelf`,"
             " ALL versions of `libelf` are uninstalled. if no spec is "
             "supplied all installed software will be uninstalled. this "
             "is both useful and dangerous, like rm -r")

    subparser.add_argument(
        '-d', '--dependents', action='store_true', dest='dependents',
        help='also uninstall any packages that depend on the ones given '
             'via command line')

    subparser.add_argument(
        '-y', '--yes-to-all', action='store_true', dest='yes_to_all',
        help='assume "yes" is the answer to every confirmation requested')

    subparser.add_argument(
        'packages',
        nargs=argparse.REMAINDER,
        help="specs of packages to uninstall")


def concretize_specs(specs, allow_multiple_matches=False, force=False):
    """Returns a list of specs matching the non necessarily
    concretized specs given from cli

    Args:
        specs: list of specs to be matched against installed packages
        allow_multiple_matches : if True multiple matches are admitted

    Return:
        list of specs
    """
    # List of specs that match expressions given via command line
    specs_from_cli = []
    has_errors = False
    for spec in specs:
        matching = spack.store.db.query(spec)
        # For each spec provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matching) > 1:
            tty.error("%s matches multiple packages:" % spec)
            print()
            spack.cmd.display_specs(matching, **display_args)
            print()
            has_errors = True

        # No installed package matches the query
        if len(matching) == 0 and spec is not any:
            tty.error("%s does not match any installed packages." % spec)
            has_errors = True

        specs_from_cli.extend(matching)
    if has_errors:
        tty.die(error_message)

    return specs_from_cli


def installed_dependents(specs):
    """Returns a dictionary that maps a spec with a list of its
    installed dependents

    Args:
        specs: list of specs to be checked for dependents

    Returns:
        dictionary of installed dependents
    """
    dependents = {}
    for item in specs:
        lst = [x for x in spack.store.db.installed_dependents(item)
               if x not in specs]
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
        except spack.repository.UnknownPackageError:
            # The package.py file has gone away -- but still
            # want to uninstall.
            spack.Package(item).do_uninstall(force=True)

    # Sort packages to be uninstalled by the number of installed dependents
    # This ensures we do things in the right order
    def num_installed_deps(pkg):
        return len(spack.store.db.installed_dependents(pkg.spec))

    packages.sort(key=num_installed_deps)
    for item in packages:
        item.do_uninstall(force=force)


def get_uninstall_list(args):
    specs = [any]
    if args.packages:
        specs = spack.cmd.parse_specs(args.packages)

    # Gets the list of installed specs that match the ones give via cli
    # takes care of '-a' is given in the cli
    uninstall_list = concretize_specs(specs, args.all, args.force)

    # Takes care of '-d'
    dependent_list = installed_dependents(uninstall_list)

    # Process dependent_list and update uninstall_list
    has_error = False
    if dependent_list and not args.dependents and not args.force:
        for spec, lst in dependent_list.items():
            tty.error("Will not uninstall %s" %
                      spec.format("$_$@$%@$/", color=True))
            print('')
            print("The following packages depend on it:")
            spack.cmd.display_specs(lst, **display_args)
            print('')
            has_error = True
    elif args.dependents:
        for key, lst in dependent_list.items():
            uninstall_list.extend(lst)
        uninstall_list = list(set(uninstall_list))
    if has_error:
        tty.die('You can use spack uninstall --dependents '
                'to uninstall these dependencies as well')

    return uninstall_list


def uninstall(parser, args):
    if not args.packages and not args.all:
        tty.die("uninstall requires at least one package argument.")

    uninstall_list = get_uninstall_list(args)

    if not uninstall_list:
        tty.msg("There are no package to uninstall.")
        return

    if not args.yes_to_all:
        tty.msg("The following packages will be uninstalled : ")
        print('')
        spack.cmd.display_specs(uninstall_list, **display_args)
        print('')
        spack.cmd.ask_for_confirmation('Do you want to proceed ? ')

    # Uninstall everything on the list
    do_uninstall(uninstall_list, args.force)
