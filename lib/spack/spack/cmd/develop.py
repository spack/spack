# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import os

import llnl.util.tty as tty
import llnl.util.filesystem as fs

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev

from spack.error import SpackError

description = 'add a spec to an environments dev-build information'
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-p', '--path', help='Source location of package')

    clone_group = subparser.add_mutually_exclusive_group()
    clone_group.add_argument(
        '--no-clone', action='store_false', dest='clone', default=None,
        help='Do not clone. The package already exists at the source path')
    clone_group.add_argument(
        '--clone', action='store_true', dest='clone', default=None,
        help='Clone the package even if the path already exists')
    arguments.add_common_arguments(subparser, ['spec'])


def develop(parser, args):
    env = ev.get_env(args, 'develop', required=True)

    if not args.spec:
        if args.clone is False:
            raise SpackError("No spec provided to spack develop command")

        # download all dev specs
        for name, entry in env.dev_specs.items():
            path = entry.get('path', name)
            abspath = path if os.path.isabs(path) else os.path.join(
                env.path, path)
            fs.mkdirp(abspath)

            if os.path.exists(abspath):
                msg = "Skipping developer download of %s" % entry['spec']
                msg += " because its path already exists."
                tty.msg(msg)
                continue

            stage = spack.spec.Spec(entry['spec']).package.stage
            stage.create()
            stage.fetch()
            stage.expand_archive()

            # glob all files and directories in the stage source_path
            hidden_entries = glob.glob(os.path.join(stage.source_path, '.*'))
            entries = glob.glob(os.path.join(stage.source_path, '*'))

            # Move all files from stage to destination directory
            # Include hidden files for VCS repo history
            for entry in hidden_entries + entries:
                if os.path.isdir(entry):
                    dest = os.path.join(abspath, os.path.basename(entry))
                    shutil.copytree(entry, dest)
                else:
                    shutil.copy2(entry, abspath)

            # copy archive file if we downloaded from url -- replaces for vcs
            if stage.archive_file and os.path.exists(stage.archive_file):
                shutil.copy2(stage.archive_file, abspath)

            # remove leftover stage
            stage.destroy()

        if not env.dev_specs:
            tty.warn("No develop specs to download")

        return

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        raise SpackError("spack develop requires at most one named spec")

    spec = specs[0]
    if not spec.versions.concrete:
        raise SpackError("Packages to develop must have a concrete version")

    # default path is relative path to spec.name
    path = args.path or spec.name

    # get absolute path to check
    abspath = path
    if not os.path.isabs(abspath):
        abspath = os.path.join(env.path, path)

    # clone default: only if the path doesn't exist
    clone = args.clone
    if clone is None:
        clone = not os.path.exists(abspath)

    if not clone and not os.path.exists(abspath):
        raise SpackError("Provided path %s does not exist" % abspath)

    with env.write_transaction():
        changed = env.develop(spec, path, clone)
        if changed:
            env.write()
