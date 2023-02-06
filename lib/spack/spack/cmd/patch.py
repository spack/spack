# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.repo

description = "patch expanded archive sources in preparation for install"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["no_checksum", "deprecated", "specs"])
    arguments.add_concretizer_args(subparser)


def patch(parser, args):
    if not args.specs:
        tty.die("patch requires at least one spec argument")

    if args.no_checksum:
        spack.config.set("config:checksum", False, scope="command_line")

    if args.deprecated:
        spack.config.set("config:deprecated", True, scope="command_line")

    specs = spack.cmd.parse_specs(args.specs, concretize=True)
    for spec in specs:
        spec.package.do_patch()
