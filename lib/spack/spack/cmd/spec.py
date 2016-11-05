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

import spack
import spack.cmd
import spack.cmd.common.arguments as arguments

description = "print out abstract and concrete versions of a spec."


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['long', 'very_long'])
    subparser.add_argument(
        '-y', '--yaml', action='store_true', default=False,
        help='Print concrete spec as YAML.')
    subparser.add_argument(
        '-c', '--cover', action='store',
        default='nodes', choices=['nodes', 'edges', 'paths'],
        help='How extensively to traverse the DAG. (default: nodes).')
    subparser.add_argument(
        '-I', '--install-status', action='store_true', default=False,
        help='Show install status of packages.  Packages can be: '
             'installed [+], missing and needed by an installed package [-], '
             'or not installed (no annotation).')
    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="specs of packages")


def spec(parser, args):
    kwargs = {'color': True,
              'cover': args.cover,
              'install_status': args.install_status,
              'hashes': args.long or args.very_long,
              'hashlen': None if args.very_long else 7}

    for spec in spack.cmd.parse_specs(args.specs):
        # With -y, just print YAML to output.
        if args.yaml:
            spec.concretize()
            print spec.to_yaml()
            continue

        # Print some diagnostic info by default.
        print "Input spec"
        print "--------------------------------"
        print spec.tree(**kwargs)

        print "Normalized"
        print "--------------------------------"
        spec.normalize()
        print spec.tree(**kwargs)

        print "Concretized"
        print "--------------------------------"
        spec.concretize()
        print spec.tree(**kwargs)
