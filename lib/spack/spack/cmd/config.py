# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import os
import re

import llnl.util.tty as tty

import spack.config
import spack.schema.env
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
    add_parser.add_argument(
        'path', nargs='?',
        help="colon-separated path to config that should be added,"
        " e.g. 'config:default:true'")
    add_parser.add_argument(
        '-f', '--file',
        help="file from which to set all config values"
    )

    remove_parser = sp.add_parser('remove', aliases=['rm'],
                                  help='remove configuration parameters')
    remove_parser.add_argument(
        'path',
        help="colon-separated path to config that should be removed,"
        " e.g. 'config:default:true'")

    # Make the add parser available later
    setup_parser.add_parser = add_parser


def _get_scope_and_section(args):
    """Extract config scope and section from arguments."""
    scope = args.scope
    section = getattr(args, 'section', None)
    path = getattr(args, 'path', None)

    # w/no args and an active environment, point to env manifest
    if not section:
        env = ev.get_env(args, 'config edit')
        if env:
            scope = env.env_file_config_scope_name()

    # set scope defaults
    elif not scope:
        scope = spack.config.default_modify_scope(section)

    # special handling for commands that take value instead of section
    if path:
        section = path[:path.find(':')] if ':' in path else path
        if not scope:
            scope = spack.config.default_modify_scope(section)

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


def set_config(args, section, new, scope):
    if re.match(r'env.*', scope):
        e = ev.get_env(args, 'config add')
        e.set_config(section, new)
    else:
        spack.config.set(section, new, scope=scope)


def config_add(args):
    """Add the given configuration to the specified config scope

    This is a stateful operation that edits the config files."""
    if not (args.file or args.path):
        tty.error("No changes requested. Specify a file or value.")
        setup_parser.add_parser.print_help()
        exit(1)

    scope, section = _get_scope_and_section(args)

    # Updates from file
    if args.file:
        # Get file as config dict
        data = spack.config.read_config_file(args.file)
        if any(k in data for k in spack.schema.env.keys):
            data = ev.config_dict(data)

        # update all sections from config dict
        # We have to iterate on keys to keep overrides from the file
        for section in data.keys():
            if section in spack.config.section_schemas.keys():
                # Special handling for compiler scope difference
                # Has to be handled after we choose a section
                if scope is None:
                    scope = spack.config.default_modify_scope(section)

                value = data[section]
                existing = spack.config.get(section, scope=scope)
                new = spack.config.merge_yaml(existing, value)

                set_config(args, section, new, scope)

    if args.path:
        components = spack.config.process_config_path(args.path)

        has_existing_value = True
        path = ''
        override = False
        for idx, name in enumerate(components[:-1]):
            # First handle double colons in constructing path
            colon = '::' if override else ':' if path else ''
            path += colon + name
            if getattr(name, 'override', False):
                override = True
            else:
                override = False

            # Test whether there is an existing value at this level
            existing = spack.config.get(path, scope=scope)

            if existing is None:
                has_existing_value = False
                # We've nested further than existing config, so we need the
                # type information for validation to know how to handle bare
                # values appended to lists.
                existing = spack.config.get_valid_type(path)

                # construct value from this point down
                value = syaml.load_config(components[-1])
                for component in reversed(components[idx + 1:-1]):
                    value = {component: value}
                break

        if has_existing_value:
            path, _, value = args.path.rpartition(':')
            value = syaml.load_config(value)
            existing = spack.config.get(path, scope=scope)

        # append values to lists
        if isinstance(existing, list) and not isinstance(value, list):
            value = [value]

        # merge value into existing
        new = spack.config.merge_yaml(existing, value)
        set_config(args, path, new, scope)


def config_remove(args):
    """Remove the given configuration from the specified config scope

    This is a stateful operation that edits the config files."""
    scope, _ = _get_scope_and_section(args)

    path, _, value = args.path.rpartition(':')
    existing = spack.config.get(path, scope=scope)

    if not isinstance(existing, (list, dict)):
        path, _, value = path.rpartition(':')
        existing = spack.config.get(path, scope=scope)

    value = syaml.load(value)

    if isinstance(existing, list):
        values = value if isinstance(value, list) else [value]
        for v in values:
            existing.remove(v)
    elif isinstance(existing, dict):
        existing.pop(value, None)
    else:
        # This should be impossible to reach
        raise spack.config.ConfigError('Config has nested non-dict values')

    set_config(args, path, existing, scope)


def config(parser, args):
    action = {'get': config_get,
              'blame': config_blame,
              'edit': config_edit,
              'list': config_list,
              'add': config_add,
              'rm': config_remove,
              'remove': config_remove}
    action[args.config_command](args)
