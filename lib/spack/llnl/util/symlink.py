# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
import sys
import tempfile

from llnl.util import lang, tty

from spack.error import SpackError

if sys.platform == "win32":
    from win32file import CreateHardLink


def symlink(source_path: str, link_path: str):
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

    Junction: A link to a directory on the same or different
    volume (drive letter) but not to a remote directory. Don't
    need System Administrator privileges.
    """
    # Perform basic checks to make sure symlinking will succeed
    if os.path.exists(link_path):
        raise SymlinkError(f"Link path ({link_path}) already exists. Cannot create link.")

    # Create the symlink
    if sys.platform == "win32" and not _windows_can_symlink():
        _windows_create_link(source_path, link_path)
    else:
        try:
            os.symlink(source_path, link_path, target_is_directory=os.path.isdir(source_path))
        except Exception as e:
            raise SymlinkError("An exception occurred while creating symlink") from e

    # Redundancy check to make sure the link created successfully
    if os.path.lexists(link_path):
        if not os.path.exists(link_path):
            # This is a broken link.
            raise SymlinkError(
                f"Broken link does not point to the source path ({source_path}).",
                long_message="This can be caused by the source path not being relative to "
                             "either the link's parent directory or the current working directory."
            )
    else:
        raise SymlinkError('Link does not exist after symlink methods finished.')


def islink(path: str) -> bool:
    """Override os.islink to give correct answer for spack logic.

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
        return any([os.path.islink(path), _windows_is_junction(path), _windows_is_hardlink(path)])
    except Exception as e:
        raise SymlinkError("Could not determine if given path is a link") from e


def _windows_is_hardlink(path: str) -> bool:
    """Determines if a path is a windows hard link. This is accomplished
    by looking at the number of links using os.stat. A non-hard-linked file
    will have a st_nlink value of 1, whereas a hard link will have a value
    larger than 1. Note that both the original and hard-linked file will
    return True because they share the same inode.

    Args:
        path (str): Windows path to check for a hard link

    Returns:
         bool - Whether the path is a hard link or not.
    """
    if sys.platform != "win32" or os.path.islink(path) or not os.path.exists(path):
        return False

    try:
        return os.stat(path).st_nlink > 1
    except Exception as e:
        raise SymlinkError("Could not determine if path is a hard link") from e


def _windows_is_junction(path: str) -> bool:
    """Determines if a path is a windows junction. A junction can be
    determined using a bitwise AND operation between the file's
    attribute bitmask and the known junction bitmask (0x400).

    Args:
        path (str): A non-file path

    Returns:
        bool - whether the path is a junction or not.
    """
    if sys.platform != "win32" or os.path.islink(path) or os.path.isfile(path):
        return False

    import ctypes.wintypes

    get_file_attributes = ctypes.windll.kernel32.GetFileAttributesW  # type: ignore[attr-defined]
    get_file_attributes.argtypes = (ctypes.wintypes.LPWSTR,)
    get_file_attributes.restype = ctypes.wintypes.DWORD

    invalid_file_attributes = 0xFFFFFFFF
    reparse_point = 0x400
    file_attr = get_file_attributes(path)

    if file_attr == invalid_file_attributes:
        return False

    return file_attr & reparse_point > 0


@lang.memoized
def _windows_can_symlink() -> bool:
    """
    Determines if windows is able to make a symlink depending on
    the system configuration and the level of the user's permissions.
    """
    if sys.platform != "win32":
        tty.warn("windows_can_symlink method can't be used on non-Windows OS.")
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


def _windows_create_link(source: str, link: str):
    """
    Attempts to create a Hard Link or Junction as an alternative
    to a symbolic link. This is called when symbolic links cannot
    be created.

    os.symlink can create a link with relative paths, even if the source paths is not
    relative to the current working directory. In order to emulate that behavior,
    if the source path doesn't exist, check to see if the source path exists relative
    to the link's parent directory.
    """
    if sys.platform != "win32":
        tty.warn("windows_create_link method can't be used on non-Windows OS.")
        return
    elif os.path.isabs(source) and not os.path.exists(source):
        raise SymlinkError(
            f"Source path ({source}) is absolute but does not exist. Cannot create link."
        )
    elif not os.path.exists(source):
        # Emulate how the os.symlink method creates links where the source is
        # relative to the target.
        link_parent = os.path.dirname(link)
        relative_path = os.path.join(link_parent, source)
        if os.path.exists(relative_path):
            source = relative_path
        else:
            raise SymlinkError(f"Source path ({source}) does not exist. Cannot create link.")

    source = os.path.normpath(source)
    link = os.path.normpath(link)

    if os.path.isdir(source):
        _windows_create_junction(source=source, link=link)
    elif os.path.isfile(source):
        _windows_create_hard_link(path=source, link=link)
    else:
        raise SymlinkError(
            f"Cannot create link from {source}. It is neither a file nor a directory."
        )


def _windows_create_junction(source: str, link: str):
    """Duly verify that the path and link are eligible to create a junction,
    then create the junction.
    """
    if sys.platform != "win32":
        tty.warn("windows_create_junction method can't be used on non-Windows OS.")
        return
    elif not os.path.exists(source):
        raise SymlinkError("Source path does not exist, cannot create a junction.")
    elif os.path.exists(link):
        raise SymlinkError("Link path already exists, cannot create a junction.")
    elif not os.path.isdir(source):
        raise SymlinkError("Source path is not a directory, cannot create a junction.")

    import subprocess

    try:
        cmd = ["cmd", "/C", "mklink", "/J", link, source]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        tty.debug(out.decode())
        if proc.returncode != 0:
            err = err.decode()
            tty.error(err)
            raise SymlinkError("Make junction command returned a non-zero return code.", err)
    except subprocess.CalledProcessError as e:
        raise SymlinkError(f"Failed to make junction {link} from directory {source}") from e


def _windows_create_hard_link(path: str, link: str):
    """Duly verify that the path and link are eligible to create a hard
    link, then create the hard link.
    """
    if sys.platform != "win32":
        tty.warn("windows_create_hard_link method can't be used on non-Windows OS.")
        return
    elif not os.path.exists(path):
        raise SymlinkError(f"File path {path} does not exist. Cannot create hard link.")
    elif os.path.exists(link):
        raise SymlinkError(f"Link path ({link}) already exists. Cannot create hard link.")
    elif not os.path.isfile(path):
        raise SymlinkError(f"File path ({link}) is not a file. Cannot create hard link.")
    else:
        tty.debug(f"Creating hard link {link} pointing to {path}")
        CreateHardLink(link, path)


class SymlinkError(SpackError):
    """Exception class for errors raised while creating symlinks,
    junctions and hard links
    """
