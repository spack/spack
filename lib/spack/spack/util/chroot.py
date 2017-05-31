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
import copy
import spack
import subprocess
import llnl.util.tty as tty
from itertools import product
from spack.util.executable import which
from llnl.util.filesystem import join_path

# Packages to include into the chroot enviroment
PACKAGES = [
    'bash',
    'curl',
    'gcc',
    'g++',
    'lsb-release',

    # only exact matches
    ('apt-cache', True),
    ('coreutils', True),
    ('diffutils', True),
    ('findutils', True),
    ('gawk', True),
    ('libc5', True),
    ('libc5-dev', True),
    ('libc6', True),
    ('libc6-dev', True),
    ('linux-libc-dev', True),
    ('make', True),
    ('mawk', True),
    ('patch', True),
    ('perl', True),
    ('python', True),
    ('python3', True),
]

# Paths which are always needed
DEFAULT_PATHS = [
    '/usr/bin/awk',

    #'/bin',
    '/dev',
    '/etc',
    '/lib',
    '/lib64',
    '/proc',
    '/run',
    '/sys',
]

# Package which are unnecessary and shouldn't be included
EXCLUDE_PACKAGES = [
    # unnecessary packages
    'base-files',
    'libpcre3',
]

# Paths which shouldn't be included into the chroot enviroment
EXCLUDE_PATHS = [
    '/tmp',
    '/sbin',
    '/home',
    '/boot',
    '/root',
    '/lost+found',
    '/cdrom',
]

def find_dependencies(package_name, package_cache):
    apt_cache = spack.util.executable.which("apt-cache", requred=True)
    cmd = '%s depends %s' % (apt_cache.exe[0], package_name)
    dependencies = os.popen(cmd).read()

    results = set()
    reg = re.compile(r'(\s+)?(PreDepends|Depends):\s*([^\s]+)')
    for dependency in dependencies.split('\n'):
        found = reg.match(dependency)
        if found:
            name = found.group(3)
            if name not in EXCLUDE_PACKAGES:
                results.add(name)
                if name not in package_cache:
                    package_cache.add(name)
                    results.update(find_dependencies(name, package_cache))

    return results


def find_packages(name, exact, package_cache):
    dpkg = spack.util.executable.which("dpkg", requred=True)
    installedPackages = dpkg('-l',output=str)
    name = name.replace('\n', '').replace('+', r'\+')

    result = set()
    if not exact:
        regStr = r'ii\s+(([^\s]*' + name + \
                 r'[^\s|:]*)(:[^\s]+)?)\s+[^\s]+\s+[^\s]+\s+[^\n]+'
    else:
        regStr = r'ii\s+((' + name + r')(:[^\s]+)?)\s+[^\s]+\s+[^\s]+\s+[^\n]+'

    regex = re.compile(regStr)
    for package in installedPackages.split('\n'):
        found = regex.match(package)
        if found:
            package_name = found.group(2)
            dependencies = find_dependencies(package_name, package_cache)

            result.add(name)
            result.update(dependencies)
    return result


def find_package_files(package_name, file_cache):
    if package_name in file_cache:
        return file_cache[package_name]

    dpkg = spack.util.executable.which("dpkg", requred=True)

    package_name = package_name.replace('\n', '')
    # TODO: Only works with popen and produces an invalid command without?
    results = os.popen("%s -L %s" % (dpkg.exe[0], package_name)).read()

    toRemove = set(['/.'])
    results = set(results.split('\n'))
    for file in results:
        path = os.path.dirname(file)
        while path != '/':
            if path in results:
                toRemove.add(path)
                break
            path = os.path.dirname(path)

    for dub in toRemove:
        if dub in results:
            results.remove(dub)

    for result in results:
        if result == "/usr/bin":
            print "USER:", package_name

    file_cache[package_name] = list(results)
    return file_cache[package_name]


def merge_files(files, libraries):
    merged = 0
    final = set()
    for file in files:
        if not os.path.exists(file):
            continue

        dirname = os.path.dirname(file)
        if dirname in final:
            continue

        files = [join_path(dirname, x) for x in os.listdir(dirname)]
        count = sum([(1 if x in libraries else 0) for x in files])
        if count == len(files):
            merged += 1
            final.add(dirname)
        else:
            final.add(file)

    if merged != 0:
        return merge_files(final, libraries)
    return final

def get_all_library_directories():
    libraries = set(DEFAULT_PATHS)

    package_cache = set()
    file_cache = dict()
    for package in PACKAGES:
        if type(package) is tuple:
            name, exact = package[0], package[1]
        else:
            name, exact = package, False

        tty.msg("Search for %s " % (name))
        package_names = find_packages(name, exact, package_cache)
        for package_name in package_names:
            for file in find_package_files(package_name, file_cache):
                if file and file not in EXCLUDE_PATHS:
                    libraries.add(file)

    tty.msg("Compute amount of required files: %d" % (len(libraries)))

    final = merge_files(libraries, libraries)
    for lib in copy.deepcopy(final):
        path = os.path.dirname(lib)
        # Don't mount documentation files
        if 'doc' in path or 'man' in path or '.mo' in path or '.po' in path:
            final.remove(lib)
        else:
            while path and path != '/':
                if path in final:
                    final.remove(lib)
                    break
                path = os.path.dirname(path)

    tty.msg("Compressed required files to: %d" % (len(final)))
    return final


def mount_bind_path(realpath, chrootpath):
    mount = True
    if os.path.isfile(realpath):
        if not os.path.exists(os.path.dirname(chrootpath)):
            os.makedirs(os.path.dirname(chrootpath))

        if not os.path.exists(chrootpath):
            with open(chrootpath, "w") as out:
                pass
    else:
        # Don't include empty directories
        if os.listdir(realpath):
            if not os.path.exists(chrootpath):
                os.makedirs(chrootpath)
        else:
            mount = False

    if mount:
        os.system ("sudo mount --bind %s %s" % (realpath, chrootpath))

def umount_bind_path(chrootpath):
    # Don't unmount no existing directories
    if os.path.exists(chrootpath):
        os.system ("sudo umount -l %s" % (chrootpath))

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

def isolate_enviroment():
    tty.msg("Isolate spack")

    lockFile = os.path.join(spack.spack_root, '.env')
    existed = True
    # check if the enviroment has to be generated
    if not os.path.exists(lockFile):
        build_chroot_enviroment(spack.spack_bootstrap_root)
        existed = False

    whoami = which("whoami", required=True)
    username = whoami(output=str).replace('\n', '')
    groups = which("groups", required=True)

    # just use the first group
    group = groups(username, output=str).split(':')[1].strip().split(' ')[0]

    #restart the command in the chroot jail
    os.system ("sudo chroot --userspec=%s:%s %s /home/spack/bin/spack %s"
        % (username, group, spack.spack_bootstrap_root, ' '.join(sys.argv[1:])))

    if not existed:
        remove_chroot_enviroment(spack.spack_bootstrap_root)
