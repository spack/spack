##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
# 
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
# 
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import re
import shutil
import errno
import getpass
from contextlib import contextmanager, closing

import spack.tty as tty
from spack.util.compression import ALLOWED_ARCHIVE_TYPES


def install(src, dest):
    """Manually install a file to a particular location."""
    tty.info("Installing %s to %s" % (src, dest))
    shutil.copy(src, dest)


def expand_user(path):
    """Find instances of '%u' in a path and replace with the current user's
       username."""
    username = getpass.getuser()
    if not username and '%u' in path:
        tty.die("Couldn't get username to complete path '%s'" % path)

    return path.replace('%u', username)


@contextmanager
def working_dir(dirname):
    orig_dir = os.getcwd()
    os.chdir(dirname)
    yield
    os.chdir(orig_dir)


def mkdirp(*paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise OSError(errno.EEXIST, "File alredy exists", path)


def new_path(prefix, *args):
    path = str(prefix)
    for elt in args:
        path = os.path.join(path, str(elt))

    if re.search(r'\s', path):
        tty.die("Invalid path: '%s'.  Use a path without whitespace." % path)

    return path


def ancestor(dir, n=1):
    """Get the nth ancestor of a directory."""
    parent = os.path.abspath(dir)
    for i in range(n):
        parent = os.path.dirname(parent)
    return parent


def stem(path):
    """Get the part of a path that does not include its compressed
       type extension."""
    for type in ALLOWED_ARCHIVE_TYPES:
        suffix = r'\.%s$' % type
        if re.search(suffix, path):
            return re.sub(suffix, "", path)
    return path


def can_access(file_name):
    """True if we have read/write access to the file."""
    return os.access(file_name, os.R_OK|os.W_OK)


