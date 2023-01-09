# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import ctypes.wintypes
import errno
import os
import os.path
import shutil
import tempfile

import win32file

from ..lang import memoized


# '_win32' functions based on
# https://github.com/Erotemic/ubelt/blob/master/ubelt/util_links.py
def _win32_junction(path, link):
    # junctions require absolute paths
    if not os.path.isabs(link):
        link = os.path.abspath(link)

    # os.symlink will fail if link exists, emulate the behavior here
    if os.path.exists(link):
        raise OSError(errno.EEXIST, f"File  exists: {link} -> {path}")

    if not os.path.isabs(path):
        parent = os.path.join(link, os.pardir)
        path = os.path.join(parent, path)
        path = os.path.abspath(path)

    win32file.CreateHardLink(link, path)


@memoized
def _win32_can_symlink():
    from ..filesystem import touchp

    tempdir = tempfile.mkdtemp()

    dpath = os.path.join(tempdir, "dpath")
    fpath = os.path.join(tempdir, "fpath.txt")

    dlink = os.path.join(tempdir, "dlink")
    flink = os.path.join(tempdir, "flink.txt")

    touchp(fpath)

    try:
        os.symlink(dpath, dlink)
        can_symlink_directories = os.path.islink(dlink)
    except OSError:
        can_symlink_directories = False

    try:
        os.symlink(fpath, flink)
        can_symlink_files = os.path.islink(flink)
    except OSError:
        can_symlink_files = False

    # Cleanup the test directory
    shutil.rmtree(tempdir)

    return can_symlink_directories and can_symlink_files


def _win32_is_junction(path):
    """
    Determines if a path is a win32 junction
    """
    if os.path.islink(path):
        return False

    GetFileAttributes = ctypes.windll.kernel32.GetFileAttributesW
    GetFileAttributes.argtypes = (ctypes.wintypes.LPWSTR,)
    GetFileAttributes.restype = ctypes.wintypes.DWORD

    INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF
    FILE_ATTRIBUTE_REPARSE_POINT = 0x400

    res = GetFileAttributes(path)
    return res != INVALID_FILE_ATTRIBUTES and bool(res & FILE_ATTRIBUTE_REPARSE_POINT)


def symlink(real_path, link_path):
    """Create a symbolic link.

    On Windows, use junctions if os.symlink fails.
    """
    if _win32_can_symlink():
        # Windows requires target_is_directory=True when the target is a dir.
        os.symlink(real_path, link_path, target_is_directory=os.path.isdir(real_path))
    else:
        try:
            # Try to use junctions
            _win32_junction(real_path, link_path)
        except OSError:
            # If all else fails, fall back to copying files
            shutil.copyfile(real_path, link_path)


def islink(path):
    return os.path.islink(path) or _win32_is_junction(path)
