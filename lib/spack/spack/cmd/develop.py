# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

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
    subparser.add_argument('--no-clone', action='store_true',
                           help='The package already exists at the source path')
    arguments.add_common_arguments(subparser, ['spec'])


def develop(parser, args):
    env = ev.get_env(args, 'develop', required=True)

    if not args.spec:
        if args.no_clone:
            raise SpackError("No spec provided to spack develop command")
        else:
            # download all dev specs
            for name, entry in env.dev_specs.items():
                path = entry.get('path', name)
                abspath = path if os.path.isabs(path) else os.path.join(
                    env.path, path)
                if os.path.exists(abspath):
                    msg = "Skipping developer download of %s" % entry['spec']
                    msg += " because its path already exists."
                    tty.msg(msg)
                    continue
                spack.spec.Spec(entry['spec']).package.fetcher.clone(abspath)

            if not env.dev_specs:
                tty.warn("No develop specs to download")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        raise SpackError("spack develop requires at most one named spec")

    spec = specs[0]
    if not spec.versions.concrete:
        raise SpackError("Packages to develop must have a concrete version")

    if args.no_clone:
        path = args.path
    else:
        path = args.path or spec.name

    if not path:
        raise SpackError("Must provide either path or clone argument")
    elif args.no_clone and not os.path.exists(path):
        raise SpackError("Provided path %s does not exist" % args.path)

    with env.write_transaction():
        changed = env.develop(spec, path, not args.no_clone)
        if changed:
            env.write()
