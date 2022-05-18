# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.repo
import spack.stage

description = "expand downloaded archive in preparation for install"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(
        subparser, ['no_checksum', 'deprecated', 'specs'])
    subparser.add_argument(
        '-p', '--path', dest='path',
        help="path to stage package, does not add to spack tree")


def stage(parser, args):
    if not args.specs:
        env = ev.active_environment()
        if env:
            tty.msg("Staging specs from environment %s" % env.name)
            for spec in env.specs_by_hash.values():
                for dep in spec.traverse():
                    dep.package.do_stage()
                    tty.msg("Staged {0} in {1}".format(dep.package.name,
                                                       dep.package.stage.path))
            return
        else:
            tty.die("`spack stage` requires a spec or an active environment")

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    if args.deprecated:
        spack.config.set('config:deprecated', True, scope='command_line')

    specs = spack.cmd.parse_specs(args.specs, concretize=False)

    # We temporarily modify the working directory when setting up a stage, so we need to
    # convert this to an absolute path here in order for it to remain valid later.
    custom_path = os.path.abspath(args.path) if args.path else None

    # prevent multiple specs from extracting in the same folder
    if len(specs) > 1 and custom_path:
        tty.die("`--path` requires a single spec, but multiple were provided")

    for spec in specs:
        spec = spack.cmd.matching_spec_from_env(spec)
        package = spack.repo.get(spec)
        if custom_path:
            package.path = custom_path
        package.do_stage()
        tty.msg("Staged {0} in {1}".format(package.name, package.stage.path))
