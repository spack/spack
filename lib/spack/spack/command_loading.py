# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Utility functions relevant to all commands, including Spack internal
commands and extension commands provided by third party packages.
"""

from llnl.util.lang import attr_setdefault
import llnl.util.tty as tty

import spack.cmd
import spack.extensions

# Cache found spack commands.
_all_commands = None

SETUP_PARSER = "setup_parser"
DESCRIPTION = "description"


def all_commands():
    """Return all top level commands available with Spack."""
    global _all_commands
    if _all_commands is None:
        extension_paths = spack.extensions.get_command_paths()
        _all_commands\
            = spack.cmd.find_commands(spack.paths.command_path,
                                      *extension_paths)
    return _all_commands


def get_command_module_from(cmd_name, namespace):
    """Imports the module for a particular command from the specified namespace.

    Args:
        cmd_name (str): name of the command for which to get a module
            (contains ``-``, not ``_``).
        namespace (str): namespace for command.

    Invoke this from command implementations in order to find sub-commands.
    """
    spack.cmd.require_cmd_name(cmd_name)
    pname = spack.cmd.python_name(cmd_name)
    module_name = '{0}.cmd.{1}'.format(namespace, pname)
    module = __import__(module_name,
                        fromlist=[pname, SETUP_PARSER, DESCRIPTION],
                        level=0)
    tty.debug('Imported command {0} as {1}'.format(cmd_name, module_name))

    attr_setdefault(module, SETUP_PARSER, lambda *args: None)  # null-op
    attr_setdefault(module, DESCRIPTION, "")

    if not hasattr(module, pname):
        tty.die("Command module %s (%s) must define function '%s'." %
                (module.__name__, module.__file__, pname))
    return module


def get_command_module(cmd_name):
    """Imports the module for a particular Spack or extension top-level
    command name and returns it.

    Args:
        cmd_name (str): name of the command for which to get a module
            (contains ``-``, not ``_``).
    """
    spack.cmd.require_cmd_name(cmd_name)
    try:
        module = get_command_module_from(cmd_name, 'spack')
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
    return getattr(get_command_module(cmd_name), pname)
