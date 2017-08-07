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

# Files or paths which need to be binded with mount --bind
BIND_PATHS = [
    '/dev',
]

# Files or paths which need to be copied
COPY_PATHS = [
    '/etc/resolv.conf'
]

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

def copy_path(realpath, chrootpath):
    if os.path.exists(realpath):
        os.system("cp %s %s" % (realpath, chrootpath))

def build_chroot_enviroment(dir):
    if os.path.ismount(dir):
        tty.die("The path is already a bootstraped enviroment")

    for lib in BIND_PATHS:
        mount_bind_path(lib, os.path.join(dir, lib[1:]))

    for lib in COPY_PATHS:
        copy_path(lib, os.path.join(dir, lib[1:]))

def remove_chroot_enviroment(dir):
    for lib in BIND_PATHS:
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
