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
import sys
import spack
import cPickle as pickle
import llnl.util.tty as tty
from socket import *
from spack.util.executable import which

from fstab import Fstab
from daemon import Daemon

# Files or paths which need to be binded with mount --bind
BIND_PATHS = [
    '/dev',
    '/sys',
    '/proc'
]

# Files or paths which need to be copied
COPY_PATHS = [
    '/etc/resolv.conf'
]

mount_daemon_pidfile = "/tmp/spack-mount-deamon.pid"
MOUNT_DEV   = 1
MOUNT_SYS   = 2
MOUNT_PROC  = 3
UMOUNT_DEV  = 4
UMOUNT_SYS  = 5
UMOUNT_PROC = 6


class MountOperation:

    def __init__(self, operation, location):
        self.operation = operation
        self.location  = location

    def __str__(self):
        if (self.operation == 1):
            return "MOUNT DEV: " + self.location
        elif (self.operation == 2):
            return "MOUNT SYS: " + self.location
        elif (self.operation == 3):
            return "MOUNT PROC: " + self.location
        elif (self.operation == 4):
            return "UMOUNT DEV: " + self.location
        elif (self.operation == 5):
            return "UMOUNT SYS: " + self.location
        elif (self.operation == 6):
            return "UMOUNT PROC: " + self.location
        return "UNKNOWN OPERATION: " + self.operation + ", " + self.location


class MountDaemon(Daemon):

    def __init__(self,
                 stdin='/dev/null',
                 stdout='/dev/null',
                 stderr='/dev/null'):
        Daemon.__init__(self, mount_daemon_pidfile, stdin, stdout, stderr)
        self.bound_locations = set()
        self.socket = None

    def init_network(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", 11259))
        self.bufferSize = 16384

    def shutdown(self):
        Daemon.shutdown(self)
        self.socket.close()

        for mount in self.bound_locations:
            umount_bind_path(mount, False)

    def run(self):
        self.init_network()
        while True:
            # check if the file got remove and recreate it if necessary
            if (not os.path.exists(self.pidfile)):
                pid = str(os.getpid())
                with file(self.pidfile, 'w+') as f:
                    f.write("%s\n" % pid)

            # recive the commands from a spack implementation
            (data, addr) = self.socket.recvfrom(self.bufferSize)
            operation = pickle.loads(data)

            # run the mount operations
            if (operation is not None):
                if (operation.operation in [1, 2, 3]):
                    if (operation.location in self.bound_locations):
                        continue
                elif (operation.operation in [4, 5, 6]):
                    if (operation.location not in self.bound_locations):
                        continue

                if (operation.operation == 1):
                    self.bound_locations.add(operation.location)
                    mount_bind_path('/dev', operation.location, False)
                    sys.stdout.write(str(operation) + '\n')
                elif (operation.operation == 2):
                    self.bound_locations.add(operation.location)
                    mount_bind_path('/sys', operation.location, False)
                    sys.stdout.write(str(operation) + '\n')
                elif (operation.operation == 3):
                    self.bound_locations.add(operation.location)
                    mount_bind_path('/proc', operation.location, False)
                    sys.stdout.write(str(operation) + '\n')
                elif (operation.operation == 4):
                    self.bound_locations.remove(operation.location)
                    umount_bind_path(operation.location, False)
                    sys.stdout.write(str(operation) + '\n')
                elif (operation.operation == 5):
                    self.bound_locations.remove(operation.location)
                    umount_bind_path(operation.location, False)
                    sys.stdout.write(str(operation) + '\n')
                elif (operation.operation == 6):
                    self.bound_locations.remove(operation.location)
                    umount_bind_path(operation.location, False)
                    sys.stdout.write(str(operation) + '\n')
                else:
                    sys.stderr.write(str(operation) + '\n')
            else:
                sys.stderr.write("recived unknown command %s\n" %
                                 str(type(operation)))

            sys.stderr.flush()
            sys.stdout.flush()


def mount_bind_path(realpath, chrootpath, permanent):
        mount = True
        if os.path.isfile(realpath):
            if not os.path.exists(os.path.dirname(chrootpath)):
                os.makedirs(os.path.dirname(chrootpath))

            if not os.path.exists(chrootpath):
                with open(chrootpath, "w"):
                    pass
        else:
            # Don't include empty directories
            if os.listdir(realpath):
                if not os.path.exists(chrootpath):
                    os.makedirs(chrootpath)
            else:
                mount = False

        if mount:
            if permanent:
                Fstab.add(realpath, chrootpath,
                          filesystem="none", options="bind")
            os.system("sudo mount --bind %s %s" % (realpath, chrootpath))


def send_command_to_daemon(command):
    sock = socket(AF_INET, SOCK_DGRAM)
    data = pickle.dumps(command, pickle.HIGHEST_PROTOCOL)
    sock.sendto(data, ("127.0.0.1", 11259))
    sock.close()


def umount_bind_path(chrootpath, permanent):
    # remove permanent mount point
    if permanent:
        Fstab.remove_by_mountpoint(chrootpath)

    # Don't unmount no existing directories
    if os.path.exists(chrootpath):
        os.system("sudo umount -l %s" % (chrootpath))


def copy_path(realpath, chrootpath):
    if os.path.exists(realpath):
        os.system("cp %s %s" % (realpath, chrootpath))


def copy_environment(dir):
    for lib in COPY_PATHS:
        copy_path(lib, os.path.join(dir, lib[1:]))


def build_chroot_environment(dir, permanent):
    if os.path.ismount(dir):
        tty.die("The path is already a bootstraped enviroment")

    # if a daemon exist use it instead of the local command
    # which require root rights
    if (os.path.exists(mount_daemon_pidfile)):
        send_command_to_daemon(
            MountOperation(MOUNT_DEV, os.path.join(dir, 'dev')))
        send_command_to_daemon(
            MountOperation(MOUNT_SYS, os.path.join(dir, 'sys')))
        send_command_to_daemon(
            MountOperation(MOUNT_PROC, os.path.join(dir, 'proc')))
    else:
        for lib in BIND_PATHS:
            mount_bind_path(lib, os.path.join(dir, lib[1:]), permanent)

    copy_environment(dir)


def remove_chroot_environment(dir, permanent):
    if (os.path.exists(mount_daemon_pidfile)):
        send_command_to_daemon(
            MountOperation(UMOUNT_DEV, os.path.join(dir, 'dev')))
        send_command_to_daemon(
            MountOperation(UMOUNT_SYS, os.path.join(dir, 'sys')))
        send_command_to_daemon(
            MountOperation(UMOUNT_PROC, os.path.join(dir, 'proc')))
    else:
        for lib in BIND_PATHS:
            umount_bind_path(os.path.join(dir, lib[1:]), permanent)


def get_group(username):
    groups = which("groups", required=True)
    # just use the first group
    group = groups(username, output=str).split(':')[1].strip().split(' ')[0]
    return group


def get_username_and_group():
    whoami = which("whoami", required=True)
    username = whoami(output=str).replace('\n', '')
    return username, get_group(username)


def run_command(command):
    chrootCommand = "chroot %s %s" % (spack.spack_bootstrap_root, command)
    options = "--user --map-root-user --mount-proc --pid"
    os.system("unshare %s --fork sh -c '%s'" % (options, chrootCommand))


def isolate_environment():
    if (os.path.exists(mount_daemon_pidfile)):
        tty.msg("Isolate spack through a daemon process")
    else:
        tty.msg("Isolate spack through mount bind")

    lockFile = os.path.join(spack.spack_root, '.env')
    existed = True

    # check if the environment has to be generated
    config = spack.config.get_config("config", "site")
    permanent = config['permanent']

    if not os.path.exists(lockFile) and not permanent:
        build_chroot_environment(spack.spack_bootstrap_root, False)
        existed = False
    else:
        # copy necessary files
        copy_environment(spack.spack_bootstrap_root)

    run_command('/home/spack/bin/spack %s' % (' '.join(sys.argv[1:])))

    if not existed:
        remove_chroot_environment(spack.spack_bootstrap_root, False)
