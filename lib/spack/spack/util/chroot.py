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
import llnl.util.tty as tty
from itertools import product
from spack.util.executable import which

EXECUTABLES = [
    # unix tools
    'env',
    'git',
    'tar',
    'bash',
    'curl',
    'make',
    'uniq',
    'tr',
    'cat',
    'expr',
    'awk',
    'find',
    'diff',
    'base32',
    'base64',
    'printf',
    'cmp',
    'msgfmt',
    'xgettext',
    'msgmerge',
    'unzip',
    'zip',
    'id',
    'xz',
    'file',
    'patch',
    'dirname',
    'sh',
    'cut',
    'head',
    'wc',
    'seq',
    'sort',
    'comm',
    'man',
    'md5sum',
    'basename',
    'test',
    'install',
    'grep',

    # lsb_release (for os detection)
    'lsb_release',
    'apt-cache', #for lsb_release
    'dpkg-query', #for lsb_release

    #gcc
    'gcc',
    'g++',

    #fortran
    ('gfortran', False), #not required

    #python
    'python',
    'python3',

    #perl
    'perl',

    #binutils
    'addr2line',
    'ar',
    'as',
    'c++filt',
    'dwp',
    'elfedit',
    'gold',
    'gprof',
    'ld',
    'ld.bfd',
    'ld.gold',
    'nm',
    'objcopy',
    'objdump',
    'ranlib',
    'readelf',
    'size',
    'strings',
    'strip',

    #debug
    'ls',
    'tail',
    'mkdir',
]

DEFAULT_PATHS = [
    '/bin',
    '/dev',
    '/etc',
    '/lib/init',
    '/lib/lsb',
    '/lib/systemd',
    '/lib/terminfo',
    '/lib/udev',
    '/lib/x86_64-linux-gnu',
    '/lib64',
    '/proc',
    '/run',
    '/sys',

    #gcc and ld specific
    '/usr/lib/gcc/x86_64-linux-gnu',
    '/usr/lib/x86_64-linux-gnu/libisl.so.15',
    '/usr/lib/x86_64-linux-gnu/libmpc.so.3',
    '/usr/lib/x86_64-linux-gnu/libmpfr.so.4',
    '/usr/lib/x86_64-linux-gnu/crt1.o',
    '/usr/lib/x86_64-linux-gnu/crti.o',
    '/usr/lib/x86_64-linux-gnu/crtn.o',
    '/usr/lib/x86_64-linux-gnu/libquadmath.so.0',
    '/usr/lib/x86_64-linux-gnu/libgfortran.so.3',
    '/usr/lib/x86_64-linux-gnu/libgfortran.so.3.0.0',

    # lib c libraries
    '/usr/lib/x86_64-linux-gnu/libc.a',
    '/usr/lib/x86_64-linux-gnu/libc.so',
    '/usr/lib/x86_64-linux-gnu/libc_nonshared.a',

    # lib g libraries
    '/usr/lib/x86_64-linux-gnu/libg.a',

    # lib util libraries
    '/usr/lib/x86_64-linux-gnu/libutil.a',
    '/usr/lib/x86_64-linux-gnu/libutil.so',

    # lib m libraries
    '/usr/lib/x86_64-linux-gnu/libm.a',
    '/usr/lib/x86_64-linux-gnu/libm.so',
    '/usr/lib/x86_64-linux-gnu/libmvec_nonshared.a',

    # pthread libraries
    '/usr/lib/x86_64-linux-gnu/libpthread.a',
    '/usr/lib/x86_64-linux-gnu/libpthread.so',
    '/usr/lib/x86_64-linux-gnu/libpthread_nonshared.a',

    # rt libraries
    '/usr/lib/x86_64-linux-gnu/librt.a',
    '/usr/lib/x86_64-linux-gnu/librt.so',

    # dl libraries
    '/usr/lib/x86_64-linux-gnu/libdl.a',
    '/usr/lib/x86_64-linux-gnu/libdl.so',

    # libresolve libraries
    '/usr/lib/x86_64-linux-gnu/libresolv.a',
    '/usr/lib/x86_64-linux-gnu/libresolv.so',

    #lib rpc libraries
    '/usr/lib/x86_64-linux-gnu/librpcsvc.a',

    # linux headers
    '/usr/include/linux',
    '/usr/include/net',
    '/usr/include/arpa',
    '/usr/include/netinet',
    '/usr/include/drm',
    '/usr/include/X11',
    '/usr/include/nfs',
    '/usr/include/netash',
    '/usr/include/netatalk',
    '/usr/include/sound',
    '/usr/include/video',
    '/usr/include/xorg',
    '/usr/include/rpc',
    '/usr/include/netpacket',
    '/usr/include/asm-generic',
    '/usr/include/x86_64-linux-gnu',
    #'/usr/include/x86_64-linux-gnu/sys',
    #'/usr/include/x86_64-linux-gnu/asm',
    #'/usr/include/x86_64-linux-gnu/bits',
    #'/usr/include/x86_64-linux-gnu/gnu',
    #'/usr/include/x86_64-linux-gnu/c++',

    # std headers
    '/usr/include/c++',

    # libc headers
    '/usr/include/aio.h',
    '/usr/include/aliases.h',
    '/usr/include/alloca.h',
    '/usr/include/ar.h',
    '/usr/include/argp.h',
    '/usr/include/argz.h',
    '/usr/include/assert.h',
    '/usr/include/autosprintf.h',
    '/usr/include/byteswap.h',
    '/usr/include/complex.h',
    '/usr/include/cpio.h',
    '/usr/include/ctype.h',
    '/usr/include/dirent.h',
    '/usr/include/dlfcn.h',
    '/usr/include/elf.h',
    '/usr/include/endian.h',
    '/usr/include/envz.h',
    '/usr/include/err.h',
    '/usr/include/errno.h',
    '/usr/include/error.h',
    '/usr/include/execinfo.h',
    '/usr/include/fcntl.h',
    '/usr/include/features.h',
    '/usr/include/fenv.h',
    '/usr/include/fmtmsg.h',
    '/usr/include/fnmatch.h',
    '/usr/include/fts.h',
    '/usr/include/ftw.h',
    '/usr/include/_G_config.h',
    '/usr/include/gconv.h',
    '/usr/include/getopt.h',
    '/usr/include/glob.h',
    '/usr/include/gnu-versions.h',
    '/usr/include/grp.h',
    '/usr/include/gshadow.h',
    '/usr/include/iconv.h',
    '/usr/include/ifaddrs.h',
    '/usr/include/inttypes.h',
    '/usr/include/langinfo.h',
    '/usr/include/lastlog.h',
    '/usr/include/libgen.h',
    #'/usr/include/libintl.h',
    '/usr/include/libio.h',
    '/usr/include/limits.h',
    '/usr/include/link.h',
    '/usr/include/locale.h',
    '/usr/include/malloc.h',
    '/usr/include/math.h',
    '/usr/include/mcheck.h',
    '/usr/include/memory.h',
    '/usr/include/mntent.h',
    '/usr/include/monetary.h',
    '/usr/include/mqueue.h',
    '/usr/include/netdb.h',
    '/usr/include/nl_types.h',
    '/usr/include/nss.h',
    '/usr/include/obstack.h',
    '/usr/include/paths.h',
    '/usr/include/poll.h',
    '/usr/include/printf.h',
    '/usr/include/pthread.h',
    '/usr/include/pty.h',
    '/usr/include/pwd.h',
    '/usr/include/re_comp.h',
    '/usr/include/regex.h',
    '/usr/include/regexp.h',
    '/usr/include/resolv.h',
    '/usr/include/sched.h',
    '/usr/include/search.h',
    '/usr/include/semaphore.h',
    '/usr/include/setjmp.h',
    '/usr/include/sgtty.h',
    '/usr/include/shadow.h',
    '/usr/include/spawn.h',
    '/usr/include/signal.h',
    '/usr/include/stab.h',
    '/usr/include/stdc-predef.h',
    '/usr/include/stdint.h',
    '/usr/include/stdio.h',
    '/usr/include/stdio_ext.h',
    '/usr/include/stdlib.h',
    '/usr/include/string.h',
    '/usr/include/strings.h',
    '/usr/include/stropts.h',
    '/usr/include/sudo_plugin.h',
    '/usr/include/syscall.h',
    '/usr/include/sysexits.h',
    '/usr/include/syslog.h',
    '/usr/include/tar.h',
    '/usr/include/termio.h',
    '/usr/include/termios.h',
    '/usr/include/tgmath.h',
    '/usr/include/thread_db.h',
    '/usr/include/time.h',
    '/usr/include/ttyent.h',
    '/usr/include/uchar.h',
    '/usr/include/ucontext.h',
    '/usr/include/ulimit.h',
    '/usr/include/unistd.h',
    '/usr/include/ustat.h',
    '/usr/include/utime.h',
    '/usr/include/utmp.h',
    '/usr/include/utmpx.h',
    '/usr/include/values.h',
    '/usr/include/wait.h',
    '/usr/include/wchar.h',
    '/usr/include/wctype.h',
    '/usr/include/wordexp.h',
    '/usr/include/xlocale.h',

    #git
    '/usr/share/git-core',

    #distinfo
    '/usr/share/distro-info',

    #man files
    '/usr/share/man',

    #perl
    '/etc/perl',
    '/usr/lib/perl5',
    '/usr/lib/x86_64-linux-gnu/perl5',
    '/usr/lib/x86_64-linux-gnu/perl',
    '/usr/lib/x86_64-linux-gnu/perl-base',
    '/usr/share/perl5',
    '/usr/share/perl',

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
        if type(exe) is tuple:
            executable = spack.util.executable.which(exe[0], required=exe[1])
        else:
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

    os.system("sudo mount --bind %s %s" % (realpath, chrootpath))

def umount_bind_path(chrootpath):
    os.system("sudo umount -l %s" % (chrootpath))

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
    os.system("sudo chroot --userspec=%s:%s %s /home/spack/bin/spack %s"
        % (username, group, spack.spack_bootstrap_root, ' '.join(sys.argv[1:])))

    if not existed:
        remove_chroot_enviroment(spack.spack_bootstrap_root)
