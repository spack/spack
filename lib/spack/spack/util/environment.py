##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os

system_paths = ['/', '/usr/', '/usr/local']
suffixes = ['lib', 'lib64', 'include']
system_dirs = [os.path.join(p, s) for s in suffixes for p in system_paths]
system_bins = [os.path.join(p, 'bin') for p in system_paths]


def filter_system_paths(paths):
    return [p for p in paths if p not in system_dirs]


def filter_system_bin_paths(paths):
    # Turn the iterable into a list. Assume it's a list from here on.
    _paths = list(paths)
    bins = [p for p in _paths if p in system_bins]
    nobins = [p for p in _paths if p not in system_bins]
    # put bins infront as PATH is set by: prepend_path('PATH', item)
    return bins + nobins


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
            env_file.write("%s=%s\n" % (key, val))
