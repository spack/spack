# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import ctypes
import os
from typing import Optional

import llnl.util.filesystem as fs
from llnl.util.symlink import symlink

# Magic numbers from linux headers
RENAME_EXCHANGE = 2
AT_FDCWD = -100

libc: Optional[ctypes.CDLL] = None
try:
    # CDLL(None) returns the python process
    # python links against libc, so we can treat this as a libc handle
    # we could also use CDLL("libc.so.6") but this is (irrelevantly) more future proof
    libc = ctypes.CDLL(None)
except BaseException:
    pass


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


def atomic_update_renameat2(src, dest):
    # Ensure a directory that is a symlink will not be read as symlink in libc
    src = src.rstrip(os.path.sep)
    dest = dest.rstrip(os.path.sep)

    dest_exists = os.path.lexists(dest)
    if not dest_exists:
        fs.touch(dest)
    try:
        rc = libc.renameat2(AT_FDCWD, src.encode(), AT_FDCWD, dest.encode(), RENAME_EXCHANGE)
        if rc:
            raise OSError(f"renameat2 failed to exchange {src} and {dest}")
        if not dest_exists:
            os.unlink(src)
    except (OSError, IOError):
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
