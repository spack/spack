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
import argparse

import spack
import spack.cmd
from spack.graph import *

description = "Generate graphs of package dependency relationships."

def setup_parser(subparser):
    setup_parser.parser = subparser

    method = subparser.add_mutually_exclusive_group()
    method.add_argument(
        '--ascii', action='store_true',
        help="Draw graph as ascii to stdout (default).")
    method.add_argument(
        '--dot', action='store_true',
        help="Generate graph in dot format and print to stdout.")

    subparser.add_argument(
        '--concretize', action='store_true', help="Concretize specs before graphing.")

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="specs of packages to graph.")


def graph(parser, args):
    specs = spack.cmd.parse_specs(
        args.specs, normalize=True, concretize=args.concretize)

    if not specs:
        setup_parser.parser.print_help()
        return 1

    if args.dot:    # Dot graph only if asked for.
        graph_dot(*specs)

    elif specs:     # ascii is default: user doesn't need to provide it explicitly
        graph_ascii(specs[0], debug=spack.debug)
        for spec in specs[1:]:
            print # extra line bt/w independent graphs
            graph_ascii(spec, debug=spack.debug)
