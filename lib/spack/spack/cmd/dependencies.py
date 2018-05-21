##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import argparse

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.store
import spack.repo
import spack.cmd

description = "show dependencies of a package"
section = "basic"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-i', '--installed', action='store_true', default=False,
        help="List installed dependencies of an installed spec, "
        "instead of possible dependencies of a package.")
    subparser.add_argument(
        '-t', '--transitive', action='store_true', default=False,
        help="show all transitive dependencies")
    subparser.add_argument(
        '-V', '--no-expand-virtuals', action='store_false', default=True,
        dest="expand_virtuals", help="do not expand virtual dependencies")
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER, help="spec or package name")


def dependencies(parser, args):
    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) != 1:
        tty.die("spack dependencies takes only one spec.")

    if args.installed:
        spec = spack.cmd.disambiguate_spec(specs[0])

        tty.msg("Dependencies of %s" % spec.format('$_$@$%@$/', color=True))
        deps = spack.store.db.installed_relatives(
            spec, 'children', args.transitive)
        if deps:
            spack.cmd.display_specs(deps, long=True)
        else:
            print("No dependencies")

    else:
        spec = specs[0]

        if not spec.virtual:
            packages = [spec.package]
        else:
            packages = [
                spack.repo.get(s.name)
                for s in spack.repo.path.providers_for(spec)]

        dependencies = set()
        for pkg in packages:
            dependencies.update(
                set(pkg.possible_dependencies(
                    args.transitive, args.expand_virtuals)))

        if spec.name in dependencies:
            dependencies.remove(spec.name)

        if dependencies:
            colify(sorted(dependencies))
        else:
            print("No dependencies")
