# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import llnl.util.tty as tty

import spack.cmd
import spack.config
import spack.store
from spack.dependency import all_deptypes, canonical_deptype
from spack.graph import graph_dot, graph_ascii

description = "generate graphs of package dependency relationships"
section = "basic"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser

    method = subparser.add_mutually_exclusive_group()
    method.add_argument(
        '-a', '--ascii', action='store_true',
        help="draw graph as ascii to stdout (default)")
    method.add_argument(
        '-d', '--dot', action='store_true',
        help="generate graph in dot format and print to stdout")

    subparser.add_argument(
        '-n', '--normalize', action='store_true',
        help="skip concretization; only print normalized spec")

    subparser.add_argument(
        '-s', '--static', action='store_true',
        help="use static information from packages, not dynamic spec info")

    subparser.add_argument(
        '-i', '--installed', action='store_true',
        help="graph all installed specs in dot format (implies --dot)")

    subparser.add_argument(
        '-t', '--deptype', action='store',
        help="comma-separated list of deptypes to traverse. default=%s"
        % ','.join(all_deptypes))

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER,
        help="specs of packages to graph")


def graph(parser, args):
    concretize = not args.normalize
    if args.installed:
        if args.specs:
            tty.die("Can't specify specs with --installed")
        args.dot = True
        specs = spack.store.db.query()

    else:
        specs = spack.cmd.parse_specs(
            args.specs, normalize=True, concretize=concretize)

    if not specs:
        setup_parser.parser.print_help()
        return 1

    deptype = all_deptypes
    if args.deptype:
        deptype = tuple(args.deptype.split(','))
        if deptype == ('all',):
            deptype = 'all'
        deptype = canonical_deptype(deptype)

    if args.dot:  # Dot graph only if asked for.
        graph_dot(specs, static=args.static, deptype=deptype)

    elif specs:  # ascii is default: user doesn't need to provide it explicitly
        debug = spack.config.get('config:debug')
        graph_ascii(specs[0], debug=debug, deptype=deptype)
        for spec in specs[1:]:
            print()  # extra line bt/w independent graphs
            graph_ascii(spec, debug=debug)
