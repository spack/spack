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

from llnl.util.tty.colify import colify

import spack
import spack.cmd

description = "list packages that provide a particular virtual package"


def setup_parser(subparser):
    subparser.add_argument(
        'vpkg_spec', metavar='VPACKAGE_SPEC', nargs=argparse.REMAINDER,
        help='find packages that provide this virtual package')


def providers(parser, args):
    for spec in spack.cmd.parse_specs(args.vpkg_spec):
        colify(sorted(spack.repo.providers_for(spec)), indent=4)
