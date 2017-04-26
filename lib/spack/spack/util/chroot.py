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
import re
import os
import spack
from itertools import product
from spack.util.executable import which

EXECUTABLES = [
    'bash',
    'git',
    'tar',
    'curl'
]

DEFAULT_PATHS = [
    u'dev',
    u'sys',
    u'bin',
    u'run',
    u'etc',
    u'lib',
    u'lib32',
    u'lib64'
]

def get_all_library_directories():
    libraries = set(DEFAULT_PATHS)
    for exe in EXECUTABLES:
        executable = spack.util.executable.which(exe, required=True)
        for lib in executable.get_shared_libraries():
            libraries.add(os.path.dirname(lib[1:]))
    return list(libraries)

def mount_bind_path(realpath, chrootpath):
    os.system("mount --bind %s %s" % (realpath, chrootpath))

def build_chroot_enviroment(dir):
    libraries = get_all_library_directories()
    for lib in libraries:
        mount_bind_path(lib, os.path.join(dir, lib))
