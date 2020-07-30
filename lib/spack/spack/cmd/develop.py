# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev

from spack.error import SpackError

description = 'add a spec to an environments dev-build information'
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument('-p', '--path',
                           help='Source location of package')
    subparser.add_argument('-c', '--clone', action='store_true',
                           help='Clone package into source path')
    arguments.add_common_arguments(subparser, ['spec'])


def develop(parser, args):
    env = ev.get_env(args, 'develop', required=True)

    if not args.spec:
        raise SpackError("No spec provided to spack develop command")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) != 1:
        raise SpackError("spack develop requires exactly one named spec")

    spec = specs[0]
    if not spec.versions.concrete:
        raise SpackError("Packages to develop must have a concrete version")

    if args.clone:
        path = args.path or os.path.join(os.getcwd(), spec.name)
        # TODO: clone to path
        raise NotImplementedError
    else:
        if not args.path:
            raise SpackError("Must provide either path or clone argument")
        elif not os.path.exists(args.path):
            raise SpackError("Provided path %s does not exist" % args.path)
        path = args.path

    with env.write_transaction():
        changed = env.develop(spec, path)
        if changed:
            env.write()
