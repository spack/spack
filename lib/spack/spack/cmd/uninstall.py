# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse

import spack.cmd
import spack.package
import spack.cmd.common.arguments as arguments
import spack.repo
import spack.store

from llnl.util import tty

description = "remove installed packages"
section = "build"
level = "short"

error_message = """You can either:
    a) use a more specific spec, or
    b) use `spack uninstall --all` to uninstall ALL matching specs.
"""

# Arguments for display_specs when we find ambiguity
display_args = {
    'long': True,
    'show_flags': True,
    'variants': True
}


def add_common_arguments(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="remove regardless of whether other packages depend on this one")
    arguments.add_common_arguments(
        subparser, ['recurse_dependents', 'yes_to_all'])


def setup_parser(subparser):
    add_common_arguments(subparser)
    subparser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="USE CAREFULLY. remove ALL installed packages that match each "
             "supplied spec. i.e., if you `uninstall --all libelf`,"
             " ALL versions of `libelf` are uninstalled. if no spec is "
             "supplied all installed software will be uninstalled.")

    subparser.add_argument(
        'packages',
        nargs=argparse.REMAINDER,
        help="specs of packages to uninstall")


def find_matching_specs(specs, allow_multiple_matches=False, force=False):
    """Returns a list of specs matching the not necessarily
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
            tty.error('{0} matches multiple packages:'.format(spec))
            print()
            spack.cmd.display_specs(matching, **display_args)
            print()
            has_errors = True

        # No installed package matches the query
        if len(matching) == 0 and spec is not any:
            tty.error('{0} does not match any installed packages.'.format(
                spec))
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
        installed = spack.store.db.installed_relatives(
            item, 'parents', True)
        lst = [x for x in installed if x not in specs]
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
        except spack.repo.UnknownEntityError:
            # The package.py file has gone away -- but still
            # want to uninstall.
            spack.package.Package.uninstall_by_spec(item, force=True)

    # Sort packages to be uninstalled by the number of installed dependents
    # This ensures we do things in the right order
    def num_installed_deps(pkg):
        dependents = spack.store.db.installed_relatives(
            pkg.spec, 'parents', True)
        return len(dependents)

    packages.sort(key=num_installed_deps)
    for item in packages:
        item.do_uninstall(force=force)


def get_uninstall_list(args, specs):
    # Gets the list of installed specs that match the ones give via cli
    # takes care of '-a' is given in the cli
    uninstall_list = find_matching_specs(specs, args.all, args.force)

    # Takes care of '-R'
    dependent_list = installed_dependents(uninstall_list)

    # Process dependent_list and update uninstall_list
    has_error = False
    if dependent_list and not args.dependents and not args.force:
        for spec, lst in dependent_list.items():
            tty.error("Will not uninstall %s" % spec.cformat("$_$@$%@$/"))
            print('')
            print('The following packages depend on it:')
            spack.cmd.display_specs(lst, **display_args)
            print('')
            has_error = True
    elif args.dependents:
        for key, lst in dependent_list.items():
            uninstall_list.extend(lst)
        uninstall_list = list(set(uninstall_list))
    if has_error:
        tty.die('Use `spack uninstall --dependents` '
                'to uninstall these dependencies as well.')

    return uninstall_list


def uninstall_specs(args, specs):
    uninstall_list = get_uninstall_list(args, specs)

    if not uninstall_list:
        tty.warn('There are no package to uninstall.')
        return

    if not args.yes_to_all:
        tty.msg('The following packages will be uninstalled:\n')
        spack.cmd.display_specs(uninstall_list, **display_args)
        answer = tty.get_yes_or_no('Do you want to proceed?', default=False)
        if not answer:
            tty.die('Will not uninstall any packages.')

    # Uninstall everything on the list
    do_uninstall(uninstall_list, args.force)


def uninstall(parser, args):
    if not args.packages and not args.all:
        tty.die('uninstall requires at least one package argument.',
                '  Use `spack uninstall --all` to uninstall ALL packages.')

    uninstall_specs(
        args, spack.cmd.parse_specs(args.packages) if args.packages else [any])
