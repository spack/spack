# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import llnl.util.tty as tty

import spack.repo
import spack.cmd
import spack.cmd.common.arguments as arguments

description = "expand downloaded archive in preparation for install"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        '-p', '--path', dest='path',
        help="path to stage package, does not add to spack tree")

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="specs of packages to stage")


def stage(parser, args):
    if not args.specs:
        tty.die("stage requires at least one package argument")

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    specs = spack.cmd.parse_specs(args.specs, concretize=True)
    for spec in specs:
        package = spack.repo.get(spec)
        if args.path:
            package.path = args.path
        package.do_stage()
