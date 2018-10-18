# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import os


system_paths = ['/', '/usr', '/usr/local']
suffixes = ['bin', 'bin64', 'include', 'lib', 'lib64']
system_dirs = [os.path.join(p, s) for s in suffixes for p in system_paths] + \
    system_paths


def is_system_path(path):
    """Predicate that given a path returns True if it is a system path,
    False otherwise.

    Args:
        path (str): path to a directory

    Returns:
        True or False
    """
    return os.path.normpath(path) in system_dirs


def filter_system_paths(paths):
    return [p for p in paths if not is_system_path(p)]


def get_path(name):
    path = os.environ.get(name, "").strip()
    if path:
        return path.split(":")
    else:
        return []


def env_flag(name):
    if name in os.environ:
        value = os.environ[name].lower()
        return value == "true" or value == "1"
    return False


def path_set(var_name, directories):
    path_str = ":".join(str(dir) for dir in directories)
    os.environ[var_name] = path_str


def path_put_first(var_name, directories):
    """Puts the provided directories first in the path, adding them
       if they're not already there.
    """
    path = os.environ.get(var_name, "").split(':')

    for dir in directories:
        if dir in path:
            path.remove(dir)

    new_path = tuple(directories) + tuple(path)
    path_set(var_name, new_path)


def dump_environment(path):
    """Dump the current environment out to a file."""
    with open(path, 'w') as env_file:
        for key, val in sorted(os.environ.items()):
            env_file.write('export %s="%s"\n' % (key, val))


@contextlib.contextmanager
def set_env(**kwargs):
    """Temporarily sets and restores environment variables.

    Variables can be set as keyword arguments to this function.
    """
    saved = {}
    for var, value in kwargs.items():
        if var in os.environ:
            saved[var] = os.environ[var]

        if value is None:
            if var in os.environ:
                del os.environ[var]
        else:
            os.environ[var] = value

    yield

    for var, value in kwargs.items():
        if var in saved:
            os.environ[var] = saved[var]
        else:
            if var in os.environ:
                del os.environ[var]
