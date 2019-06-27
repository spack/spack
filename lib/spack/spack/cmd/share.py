# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd


description = "enable shared mode for multi-user support"
section = "share"
level = "long"


subcommands = [
    'activate',
    'deactivate',
    'status'
]

subcommand_functions = {}


def shr_activate_setup_parser(subparser):
    pass


def shr_deactivate_setup_parser(subparser):
    pass


def shr_status_setup_parser(subparser):
    pass


def shr_activate(args):
    if spack.config.get('config:shared'):
        tty.die("Shared mode already activated")
    spack.config.set('config:shared', True, scope='site')


def shr_deactivate(args):
    if not spack.config.get('config:shared'):
        tty.die("Shared mode already deactivated")
    spack.config.set('config:shared', False, scope='site')


def shr_status(args):
    if spack.config.get('config:shared'):
        tty.msg("Shared mode enabled")
    else:
        tty.msg("Shared mode disabled")


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='share_command')

    for name in subcommands:
        if isinstance(name, (list, tuple)):
            name, aliases = name[0], name[1:]
        else:
            aliases = []

        # add commands to subcommands dict
        function_name = 'shr_%s' % name
        function = globals()[function_name]
        for alias in [name] + aliases:
            subcommand_functions[alias] = function

        # make a subparser and run the command's setup function on it
        setup_parser_cmd_name = 'shr_%s_setup_parser' % name
        setup_parser_cmd = globals()[setup_parser_cmd_name]

        subsubparser = sp.add_parser(
            name, aliases=aliases, help=setup_parser_cmd.__doc__)
        setup_parser_cmd(subsubparser)


def share(parser, args):
    action = subcommand_functions[args.share_command]
    action(args)
