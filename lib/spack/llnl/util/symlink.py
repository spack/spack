# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import errno
import os
import shutil
import sys
import tempfile
from pathlib import Path

from llnl.util import lang

if sys.platform == "win32":
    from win32file import CreateHardLink


def symlink(real_path, link_path):
    """
    Create a symbolic link.

    On Windows, use junctions if os.symlink fails.
    """
    if sys.platform != "win32":
        os.symlink(real_path, link_path)
    elif _win32_can_symlink():
        # Windows requires target_is_directory=True when the target is a dir.
        os.symlink(real_path, link_path, target_is_directory=os.path.isdir(real_path))
    else:
        try:
            # Try to use junctions
            _win32_junction(real_path, link_path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                # EEXIST error indicates that file we're trying to "link"
                # is already present, don't bother trying to copy which will also fail
                # just raise
                raise
            else:
                # If all else fails, fall back to copying files
                shutil.copyfile(real_path, link_path)


def islink(path):
    return Path(path).is_link() or _win32_is_junction(path)


# '_win32' functions based on
# https://github.com/Erotemic/ubelt/blob/master/ubelt/util_links.py
def _win32_junction(path, link):
    path = Path(path)
    link = Path(link)
    # junctions require absolute paths
    link = link.absolute()

    # os.symlink will fail if link exists, emulate the behavior here
    if link.exists():
        raise OSError(errno.EEXIST, "File  exists: %s -> %s" % (str(link), str(path)))

    if not path.is_absolute():
        parent = link / os.pardir
        path = parent / path
        path = path.absolute()

    CreateHardLink(link, path)


@lang.memoized
def _win32_can_symlink():
    tempdir = Path(tempfile.mkdtemp())

    dpath = tempdir / "dpath"
    fpath = tempdir / "fpath.txt"

    dlink = tempdir / "dlink"
    flink = tempdir / "flink.txt"

    import llnl.util.filesystem as fs

    fs.touchp(fpath)

    try:
        os.symlink(dpath, dlink)
        can_symlink_directories = dlink.is_symlink()
    except OSError:
        can_symlink_directories = False

    try:
        os.symlink(fpath, flink)
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
    if Path(path).is_symlink():
        return False

    if sys.platform == "win32":
        import ctypes.wintypes

        GetFileAttributes = ctypes.windll.kernel32.GetFileAttributesW
        GetFileAttributes.argtypes = (ctypes.wintypes.LPWSTR,)
        GetFileAttributes.restype = ctypes.wintypes.DWORD

        INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF
        FILE_ATTRIBUTE_REPARSE_POINT = 0x400

        res = GetFileAttributes(path)
        return res != INVALID_FILE_ATTRIBUTES and bool(res & FILE_ATTRIBUTE_REPARSE_POINT)

    return False
