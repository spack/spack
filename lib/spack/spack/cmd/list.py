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
import cgi
import fnmatch
import re
import sys
from six import StringIO

import llnl.util.tty as tty
import spack
from llnl.util.tty.colify import colify

description = "print available spack packages to stdout in different formats"

formatters = {}


def formatter(func):
    """Decorator used to register formatters"""
    formatters[func.__name__] = func
    return func


def setup_parser(subparser):
    subparser.add_argument(
        'filter', nargs=argparse.REMAINDER,
        help='optional case-insensitive glob patterns to filter results')
    subparser.add_argument(
        '-d', '--search-description', action='store_true', default=False,
        help='filtering will also search the description for a match')
    subparser.add_argument(
        '--format', default='name_only', choices=formatters,
        help='format to be used to print the output [default: name_only]')


def filter_by_name(pkgs, args):
    """
    Filters the sequence of packages according to user prescriptions

    Args:
        pkgs: sequence of packages
        args: parsed command line arguments

    Returns:
        filtered and sorted list of packages
    """
    if args.filter:
        res = []
        for f in args.filter:
            if '*' not in f and '?' not in f:
                r = fnmatch.translate('*' + f + '*')
            else:
                r = fnmatch.translate(f)

            rc = re.compile(r, flags=re.IGNORECASE)
            res.append(rc)

        if args.search_description:
            def match(p, f):
                if f.match(p):
                    return True

                pkg = spack.repo.get(p)
                if pkg.__doc__:
                    return f.match(pkg.__doc__)
                return False
        else:
            def match(p, f):
                return f.match(p)
        pkgs = [p for p in pkgs if any(match(p, f) for f in res)]

    return sorted(pkgs, key=lambda s: s.lower())


@formatter
def name_only(pkgs):
    indent = 0
    if sys.stdout.isatty():
        tty.msg("%d packages." % len(pkgs))
    colify(pkgs, indent=indent)


@formatter
def rst(pkgs):
    """Print out information on all packages in restructured text."""

    def github_url(pkg):
        """Link to a package file on github."""
        url = 'https://github.com/LLNL/spack/blob/develop/var/spack/repos/builtin/packages/{0}/package.py'
        return url.format(pkg.name)

    def rst_table(elts):
        """Print out a RST-style table."""
        cols = StringIO()
        ncol, widths = colify(elts, output=cols, tty=True)
        header = ' '.join('=' * (w - 1) for w in widths)
        return '%s\n%s%s' % (header, cols.getvalue(), header)

    pkg_names = pkgs
    pkgs = [spack.repo.get(name) for name in pkg_names]

    print('.. _package-list:')
    print()
    print('============')
    print('Package List')
    print('============')
    print()
    print('This is a list of things you can install using Spack.  It is')
    print('automatically generated based on the packages in the latest Spack')
    print('release.')
    print()
    print('Spack currently has %d mainline packages:' % len(pkgs))
    print()
    print(rst_table('`%s`_' % p for p in pkg_names))
    print()

    # Output some text for each package.
    for pkg in pkgs:
        print('-----')
        print()
        print('.. _%s:' % pkg.name)
        print()
        # Must be at least 2 long, breaks for single letter packages like R.
        print('-' * max(len(pkg.name), 2))
        print(pkg.name)
        print('-' * max(len(pkg.name), 2))
        print()
        print('Homepage:')
        print('  * `%s <%s>`__' % (cgi.escape(pkg.homepage), pkg.homepage))
        print()
        print('Spack package:')
        print('  * `%s/package.py <%s>`__' % (pkg.name, github_url(pkg)))
        print()
        if pkg.versions:
            print('Versions:')
            print('  ' + ', '.join(str(v) for v in
                                   reversed(sorted(pkg.versions))))
            print()

        for deptype in spack.alldeps:
            deps = pkg.dependencies_of_type(deptype)
            if deps:
                print('%s Dependencies' % deptype.capitalize())
                print('  ' + ', '.join('%s_' % d if d in pkg_names
                                       else d for d in deps))
                print()

        print('Description:')
        print(pkg.format_doc(indent=2))
        print()


def list(parser, args):
    # Retrieve the names of all the packages
    pkgs = set(spack.repo.all_package_names())
    # Filter the set appropriately
    sorted_packages = filter_by_name(pkgs, args)
    # Print to stdout
    formatters[args.format](sorted_packages)
