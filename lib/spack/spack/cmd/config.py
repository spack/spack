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
import argparse

import llnl.util.tty as tty

import spack.config

description = "Get and set configuration options."

def setup_parser(subparser):
    scope_group = subparser.add_mutually_exclusive_group()

    # File scope
    scope_group.add_argument(
        '--user', action='store_const', const='user', dest='scope',
        help="Use config file in user home directory (default).")
    scope_group.add_argument(
        '--site', action='store_const', const='site', dest='scope',
        help="Use config file in spack prefix.")

    # Get (vs. default set)
    subparser.add_argument(
        '--get', action='store_true', dest='get',
        help="Get the value associated with a key.")

    # positional arguments (value is only used on set)
    subparser.add_argument(
        'key', help="Get the value associated with KEY")
    subparser.add_argument(
        'value', nargs='?', default=None,
        help="Value to associate with key")


def config(parser, args):
    key, value = args.key, args.value

    # If we're writing need to do a few checks.
    if not args.get:
        # Default scope for writing is user scope.
        if not args.scope:
            args.scope = 'user'

        if args.value is None:
            tty.die("No value for '%s'.  " % args.key
                    + "Spack config requires a key and a value.")

    config = spack.config.get_config(args.scope)

    if args.get:
        print config.get_value(key)
    else:
        config.set_value(key, value)
        config.write()
