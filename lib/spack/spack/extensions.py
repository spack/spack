# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Service functions and classes to implement the hooks
for Spack's command extensions.
"""
import os
import re
import sys
import types

import llnl.util.lang
import spack.cmd
import spack.config
from spack.error import SpackError

_command_paths = []
_extension_regexp = re.compile(r'spack-([\w]*)')
_extension_command_map = None


class CommandNotFoundError(SpackError):
    """Exception class thrown when a requested command is not recognized as
    such.
    """
    def __init__(self, cmd_name):
        super(CommandNotFoundError, self).__init__(
            '{0} is not a recognized Spack command or extension command.'
            .format(cmd_name),
            'Known commands: {0}'.format(' '.join(spack.cmd.all_commands())))


class ExtensionNamingError(SpackError):
    """Exception class thrown when a configured extension does not follow
    the expected naming convention.
    """
    def __init__(self, path):
        super(ExtensionNamingError, self).__init__(
            '{0} does not match the format for a Spack extension path.'
            .format(path))


def _init_extension_command_map():
    """Return the list of paths where to search for command files."""
    global _extension_command_map
    if _extension_command_map is None:
        _extension_command_map = {}
        extension_paths = spack.config.get('config:extensions') or []
        for path in extension_paths:
            extension = extension_name(path)
            command_path = os.path.join(path, extension, 'cmd')
            _command_paths.append(command_path)
            commands = spack.cmd.find_commands(command_path)
            _extension_command_map.update(
                dict((command, path) for command in
                     commands if command not in _extension_command_map))


def reset_command_cache():
    """For testing purposes, reset the command cache e.g. for a modified
    extension configuration.
    """
    global _command_paths
    _command_paths = []
    global _extension_command_map
    _extension_command_map = None


def get_command_paths():
    _init_extension_command_map()  # Ensure we are initialized.
    return _command_paths


def extension_name(path):
    """Returns the name of the extension in the path passed as argument.

    Args:
        path (str): path where the extension resides

    Returns:
        The extension name or None if path doesn't match the format
        for Spack's extension.
    """
    regexp_match = re.search(_extension_regexp, os.path.basename(path))
    if not regexp_match:
        raise ExtensionNamingError(path)
    return regexp_match.group(1)


def load_command_extension(command):
    """Loads a command extension from the path passed as argument.

    Args:
        command (str): name of the command

    Returns:
        A valid module object if the command is found or None
    """
    _init_extension_command_map()  # Ensure we have initialized.
    global _extension_command_map
    if command not in _extension_command_map:
        raise CommandNotFoundError(command)
    path = _extension_command_map[command]
    extension = extension_name(path)

    # Compute the name of the module we search, exit early if already imported
    cmd_package = '{0}.{1}.cmd'.format(__name__, extension)
    python_name = command.replace('-', '_')
    module_name = '{0}.{1}'.format(cmd_package, python_name)
    if module_name in sys.modules:
        return sys.modules[module_name]

    def ensure_package_creation(name):
        package_name = '{0}.{1}'.format(__name__, name)
        if package_name in sys.modules:
            return

        parts = [path] + name.split('.') + ['__init__.py']
        init_file = os.path.join(*parts)
        if os.path.exists(init_file):
            m = llnl.util.lang.load_module_from_file(package_name, init_file)
        else:
            m = types.ModuleType(package_name)

        # Setting __path__ to give spack extensions the
        # ability to import from their own tree, see:
        #
        # https://docs.python.org/3/reference/import.html#package-path-rules
        #
        m.__path__ = [os.path.dirname(init_file)]
        sys.modules[package_name] = m

    # Create a searchable package for both the root folder of the extension
    # and the subfolder containing the commands
    ensure_package_creation(extension)
    ensure_package_creation(extension + '.cmd')

    # Compute the absolute path of the file to be loaded, along with the
    # name of the python module where it will be stored
    cmd_path = os.path.join(path, extension, 'cmd', command + '.py')

    # TODO: Upon removal of support for Python 2.6 substitute the call
    # TODO: below with importlib.import_module(module_name)
    module = llnl.util.lang.load_module_from_file(module_name, cmd_path)
    sys.modules[module_name] = module

    return module


def path_for_extension(target_name, *paths):
    """Return the test root dir for a given extension.

    Args:
        target_name (str): name of the extension to test
        *paths: paths where the extensions reside

    Returns:
        Root directory where tests should reside or None
    """
    for path in paths:
        name = extension_name(path)
        if name == target_name:
            return path
    else:
        raise IOError('extension "{0}" not found'.format(target_name))


def get_template_dirs():
    """Returns the list of directories where to search for templates
    in extensions.
    """
    extension_dirs = spack.config.get('config:extensions') or []
    extensions = [os.path.join(x, 'templates') for x in extension_dirs]
    return extensions
