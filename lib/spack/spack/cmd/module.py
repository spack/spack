# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import llnl.util.tty as tty

import spack.cmd.modules.lmod
import spack.cmd.modules.tcl

description = "manipulate module files"
section = "user environment"
level = "short"


_subcommands = {}

_deprecated_commands = ('refresh', 'find', 'rm', 'loads')


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='module_command')
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
