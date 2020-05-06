# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.environment as ev
import llnl.util.tty.color as clr

description = clr.colorize(
    'Concretize an environment and write a lockfile. The package status, '
    'hash, and spec for each package and dependency are shown. \n\n'
    'The status symbols are: \n'
    ' @*g{[\u2714]} Package is installed. \n'
    ' @*K{[-]} Package is not installed.\n'
    ' @*b{[^]} Package is installed upstream.\n'
    ' @*r{[?]} Package install is missing.')
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")
    subparser.add_argument(
        '-d', '--dry-run', action='store_true', default=False,
        help="(Re-)concretize, but don't generate the lockfile.")


def concretize(parser, args):
    env = ev.get_env(args, 'concretize', required=True)
    with env.write_transaction():
        concretized_specs = env.concretize(force=args.force or args.dry_run)
        ev.display_specs(concretized_specs)

        if not args.dry_run:
            env.write()
