##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
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
import argparse
import os

import llnl.util.tty as tty

import spack
import spack.cmd
from spack.util.executable import which
from spack.binary_distribution import tarball_name

description = "Create tarballs for given packages"

def setup_parser(subparser):
    subparser.add_argument('-r','--recurse',action='store_true',
                           help="also make tarballs for dependencies.")
    subparser.add_argument('-f','--force',action='store_true',
                           help="overwrite tarball if it exists.")
    subparser.add_argument('-d','--directory',default=".",
                           help="directory in which to save the tarballs.")

    subparser.add_argument(
        'packages', nargs=argparse.REMAINDER, help="specs of packages to package")

def do_tar(spec, outdir, force=False, ):
    tarfile = os.path.join(outdir, tarball_name(spec))
    if os.path.exists(tarfile):
        if force:
            os.remove(tarfile)
        else:
            tty.die("file exists, use -f to force overwrite: %s"%tarfile)

    tar = which('tar', required=True)
    dirname = os.path.dirname(spec.prefix)
    basename = os.path.basename(spec.prefix)
    tar("--directory=%s" %dirname, "-cf", tarfile, basename)
    tty.msg(tarfile)

def create_tarball(parser, args):
    if not args.packages:
        tty.die("tarball creation requires at least one package argument")

    pkgs = set(args.packages)
    if args.recurse:
        for name in args.packages:
            for spec in spack.cmd.parse_specs(name, concretize=True):
                pkgs.update(spec.flat_dependencies())

    for pkg in pkgs:
        for spec in spack.cmd.parse_specs(pkg, concretize=True):
            do_tar(spec, args.directory, args.force)

