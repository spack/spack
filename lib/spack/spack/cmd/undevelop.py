# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments

description = 'remove specs from an environment'
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-a', '--all', action='store_true',
        help="remove all specs from (clear) the environment")
    arguments.add_common_arguments(subparser, ['specs'])


def undevelop(parser, args):
    env = spack.cmd.require_active_env(cmd_name='undevelop')

    if args.all:
        specs = env.dev_specs.keys()
    else:
        specs = spack.cmd.parse_specs(args.specs)

    with env.write_transaction():
        changed = False
        for spec in specs:
            tty.msg('Removing %s from environment %s development specs'
                    % (spec, env.name))
            changed |= env.undevelop(spec)
        if changed:
            env.write()
