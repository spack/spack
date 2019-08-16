# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Utility functions relevant to all commands, including Spack internal
commands and extension commands provided by third party packages.
"""

import spack.cmd
import spack.extensions

# Cache found spack commands.
_all_commands = None


def all_commands():
    """Return all top level commands available with Spack."""
    global _all_commands
    if _all_commands is None:
        extension_paths = spack.extensions.get_command_paths()
        _all_commands\
            = spack.cmd.find_commands(spack.paths.command_path,
                                      *extension_paths)
    return _all_commands


def get_module(cmd_name):
    """Imports the module for a particular Spack or extension top-level
    command name and returns it.

    Args:
        cmd_name (str): name of the command for which to get a module
            (contains ``-``, not ``_``).
    """
    spack.cmd.require_cmd_name(cmd_name)
    try:
        module = spack.cmd.get_module_from(cmd_name, 'spack')
    except ImportError:
        module = spack.extensions.load_command_extension(cmd_name)
    return module


def get_command(cmd_name):
    """Imports a top level command's function from a module and returns it.

    Args:
        cmd_name (str): name of the command for which to get a module
            (contains ``-``, not ``_``).
    """
    spack.cmd.require_cmd_name(cmd_name)
    pname = spack.cmd.python_name(cmd_name)
    return getattr(get_module(cmd_name), pname)
