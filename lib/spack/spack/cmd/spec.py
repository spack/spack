# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import sys

import llnl.util.tty as tty

import spack
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.spec
import spack.hash_types as ht

description = "show what would be installed, given a spec"
section = "build"
level = "short"


def setup_parser(subparser):
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


def spec(parser, args):
    name_fmt = '{namespace}.{name}' if args.namespaces else '{name}'
    fmt = '{@version}{%compiler}{compiler_flags}{variants}{arch=architecture}'
    install_status_fn = spack.spec.Spec.install_status
    kwargs = {
        'cover': args.cover,
        'format': name_fmt + fmt,
        'hashlen': None if args.very_long else 7,
        'show_types': args.types,
        'status_fn': install_status_fn if args.install_status else None
    }

    if not args.specs:
        tty.die("spack spec requires at least one spec")

    for spec in spack.cmd.parse_specs(args.specs):
        # With -y, just print YAML to output.
        if args.yaml:
            if spec.name in spack.repo.path or spec.virtual:
                spec.concretize()

            # use write because to_yaml already has a newline.
            sys.stdout.write(spec.to_yaml(hash=ht.build_hash))
            continue

        kwargs['hashes'] = False  # Always False for input spec
        print("Input spec")
        print("--------------------------------")
        print(spec.tree(**kwargs))

        kwargs['hashes'] = args.long or args.very_long
        print("Concretized")
        print("--------------------------------")
        spec.concretize()
        print(spec.tree(**kwargs))
