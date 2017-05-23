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

import llnl.util.tty as tty

import spack
import spack.store
import spack.cmd
import spack.binary_distribution
import spack.relocate


description = "Download and extract binary cache files for given packages"
section = "caching"
level = "long"


def setup_parser(subparser):
    subparser.add_argument('-f', '--force', action='store_true',
                           help="overwrite install directory if it exists.")
    subparser.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to package")


def install_tarball(parser, args):
    if not args.packages:
        tty.die("binary cache file extraction requires at least one" +
                " package argument")

    pkgs = set(args.packages)
    specs = set()
    for pkg in pkgs:
        for spec in spack.cmd.parse_specs(pkg, concretize=True):
            specs.add(spec)
            tty.msg('recursing dependencies')
            for d, node in spec.traverse(order='pre', depth=True):
                tty.msg('adding dependency %s' % node)
                specs.add(node)

    for spec in specs:
        package = spack.repo.get(spec)
        tarball_available = spack.binary_distribution.download_tarball(
            package)
        if tarball_available:
            spack.binary_distribution.prepare()
            if package.installed and not force:
                tty.warn("Package for spec %s already installed." % spec)
            else:
                spack.binary_distribution.extract_tarball(package)
                spack.binary_distribution.relocate_package(package)
                spack.store.db.reindex(spack.store.layout)
        else:
            tty.die("Download of binary cache file for spec %s failed." % spec)
