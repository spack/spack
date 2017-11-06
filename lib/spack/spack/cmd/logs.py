##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os.path

import llnl.util.tty as tty
import spack
import spack.cmd


description = "fetch the logs of an installed spec"
section = "basic"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        'spec',
        nargs=argparse.REMAINDER,
        help="spec identifying a unique software installation"
    )


def logs(parser, args):
    specs = spack.cmd.parse_specs(args.spec)

    if len(specs) != 1:
        msg = 'only one spec is allowed in the query [{0} given]'
        tty.die(msg.format(len(specs)))

    spec = spack.cmd.disambiguate_spec(specs[0])

    if spec.external:
        msg = '{0} is an external and has no logs.'
        tty.die(msg.format_map(spec.short_spec))

    filename = 'build.out'
    abs_filename = os.path.join(spec.prefix, '.spack', filename)

    if not os.path.exists(abs_filename):
        msg = 'log file does not exist! [{0}]'
        tty.die(msg.format(abs_filename))

    with open(abs_filename, 'r') as fstream:
        print(''.join(fstream.readlines()))
