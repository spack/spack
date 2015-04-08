##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
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
from external import argparse
import spack
import spack.cmd

description = "Build a package for an existing source directory."

def setup_parser(subparser):
    subparser.add_argument(
        '-i', '--ignore-dependencies', action='store_true', dest='ignore_deps',
        help="Do not try to install dependencies of requested packages.")
    subparser.add_argument(
        '--keep-prefix', action='store_true', dest='keep_prefix',
        help="Don't remove the install prefix if installation fails.")
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="specs to use for install.  Must contain package AND verison.")


def diy(self, args):
    if not args.spec:
        tty.die("spack diy requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.specs, concretize=True)
    if len(specs) > 1:
        tty.die("spack diy only takes one spec.")

    spec = specs[0]
    package = spack.db.get(spec)

    package.do_install(
        keep_prefix=args.keep_prefix,
        ignore_deps=args.ignore_deps,
        keep_stage=True)   # don't remove stage dir for diy.
