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
import spack.store
import spack.cmd

description = "show installed packages that depend on another"


def setup_parser(subparser):
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="specs to list dependencies of")


def dependents(parser, args):
    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) != 1:
        tty.die("spack dependents takes only one spec.")
    spec = spack.cmd.disambiguate_spec(specs[0])

    tty.msg("Dependents of %s" % spec.format('$_$@$%@$/', color=True))
    deps = spack.store.db.installed_dependents(spec)
    if deps:
        spack.cmd.display_specs(deps)
    else:
        print "No dependents"
