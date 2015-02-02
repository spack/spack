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
from external import argparse

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack
import spack.cmd
import spack.cmd.find

description = "List extensions for package."

def setup_parser(subparser):
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument(
        '-l', '--long', action='store_const', dest='mode', const='long',
        help='Show dependency hashes as well as versions.')
    format_group.add_argument(
        '-p', '--paths', action='store_const', dest='mode', const='paths',
        help='Show paths to extension install directories')
    format_group.add_argument(
        '-d', '--deps', action='store_const', dest='mode', const='deps',
        help='Show full dependency DAG of extensions')

    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER, help='Spec of package to list extensions for')


def extensions(parser, args):
    if not args.spec:
        tty.die("extensions requires a package spec.")

    spec = spack.cmd.parse_specs(args.spec)
    if len(spec) > 1:
        tty.die("Can only list extensions for one package.")
    spec = spack.cmd.disambiguate_spec(spec[0])

    if not spec.package.extendable:
        tty.die("%s does not have extensions." % spec.short_spec)

    if not args.mode:
        args.mode = 'short'

    exts = spack.install_layout.get_extensions(spec)
    if not exts:
        tty.msg("%s has no activated extensions." % spec.cshort_spec)
    else:
        tty.msg("Extensions for package %s:" % spec.cshort_spec)
        colify(pkg.name for pkg in spack.db.extensions_for(spec))
        print
        tty.msg("%d currently activated:" % len(exts))
        spack.cmd.find.display_specs(exts, mode=args.mode)
