# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import errno
import os
import shutil
import tempfile
from os.path import exists, join
from sys import platform as _platform

import llnl.util.tty as console
from llnl.util import lang

is_windows = _platform == "win32"

if is_windows:
    import subprocess

    from win32file import CreateHardLink


def symlink(real_path, link_path):
    """
    Try to create a symbolic link.

    On non-Windows and Windows with System Administrator
    privleges this will be a normal symbolic link via
    os.symlink.

    On Windows without privledges the link will be a
    junction for a directory and a hardlink for a file.
    On Windows the various link types are:

    Symbolic Link: A link to a file or directory on the
    same or different volume (drive letter) or even to
    a remote file or directory (using UNC in its path).
    Need System Administrator privileges to make these.

    Hard Link: A link to a file on the same volume (drive
    letter) only. Every file (file's data) has at least 1
    hard link (file's name). But when this method creates
    a new hard link there will be 2. Deleting all hard
    links effectively deletes the file. Don't need System
    Administrator privileges.

    Junction (sometimes called soft link): A link to a
    directory on the same or different volume (drive
    letter) but not to a remote directory. Don't need
    System Administrator privileges.
    """
    if not is_windows:
        return os.symlink(real_path, link_path)

    # If we get here, we are on Windows
    if windows_can_symlink():
        # Windows requires target_is_directory=True when
        # the target is a dir.
        return os.symlink(real_path, link_path, target_is_directory=os.path.isdir(real_path))
    else:
        # If windows can not make normal symbolic links
        # we try junction for a directory or hardlink
        # for a file.
        if not os.path.isabs(link_path):
            link_path = os.path.abspath(link_path)
        # os.symlink will fail if link exists, emulate the behavior here
        if exists(link_path):
            raise OSError(errno.EEXIST, "Link exists: %s" % (link_path))
        else:
            windows_non_symlink(real_path, link_path)
            if not os.path.exists(link_path):
                raise OSError("Failed to create link: %s" % (link_path))


def islink(path):
    """
    Override os.islink to give correct answer for spack logic
    """
    if not is_windows:
        return os.path.islink(path)

    if windows_can_symlink():
        return os.path.islink(path)

    return windows_is_junction(path) or windows_is_hardlink(path)


def windows_is_hardlink(path):
    """
    Determines if a path is a windows hardlink
    """
    if not is_windows or os.path.islink(path) or not os.path.exists(path):
        return False

    try:
        cmd = ["fsutil", "hardlink", "list", path]
        ret = subprocess.check_output(cmd)
        lines = ret.decode().splitlines()
        # We expect output of fsutil call to have at least
        # two lines if the path is a hardlink
        if len(lines) == 1:
            return False
        elif len(lines) > 1:
            return True
        else:
            console.msg("[symlink] Cannot determine if hardlink. Returning false.")
            return False
    except subprocess.CalledProcessError as e:
        console.msg("[symlink] Check on hardlink failed with error: " + str(e))
        return False


def windows_is_junction(path):
    """
    Determines if a path is a windows junction.
    """
    if not is_windows:
        return False

    if os.path.islink(path):
        return False

    import ctypes.wintypes

    GetFileAttributes = ctypes.windll.kernel32.GetFileAttributesW
    GetFileAttributes.argtypes = (ctypes.wintypes.LPWSTR,)
    GetFileAttributes.restype = ctypes.wintypes.DWORD

    INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF
    FILE_ATTRIBUTE_REPARSE_POINT = 0x400
    res = GetFileAttributes(path)
    return res != INVALID_FILE_ATTRIBUTES and bool(res & FILE_ATTRIBUTE_REPARSE_POINT)


@lang.memoized
def windows_can_symlink():
    """
    Determines if windows is able to make a symlink depending on
    the system configuration and the level of the user's permissions.
    """
    if not is_windows:
        console.msg("[symlink] WARNING: window_can_symlink called on non-windows")
        return False

    tempdir = tempfile.mkdtemp()

    dpath = join(tempdir, "dpath")
    fpath = join(tempdir, "fpath.txt")

    dlink = join(tempdir, "dlink")
    flink = join(tempdir, "flink.txt")

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


def windows_non_symlink(path, link):
    """
    Attempts to create a Hard Link or Junction as an alternative
    to a symbolic link. This is called when symbolic links cannot
    be created.
    """
    if os.path.isdir(path):
        try:
            cmd = ["cmd", "/C", "mklink", "/J", link, path]
            result = subprocess.check_output(cmd).decode()
            if "Junction created" not in result:
                raise OSError(errno.EEXIST, "Junction exists: %s" % (link))
        except subprocess.CalledProcessError as e:
            console.msg(
                "[symlink] Junction {} not created for directory "
                "{}. error was {}".format(link, path, str(e))
            )
    if os.path.isfile(path):
        print("[symlink] Calling CreateHardLink(" + link + "," + path + ")")
        console.msg(
            "[symlink] Junction fallback to create HardLink {} for file {}".format(link, path)
        )
        CreateHardLink(link, path)
