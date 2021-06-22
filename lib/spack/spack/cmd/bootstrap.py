# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

import llnl.util.tty
import spack.cmd.common.arguments
import spack.config
import spack.main
import spack.util.path

description = "manage bootstrap configuration"
section = "system"
level = "long"


def _add_scope_option(parser):
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar
    parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        help="configuration scope to read/modify"
    )


def setup_parser(subparser):
    sp = subparser.add_subparsers(dest='subcommand')

    enable = sp.add_parser('enable', help='enable bootstrapping')
    _add_scope_option(enable)

    disable = sp.add_parser('disable', help='disable bootstrapping')
    _add_scope_option(disable)

    reset = sp.add_parser(
        'reset', help='reset bootstrapping configuration to Spack defaults'
    )
    spack.cmd.common.arguments.add_common_arguments(
        reset, ['yes_to_all']
    )

    root = sp.add_parser(
        'root', help='get/set the root bootstrap directory'
    )
    _add_scope_option(root)
    root.add_argument(
        'path', nargs='?', default=None,
        help='set the bootstrap directory to this value'
    )


def _enable_or_disable(args):
    _config = spack.main.SpackCommand('config')

    # Set to True if we called "enable", otherwise set to false
    value = str(args.subcommand == 'enable').lower()
    scope, config_args = args.scope, []
    if scope:
        config_args.append('--scope={0}'.format(scope))
    config_args.extend([
        'add', 'bootstrap:enable:{0}'.format(value)
    ])
    _config(*config_args)


def _reset(args):
    if not args.yes_to_all:
        msg = [
            "Bootstrapping configuration is being reset to Spack's defaults. "
            "Current configuration will be lost.\n",
            "Do you want to continue?"
        ]
        ok_to_continue = llnl.util.tty.get_yes_or_no(
            ''.join(msg), default=True
        )
        if not ok_to_continue:
            raise RuntimeError('Aborting')

    for scope in spack.config.config.file_scopes:
        if 'defaults' in scope.path:
            continue
        bootstrap_yaml = os.path.join(scope.path, 'bootstrap.yaml')
        if os.path.exists(bootstrap_yaml):
            os.remove(bootstrap_yaml)


def _root(args):
    if args.path:
        spack.config.set('bootstrap:root', args.path, scope=args.scope)

    root = spack.config.get('bootstrap:root', default=None, scope=args.scope)
    if root:
        root = spack.util.path.canonicalize_path(root)
    print(root)


def bootstrap(parser, args):
    callbacks = {
        'enable': _enable_or_disable,
        'disable': _enable_or_disable,
        'reset': _reset,
        'root': _root
    }
    callbacks[args.subcommand](args)
