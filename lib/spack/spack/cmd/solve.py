# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse

import spack
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.package
import spack.solver.asp as asp

description = "concretize a specs using an ASP solver"
section = 'developer'
level = 'long'


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['long', 'very_long'])
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
        '-I', '--install-status', action='store_true', default=False,
        help='show install status of packages. packages can be: '
             'installed [+], missing and needed by an installed package [-], '
             'or not installed (no annotation)')
    subparser.add_argument(
        '-t', '--types', action='store_true', default=False,
        help='show dependency types')
    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="specs of packages")


def solve(parser, args):
    specs = spack.cmd.parse_specs(args.specs)
    asp.solve(specs)
