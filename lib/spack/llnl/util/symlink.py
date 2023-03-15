# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import errno
import os
import shutil
import tempfile
from sys import platform as _platform

from spack.error import SpackError
from llnl.util import lang, tty

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
    if not is_windows or windows_can_symlink():
        os.symlink(real_path, link_path,
                   target_is_directory=os.path.isdir(real_path))
    else:
        # If windows can not make normal symbolic links
        # we try junction for a directory or hardlink
        # for a file.
        if not os.path.isabs(link_path):
            link_path = os.path.abspath(link_path)
        # os.symlink will fail if link exists, emulate the behavior here
        if os.path.exists(link_path):
            raise OSError(errno.EEXIST, "Link exists: %s" % link_path)
        else:
            windows_create_link(real_path, link_path)
            if not os.path.exists(link_path):
                raise OSError("Failed to create link: %s" % link_path)


def islink(path: str) -> bool:
    """ Override os.islink to give correct answer for spack logic.

    For Non-Windows: a link can be determined with the os.path.islink method.
    Windows-only methods will return false for other operating systems.

    For Windows: spack considers symlinks, hard links, and junctions to
    all be links, so if any of those are True, return True.

    Args:
        path (str): path to check if it is a link.

    Returns:
         bool - whether the path is any kind link or not.
    """
    try:
        return any([
            os.path.islink(path),
            windows_is_junction(path),
            windows_is_hardlink(path),
        ])
    except Exception as e:
        raise SymlinkError('Could not determine if given path is a link') from e


def windows_is_hardlink(path: str) -> bool:
    """ Determines if a path is a windows hard link. This is accomplished
    by looking at the number of links using os.stat. A non-hard-linked file
    will have a st_nlink value of 1, whereas a hard link will have a value
    larger than 1. Note that both the original and hard-linked file will
    return True because they share the same inode.

    Args:
        path (str): Windows path to check for a hard link

    Returns:
         bool - Whether the path is a hard link or not.
    """
    if not is_windows or os.path.islink(path) or not os.path.exists(path):
        return False

    try:
        return os.stat(path).st_nlink > 1
    except Exception as e:
        raise SymlinkError('Could not determine if path is a hard link') from e


def windows_is_junction(path) -> bool:
    """ Determines if a path is a windows junction. A junction can be
    determined using a bitwise AND operation between the file's
    attribute bitmask and the known junction bitmask (0x400).

    Args:
        path (str): A non-file path

    Returns:
        bool - whether the path is a junction or not.
    """
    if not is_windows or os.path.islink(path) or os.path.isfile(path):
        return False

    import ctypes.wintypes

    get_file_attributes = ctypes.windll.kernel32.GetFileAttributesW
    get_file_attributes.argtypes = (ctypes.wintypes.LPWSTR,)
    get_file_attributes.restype = ctypes.wintypes.DWORD

    invalid_file_attributes: hex = 0xFFFFFFFF
    reparse_point: hex = 0x400
    file_attr: hex = get_file_attributes(path)

    if file_attr == invalid_file_attributes:
        return False

    return file_attr & reparse_point > 0


@lang.memoized
def windows_can_symlink():
    """
    Determines if windows is able to make a symlink depending on
    the system configuration and the level of the user's permissions.
    """
    if not is_windows:
        tty.warn("[symlink] window_can_symlink called on non-windows")
        return False

    tempdir = tempfile.mkdtemp()

    dpath = os.path.join(tempdir, "dpath")
    fpath = os.path.join(tempdir, "fpath.txt")

    dlink = os.path.join(tempdir, "dlink")
    flink = os.path.join(tempdir, "flink.txt")

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


def windows_create_link(path, link):
    """
    Attempts to create a Hard Link or Junction as an alternative
    to a symbolic link. This is called when symbolic links cannot
    be created.
    """
    if os.path.isdir(path):
        try:
            cmd = ["cmd", "/C", "mklink", "/J", link, path]
            proc = subprocess.run(cmd, capture_output=True)
            if proc.returncode != 0:
                # TODO: How do we know that this only happens if the
                #  junction already exists?
                raise OSError(errno.EEXIST, "Junction exists: %s" % link)
        except subprocess.CalledProcessError as e:
            tty.error("[symlink] Junction {} not created for directory {}. "
                      "error was: {}".format(link, path, str(e)))
    if os.path.isfile(path):
        tty.warn("[symlink] Junction fallback to create HardLink {} for "
                 "file {}".format(link, path))
        CreateHardLink(link, path)


class SymlinkError(SpackError):
    ...
