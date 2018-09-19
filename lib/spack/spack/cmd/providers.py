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
import six
import sys

import llnl.util.tty.colify as colify

import spack.cmd
import spack.repo

description = "list packages that provide a particular virtual package"
section = "basic"
level = "long"


def setup_parser(subparser):
    subparser.epilog = 'If called without argument returns ' \
                       'the list of all valid virtual packages'
    subparser.add_argument(
        'virtual_package',
        nargs='*',
        help='find packages that provide this virtual package'
    )


def providers(parser, args):
    valid_virtuals = sorted(spack.repo.path.provider_index.providers.keys())

    buffer = six.StringIO()
    isatty = sys.stdout.isatty()
    if isatty:
        buffer.write('Virtual packages:\n')
    colify.colify(valid_virtuals, output=buffer, tty=isatty, indent=4)
    valid_virtuals_str = buffer.getvalue()

    # If called without arguments, list all the virtual packages
    if not args.virtual_package:
        print(valid_virtuals_str)
        return

    # Otherwise, parse the specs from command line
    specs = spack.cmd.parse_specs(args.virtual_package)

    # Check prerequisites
    non_virtual = [
        str(s) for s in specs if not s.virtual or s.name not in valid_virtuals
    ]
    if non_virtual:
        msg = 'non-virtual specs cannot be part of the query '
        msg += '[{0}]\n'.format(', '.join(non_virtual))
        msg += valid_virtuals_str
        raise ValueError(msg)

    # Display providers
    for spec in specs:
        if sys.stdout.isatty():
            print("{0}:".format(spec))
        spack.cmd.display_specs(sorted(spack.repo.path.providers_for(spec)))
        print('')
