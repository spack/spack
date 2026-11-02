# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Common argument definitions shared between main.py and config.py.

This module defines global spack arguments without importing heavy dependencies,
so it can be imported during config.py module initialization without circular imports.
"""

import os


def add_all_global_arguments(parser):
    """Add all global spack arguments to a parser.

    This is shared between main.py's make_argument_parser() and config.py's
    command extraction logic.

    Args:
        parser: An ArgumentParser (or subclass) to add arguments to
    """
    import argparse

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
