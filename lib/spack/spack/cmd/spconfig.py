##############################################################################
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Elizabeth Fischer
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import sys
import os
import argparse

import llnl.util.tty as tty

import spack
import spack.cmd
from spack.cmd.edit import edit_package
from spack.stage import DIYStage

description = "Create a configuration script and module, but don't build."

def setup_parser(subparser):
    subparser.add_argument(
        '-i', '--ignore-dependencies', action='store_true', dest='ignore_deps',
        help="Do not try to install dependencies of requested packages.")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="Display verbose build output while installing.")
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="specs to use for install.  Must contain package AND verison.")


def spconfig(self, args):
    if not args.spec:
        tty.die("spack spconfig requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack spconfig only takes one spec.")

    # Take a write lock before checking for existence.
    with spack.installed_db.write_transaction():
        spec = specs[0]

#        if not spack.repo.exists(spec.name):
#            tty.warn("No such package: %s" % spec.name)
#            create = tty.get_yes_or_no("Create this package?", default=False)
#            if not create:
#                tty.msg("Exiting without creating.")
#                sys.exit(1)
#            else:
#                tty.msg("Running 'spack edit -f %s'" % spec.name)
#                edit_package(spec.name, spack.repo.first_repo(), None, True)
#                return

        if not spec.versions.concrete:
            tty.die("spack spconfig spec must have a single, concrete version.  Did you forget a package version number?")

        spec.concretize()
        package = spack.repo.get(spec)

        # It's OK if the package is already installed.
        #if package.installed:
        #    tty.error("Already installed in %s" % package.prefix)
        #    tty.msg("Uninstall or try adding a version suffix for this SPCONFIG build.")
        #    sys.exit(1)

        # Forces the build to run out of the current directory.
        package.stage = DIYStage(os.getcwd())

        # TODO: make this an argument, not a global.
        spack.do_checksum = False

        package.do_install(
            force=True,              # Overwrite any "junk" in the install directory
            keep_prefix=False,        # Don't remove stage, even if you think you should
            ignore_deps=args.ignore_deps,
            verbose=args.verbose,
            keep_stage=True,   # don't remove source dir for SPCONFIG.
            install_phases = set(['spconfig', 'provenance', 'db']))
