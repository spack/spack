##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import collections
import sys

import spack
import spack.cmd

description = "filter specs based on their properties"
section = "build"
level = "long"


def setup_parser(subparser):
    install_status = subparser.add_mutually_exclusive_group()
    install_status.add_argument(
        '--installed', dest='installed', default=None, action='store_true',
        help='select installed specs'
    )
    install_status.add_argument(
        '--not-installed', dest='installed', default=None,
        action='store_false',
        help='select specs that are not yet installed'
    )

    explicit_status = subparser.add_mutually_exclusive_group()
    explicit_status.add_argument(
        '--explicit', dest='explicit', default=None, action='store_true',
        help='select specs that were installed explicitly'
    )
    explicit_status.add_argument(
        '--implicit', dest='explicit', default=None,
        action='store_false',
        help='select specs that are not installed or were installed implicitly'
    )

    subparser.add_argument(
        '--output', default=sys.stdout, type=argparse.FileType('w'),
        help='where to dump the result'
    )

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help='specs to be filtered'
    )


def filter(parser, args):

    Request = collections.namedtuple('Request', 'abstract,concrete')
    specs = [Request(s, s.concretized())
             for s in spack.cmd.parse_specs(args.specs)]

    # Filter specs eagerly
    if args.installed is True:
        specs = [s for s in specs if s.concrete.package.installed]
    elif args.installed is False:
        specs = [s for s in specs if not s.concrete.package.installed]

    if args.explicit is True:
        specs = [s for s in specs if s.concrete._installed_explicitly()]
    elif args.explicit is False:
        specs = [s for s in specs if not s.concrete._installed_explicitly()]

    for spec in specs:
        args.output.write(str(spec.abstract) + '\n')
