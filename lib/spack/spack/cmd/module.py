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

import llnl.util.tty as tty

import spack.cmd.modules.dotkit
import spack.cmd.modules.lmod
import spack.cmd.modules.tcl

description = "manipulate module files"
section = "environment"
level = "short"


_subcommands = {}

_deprecated_commands = ('refresh', 'find', 'rm', 'loads')


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='module_command')
    spack.cmd.modules.dotkit.add_command(sp, _subcommands)
    spack.cmd.modules.lmod.add_command(sp, _subcommands)
    spack.cmd.modules.tcl.add_command(sp, _subcommands)

    for name in _deprecated_commands:
        add_deprecated_command(sp, name)


def add_deprecated_command(subparser, name):
    parser = subparser.add_parser(name)
    parser.add_argument(
        '-m', '--module-type', help=argparse.SUPPRESS,
        choices=spack.modules.module_types.keys(), action='append'
    )


def handle_deprecated_command(args, unknown_args):
    command = args.module_command
    unknown = ' '.join(unknown_args)

    module_types = args.module_type or ['tcl']

    msg = '`spack module {0} {1}` has moved. Use these commands instead:\n'
    msg = msg.format(command, ' '.join('-m ' + x for x in module_types))
    for x in module_types:
        msg += '\n\t$ spack module {0} {1} {2}'.format(x, command, unknown)
    msg += '\n'
    tty.die(msg)


def module(parser, args, unknown_args):

    # Here we permit unknown arguments to intercept deprecated calls
    if args.module_command in _deprecated_commands:
        handle_deprecated_command(args, unknown_args)

    # Fail if unknown arguments are present, once we excluded a deprecated
    # command
    if unknown_args:
        tty.die('unrecognized arguments: {0}'.format(' '.join(unknown_args)))

    _subcommands[args.module_command](parser, args)
