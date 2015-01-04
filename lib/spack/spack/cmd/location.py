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
from external import argparse

import llnl.util.tty as tty
from llnl.util.filesystem import join_path

import spack
import spack.cmd

description="Print out locations of various diectories used by Spack"

def setup_parser(subparser):
    global directories
    directories = subparser.add_mutually_exclusive_group()

    directories.add_argument(
        '-m', '--module-dir', action='store_true', help="Spack python module directory.")
    directories.add_argument(
        '-r', '--spack-root', action='store_true', help="Spack installation root.")

    directories.add_argument(
        '-i', '--install-dir', action='store_true',
        help="Install prefix for spec (spec need not be installed).")
    directories.add_argument(
        '-p', '--package-dir', action='store_true',
        help="Directory enclosing a spec's package.py file.")
    directories.add_argument(
        '-P', '--packages', action='store_true',
        help="Top-level packages directory for Spack.")
    directories.add_argument(
        '-s', '--stage-dir', action='store_true', help="Stage directory for a spec.")
    directories.add_argument(
        '-b', '--build-dir', action='store_true',
        help="Checked out or expanded source directory for a spec (requires it to be staged first).")

    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER, help="spec of package to fetch directory for.")


def location(parser, args):
    if args.module_dir:
        print spack.module_path

    elif args.spack_root:
        print spack.prefix

    elif args.packages:
        print spack.db.root

    else:
        specs = spack.cmd.parse_specs(args.spec)
        if not specs:
            tty.die("You must supply a spec.")
        if len(specs) != 1:
            tty.die("Too many specs.  Supply only one.")
        spec = specs[0]

        if args.install_dir:
            # install_dir command matches against installed specs.
            matching_specs = spack.db.get_installed(spec)
            if not matching_specs:
                tty.die("Spec '%s' matches no installed packages." % spec)

            elif len(matching_specs) > 1:
                args =  ["%s matches multiple packages." % spec,
                         "Matching packages:"]
                args += ["  " + str(s) for s in matching_specs]
                args += ["Use a more specific spec."]
                tty.die(*args)

            print matching_specs[0].prefix

        elif args.package_dir:
            # This one just needs the spec name.
            print join_path(spack.db.root, spec.name)

        else:
            # These versions need concretized specs.
            spec.concretize()
            pkg = spack.db.get(spec)

            if args.stage_dir:
                print pkg.stage.path

            else:  #  args.build_dir is the default.
                if not pkg.stage.source_path:
                    tty.die("Build directory does not exist yet. Run this to create it:",
                            "spack stage " + " ".join(args.spec))
                print pkg.stage.source_path
