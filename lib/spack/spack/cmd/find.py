##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
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
import sys
import collections
import itertools
from external import argparse
from StringIO import StringIO

import llnl.util.tty as tty
from llnl.util.tty.colify import *
from llnl.util.tty.color import *
from llnl.util.lang import *

import spack
import spack.spec

description ="Find installed spack packages"

def setup_parser(subparser):
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument(
        '-p', '--paths', action='store_const', dest='mode', const='paths',
        help='Show paths to package install directories')
    format_group.add_argument(
        '-d', '--deps', action='store_const', dest='mode', const='deps',
        help='Show full dependency DAG of installed packages')

    subparser.add_argument(
        '-l', '--long', action='store_true', dest='long',
        help='Show dependency hashes as well as versions.')
    subparser.add_argument(
        '-L', '--very-long', action='store_true', dest='very_long',
        help='Show dependency hashes as well as versions.')

    subparser.add_argument(
        'query_specs', nargs=argparse.REMAINDER,
        help='optional specs to filter results')


def gray_hash(spec, length):
    return colorize('@K{%s}' % spec.dag_hash(length))


def display_specs(specs, **kwargs):
    mode = kwargs.get('mode', 'short')
    hashes = kwargs.get('long', False)

    hlen = 7
    if kwargs.get('very_long', False):
        hashes = True
        hlen = None

    # Make a dict with specs keyed by architecture and compiler.
    index = index_by(specs, ('architecture', 'compiler'))

    # Traverse the index and print out each package
    for i, (architecture, compiler) in enumerate(sorted(index)):
        if i > 0: print

        header = "%s{%s} / %s{%s}" % (
            spack.spec.architecture_color, architecture,
            spack.spec.compiler_color, compiler)
        tty.hline(colorize(header), char='-')

        specs = index[(architecture,compiler)]
        specs.sort()

        abbreviated = [s.format('$_$@$+', color=True) for s in specs]
        if mode == 'paths':
            # Print one spec per line along with prefix path
            width = max(len(s) for s in abbreviated)
            width += 2
            format = "    %%-%ds%%s" % width

            for abbrv, spec in zip(abbreviated, specs):
                if hashes:
                    print gray_hash(spec, hlen),
                print format % (abbrv, spec.prefix)

        elif mode == 'deps':
            for spec in specs:
                print spec.tree(
                    format='$_$@$+',
                    color=True,
                    indent=4,
                    prefix=(lambda s: gray_hash(s, hlen)) if hashes else None)

        elif mode == 'short':
            def fmt(s):
                string = ""
                if hashes:
                    string += gray_hash(s, hlen) + ' '
                string += s.format('$-_$@$+', color=True)
                return string
            colify(fmt(s) for s in specs)

        else:
            raise ValueError(
                "Invalid mode for display_specs: %s. Must be one of (paths, deps, short)." % mode)



def find(parser, args):
    # Filter out specs that don't exist.
    query_specs = spack.cmd.parse_specs(args.query_specs)
    query_specs, nonexisting = partition_list(
        query_specs, lambda s: spack.db.exists(s.name))

    if nonexisting:
        msg = "No such package%s: " % ('s' if len(nonexisting) > 1 else '')
        msg += ", ".join(s.name for s in nonexisting)
        tty.msg(msg)

        if not query_specs:
            return

    # Get all the specs the user asked for
    if not query_specs:
        specs = set(spack.db.installed_package_specs())
    else:
        results = [set(spack.db.get_installed(qs)) for qs in query_specs]
        specs = set.union(*results)

    if not args.mode:
        args.mode = 'short'

    if sys.stdout.isatty():
        tty.msg("%d installed packages." % len(specs))
    display_specs(specs, mode=args.mode,
                  long=args.long,
                  very_long=args.very_long)
