# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev


description = 'remove specs from an environment'
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-a', '--all', action='store_true',
        help="remove all specs from (clear) the environment")
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="remove concretized spec (if any) immediately")
    arguments.add_common_arguments(subparser, ['specs'])


def remove(parser, args):
    env = ev.get_env(args, 'remove', required=True)

    if args.all:
        env.clear()
    else:
        for spec in spack.cmd.parse_specs(args.specs):
            tty.msg('Removing %s from environment %s' % (spec, env.name))
            env.remove(spec, force=args.force)
    env.write()
