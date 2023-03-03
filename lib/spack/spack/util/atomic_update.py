# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from contextlib import contextmanager

import llnl.util.filesystem as fs
from llnl.util.symlink import symlink

try:
    from ctypes import CDLL

    libc = CDLL("/lib64/libc.so.6", 0x04)  # 0x04 is RTLD_NOLOAD
except BaseException:
    libc = None


def use_renameat2():
    return hasattr(libc, "renameat2")


def atomic_update(oldpath, newpath):
    """
    atomically update newpath to contain the information at oldpath

    on linux systems supporting renameat2, the paths are swapped.
    on other systems, oldpath is not affected but all paths are abstracted
    by a symlink to allow for atomic updates.
    """
    if use_renameat2():
        return atomic_update_renameat2(oldpath, newpath)
    else:
        return atomic_update_symlink(oldpath, newpath)


@contextmanager
def open_safely(path):
    fd = os.open(path, os.O_CLOEXEC | os.O_PATH)
    try:
        yield fd
    finally:
        os.close(fd)


def atomic_update_renameat2(src, dest):
    dest_exists = os.path.exists(dest)
    if not dest_exists:
        fs.touch(dest)
    with open_safely(src) as srcfd:
        with open_safely(dest) as destfd:
            try:
                libc.renameat2(
                    srcfd, src.encode(), destfd, dest.encode(), 2
                )  # 2 is RENAME_EXCHANGE
                if not dest_exists:
                    os.unlink(src)
            except Exception:
                if not dest_exists:
                    os.unlink(dest)
                # Some filesystems don't support this
                # fail over to symlink method
                atomic_update_symlink(src, dest)


def atomic_update_symlink(src, dest):
    # Create temporary symlink to point to src
    tmp_symlink_name = os.path.join(os.path.dirname(dest), "._tmp_symlink")
    if os.path.exists(tmp_symlink_name):
        os.unlink(tmp_symlink_name)
    symlink(src, tmp_symlink_name)

    # atomically mv the symlink to destpath (still points to srcpath)
    try:
        fs.rename(tmp_symlink_name, dest)
    except Exception:
        os.unlink(tmp_symlink_name)
        raise
