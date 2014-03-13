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
import os
import shutil
import argparse

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, join_path

import spack.packages as packages
import spack.cmd

from spack.stage import Stage


description = "Create a directory full of package tarballs that can be used as a spack mirror."

def setup_parser(subparser):
    subparser.add_argument(
        'directory', help="Directory in which to create mirror.")
    subparser.add_argument(
        'packages', nargs=argparse.REMAINDER, help="names of packages to put in mirror")


def mirror(parser, args):
    if not args.packages:
        args.packages = [p for p in packages.all_package_names()]

    if os.path.isfile(args.directory):
        tty.error("%s already exists and is a file." % args.directory)

    if not os.path.isdir(args.directory):
        mkdirp(args.directory)

    # save working directory
    working_dir = os.getcwd()

    # Iterate through packages and download all the safe tarballs for each of them
    for pkg_name in args.packages:
        pkg = packages.get(pkg_name)

        # Skip any package that has no checksummed versions.
        if not pkg.versions:
            tty.msg("No safe (checksummed) versions for package %s.  Skipping."
                    % pkg_name)
            continue

        # create a subdir for the current package.
        pkg_path = join_path(args.directory, pkg_name)
        mkdirp(pkg_path)

        # Download all the tarballs using Stages, then move them into place
        for version in pkg.versions:
            url = pkg.url_for_version(version)
            stage = Stage(url)
            try:
                stage.fetch()
                basename = os.path.basename(stage.archive_file)
                final_dst = join_path(pkg_path, basename)

                os.chdir(working_dir)
                shutil.move(stage.archive_file, final_dst)
                tty.msg("Added %s to mirror" % final_dst)

            finally:
                stage.destroy()

    # Success!
    tty.msg("Created Spack mirror in %s" % args.directory)
