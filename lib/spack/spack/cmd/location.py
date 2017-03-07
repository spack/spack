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
import llnl.util.tty as tty

import spack
import spack.cmd

description = "print out locations of various directories used by Spack"


def setup_parser(subparser):
    global directories
    directories = subparser.add_mutually_exclusive_group()

    directories.add_argument(
        '-m', '--module-dir', action='store_true',
        help="spack python module directory")
    directories.add_argument(
        '-r', '--spack-root', action='store_true',
        help="spack installation root")

    directories.add_argument(
        '-i', '--install-dir', action='store_true',
        help="install prefix for spec (spec need not be installed)")
    directories.add_argument(
        '-p', '--package-dir', action='store_true',
        help="directory enclosing a spec's package.py file")
    directories.add_argument(
        '-P', '--packages', action='store_true',
        help="top-level packages directory for Spack")
    directories.add_argument(
        '-s', '--stage-dir', action='store_true',
        help="stage directory for a spec")
    directories.add_argument(
        '-S', '--stages', action='store_true',
        help="top level stage directory")
    directories.add_argument(
        '-b', '--build-dir', action='store_true',
        help="checked out or expanded source directory for a spec "
             "(requires it to be staged first)")

    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="spec of package to fetch directory for")


def location(parser, args):
    if args.module_dir:
        print(spack.module_path)

    elif args.spack_root:
        print(spack.prefix)

    elif args.packages:
        print(spack.repo.first_repo().root)

    elif args.stages:
        print(spack.stage_path)

    else:
        specs = spack.cmd.parse_specs(args.spec)
        if not specs:
            tty.die("You must supply a spec.")
        if len(specs) != 1:
            tty.die("Too many specs.  Supply only one.")

        if args.install_dir:
            # install_dir command matches against installed specs.
            spec = spack.cmd.disambiguate_spec(specs[0])
            print(spec.prefix)

        else:
            spec = specs[0]

            if args.package_dir:
                # This one just needs the spec name.
                print(spack.repo.dirname_for_package_name(spec.name))

            else:
                # These versions need concretized specs.
                spec.concretize()
                pkg = spack.repo.get(spec)

                if args.stage_dir:
                    print(pkg.stage.path)

                else:  # args.build_dir is the default.
                    if not pkg.stage.source_path:
                        tty.die("Build directory does not exist yet. "
                                "Run this to create it:",
                                "spack stage " + " ".join(args.spec))
                    print(pkg.stage.source_path)
