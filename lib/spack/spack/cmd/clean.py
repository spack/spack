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
import argparse

import llnl.util.tty as tty

import spack.cmd
import spack.packages as packages
import spack.stage as stage

description = "Remove staged files for packages"

def setup_parser(subparser):
    subparser.add_argument('-c', "--clean", action="store_true", dest='clean',
                           help="run make clean in the build directory (default)")
    subparser.add_argument('-w', "--work", action="store_true", dest='work',
                           help="delete the build directory and re-expand it from its archive.")
    subparser.add_argument('-d', "--dist", action="store_true", dest='dist',
                           help="delete the downloaded archive.")
    subparser.add_argument('packages', nargs=argparse.REMAINDER,
                           help="specs of packages to clean")


def clean(parser, args):
    if not args.packages:
        tty.die("spack clean requires at least one package argument")

    specs = spack.cmd.parse_specs(args.packages, concretize=True)
    for spec in specs:
        package = packages.get(spec)
        if args.dist:
            package.do_clean_dist()
        elif args.work:
            package.do_clean_work()
        else:
            package.do_clean()
