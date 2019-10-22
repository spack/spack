# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.environment as ev

description = 'concretize an environment and write a lockfile'
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")


def concretize(parser, args):
    env = ev.get_env(args, 'concretize', required=True)
    concretized_specs = env.concretize(force=args.force)
    ev.display_specs(concretized_specs)
    env.write()
