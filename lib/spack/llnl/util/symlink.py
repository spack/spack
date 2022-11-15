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

is_windows = _platform == "win32"

if is_windows:
    import subprocess

    from win32file import CreateHardLink


def symlink(real_path, link_path):
    """
    Try to create a symbolic link.

    On non-Windows and Windows with System Administrator
    privleges this will be a symbolic link. On Windows
    without privledges the link will be a junction for a
    directory and a hardlink for a file. On Windows the
    definitions are:

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
    if not is_windows or os_can_symlink():
        os.symlink(real_path, link_path)
    else:
        # Here (on windows and not able to use os.symlink()
        # We next try junction for a directory or hardlink
        # for a file. The fallback is to make a copy.
        if not os.path.isabs(link_path):
            link_path = os.path.abspath(link_path)
        # os.symlink will fail if link exists, emulate the behavior here
        if exists(link_path):
            raise OSError(errno.EEXIST, "Link exists: %s"
                % (link_path))
        else:
            mkNonsymbolicLink(real_path, link_path)
            if not os.path.exists(link_path):
                print("[symlink] Fallback to copying file.")
                shutil.copyfile(real_path, link_path)


def islink(path):
    return os.path.islink(path) or isjunction(path) or ishardlink(path)


def mkNonsymbolicLink(path, link):
    if os.path.isdir(path):
        print("[symlink] Making a junction for directory")
        try:
            cmd = ["cmd", "/C", "mklink", "/J", link, path]
            result = subprocess.check_output(cmd).decode()
            print("[symlink] Result: " + result)
            if "Junction created" not in result:
                raise OSError(errno.EEXIST, "Link exists: %s" % (link))
        except subprocess.CalledProcessError as e:
            print("Junction failed with error: " + str(e))
    if os.path.isfile(path):
        print("[symlink] Calling CreateHardLink(" + link + "," + path + ")")
        CreateHardLink(link, path)


@lang.memoized
def os_can_symlink():
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


def ishardlink(path):
    """
    Determines if a path is a windows hardlink
    """
    if not is_windows:
        return False

    if os.path.islink(path):
        return False

    try:
        cmd = ["fsutil", "hardlink", "list", path]
        ret = subprocess.check_output(cmd)
        lines = ret.decode().splitlines()
        # We expect output of fsutil call to have at least two lines
        # if the path is a hardlink
        if len(lines) == 1:
            print("[symlink] Path not hardlink")
            return False
        elif len(lines) > 1:
            print("[symlink] Path is hardlink")
            return True
        else:
            print("[symlink] Can't determine if path is a hardlink.")
            return False
    except subprocess.CalledProcessError as e:
        print("[symlink] Check on hardlink failed with error: " + str(e))
        return False


def isjunction(path):
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

