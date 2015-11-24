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
import sys
import argparse

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack
import spack.cmd
import spack.packages
from spack.cmd.find import display_specs
from spack.package import PackageStillNeededError

description="Remove an installed package"

def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="Remove regardless of whether other packages depend on this one.")
    subparser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="USE CAREFULLY.  Remove ALL installed packages that match each supplied spec. " +
        "i.e., if you say uninstall libelf, ALL versions of libelf are uninstalled. " +
        "This is both useful and dangerous, like rm -r.")
    subparser.add_argument(
        'packages', nargs=argparse.REMAINDER, help="specs of packages to uninstall")


def uninstall(parser, args):
    if not args.packages:
        tty.die("uninstall requires at least one package argument.")

    with spack.installed_db.write_transaction():
        specs = spack.cmd.parse_specs(args.packages)

        # For each spec provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        pkgs = []
        for spec in specs:
            matching_specs = spack.installed_db.query(spec)
            if not args.all and len(matching_specs) > 1:
                tty.error("%s matches multiple packages:" % spec)
                print
                display_specs(matching_specs, long=True)
                print
                print "You can either:"
                print "  a) Use a more specific spec, or"
                print "  b) use spack uninstall -a to uninstall ALL matching specs."
                sys.exit(1)

            if len(matching_specs) == 0:
                if args.force: continue
                tty.die("%s does not match any installed packages." % spec)

            for s in matching_specs:
                try:
                    # should work if package is known to spack
                    pkgs.append(s.package)

                except spack.packages.UnknownPackageError, e:
                    # The package.py file has gone away -- but still want to uninstall.
                    spack.Package(s).do_uninstall(force=True)

        # Sort packages to be uninstalled by the number of installed dependents
        # This ensures we do things in the right order
        def num_installed_deps(pkg):
            return len(pkg.installed_dependents)
        pkgs.sort(key=num_installed_deps)

        # Uninstall packages in order now.
        for pkg in pkgs:
            try:
                pkg.do_uninstall(force=args.force)
            except PackageStillNeededError, e:
                tty.error("Will not uninstall %s" % e.spec.format("$_$@$%@$#", color=True))
                print
                print "The following packages depend on it:"
                display_specs(e.dependents, long=True)
                print
                print "You can use spack uninstall -f to force this action."
                sys.exit(1)
