# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from llnl.util import tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.config
import spack.environment as ev
import spack.store
from spack.graph import DAGWithDependencyTypes, SimpleDAG, graph_ascii, graph_dot, static_graph_dot

description = "generate graphs of package dependency relationships"
section = "basic"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser

    method = subparser.add_mutually_exclusive_group()
    method.add_argument(
        "-a", "--ascii", action="store_true", help="draw graph as ascii to stdout (default)"
    )
    method.add_argument(
        "-d", "--dot", action="store_true", help="generate graph in dot format and print to stdout"
    )

    subparser.add_argument(
        "-s",
        "--static",
        action="store_true",
        help="graph static (possible) deps, don't concretize (implies --dot)",
    )
    subparser.add_argument(
        "-c",
        "--color",
        action="store_true",
        help="use different colors for different dependency types",
    )

    subparser.add_argument(
        "-i",
        "--installed",
        action="store_true",
        help="graph installed specs, or specs in the active env (implies --dot)",
    )

    arguments.add_common_arguments(subparser, ["deptype", "specs"])


def graph(parser, args):
    if args.installed and args.specs:
        tty.die("cannot specify specs with --installed")

    if args.color and not args.dot:
        tty.die("the --color option can be used only with --dot")

    if args.installed:
        args.dot = True
        env = ev.active_environment()
        if env:
            specs = env.concrete_roots()
        else:
            specs = spack.store.STORE.db.query()

    else:
        specs = spack.cmd.parse_specs(args.specs, concretize=not args.static)

    if not specs:
        setup_parser.parser.print_help()
        return 1

    if args.static:
        args.dot = True
        static_graph_dot(specs, depflag=args.deptype)
        return

    if args.dot:
        builder = SimpleDAG()
        if args.color:
            builder = DAGWithDependencyTypes()
        graph_dot(specs, builder=builder, depflag=args.deptype)
        return

    # ascii is default: user doesn't need to provide it explicitly
    debug = spack.config.get("config:debug")
    graph_ascii(specs[0], debug=debug, depflag=args.deptype)
    for spec in specs[1:]:
        print()  # extra line bt/w independent graphs
        graph_ascii(spec, debug=debug)
