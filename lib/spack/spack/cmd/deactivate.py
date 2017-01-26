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
import argparse
import llnl.util.tty as tty

import spack
import spack.cmd
import spack.store
from spack.graph import topological_sort

description = "deactivate a package extension"


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="run deactivation even if spec is NOT currently activated")
    subparser.add_argument(
        '-a', '--all', action='store_true',
        help="deactivate all extensions of an extendable package, or "
        "deactivate an extension AND its dependencies")
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="spec of package extension to deactivate")


def deactivate(parser, args):
    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) != 1:
        tty.die("deactivate requires one spec.  %d given." % len(specs))

    spec = spack.cmd.disambiguate_spec(specs[0])
    pkg = spec.package

    if args.all:
        if pkg.extendable:
            tty.msg("Deactivating all extensions of %s" % pkg.spec.short_spec)
            ext_pkgs = spack.store.db.installed_extensions_for(spec)

            for ext_pkg in ext_pkgs:
                ext_pkg.spec.normalize()
                if ext_pkg.activated:
                    ext_pkg.do_deactivate(force=True)

        elif pkg.is_extension:
            if not args.force and not spec.package.activated:
                tty.die("%s is not activated." % pkg.spec.short_spec)

            tty.msg("Deactivating %s and all dependencies." %
                    pkg.spec.short_spec)

            topo_order = topological_sort(spec)
            index = spec.index()

            for name in topo_order:
                espec = index[name]
                epkg = espec.package
                if epkg.extends(pkg.extendee_spec):
                    if epkg.activated or args.force:

                        epkg.do_deactivate(force=args.force)

        else:
            tty.die(
                "spack deactivate --all requires an extendable package "
                "or an extension.")

    else:
        if not pkg.is_extension:
            tty.die("spack deactivate requires an extension.",
                    "Did you mean 'spack deactivate --all'?")

        if not args.force and not spec.package.activated:
            tty.die("Package %s is not activated." % specs[0].short_spec)

        spec.package.do_deactivate(force=args.force)
