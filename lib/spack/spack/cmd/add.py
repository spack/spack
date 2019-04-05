# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev


description = 'add a spec to an environment'
section = "environments"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['specs'])


def add(parser, args):
    env = ev.get_env(args, 'add', required=True)

    for spec in spack.cmd.parse_specs(args.specs):
        if not env.add(spec):
            tty.msg("Package {0} was already added to {1}"
                    .format(spec.name, env.name))
        else:
            tty.msg('Adding %s to environment %s' % (spec, env.name))
    env.write()
