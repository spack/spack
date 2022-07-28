# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import errno
import os
import shutil
import tempfile
from os.path import exists, join
from sys import platform as _platform

from llnl.util import lang

is_windows = _platform == 'win32'

if is_windows:
    from win32file import CreateHardLink


def symlink(real_path, link_path):
    """
    Create a symbolic link.

    On Windows, use junctions if os.symlink fails.
    """
    if not is_windows or _win32_can_symlink():
        link_path.symlink_to(real_path)
    else:
        try:
            # Try to use junctions
            _win32_junction(real_path, link_path)
        except OSError:
            # If all else fails, fall back to copying files
            shutil.copyfile(real_path, link_path)


def islink(path):
    return path.is_symlink() or _win32_is_junction(path)


# '_win32' functions based on
# https://github.com/Erotemic/ubelt/blob/master/ubelt/util_links.py
def _win32_junction(path, link):
    # junctions require absolute paths
    if not link.is_absolute():
        link = link.resolve()

    # os.symlink will fail if link exists, emulate the behavior here
    if exists(link):
        raise OSError(errno.EEXIST, 'File  exists: %s -> %s' % (link, path))

    if not path.is_absolute():
        parent = link.joinpath(os.pardir)
        path = parent.joinpath(path)
        path = path.resolve()

    CreateHardLink(link, path)


@lang.memoized
def _win32_can_symlink():
    tempdir = tempfile.mkdtemp()

    dpath = join(tempdir, 'dpath')
    fpath = join(tempdir, 'fpath.txt')

    dlink = join(tempdir, 'dlink')
    flink = join(tempdir, 'flink.txt')

    import llnl.util.filesystem as fs
    fs.touchp(fpath)

    try:
        dlink.symlink_to(dpath)
        can_symlink_directories = dlink.is_symlink()
    except OSError:
        can_symlink_directories = False

    try:
        flink.symlink_to(fpath)
        can_symlink_files = flink.is_symlink()
    except OSError:
        can_symlink_files = False

    # Cleanup the test directory
    shutil.rmtree(tempdir)

    return can_symlink_directories and can_symlink_files


def _win32_is_junction(path):
    """
    Determines if a path is a win32 junction
    """
    if path.is_symlink():
        return False

    if is_windows:
        import ctypes.wintypes

        GetFileAttributes = ctypes.windll.kernel32.GetFileAttributesW
        GetFileAttributes.argtypes = (ctypes.wintypes.LPWSTR,)
        GetFileAttributes.restype = ctypes.wintypes.DWORD

        INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF
        FILE_ATTRIBUTE_REPARSE_POINT = 0x400

        res = GetFileAttributes(path)
        return res != INVALID_FILE_ATTRIBUTES and \
            bool(res & FILE_ATTRIBUTE_REPARSE_POINT)

    return False
