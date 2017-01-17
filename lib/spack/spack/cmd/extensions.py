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
from llnl.util.tty.colify import colify

import spack
import spack.cmd
import spack.cmd.find
import spack.store

description = "list extensions for package"


def setup_parser(subparser):
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument(
        '-l', '--long', action='store_true', dest='long',
        help='show dependency hashes as well as versions')
    format_group.add_argument(
        '-p', '--paths', action='store_const', dest='mode', const='paths',
        help='show paths to extension install directories')
    format_group.add_argument(
        '-d', '--deps', action='store_const', dest='mode', const='deps',
        help='show full dependency DAG of extensions')

    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help='spec of package to list extensions for')


def extensions(parser, args):
    if not args.spec:
        tty.die("extensions requires a package spec.")

    #
    # Checks
    #
    spec = spack.cmd.parse_specs(args.spec)
    if len(spec) > 1:
        tty.die("Can only list extensions for one package.")

    if not spec[0].package.extendable:
        tty.die("%s is not an extendable package." % spec[0].name)

    spec = spack.cmd.disambiguate_spec(spec[0])

    if not spec.package.extendable:
        tty.die("%s does not have extensions." % spec.short_spec)

    if not args.mode:
        args.mode = 'short'

    #
    # List package names of extensions
    extensions = spack.repo.extensions_for(spec)
    if not extensions:
        tty.msg("%s has no extensions." % spec.cshort_spec)
        return
    tty.msg(spec.cshort_spec)
    tty.msg("%d extensions:" % len(extensions))
    colify(ext.name for ext in extensions)

    #
    # List specs of installed extensions.
    #
    installed = [s.spec
                 for s in spack.store.db.installed_extensions_for(spec)]

    print
    if not installed:
        tty.msg("None installed.")
        return
    tty.msg("%d installed:" % len(installed))
    spack.cmd.find.display_specs(installed, mode=args.mode)

    #
    # List specs of activated extensions.
    #
    activated = spack.store.layout.extension_map(spec)
    print
    if not activated:
        tty.msg("None activated.")
        return
    tty.msg("%d currently activated:" % len(activated))
    spack.cmd.find.display_specs(
        activated.values(), mode=args.mode, long=args.long)
