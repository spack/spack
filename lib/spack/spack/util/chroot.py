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
import sys
import spack
from itertools import product
from spack.util.executable import which

EXECUTABLES = [
    'env',
    'git',
    'tar',
    'bash',
    'curl',
    'python',
    'python3',
    'lsb_release',

    'apt-cache', #for lsb_release
    'dpkg-query',

    #debug
    'ls',
    'cat',
    'tail',
    'mkdir',
]

DEFAULT_PATHS = [
    '/bin',
    '/dev',
    '/sys',
    '/run',
    '/proc',
    '/etc',
    '/lib',

    #networking
    #'/etc/resolv.conf',
    '/lib/x86_64-linux-gnu/libnss_files.so.2',
    '/lib/x86_64-linux-gnu/libnss_dns.so.2',

    #git
    '/usr/share/git-core',

    #distinfo
    '/usr/share/distro-info',

    #python
    #todo find a better way
    '/usr/lib/python2.7',
    '/usr/lib/python3',
    '/usr/lib/python3.5',
    '/usr/share/pyshared' # for lsb_release
]

def get_all_library_directories():
    libraries = set(DEFAULT_PATHS)
    for exe in EXECUTABLES:
        executable = spack.util.executable.which(exe, required=True)
        files = executable.get_shared_libraries()
        files.extend(executable.exe)
        for lib in files:
            libraries.add(os.path.normpath(lib))

    duplicates = list()
    for lib in libraries:
        path = os.path.dirname(lib)
        while path != '/':
            if path in libraries:
                duplicates.append(lib)
                break
            path = os.path.dirname(path)

    for dub in duplicates:
        libraries.remove(dub)

    return list(libraries)

def mount_bind_path(realpath, chrootpath):
    if os.path.isfile(realpath):
        if not os.path.exists(os.path.dirname(chrootpath)):
            os.makedirs(os.path.dirname(chrootpath))

        if not os.path.exists(chrootpath):
            with open(chrootpath, "w") as out:
                pass
    else:
        if not os.path.exists(chrootpath):
            os.makedirs(chrootpath)

    os.system("mount --bind %s %s" % (realpath, chrootpath))

def umount_bind_path(chrootpath):
    os.system("umount -l %s" % (chrootpath))

def build_chroot_enviroment(dir):
    if os.path.ismount(dir):
        tty.die("The path is already a bootstraped enviroment")

    libraries = get_all_library_directories()
    for lib in libraries:
        mount_bind_path(lib, os.path.join(dir, lib[1:]))

def remove_chroot_enviroment(dir):
    libraries = get_all_library_directories()
    for lib in libraries:
        umount_bind_path(os.path.join(dir, lib[1:]))
