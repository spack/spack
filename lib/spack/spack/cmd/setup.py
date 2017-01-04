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
from __future__ import print_function

import argparse
import copy
import os
import string
import sys

import llnl.util.tty as tty
import spack
import spack.store
import spack.package
import spack.cmd
import spack.cmd.install as install
import spack.cmd.common.arguments as arguments
from llnl.util.filesystem import set_executable
from spack import which
from spack.stage import DIYStage

description = "Create a configuration script and module, but don't build."

# Same cmd line arguments as `spack install`
def setup_parser(subparser):
    install.setup_common_parser(subparser)
    subparser.add_argument(
        '-d', '--default-version', action='store_true', dest='default',
        help="Allow default version if user did not specify a single concrete version")


def top_install(spec, install_package=True, install_dependencies=True, **kwargs):
    """Top-level install method for spack setup."""
    if install_dependencies:
        # Install dependencies as-if they were installed
        # for root (explicit=False in the DB)
        for s in spec.dependencies():
            package = spack.repo.get(s)
            package.do_install(install_dependencies=True, explicit=False, **kwargs)

    if install_package:
        package = spack.repo.get(spec)
        package.stage = DIYStage(os.getcwd())    # Force build in cwd

        # --- Generate spconfig.py
        tty.msg(
            'Generating spconfig.py [{0}]'.format(package.spec.cshort_spec)
        )
        package.write_spconfig()

        # --- Install this package to register it in the DB
        # --- and permit module file regeneration
        del kwargs['fake']
        package.do_install(
            install_dependencies=False, explicit=True, fake=True,
            **kwargs)


def setup(self, args):
    # Further parsing of arguments
    kwargs = install.validate_args(args)
    spec = spack.cmd.parse_specs(args.package, concretize=False, allow_multi=False)

    # Log if command line args call for it
    with install.setup_logging(spec, args):
        # Take a write lock before checking for existence.
        with spack.store.db.write_transaction():

            if not spack.repo.exists(spec.name):
                tty.die("No such package: %s" % spec.name)

            if not (args.default or spec.versions.concrete):
                tty.die(
                    "spack setup spec must have a single, concrete version. "
                    "Did you forget a package version number?")

            spec.concretize()
            install.show_spec(spec, args)

            package = spack.repo.get(spec)
            if not isinstance(package, spack.CMakePackage):
                tty.die(
                    'Support for packages derived from {0} '
                    'is not yet implemented'.format(
                        package.build_system_class
                    )
                )

            top_install(spec, **kwargs)
