# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.cmd
import spack.cmd.common.arguments
import spack.environment as ev

description = 'concretize an environment and write a lockfile'
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")
    subparser.add_argument(
        '--test', default=None,
        choices=['root', 'all'],
        help="""Concretize with test dependencies. When 'root' is chosen, test
dependencies are only added for the environment's root specs. When 'all' is
chosen, test dependencies are enabled for all packages in the environment.""")
    subparser.add_argument(
        '-q', '--quiet', action='store_true',
        help="Don't print concretized specs")

    spack.cmd.common.arguments.add_concretizer_args(subparser)


def concretize(parser, args):
    env = spack.cmd.require_active_env(cmd_name='concretize')

    if args.test == 'all':
        tests = True
    elif args.test == 'root':
        tests = [spec.name for spec in env.user_specs]
    else:
        tests = False

    with env.write_transaction():
        concretized_specs = env.concretize(force=args.force, tests=tests)
        if not args.quiet:
            ev.display_specs(concretized_specs)
        env.write()
