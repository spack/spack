##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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

import llnl.util.tty as tty

import spack.cmd
import spack.repo
import spack.util.crypto
import spack.util.web
from spack.util.naming import valid_fully_qualified_module_name
from spack.version import ver, Version

description = "checksum available versions of a package"
section = "packaging"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        'package',
        help='package to checksum versions for')
    subparser.add_argument(
        '--keep-stage', action='store_true',
        help="don't clean up staging area when command completes")
    subparser.add_argument(
        'versions', nargs=argparse.REMAINDER,
        help='versions to generate checksums for')


def checksum(parser, args):
    # Make sure the user provided a package and not a URL
    if not valid_fully_qualified_module_name(args.package):
        tty.die("`spack checksum` accepts package names, not URLs.")

    # Get the package we're going to generate checksums for
    pkg = spack.repo.get(args.package)

    if args.versions:
        # If the user asked for specific versions, use those
        url_dict = {}
        for version in args.versions:
            version = ver(version)
            if not isinstance(version, Version):
                tty.die("Cannot generate checksums for version lists or "
                        "version ranges. Use unambiguous versions.")
            url_dict[version] = pkg.url_for_version(version)
    else:
        # Otherwise, see what versions we can find online
        url_dict = pkg.fetch_remote_versions()
        if not url_dict:
            tty.die("Could not find any versions for {0}".format(pkg.name))

    version_lines = spack.util.web.get_checksums_for_versions(
        url_dict, pkg.name, keep_stage=args.keep_stage)

    print()
    print(version_lines)
