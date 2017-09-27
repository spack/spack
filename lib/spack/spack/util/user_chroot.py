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
import signal
import ctypes
import platform
import ctypes.util
import llnl.util.tty as tty

libc_so = ctypes.util.find_library('c')
libc = ctypes.CDLL(libc_so, use_errno=True)

# defines
PR_CAP_AMBIENT = 47
PR_CAP_AMBIENT_RAISE = 2
PR_CAPBSET_DROP = 24
PR_SET_PDEATHSIG = 1
PR_SET_NO_NEW_PRIVS = 38


LINUX_CAPABILITY_VERSION_3 = 0x20080522


CAP_SETGID = 6
CAP_SETUID = 7
CAP_NET_ADMIN = 12
CAP_SYS_CHROOT = 18
CAP_SYS_ADMIN = 21


AT_FDCWD = -100


O_PATH = 0o10000000
O_CLOEXEC = 0o2000000


MS_NOSUID = 2
MS_NODEV = 4
MS_BIND = 4096
MS_REC = 16384
MS_PRIVATE = 262144
MS_SLAVE = 524288


MNT_DETACH = 2


EFD_SEMAPHORE = 0o0000001
EFD_CLOEXEC = 0o2000000
EFD_NONBLOCK = 0o0004000


SFD_CLOEXEC = 0o2000000
SFD_NONBLOCK = 0o0004000


SIG_BLOCK = 0
SIG_UNBLOCK = 1
SIG_SETMASK = 2


CLONE_NEWNS = 0x00020000
CLONE_NEWUSER = 0x10000000
CLONE_NEWPID = 0x20000000


POLLIN = 0x001


WNOHANG = 1

# path of the new root
base_path = None


def cap_to_mask0(x):
    return 1 << (x & 31)


def cap_to_mask1(x):
    return cap_to_mask0(x - 32)


REQUIRED_CAPS_1 = 0
REQUIRED_CAPS_0 = \
    cap_to_mask0(CAP_SETGID) | \
    cap_to_mask0(CAP_SETUID) | \
    cap_to_mask0(CAP_NET_ADMIN) | \
    cap_to_mask0(CAP_SYS_CHROOT) | \
    cap_to_mask0(CAP_SYS_ADMIN)


if platform.architecture()[0] == '64bit':
    NR_CLONE = 56
elif platform.architecture()[0] == '32bit':
    NR_CLONE = 120

if platform.architecture()[0] == '64bit':
    NR_PIVOT_ROOT = 155
elif platform.architecture()[0] == '32bit':
    NR_PIVOT_ROOT = 217


# structures
class User_Cap_Header(ctypes.Structure):
    _fields_ = [
        ("version", ctypes.c_uint32),
        ("pid", ctypes.c_int)]


class User_Cap_Data(ctypes.Structure):
    _fields_ = [
        ("effective0", ctypes.c_uint32),
        ("permitted0", ctypes.c_uint32),
        ("inheritable0", ctypes.c_uint32),
        ("effective1", ctypes.c_uint32),
        ("permitted1", ctypes.c_uint32),
        ("inheritable1", ctypes.c_uint32)]


class PollFd2(ctypes.Structure):
    _fields_ = [("fd0", ctypes.c_int),
                ("events0", ctypes.c_short),
                ("revents0", ctypes.c_short),
                ("fd1", ctypes.c_int),
                ("events1", ctypes.c_short),
                ("revents1", ctypes.c_short)]


def die(reason):
    if base_path:
        os.rmdir(base_path)
    tty.die(reason)


def get_cap_count():
    with open('/proc/sys/kernel/cap_last_cap') as f:
        return int(f.read())
    return -1


def eventfd(initval, flags):
    return libc.eventfd(ctypes.c_uint(initval),
                        ctypes.c_int(flags))


def waitpid(id, flags):
    status = ctypes.c_int(0)
    return libc.waitpid(ctypes.c_ulong(id),
                        ctypes.byref(status),
                        ctypes.c_int(flags))


def prctl(option, arg2, arg3, arg4, arg5):
    return libc.prctl(ctypes.c_int(option),
                      ctypes.c_ulong(arg2),
                      ctypes.c_ulong(arg3),
                      ctypes.c_ulong(arg4),
                      ctypes.c_ulong(arg5))


def pivot_syscall(new_root, old_root):
    clone = ctypes.CDLL(None).syscall
    return clone(NR_PIVOT_ROOT,
                 ctypes.c_char_p(new_root),
                 ctypes.c_char_p(old_root))


def clone_syscall(flags, stack):
    clone = ctypes.CDLL(None).syscall
    return clone(NR_CLONE,
                 ctypes.c_ulong(flags),
                 ctypes.c_void_p(stack))


def mount(source, dest, type, flags, data):
    return libc.mount(ctypes.c_char_p(source),
                      ctypes.c_char_p(dest),
                      ctypes.c_char_p(type),
                      ctypes.c_ulong(flags),
                      ctypes.c_void_p(data))


def umount(target, flags):
    return libc.umount2(ctypes.c_char_p(target), ctypes.c_int(flags))


def setfsuid(fsuid):
    """Set user identity used for filesystem checks. See setfsuid(2)."""
    libc.setfsuid(ctypes.c_int(fsuid))
    new_fsuid = libc.setfsuid(ctypes.c_int(fsuid))
    err = errno.EPERM if new_fsuid != fsuid else ctypes.get_errno()
    if err:
        raise OSError(err, os.strerror(err))
    return new_fsuid


def get_caps():
    header = User_Cap_Header()
    header.version = LINUX_CAPABILITY_VERSION_3
    header.pid = 0

    data = User_Cap_Data()
    if (libc.capget(ctypes.byref(header), ctypes.byref(data)) < 0):
        die("capset failed")
    return data


def prctl_caps(caps, do_cap_bounding, do_set_ambient):
    cap_count = get_cap_count()
    for cap in range(0, cap_count + 1):
        keep = False
        if cap < 32:
            if cap_to_mask0(cap) & caps[0]:
                keep = True
        else:
            if cap_to_mask1(cap) & caps[1]:
                keep = True

        if keep and do_set_ambient:
            result = prctl(PR_CAP_AMBIENT, PR_CAP_AMBIENT_RAISE, cap, 0, 0)
            if (result == -1):
                die("Error while setting ambient capability")
        if not keep and do_cap_bounding:
            result = prctl(PR_CAPBSET_DROP, cap, 0, 0, 0)
            if (result == -1):
                die("Error while dropping ambient capability")


def drop_cap_set(requested_caps=None):
    if requested_caps:
        prctl_caps(requested_caps, True, False)
    else:
        prctl_caps([0, 0], True, False)


def drop_all_caps(keep_requested_caps):
    if keep_requested_caps:
        return
    else:
        header = User_Cap_Header()
        header.version = LINUX_CAPABILITY_VERSION_3
        header.pid = 0

        data = User_Cap_Data()
        data.effective0 = 0
        data.permitted0 = 0
        data.inheritable0 = 0
        data.effective1 = 0
        data.permitted1 = 0
        data.inheritable1 = 0

        if libc.capset(ctypes.byref(header), ctypes.byref(data)) < 0:
            die('Could not drop caps')


def set_required_caps():
    header = User_Cap_Header()
    header.version = LINUX_CAPABILITY_VERSION_3
    header.pid = 0

    data = User_Cap_Data()
    data.effective0 = REQUIRED_CAPS_0
    data.permitted0 = REQUIRED_CAPS_0
    data.inheritable0 = 0
    data.effective1 = REQUIRED_CAPS_1
    data.permitted1 = REQUIRED_CAPS_1
    data.inheritable1 = 0
    if (libc.capset(ctypes.byref(header), ctypes.byref(data)) < 0):
        die("capset failed")


def die_with_parent():
    if prctl(PR_SET_PDEATHSIG, signal.SIGKILL, 0, 0, 0) != 0:
        die('Could not die with parent')


def drop_privileges(new_uid, keep_requested_caps):
    if os.getuid() == 0:
        os.setuid(new_uid)
    drop_all_caps(keep_requested_caps)


def block_sigchild():
    mask = ctypes.pointer(ctypes.c_ulong(0))
    libc.sigemptyset(mask)
    libc.sigaddset(mask, signal.SIGCHLD)
    if libc.sigprocmask(SIG_BLOCK, mask, ctypes.c_void_p(0)) < 0:
        die('sigprocmask')
    while (waitpid(-1, WNOHANG) > 0):
        pass


def check_privileges(real_uid):
    privileged = False
    euid = os.geteuid()

    caps = get_caps()
    if euid != real_uid:
        if euid == 0:
            privileged = True
        else:
            die("Unexpected user should be 0")

        if setfsuid(real_uid) < 0:
            die("Unable to set fsuid")

        new_fsuid = setfsuid(-1)
        if (new_fsuid != real_uid):
            die("Unable to set fsuid")

        drop_cap_set()
        set_required_caps()
    elif real_uid != 0 and (caps.permitted0 != 0 or caps.permitted1 != 0):
        die("Unexpected capabilities")
    elif real_uid == 0:
        privileged = True
    return privileged, caps


def create_dir(path, mode):
    try:
        os.mkdir(path, mode)
        return True
    except Exception:
        return False


def monitor_child(proc_fd, child_pid, base_path):
    while True:
        died_pid = waitpid(-1, WNOHANG)
        while died_pid > 0:
            if died_pid == child_pid:
                os.rmdir(base_path)
                sys.exit(0)
            died_pid = waitpid(-1, WNOHANG)


def create_file(path, mode):
    if os.path.exists(path):
        return 0

    fd = libc.creat(ctypes.c_char_p(path), ctypes.c_int(mode))
    if fd == -1:
        return -1

    libc.close(fd)
    return 0


def write_file_at(dir_fd, path, content):
    fd = libc.openat(dir_fd, ctypes.c_char_p(path),
                     ctypes.c_int(os.O_RDWR | O_CLOEXEC),
                     ctypes.c_int(0))
    if fd == -1:
        return -1

    if content:
        os.write(fd, content)

    libc.close(fd)
    return 0


def read_file_at(dir_fd, path):
    fd = libc.openat(dir_fd, path, O_CLOEXEC | os.O_RDONLY)
    if fd == -1:
        return None

    data = ""
    tmp = os.read(fd, 1)
    while tmp:
        data += tmp
        tmp = os.read(fd, 1)

    libc.close(fd)
    return data


def switch_to_user_with_privs(priv, caps):
    drop_cap_set()
    if not priv:
        return 0
    else:
        die('Program is not supposed to be root')


def read_overflow_ids():
    uid_data = read_file_at(AT_FDCWD, b'/proc/sys/kernel/overflowuid')
    if not uid_data:
        die('Could not read overflowuid')

    gid_data = read_file_at(AT_FDCWD, b'/proc/sys/kernel/overflowgid')
    if not gid_data:
        die('Could not read overflowuid')
    return int(uid_data), int(gid_data)


def write_uid_gid_map(proc_fd,
                      chroot_uid, parent_uid,
                      chroot_gid, parent_gid,
                      pid, deny_groups, map_root):
    if pid == -1:
        dir = b'self'

    dir_fd = libc.openat(proc_fd, ctypes.c_char_p(dir),
                         ctypes.c_int(os.O_RDONLY | O_PATH))
    if dir_fd < 0:
        die('could not open proc/self')

    if map_root and parent_uid != 0 and chroot_uid != 0:
        uid_map = "0 %s 1\n%d %d 1\n" % (overflow_uid, chroot_uid, parent_uid)
    else:
        uid_map = "%s %s 1\n" % (chroot_uid, parent_uid)
    gid_map = "%s %s 1\n" % (chroot_gid, parent_gid)

    if write_file_at(dir_fd, b'uid_map', uid_map.encode()) != 0:
        die('Error setting uid map')

    if deny_groups:
        if write_file_at(dir_fd, b'setgroups', b'deny\n') != 0:
            die('Error writing to setgroups')

    if write_file_at(dir_fd, b'gid_map', gid_map.encode()) != 0:
        die('Error setting gid map')


def setup_newroot(location):
    # Mount new home as /
    if mount(('/oldroot/%s' % location).encode(), b'/newroot/', None,
             MS_BIND | MS_REC, None) != 0:
        die('Could not mount home')

    # TODO maybe allow only a few files to be mounted
    if mount(b'/oldroot/dev', b'/newroot/dev', None,
             MS_BIND | MS_REC, None) != 0:
        die('Could not mount dev')

    if mount(b'/oldroot/sys', b'/newroot/sys', None,
             MS_BIND | MS_REC, None) != 0:
        die('Could not mount sys')

    if mount(b'/oldroot/proc', b'/newroot/proc', None,
             MS_BIND | MS_REC, None) != 0:
        die('Could not mount proc')


def user_chroot(location, command, arguments):
    """
    The command allows the use of chroot while being user.
    This is possible because, it creates a new namespace for the
    user, like unshare but allows to change the uid and gid, as well
    as mount bind files via the namespace.

    The implementation is based on bubblewrap:
    https://github.com/projectatomic/bubblewrap

    But is simplified to work with python, without the need
    for c modules. Therefore this implementation does not allow to
    create a pid or net newspace. It also maps dev, sys and proc automatically.
    """

    real_uid, real_gid = os.getuid(), os.getgid()
    chroot_uid, chroot_gid = real_uid, real_gid

    if real_uid == 0:
        die('User namespaces must be called without root privileges')

    priv, caps = check_privileges(real_uid)

    # dont let the process get any new privileges to avoid
    # utilization of setuid and setguid to become root or leave the jail
    if prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0:
        die('Could not set PR_SET_NO_NEW_PRIVS')

    # overflow_uid, overflow_gid = read_overflow_ids()

    # open the proc directory
    proc_fd = os.open('/proc', os.O_RDONLY | O_PATH)
    if proc_fd == -1:
        die('could not open proc')

    # check for execution path
    base_path = "/usr/run/%d/userchroot" % (real_uid)
    if (not create_dir(base_path, 755)):
        base_path = "/tmp/userchroot-%d" % (real_uid)
        if (not create_dir(base_path, 755)):
            die('Could not create mount root')

    child_event_fd = eventfd(0, EFD_CLOEXEC)
    if child_event_fd == -1:
        die('Could not create a child event file discriptor')

    # call clone manually to clone the program without
    # an extra function and predefined stack
    clone_flags = signal.SIGCHLD | CLONE_NEWNS | CLONE_NEWUSER
    pid = clone_syscall(clone_flags, None)
    if pid == -1:
        die('Could not create new namespace')

    # This gets executed by the initially called process
    if pid != 0:
        drop_privileges(chroot_uid, False)
        die_with_parent()

        # inform the child process after all privileges got
        # dropped to continue running
        val = ctypes.pointer(ctypes.c_ulong(1))
        if libc.write(child_event_fd, val, 8) < 0:
            die('Could not write to child event file discriptor')
        os.close(child_event_fd)
        monitor_child(proc_fd, pid, base_path)
        sys.exit(0)

    # wait for parent to drop privileges
    os.read(child_event_fd, 8)
    os.close(child_event_fd)

    # drop all privileges
    switch_to_user_with_privs(priv, caps)

    ns_uid, ns_gid = chroot_uid, chroot_gid

    # rewrite the mapping from the namespace id to the real user id
    write_uid_gid_map(proc_fd,
                      ns_uid, real_uid,
                      ns_gid, real_gid,
                      -1, True, False)

    # mount everything as slave to recive bind calls
    # but to avoid the propergation of bind calls
    if mount(None, b'/', None, MS_SLAVE | MS_REC, None) < 0:
        die('failed to mount /')

    # create a temporary file system mount as the / path for
    # all other mount calls
    if mount(b'', base_path.encode(), b'tmpfs',
             MS_NODEV | MS_NOSUID, None) != 0:
        die('failed to mount tmpfs')

    # change dir to new mounted base path
    if libc.chdir(ctypes.c_char_p(base_path.encode())) != 0:
        die('Could not change dir')

    # Create a second root to allow the user to mount something
    # at /
    if libc.mkdir(ctypes.c_char_p(b'newroot'), ctypes.c_uint32(0o755)) < 0:
        die('Could not create new root dir')

    # Create the old root path
    if libc.mkdir(ctypes.c_char_p(b'oldroot'), ctypes.c_uint32(0o755)) < 0:
        die('Could not create old root dir')

    # Switch the current root to old root
    if pivot_syscall(base_path.encode(), b'oldroot') != 0:
        die('Could not pivot root')

    # change to the root which contains oldroot and newroot
    if libc.chdir(ctypes.c_char_p(b'/')) != 0:
        die('Could not change to new root')

    # mount everything which isrequired to bootstrap an environment
    setup_newroot(location)

    # Set oldroot as private to allow to unmount in the current
    # namespace without unmouting oldroot in the parent namespace
    if mount(b'oldroot', b'oldroot', None, MS_REC | MS_PRIVATE, None) != 0:
        die('Could not mount oldroot')

    # Unmount the old root
    if umount(b'oldroot', MNT_DETACH) != 0:
        die('Could not unmount old root')

    if libc.chdir(ctypes.c_char_p(b'/newroot')) != 0:
        die('Could not change to new root')

    if libc.chroot(ctypes.c_char_p(b'/newroot')) != 0:
        die('Could not chroot into new root')

    if libc.chdir(ctypes.c_char_p(b'/')) != 0:
        die('Could not change to /')

    die_with_parent()

    # Execute the specified command with arguments
    # and convert them to char*[]
    if arguments:
        args = (ctypes.c_char_p * (len(arguments) + 1))()
        args[0] = ctypes.c_char_p(command.encode())
        for i in range(1, len(arguments)):
            args[i] = ctypes.c_char_p(arguments[i].encode())
    else:
        args = (ctypes.c_char_p * 1)()
        args[0] = ctypes.c_char_p(command.encode())

    if libc.execvp(ctypes.c_char_p(command.encode()), args) == -1:
        die('Could not start %s %s' % (command, arguments))


# example usage
# user_chroot('/home/spack/Documents/Spack-Test/', '/bin/bash', None)
