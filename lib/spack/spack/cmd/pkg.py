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

import os

import argparse
import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack
from spack.util.executable import *

description = "query packages associated with particular git revisions"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='pkg_command')

    add_parser = sp.add_parser('add', help=pkg_add.__doc__)
    add_parser.add_argument('packages', nargs=argparse.REMAINDER,
                            help="names of packages to add to git repo")

    list_parser = sp.add_parser('list', help=pkg_list.__doc__)
    list_parser.add_argument('rev', default='HEAD', nargs='?',
                             help="revision to list packages for")

    diff_parser = sp.add_parser('diff', help=pkg_diff.__doc__)
    diff_parser.add_argument(
        'rev1', nargs='?', default='HEAD^',
        help="revision to compare against")
    diff_parser.add_argument(
        'rev2', nargs='?', default='HEAD',
        help="revision to compare to rev1 (default is HEAD)")

    add_parser = sp.add_parser('added', help=pkg_added.__doc__)
    add_parser.add_argument(
        'rev1', nargs='?', default='HEAD^',
        help="revision to compare against")
    add_parser.add_argument(
        'rev2', nargs='?', default='HEAD',
        help="revision to compare to rev1 (default is HEAD)")

    rm_parser = sp.add_parser('removed', help=pkg_removed.__doc__)
    rm_parser.add_argument(
        'rev1', nargs='?', default='HEAD^',
        help="revision to compare against")
    rm_parser.add_argument(
        'rev2', nargs='?', default='HEAD',
        help="revision to compare to rev1 (default is HEAD)")


def get_git():
    # cd to spack prefix to do git operations
    os.chdir(spack.prefix)

    # If this is a non-git version of spack, give up.
    if not os.path.isdir('.git'):
        tty.die("No git repo in %s. Can't use 'spack pkg'" % spack.prefix)

    return which("git", required=True)


def list_packages(rev):
    git = get_git()
    pkgpath = os.path.join(spack.packages_path, 'packages')
    relpath = pkgpath[len(spack.prefix + os.path.sep):] + os.path.sep
    output = git('ls-tree', '--full-tree', '--name-only', rev, relpath,
                 output=str)
    return sorted(line[len(relpath):] for line in output.split('\n') if line)


def pkg_add(args):
    for pkg_name in args.packages:
        filename = spack.repo.filename_for_package_name(pkg_name)
        if not os.path.isfile(filename):
            tty.die("No such package: %s.  Path does not exist:" %
                    pkg_name, filename)

        git = get_git()
        git('-C', spack.packages_path, 'add', filename)


def pkg_list(args):
    """List packages associated with a particular spack git revision."""
    colify(list_packages(args.rev))


def diff_packages(rev1, rev2):
    p1 = set(list_packages(rev1))
    p2 = set(list_packages(rev2))
    return p1.difference(p2), p2.difference(p1)


def pkg_diff(args):
    """Compare packages available in two different git revisions."""
    u1, u2 = diff_packages(args.rev1, args.rev2)

    if u1:
        print("%s:" % args.rev1)
        colify(sorted(u1), indent=4)
        if u1:
            print()

    if u2:
        print("%s:" % args.rev2)
        colify(sorted(u2), indent=4)


def pkg_removed(args):
    """Show packages removed since a commit."""
    u1, u2 = diff_packages(args.rev1, args.rev2)
    if u1:
        colify(sorted(u1))


def pkg_added(args):
    """Show packages added since a commit."""
    u1, u2 = diff_packages(args.rev1, args.rev2)
    if u2:
        colify(sorted(u2))


def pkg(parser, args):
    action = {'add': pkg_add,
              'diff': pkg_diff,
              'list': pkg_list,
              'removed': pkg_removed,
              'added': pkg_added}
    action[args.pkg_command](args)
