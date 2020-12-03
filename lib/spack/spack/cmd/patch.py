# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.repo
import spack.cmd
import spack.cmd.common.arguments as arguments


description = "patch expanded archive sources in preparation for install"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['no_checksum', 'specs'])


def patch(parser, args):
    if not args.specs:
        tty.die("patch requires at least one spec argument")

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    specs = spack.cmd.parse_specs(args.specs, concretize=True)
    for spec in specs:
        package = spack.repo.get(spec)
        package.do_patch()
