# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import sys

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.util.environment
import spack.user_environment as uenv

description = "add package to the user environment variables"
section = "user environment"
level = "short"


def setup_parser(subparser):
    """Parser is only constructed so that this prints a nice help
       message with -h. """
    arguments.add_common_arguments(
        subparser, ['recurse_dependencies', 'installed_spec'])

    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        '--sh', action='store_const', dest='shell', const='sh',
        help="print sh commands to load the package")
    shells.add_argument(
        '--csh', action='store_const', dest='shell', const='csh',
        help="print csh commands to load the package")

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER,
        help="spec of package to load"
    )
    arguments.add_common_arguments(subparser, ['recurse_dependencies'])


def load(parser, args):
    env = ev.get_env(args, 'load')
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
            '    eval `spack load --sh %s`   # for bash/sh' % args.specs,
            '    eval `spack load --csh %s`  # for csh/tcsh' % args.specs,
        ]
        tty.msg(*msg)
        return 1

    if args.recurse_dependencies:
        specs = [dep for spec in specs
                 for dep in spec.traverse(root=True, order='post')]

    env_mod = spack.util.environment.EnvironmentModifications()
    for spec in specs:
        env_mod.extend(uenv.environment_modifications_for_spec(spec))
    cmds = env_mod.shell_modifications(args.shell)

    sys.stdout.write(cmds)
