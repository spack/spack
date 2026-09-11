# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Low-level argument parsing utilities for Spack CLI.

This module provides argument parsing primitives that can be used by both
main.py (for full command execution) and config.py (for command detection
during initialization) without creating circular dependencies.

DO NOT import spack.main or spack.config from this module.
"""

import argparse
import os
import shlex
import sys
from typing import List, Optional


def create_basic_parser(parser_class=None, **kwargs) -> argparse.ArgumentParser:
    """Create a basic argument parser with Spack's global flags.

    This creates an ArgumentParser configured with all of Spack's global
    flags (--debug, --config, --env, etc.) but does NOT add any subcommands.

    The caller should add a 'command' argument with nargs=REMAINDER to
    capture the command and its arguments:

        parser = create_basic_parser()
        parser.add_argument("command", nargs=argparse.REMAINDER)
        args = parser.parse_args()

    This function is used by:
    - config.py: for detecting commands during config initialization
    - main.py: as the base for creating the full SpackArgumentParser

    Args:
        parser_class: Optional custom ArgumentParser subclass to use.
                      If None, uses argparse.ArgumentParser.
                      main.py passes SpackArgumentParser for fancy help formatting.

    Returns:
        ArgumentParser (or subclass) configured with Spack's global flags
    """
    if parser_class is None:
        parser_class = argparse.ArgumentParser

    parser = parser_class(
        prog="spack",
        add_help=False,  # We handle help specially
        **kwargs,
    )

    general = parser.add_argument_group("general")
    general.add_argument(
        "--color",
        action="store",
        default=None,
        choices=("always", "never", "auto"),
        help="when to colorize output (default: auto)",
    )
    general.add_argument(
        "-v", "--verbose", action="store_true", help="print additional output during builds"
    )
    general.add_argument(
        "-k",
        "--insecure",
        action="store_true",
        help="do not check ssl certificates when downloading",
    )
    general.add_argument(
        "-b", "--bootstrap", action="store_true", help="use bootstrap config, store, and externals"
    )
    general.add_argument(
        "-V", "--version", action="store_true", help="show version number and exit"
    )
    general.add_argument(
        "-h",
        "--help",
        dest="help",
        action="store_const",
        const="short",
        default=None,
        help="show this help message and exit",
    )
    general.add_argument(
        "-H",
        "--all-help",
        dest="help",
        action="store_const",
        const="long",
        default=None,
        help="show help for all commands (same as `spack help --all`)",
    )

    config = parser.add_argument_group("configuration and environments")
    config.add_argument(
        "-c",
        "--config",
        default=None,
        action="append",
        dest="config_vars",
        help="add one or more custom, one-off config settings",
    )
    config.add_argument(
        "-C",
        "--config-scope",
        dest="config_scopes",
        action="append",
        metavar="DIR|ENV",
        help="add directory or environment as read-only config scope",
    )
    envs = config
    env_mutex = envs.add_mutually_exclusive_group()
    env_mutex.add_argument(
        "-e", "--env", dest="env", metavar="ENV", action="store", help="run with an environment"
    )
    env_mutex.add_argument(
        "-D",
        "--env-dir",
        dest="env_dir",
        metavar="DIR",
        action="store",
        help="run with environment in directory (ignore managed envs)",
    )
    env_mutex.add_argument(
        "-E",
        "--no-env",
        dest="no_env",
        action="store_true",
        help="run without any environments activated (see spack env)",
    )
    envs.add_argument(
        "--use-env-repo",
        action="store_true",
        help="when in an environment, use its package repository",
    )

    debug = parser.add_argument_group("debug")
    debug.add_argument(
        "-d",
        "--debug",
        action="count",
        default=0,
        help="write out debug messages\n\n(more d's for more verbosity: -d, -dd, -ddd, etc.)",
    )
    debug.add_argument(
        "-t",
        "--backtrace",
        action="store_true",
        default="SPACK_BACKTRACE" in os.environ,
        help="always show backtraces for exceptions",
    )
    debug.add_argument("--pdb", action="store_true", help=argparse.SUPPRESS)
    debug.add_argument("--timestamp", action="store_true", help="add a timestamp to tty output")
    debug.add_argument(
        "-m", "--mock", action="store_true", help="use mock packages instead of real ones"
    )
    debug.add_argument(
        "--print-shell-vars", action="store", help="print info needed by setup-env.*sh"
    )
    debug.add_argument(
        "--stacktrace",
        action="store_true",
        default="SPACK_STACKTRACE" in os.environ,
        help="add stacktraces to all printed statements",
    )

    locks = general
    lock_mutex = locks.add_mutually_exclusive_group()
    lock_mutex.add_argument(
        "-l",
        "--enable-locks",
        action="store_true",
        dest="locks",
        default=None,
        help="use filesystem locking (default)",
    )
    lock_mutex.add_argument(
        "-L",
        "--disable-locks",
        action="store_false",
        dest="locks",
        help="do not use filesystem locking (unsafe)",
    )

    debug.add_argument(
        "-p", "--profile", action="store_true", dest="spack_profile", help=argparse.SUPPRESS
    )
    debug.add_argument("--profile-file", default=None, help=argparse.SUPPRESS)
    debug.add_argument("--sorted-profile", default=None, metavar="STAT", help=argparse.SUPPRESS)
    debug.add_argument("--lines", default=20, action="store", help=argparse.SUPPRESS)

    return parser


def resolve_command_alias(cmd_name: str, aliases: dict) -> str:
    """Resolve a command alias to its actual command.

    Args:
        cmd_name: The command name (possibly an alias)
        aliases: Dictionary of aliases from config (e.g., config.get('config:aliases'))

    Returns:
        The resolved command name (first word of alias expansion, or original if not aliased)

    Examples:
        >>> resolve_command_alias('i', {'i': 'install'})
        'install'
        >>> resolve_command_alias('install', {'i': 'install'})
        'install'
        >>> resolve_command_alias('foo', {})
        'foo'
    """
    if not aliases or cmd_name not in aliases:
        return cmd_name

    alias = aliases.get(cmd_name)
    if not alias:
        return cmd_name

    # Parse the alias and return the first word (the actual command)
    try:
        alias_parts = shlex.split(alias)
        return alias_parts[0] if alias_parts else cmd_name
    except ValueError:
        # Invalid shell syntax in alias - treat as not aliased
        return cmd_name


def get_command_from_argv(argv: Optional[List[str]] = None, aliases: Optional[dict] = None) -> Optional[str]:
    """Extract and resolve the Spack command from argv.

    This function:
    1. Parses argv using Spack's global flags
    2. Extracts the command name (skipping all flags)
    3. Resolves any aliases using the provided aliases dict

    This is a low-level utility used by:
    - config.py: to detect 'spack isolate' during config initialization
    - main.py: to get the command for execution

    Args:
        argv: Command-line arguments (defaults to sys.argv).
              Expected format: ['spack', 'command', 'args...'] or ['command', 'args...']
        aliases: Dictionary of command aliases (e.g., {'i': 'install'}).
                 If None, no alias resolution is performed.

    Returns:
        The resolved command name, or None if no command found.

    Examples:
        >>> get_command_from_argv(['spack', 'install', 'zlib'])
        'install'

        >>> # With aliases = {'i': 'install'}
        >>> get_command_from_argv(['spack', 'i', 'zlib'], aliases={'i': 'install'})
        'install'

        >>> get_command_from_argv(['spack', '-d', 'isolate', '--path', '/tmp'])
        'isolate'

        >>> get_command_from_argv(['spack', '--help'])
        None
    """
    if argv is None:
        argv = sys.argv

    # Handle both ['spack', 'command', ...] and ['command', ...] formats
    # (main.py passes full sys.argv, some tests might pass without 'spack')
    parse_argv = argv[1:] if argv and (argv[0].endswith('spack') or argv[0] == 'spack') else argv

    # Create parser with Spack's global flags and add command argument
    parser = create_basic_parser()
    parser.add_argument("command", nargs=argparse.REMAINDER)

    try:
        # parse_known_args is more forgiving - ignores unrecognized flags
        # (important during config init before everything is set up)
        args, _ = parser.parse_known_args(parse_argv)
    except SystemExit:
        # Parser exits on --help, --version, etc.
        return None

    if not args.command:
        return None

    cmd_name = args.command[0]

    # Resolve aliases if provided
    if aliases:
        cmd_name = resolve_command_alias(cmd_name, aliases)

    return cmd_name
