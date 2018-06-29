# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Service functions and classes to implement the hooks
for Spack's command extensions.
"""
import os
import re

import llnl.util.lang
import llnl.util.tty as tty

extension_regexp = re.compile(r'spack-([\w]*)')


def extension_name(path):
    """Returns the name of the extension in the path passed as argument.

    Args:
        path (str): path where the extension resides

    Returns:
        The extension name or None if path doesn't match the format
        for Spack's extension.
    """
    regexp_match = re.search(extension_regexp, os.path.basename(path))
    if not regexp_match:
        msg = "[FOLDER NAMING]"
        msg += " {0} doesn't match the format for Spack's extensions"
        tty.warn(msg.format(path))
        return None
    return regexp_match.group(1)


def load_command_extension(command, path):
    """Loads a command extension from the path passed as argument.

    Args:
        command (str): name of the command
        path (str): base path of the command extension

    Returns:
        A valid module object if the command is found or None
    """
    extension = extension_name(path)
    if not extension:
        return None

    # Compute the absolute path of the file to be loaded, along with the
    # name of the python module where it will be stored
    cmd_path = os.path.join(path, extension, 'cmd', command + '.py')
    python_name = command.replace('-', '_')
    module_name = '{0}.{1}'.format(__name__, python_name)

    try:
        module = llnl.util.lang.load_module_from_file(module_name, cmd_path)
    except (ImportError, IOError):
        module = None

    return module


def command_paths(*paths):
    """Generator that yields paths where to search for command files.

    Args:
        *paths: paths where the extensions reside

    Returns:
        Paths where to search for command files.
    """
    for path in paths:
        extension = extension_name(path)
        if extension:
            yield os.path.join(path, extension, 'cmd')
