# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import sys

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.util.environment

description = "remove package from the user environment variables`"
section = "user environment"
level = "short"


def setup_parser(subparser):
    """Parser is only constructed so that this prints a nice help
       message with -h. """
    arguments.add_common_arguments(subparser, ['installed_spec'])

    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        '--sh', action='store_const', dest='shell', const='sh',
        help="print sh commands to activate the environment")
    shells.add_argument(
        '--csh', action='store_const', dest='shell', const='csh',
        help="print csh commands to activate the environment")

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER,
        help='spec of package to unload with modules')


def unload(parser, args):
    env = ev.get_env(args, 'unload')
    specs = list(map(lambda spec: spack.cmd.disambiguate_spec(spec, env),
                     spack.cmd.parse_specs(args.specs)))
    if not args.shell:
        msg = [
            "This command works best with Spack's shell support",
            ""
        ] + spack.cmd.common.shell_init_instructions + [
            'Or, if you want to use `spack load` without initializing',
            'shell support, you can run one of these:',
            '',
            '    eval `spack unload --sh %s`   # for bash/sh' % ' '.join(specs),
            '    eval `spack unload --csh %s`  # for csh/tcsh' % ' '.join(specs),
        ]
        tty.msg(*msg)
        return 1

    env_mod = spack.util.environment.EnvironmentModifications()
    for spec in specs:
        env_mod.extend(ev.environment_modifications_for_spec(spec).reversed())
    cmds = env_mod.shell_modifications()

    sys.stdout.write(cmds)
