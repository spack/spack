# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import llnl.util.tty as tty

import spack.repo
import spack.cmd
import spack.cmd.common.arguments as arguments


description = "patch expanded archive sources in preparation for install"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to stage")


def patch(parser, args):
    if not args.packages:
        tty.die("patch requires at least one package argument")

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    specs = spack.cmd.parse_specs(args.packages, concretize=True)
    for spec in specs:
        package = spack.repo.get(spec)
        package.do_patch()
