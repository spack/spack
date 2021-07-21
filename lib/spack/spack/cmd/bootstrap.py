# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import shutil

import llnl.util.tty
import llnl.util.tty.color

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

    list = sp.add_parser(
        'list', help='list the methods available for bootstrapping'
    )
    _add_scope_option(list)


def _enable_or_disable(args):
    # Set to True if we called "enable", otherwise set to false
    value = args.subcommand == 'enable'
    spack.config.set('bootstrap:enable', value, scope=args.scope)


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
        # The default scope should stay untouched
        if scope.name == 'defaults':
            continue

        # If we are in an env scope we can't delete a file, but the best we
        # can do is nullify the corresponding configuration
        if (scope.name.startswith('env') and
                spack.config.get('bootstrap', scope=scope.name)):
            spack.config.set('bootstrap', {}, scope=scope.name)
            continue

        # If we are outside of an env scope delete the bootstrap.yaml file
        bootstrap_yaml = os.path.join(scope.path, 'bootstrap.yaml')
        backup_file = bootstrap_yaml + '.bkp'
        if os.path.exists(bootstrap_yaml):
            shutil.move(bootstrap_yaml, backup_file)


def _root(args):
    if args.path:
        spack.config.set('bootstrap:root', args.path, scope=args.scope)

    root = spack.config.get('bootstrap:root', default=None, scope=args.scope)
    if root:
        root = spack.util.path.canonicalize_path(root)
    print(root)


def _list(args):
    sources = spack.config.get(
        'bootstrap:sources', default=None, scope=args.scope
    )

    if not sources:
        llnl.util.tty.msg(
            "No method available for bootstrapping Spack's dependencies"
        )
        return

    def _print_method(source):
        color = llnl.util.tty.color

        def fmt(header, content):
            header_fmt = "@*b{{{0}:}} {1}"
            color.cprint(header_fmt.format(header, content))

        fmt("Name", source['name'])
        print()
        fmt("  Type", source['type'])
        print()

        info_lines = ['\n']
        for key, value in source.get('info', {}).items():
            info_lines.append(' ' * 4 + '@*{{{0}}}: {1}\n'.format(key, value))
        if len(info_lines) > 1:
            fmt("  Info", ''.join(info_lines))

        description_lines = ['\n']
        for line in source['description'].split('\n'):
            description_lines.append(' ' * 4 + line + '\n')

        fmt("  Description", ''.join(description_lines))

    for s in sources:
        _print_method(s)


def bootstrap(parser, args):
    callbacks = {
        'enable': _enable_or_disable,
        'disable': _enable_or_disable,
        'reset': _reset,
        'root': _root,
        'list': _list
    }
    callbacks[args.subcommand](args)
