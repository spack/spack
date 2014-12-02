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
        '-p', '--paths', action='store_true', dest='paths',
        help='Show paths to package install directories')
    format_group.add_argument(
        '-l', '--long', action='store_true', dest='full_specs',
        help='Show full-length specs of installed packages')

    subparser.add_argument(
        'query_specs', nargs=argparse.REMAINDER,
        help='optional specs to filter results')


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

    # Make a dict with specs keyed by architecture and compiler.
    index = index_by(specs, ('architecture', 'compiler'))

    # Traverse the index and print out each package
    for i, (architecture, compiler) in enumerate(sorted(index)):
        if i > 0: print
        tty.hline("%s / %s" % (compiler, architecture), char='-')

        specs = index[(architecture, compiler)]
        specs.sort()

        abbreviated = [s.format('$_$@$+$#', color=True) for s in specs]

        if args.paths:
            # Print one spec per line along with prefix path
            width = max(len(s) for s in abbreviated)
            width += 2
            format = "    %-{}s%s".format(width)

            for abbrv, spec in zip(abbreviated, specs):
                print format % (abbrv, spec.prefix)

        elif args.full_specs:
            for spec in specs:
                print spec.tree(indent=4, format='$_$@$+', color=True),
        else:
            max_len = max([len(s.name) for s in specs])
            max_len += 4

            colify((s.format('$-_$@$+$#') for s in specs), decorator=spack.spec.colorize_spec)
