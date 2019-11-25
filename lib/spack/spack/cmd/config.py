# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import os
import six
import re

import llnl.util.tty as tty

import spack.config
import spack.environment as ev
import spack.util.spack_yaml as syaml
from spack.util.editor import editor

description = "get and set configuration options"
section = "config"
level = "long"


def setup_parser(subparser):
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    # User can only choose one
    subparser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        help="configuration scope to read/modify")

    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='config_command')

    get_parser = sp.add_parser('get', help='print configuration values')
    get_parser.add_argument('section',
                            help="configuration section to print. "
                                 "options: %(choices)s",
                            nargs='?',
                            metavar='section',
                            choices=spack.config.section_schemas)

    blame_parser = sp.add_parser(
        'blame', help='print configuration annotated with source file:line')
    blame_parser.add_argument('section',
                              help="configuration section to print. "
                              "options: %(choices)s",
                              metavar='section',
                              choices=spack.config.section_schemas)

    edit_parser = sp.add_parser('edit', help='edit configuration file')
    edit_parser.add_argument('section',
                             help="configuration section to edit. "
                                  "options: %(choices)s",
                             metavar='section',
                             nargs='?',
                             choices=spack.config.section_schemas)
    edit_parser.add_argument(
        '--print-file', action='store_true',
        help="print the file name that would be edited")

    sp.add_parser('list', help='list configuration sections')

    add_parser = sp.add_parser('add', help='add configuration parameters')
    add_parser.add_argument('value',
                            help='configuration value to set. Nested values '
                            'separated by colons (:)')

    remove_parser = sp.add_parser('remove', aliases=['rm'],
                                  help='remove configuration parameters')
    remove_parser.add_argument('value',
                            help='configuration value to remove. Nested values '
                            'separated by colons (:).')


def _get_scope_and_section(args):
    """Extract config scope and section from arguments."""
    scope = args.scope
    section = getattr(args, 'section', '')

    # w/no args and an active environment, point to env manifest
    if not section:
        env = ev.get_env(args, 'config edit')
        if env:
            scope = env.env_file_config_scope_name()

    # set scope defaults
    elif not scope:
        # set section from value if the command takes a value
        if hasattr(args, 'value'):
            value = args.value
            section = value[:value.find(':')] if ':' in value else value

        if section == 'compilers':
            scope = spack.config.default_modify_scope()
        else:
            scope = 'user'

    return scope, section


def config_get(args):
    """Dump merged YAML configuration for a specific section.

    With no arguments and an active environment, print the contents of
    the environment's manifest file (spack.yaml).
    """
    scope, section = _get_scope_and_section(args)

    if scope and scope.startswith('env:'):
        config_file = spack.config.config.get_config_filename(scope, section)
        if os.path.exists(config_file):
            with open(config_file) as f:
                print(f.read())
        else:
            tty.die('environment has no %s file' % ev.manifest_name)

    elif section is not None:
        spack.config.config.print_section(section)

    else:
        tty.die('`spack config get` requires a section argument '
                'or an active environment.')


def config_blame(args):
    """Print out line-by-line blame of merged YAML."""
    spack.config.config.print_section(args.section, blame=True)


def config_edit(args):
    """Edit the configuration file for a specific scope and config section.

    With no arguments and an active environment, edit the spack.yaml for
    the active environment.
    """
    scope, section = _get_scope_and_section(args)
    if not scope and not section:
        tty.die('`spack config edit` requires a section argument '
                'or an active environment.')

    config_file = spack.config.config.get_config_filename(scope, section)
    if args.print_file:
        print(config_file)
    else:
        editor(config_file)


def config_list(args):
    """List the possible configuration sections.

    Used primarily for shell tab completion scripts.
    """
    print(' '.join(list(spack.config.section_schemas)))


def merge_value(existing, value):
    # dictionaries have special handling
    if isinstance(value, dict) or isinstance(existing, dict):
        if isinstance(value, dict) and isinstance(existing, dict):
            if existing:
                new = existing
                new.update(value)
            new = value
        elif existing is None:
            new = value
        else:
            raise spack.config.ConfigError(
                'Cannot overwrite config dict with non-dict entry')

    elif isinstance(existing, list):
        if isinstance(value, list):
            new = existing + value
        else:
            new = existing + [value]
    else:
        new = value

    return new


def config_add(args):
    """Add the given configuration to the specified config scope

    This is a stateful operation that edits the config files under the hood"""
    scope, _ = _get_scope_and_section(args)

    components = args.value.split(':')
    path = None
    for idx, name in enumerate(components[:-1]):
        test_path = ':'.join(components[:idx + 1])
        test_existing = spack.config.get(test_path, scope=scope)
        if test_existing is None:
            path = test_path
            # We've nested further than existing config, so we need empty
            # get type to ensure we treat lists properly when empty
            existing = [] if isinstance(spack.config.get(path, scope=None), list) else None
            # construct value from this point down
            value = syaml.load(components[-1])
            for component in reversed(components[idx + 1:-1]):
                value = {component: value}
            break

    if path is None:
        path, _, value = args.value.rpartition(':')
        value = syaml.load(value)
        existing = spack.config.get(path, scope=scope)

    new = merge_value(existing, value)

    if re.match(r'env.*', scope):
        e = ev.get_env(args, 'config add')
        e.set_config(path, new)
    else:
        spack.config.set(path, new, scope=scope)


def config_remove(args):
    """Remove the given configuration from the specified config scope

    This is a stateful operation that edits the config files under the hood"""
    scope, _ = _get_scope_and_section(args)

    path, _, value = args.value.rpartition(':')
    existing = spack.config.get(path, scope=scope)

    if not isinstance(existing, (list, dict)):
        path, _, value = path.rpartition(':')
        existing = spack.config.get(path, scope=scope)

    if isinstance(existing, list):
        new = [x for x in existing if x != value] if value else []
    elif isinstance(existing, dict):
        new = dict((k, v) for k, v in existing.items()
                   if k != value) if value else {}
    else:
        # This should be impossible to reach
        raise spack.config.ConfigError('Config has nested non-dict values')

    if re.match(r'env.*', scope):
        e = ev.get_env(args, 'config remove')
        e.set_config(path, new)
    else:
        spack.config.set(path, new, scope=scope)

def config(parser, args):
    action = {'get': config_get,
              'blame': config_blame,
              'edit': config_edit,
              'list': config_list,
              'add': config_add,
              'rm': config_remove,
              'remove': config_remove}
    action[args.config_command](args)
