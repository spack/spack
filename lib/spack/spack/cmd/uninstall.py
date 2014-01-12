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

import spack.cmd
import spack.tty as tty
import spack.packages as packages

description="Remove an installed package"

def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="Remove regardless of whether other packages depend on this one.")
    subparser.add_argument(
        'packages', nargs=argparse.REMAINDER, help="specs of packages to uninstall")


def uninstall(parser, args):
    if not args.packages:
        tty.die("uninstall requires at least one package argument.")

    specs = spack.cmd.parse_specs(args.packages)

    # For each spec provided, make sure it refers to only one package.
    # Fail and ask user to be unambiguous if it doesn't
    pkgs = []
    for spec in specs:
        matching_specs = packages.get_installed(spec)
        if len(matching_specs) > 1:
            tty.die("%s matches multiple packages.  Which one did you mean?"
                    % spec, *matching_specs)

        elif len(matching_specs) == 0:
            tty.die("%s does not match any installed packages." % spec)

        installed_spec = matching_specs[0]
        pkgs.append(packages.get(installed_spec))

    # Sort packages to be uninstalled by the number of installed dependents
    # This ensures we do things in the right order
    def num_installed_deps(pkg):
        return len(pkg.installed_dependents)
    pkgs.sort(key=num_installed_deps)

    # Uninstall packages in order now.
    for pkg in pkgs:
        pkg.do_uninstall()
