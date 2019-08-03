# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import re
import sys

import llnl.util.tty as tty

import spack
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.package
import spack.solver.asp as asp

description = "concretize a specs using an ASP solver"
section = 'developer'
level = 'long'

#: output options
dump_options = ('asp', 'warnings', 'output', 'solutions')


def setup_parser(subparser):
    # Solver arguments
    subparser.add_argument(
        '--dump', action='store', default=('solutions'),
        help="outputs: a list with any of: "
        "%s (default), all" % ', '.join(dump_options))
    subparser.add_argument(
        '--models', action='store', type=int, default=1,
        help="number of solutions to display (0 for all)")

    # Below are arguments w.r.t. spec display (like spack spec)
    arguments.add_common_arguments(
        subparser, ['long', 'very_long', 'install_status'])
    subparser.add_argument(
        '-y', '--yaml', action='store_true', default=False,
        help='print concrete spec as YAML')
    subparser.add_argument(
        '-c', '--cover', action='store',
        default='nodes', choices=['nodes', 'edges', 'paths'],
        help='how extensively to traverse the DAG (default: nodes)')
    subparser.add_argument(
        '-N', '--namespaces', action='store_true', default=False,
        help='show fully qualified package names')
    subparser.add_argument(
        '-t', '--types', action='store_true', default=False,
        help='show dependency types')
    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="specs of packages")


def solve(parser, args):
    # these are the same options as `spack spec`
    name_fmt = '{namespace}.{name}' if args.namespaces else '{name}'
    fmt = '{@version}{%compiler}{compiler_flags}{variants}{arch=architecture}'
    install_status_fn = spack.spec.Spec.install_status
    kwargs = {
        'cover': args.cover,
        'format': name_fmt + fmt,
        'hashlen': None if args.very_long else 7,
        'show_types': args.types,
        'status_fn': install_status_fn if args.install_status else None,
        'hashes': args.long or args.very_long
    }

    # process dump options
    dump = re.split(r'\s*,\s*', args.dump)
    if 'all' in dump:
        dump = dump_options
    for d in dump:
        if d not in dump_options:
            raise ValueError(
                "Invalid dump option: '%s'\nchoose from: (%s)"
                % (d, ', '.join(dump_options + ('all',))))

    models = args.models
    if models < 0:
        tty.die("model count must be non-negative: %d")

    specs = spack.cmd.parse_specs(args.specs)

    # dump generated ASP program
    result = asp.solve(specs, dump=dump, models=models)

    # die if no solution was found
    # TODO: we need to be able to provide better error messages than this
    if not result.satisfiable:
        tty.die("Unsatisfiable spec.")

    # dump the solutions as concretized specs
    if 'solutions' in dump:
        for i, answer in enumerate(result.answers):
            tty.msg("Answer %d" % (i + 1))
            for spec in specs:
                answer_spec = answer[spec.name]
                if args.yaml:
                    out = answer_spec.to_yaml()
                else:
                    out = answer_spec.tree(
                        color=sys.stdout.isatty(), **kwargs)
                sys.stdout.write(out)
