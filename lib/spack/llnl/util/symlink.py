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

from spack.util.executable import Executable

is_windows = _platform == 'win32'


def symlink(real_path, link_path):
    """
    Create a symbolic link.

    On Windows, use junctions if os.symlink fails.
    """
    if not is_windows or _win32_can_symlink():
        os.symlink(real_path, link_path)
    else:
        try:
            # Try to use junctions
            _win32_junction(real_path, link_path)
        except OSError:
            # If all else fails, fall back to copying files
            shutil.copyfile(real_path, link_path)


def islink(path):
    return os.path.islink(path) or _win32_is_junction(path)


# '_win32' functions based on
# https://github.com/Erotemic/ubelt/blob/master/ubelt/util_links.py
def _win32_junction(path, link):
    # junctions require absolute paths
    if not os.path.isabs(link):
        link = os.path.abspath(link)

    # os.symlink will fail if link exists, emulate the behavior here
    if exists(link):
        raise OSError(errno.EEXIST, 'File  exists: %s -> %s' % (link, path))

    if not os.path.isabs(path):
        parent = os.path.join(link, os.pardir)
        path = os.path.join(parent, path)
        path = os.path.abspath(path)

    command = "mklink"
    default_args = [link, path]
    if os.path.isdir(path):
        # try using a junction
        default_args.insert(0, '/J')
    else:
        # try using a hard link
        default_args.insert(0, '/H')

    Executable(command)(*default_args)


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
