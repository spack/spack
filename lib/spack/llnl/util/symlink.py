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

is_windows = _platform == 'win32'

__win32_can_symlink__ = None


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

    if os.path.isdir(path):
        # try using a junction
        command = 'mklink /J "%s" "%s"' % (link, path)
    else:
        # try using a hard link
        command = 'mklink /H "%s" "%s"' % (link, path)

    _cmd(command)


def _win32_can_symlink():
    global __win32_can_symlink__
    if __win32_can_symlink__ is not None:
        return __win32_can_symlink__

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

    __win32_can_symlink__ = can_symlink_directories and can_symlink_files

    return __win32_can_symlink__


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


# Based on https://github.com/Erotemic/ubelt/blob/master/ubelt/util_cmd.py
def _cmd(command):
    import subprocess

    # Create a new process to execute the command
    def make_proc():
        # delay the creation of the process until we validate all args
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True,
                                universal_newlines=True, cwd=None, env=None)
        return proc

    proc = make_proc()
    (out, err) = proc.communicate()
    if proc.wait() != 0:
        raise OSError(str(err))
