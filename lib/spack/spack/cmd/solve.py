# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import re
import sys

import llnl.util.tty as tty
import llnl.util.tty.color as color

import spack
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.hash_types as ht
import spack.package
import spack.solver.asp as asp

description = "concretize a specs using an ASP solver"
section = 'developer'
level = 'long'

#: output options
show_options = ('asp', 'opt', 'output', 'solutions')


def setup_parser(subparser):
    # Solver arguments
    subparser.add_argument(
        '--show', action='store', default='opt,solutions',
        help="select outputs: comma-separated list of: \n"
        "  asp          asp program text\n"
        "  opt          optimization criteria for best model\n"
        "  output       raw clingo output\n"
        "  solutions    models found by asp program\n"
        "  all          all of the above"
    )
    subparser.add_argument(
        '--models', action='store', type=int, default=0,
        help="number of solutions to search (default 0 for all)")

    # Below are arguments w.r.t. spec display (like spack spec)
    arguments.add_common_arguments(
        subparser, ['long', 'very_long', 'install_status', 'reuse']
    )
    subparser.add_argument(
        '-y', '--yaml', action='store_const', dest='format', default=None,
        const='yaml', help='print concrete spec as yaml')
    subparser.add_argument(
        '-j', '--json', action='store_const', dest='format', default=None,
        const='json', help='print concrete spec as json')
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
        '--timers', action='store_true', default=False,
        help='print out timers for different solve phases')
    subparser.add_argument(
        '--stats', action='store_true', default=False,
        help='print out statistics from clingo')
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
    dump = re.split(r'\s*,\s*', args.show)
    if 'all' in dump:
        dump = show_options
    for d in dump:
        if d not in show_options:
            raise ValueError(
                "Invalid option for '--show': '%s'\nchoose from: (%s)"
                % (d, ', '.join(show_options + ('all',))))

    models = args.models
    if models < 0:
        tty.die("model count must be non-negative: %d")

    specs = spack.cmd.parse_specs(args.specs)

    # dump generated ASP program
    result = asp.solve(
        specs, dump=dump, models=models, timers=args.timers, stats=args.stats,
        reuse=args.reuse,
    )
    if 'solutions' not in dump:
        return

    # die if no solution was found
    result.raise_if_unsat()

    # dump the solutions as concretized specs
    if 'solutions' in dump:
        opt, _, _ = min(result.answers)
        if ("opt" in dump) and (not args.format):
            tty.msg("Best of %d considered solutions." % result.nmodels)
            tty.msg("Optimization Criteria:")

            maxlen = max(len(s[2]) for s in result.criteria)
            color.cprint(
                "@*{  Priority  Criterion %sInstalled  ToBuild}" % ((maxlen - 10) * " ")
            )

            fmt = "  @K{%%-8d}  %%-%ds%%9s  %%7s" % maxlen
            for i, (idx, build_idx, name) in enumerate(result.criteria, 1):
                color.cprint(
                    fmt % (
                        i,
                        name,
                        "-" if build_idx is None else opt[idx],
                        opt[idx] if build_idx is None else opt[build_idx],
                    )
                )
            print()

        for spec in result.specs:
            # With -y, just print YAML to output.
            if args.format == 'yaml':
                # use write because to_yaml already has a newline.
                sys.stdout.write(spec.to_yaml(hash=ht.build_hash))
            elif args.format == 'json':
                sys.stdout.write(spec.to_json(hash=ht.build_hash))
            else:
                sys.stdout.write(
                    spec.tree(color=sys.stdout.isatty(), **kwargs))
