##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import sys
import os
import argparse

import llnl.util.tty as tty

import spack
import spack.cmd
from spack.cmd.edit import edit_package
from spack.stage import DIYStage

description = "Do-It-Yourself: build from an existing source directory."


def setup_parser(subparser):
    subparser.add_argument(
        '-i', '--ignore-dependencies', action='store_true', dest='ignore_deps',
        help="Do not try to install dependencies of requested packages.")
    subparser.add_argument(
        '--keep-prefix', action='store_true',
        help="Don't remove the install prefix if installation fails.")
    subparser.add_argument(
        '--skip-patch', action='store_true',
        help="Skip patching for the DIY build.")
    subparser.add_argument(
        '-q', '--quiet', action='store_true', dest='quiet',
        help="Do not display verbose build output while installing.")
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="specs to use for install.  Must contain package AND version.")
    subparser.add_argument(
        '--dirty', action='store_true', dest='dirty',
        help="Install a package *without* cleaning the environment.")


def diy(self, args):
    if not args.spec:
        tty.die("spack diy requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack diy only takes one spec.")

    spec = specs[0]
    if not spack.repo.exists(spec.name):
        tty.warn("No such package: %s" % spec.name)
        create = tty.get_yes_or_no("Create this package?", default=False)
        if not create:
            tty.msg("Exiting without creating.")
            sys.exit(1)
        else:
            tty.msg("Running 'spack edit -f %s'" % spec.name)
            edit_package(spec.name, spack.repo.first_repo(), None, True)
            return

    if not spec.versions.concrete:
        tty.die(
            "spack diy spec must have a single, concrete version. "
            "Did you forget a package version number?")

    spec.concretize()
    package = spack.repo.get(spec)

    if package.installed:
        tty.error("Already installed in %s" % package.prefix)
        tty.msg("Uninstall or try adding a version suffix for this DIY build.")
        sys.exit(1)

    # Forces the build to run out of the current directory.
    package.stage = DIYStage(os.getcwd())

    # TODO: make this an argument, not a global.
    spack.do_checksum = False

    package.do_install(
        keep_prefix=args.keep_prefix,
        install_deps=not args.ignore_deps,
        verbose=not args.quiet,
        keep_stage=True,   # don't remove source dir for DIY.
        dirty=args.dirty)
