# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Windows filesystem link utilities.

Spack considers symbolic links, junctions and hard links to all be links. Creating a symbolic link
on Windows requires either administrator privileges or developer mode, so when symbolic links are
unavailable this module falls back to a junction for a directory and a hard link for a file.

This module binds Windows only APIs at import time and must only be imported on Windows.
:mod:`spack.util.filesystem` exposes the cross platform ``symlink``, ``readlink`` and ``islink``.
"""

import ctypes
import os
import re
import shutil
import subprocess
import tempfile
from ctypes import wintypes  # type: ignore[attr-defined]
from typing import Any, Union

from spack.util import lang, tty
from spack.util.link_errors import AlreadyExistsError, SymlinkError
from spack.util.path import sanitize_win_longpath

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # type: ignore[attr-defined]
_WinError = ctypes.WinError  # type: ignore[attr-defined]
_get_last_error = ctypes.get_last_error  # type: ignore[attr-defined]


def _bind(dll: ctypes.WinDLL, name: str, argtypes: list, restype: type) -> Any:  # type: ignore[name-defined]
    """Set argtypes/restype on a DLL function and return it."""
    fn = getattr(dll, name)
    fn.argtypes = argtypes
    fn.restype = restype
    return fn


_GetFileAttributesW = _bind(_kernel32, "GetFileAttributesW", [wintypes.LPCWSTR], wintypes.DWORD)

_CreateFileW = _bind(
    _kernel32,
    "CreateFileW",
    [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ],
    wintypes.HANDLE,
)

_DeviceIoControl = _bind(
    _kernel32,
    "DeviceIoControl",
    [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    ],
    wintypes.BOOL,
)

_CloseHandle = _bind(_kernel32, "CloseHandle", [wintypes.HANDLE], wintypes.BOOL)

_CreateHardLinkW = _bind(
    _kernel32,
    "CreateHardLinkW",
    [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPVOID],
    wintypes.BOOL,
)

INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
# Required to obtain a handle to a directory
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FSCTL_SET_REPARSE_POINT = 0x000900A4
IO_REPARSE_TAG_MOUNT_POINT = 0xA0000003
MAXIMUM_REPARSE_DATA_BUFFER_SIZE = 16 * 1024
INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value


def symlink(
    src: str, dst: str, target_is_directory: bool = False, *, dir_fd: Union[int, None] = None
):
    """On Windows with System Administrator privileges this will be a normal symbolic link via
    os.symlink. On Windows without privileges the link will be a junction for a directory and a
    hardlink for a file. On Windows the various link types are:

    Symbolic Link: A link to a file or directory on the same or different volume (drive letter) or
    even to a remote file or directory (using UNC in its path). Need System Administrator
    privileges to make these.

    Hard Link: A link to a file on the same volume (drive letter) only. Every file (file's data)
    has at least 1 hard link (file's name). But when this method creates a new hard link there will
    be 2. Deleting all hard links effectively deletes the file. Don't need System Administrator
    privileges.

    Junction: A link to a directory on the same or different volume (drive letter) but not to a
    remote directory. Don't need System Administrator privileges."""
    source_path = os.path.normpath(src)
    win_source_path = source_path
    link_path = os.path.normpath(dst)

    # Perform basic checks to make sure symlinking will succeed
    if os.path.lexists(link_path):
        raise AlreadyExistsError(f"Link path ({link_path}) already exists. Cannot create link.")

    if not os.path.exists(source_path):
        if os.path.isabs(source_path):
            # An absolute source path that does not exist will result in a broken link.
            raise SymlinkError(
                f"Source path ({source_path}) is absolute but does not exist. Resulting "
                f"link would be broken so not making link."
            )
        else:
            # os.symlink can create a link when the given source path is relative to
            # the link path. Emulate this behavior and check to see if the source exists
            # relative to the link path ahead of link creation to prevent broken
            # links from being made.
            link_parent_dir = os.path.dirname(link_path)
            relative_path = os.path.join(link_parent_dir, source_path)
            if os.path.exists(relative_path):
                # In order to work on windows, the source path needs to be modified to be
                # relative because hardlink/junction dont resolve relative paths the same
                # way as os.symlink. This is ignored on other operating systems.
                win_source_path = relative_path
            else:
                raise SymlinkError(
                    f"The source path ({source_path}) is not relative to the link path "
                    f"({link_path}). Resulting link would be broken so not making link."
                )

    # Create the symlink
    if not can_symlink():
        create_link(win_source_path, link_path)
    else:
        os.symlink(source_path, link_path, target_is_directory=os.path.isdir(source_path))


def islink(path: str) -> bool:
    """Override os.islink to give correct answer for spack logic.

    Spack considers symlinks, hard links, and junctions to all be links,
    so if any of those are True, return True.

    Args:
        path (str): path to check if it is a link.

    Returns:
         bool - whether the path is any kind link or not.
    """
    return any([os.path.islink(path), is_junction(path), is_hardlink(path)])


def is_hardlink(path: str) -> bool:
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
    if os.path.islink(path) or not os.path.exists(path):
        return False

    return os.stat(path).st_nlink > 1


def is_junction(path: str) -> bool:
    """Determines if a path is a windows junction. A junction can be
    determined using a bitwise AND operation between the file's
    attribute bitmask and the known junction bitmask (0x400).

    Args:
        path (str): A non-file path

    Returns:
        bool - whether the path is a junction or not.
    """
    if os.path.islink(path) or os.path.isfile(path):
        return False

    file_attr = _GetFileAttributesW(str(path))

    if file_attr == INVALID_FILE_ATTRIBUTES:
        return False

    return file_attr & FILE_ATTRIBUTE_REPARSE_POINT > 0


@lang.memoized
def can_symlink() -> bool:
    """
    Determines if windows is able to make a symlink depending on
    the system configuration and the level of the user's permissions.
    """
    tempdir = tempfile.mkdtemp()

    dpath = os.path.join(tempdir, "dpath")
    fpath = os.path.join(tempdir, "fpath.txt")

    dlink = os.path.join(tempdir, "dlink")
    flink = os.path.join(tempdir, "flink.txt")

    with open(fpath, "w", encoding="utf-8"):
        pass
    os.mkdir(dpath)

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


def create_link(source: str, link: str):
    """
    Attempts to create a Hard Link or Junction as an alternative
    to a symbolic link. This is called when symbolic links cannot
    be created.
    """
    if os.path.isdir(source):
        create_junction(source=source, link=link)
    elif os.path.isfile(source):
        create_hard_link(path=source, link=link)
    else:
        raise SymlinkError(
            f"Cannot create link from {source}. It is neither a file nor a directory."
        )


def create_junction(source: str, link: str):
    """Duly verify that the path and link are eligible to create a junction,
    then create the junction.
    """
    if not os.path.exists(source):
        raise SymlinkError("Source path does not exist, cannot create a junction.")
    elif os.path.lexists(link):
        raise AlreadyExistsError("Link path already exists, cannot create a junction.")
    elif not os.path.isdir(source):
        raise SymlinkError("Source path is not a directory, cannot create a junction.")

    tty.debug(f"Creating junction {link} pointing to {source}")
    # Junction targets must be absolute and cannot carry the \\?\ long path prefix
    target = os.path.abspath(source)
    if target.startswith("\\\\?\\"):
        target = target[4:]
    # A junction is an empty directory with a mount point reparse point attached. The
    # reparse data holds the NT namespace target (substitute name) followed by the
    # user facing target (print name), each null terminated.
    substitute_name = f"\\??\\{target}"
    print_name = target
    path_buffer = f"{substitute_name}\0{print_name}\0"
    wchar_size = ctypes.sizeof(wintypes.WCHAR)
    # Lengths are in bytes of UTF-16 and exclude the null terminators
    substitute_name_length = len(substitute_name.encode("utf-16-le"))
    print_name_length = len(print_name.encode("utf-16-le"))
    path_buffer_length = len(path_buffer.encode("utf-16-le"))

    class MountPointReparseDataBuffer(ctypes.Structure):
        _fields_ = [
            ("ReparseTag", wintypes.ULONG),
            ("ReparseDataLength", wintypes.USHORT),
            ("Reserved", wintypes.USHORT),
            ("SubstituteNameOffset", wintypes.USHORT),
            ("SubstituteNameLength", wintypes.USHORT),
            ("PrintNameOffset", wintypes.USHORT),
            ("PrintNameLength", wintypes.USHORT),
            ("PathBuffer", wintypes.WCHAR * (path_buffer_length // wchar_size)),
        ]

    # ReparseDataLength covers everything after the Reserved field
    reparse_data_offset = MountPointReparseDataBuffer.SubstituteNameOffset.offset
    reparse_data_length = ctypes.sizeof(MountPointReparseDataBuffer) - reparse_data_offset
    if ctypes.sizeof(MountPointReparseDataBuffer) > MAXIMUM_REPARSE_DATA_BUFFER_SIZE:
        raise SymlinkError(f"Source path {source} is too long to create a junction.")

    reparse_data = MountPointReparseDataBuffer(
        ReparseTag=IO_REPARSE_TAG_MOUNT_POINT,
        ReparseDataLength=reparse_data_length,
        Reserved=0,
        SubstituteNameOffset=0,
        SubstituteNameLength=substitute_name_length,
        PrintNameOffset=substitute_name_length + wchar_size,
        PrintNameLength=print_name_length,
        PathBuffer=path_buffer,
    )

    os.mkdir(link)
    try:
        handle = _CreateFileW(
            link,
            GENERIC_WRITE,
            0,
            None,
            OPEN_EXISTING,
            FILE_FLAG_OPEN_REPARSE_POINT | FILE_FLAG_BACKUP_SEMANTICS,
            None,
        )
        if handle == INVALID_HANDLE_VALUE:
            raise _WinError(_get_last_error())
        try:
            bytes_returned = wintypes.DWORD()
            success = _DeviceIoControl(
                handle,
                FSCTL_SET_REPARSE_POINT,
                ctypes.byref(reparse_data),
                ctypes.sizeof(reparse_data),
                None,
                0,
                ctypes.byref(bytes_returned),
                None,
            )
            if not success:
                raise _WinError(_get_last_error())
        finally:
            _CloseHandle(handle)
    except OSError as e:
        # Don't leave behind the plain directory that would have become the junction
        os.rmdir(link)
        raise SymlinkError(f"Failed to create junction {link} pointing to {source}") from e


def create_hard_link(path: str, link: str):
    """Duly verify that the path and link are eligible to create a hard
    link, then create the hard link.
    """
    if not os.path.exists(path):
        raise SymlinkError(f"File path {path} does not exist. Cannot create hard link.")
    elif os.path.lexists(link):
        raise AlreadyExistsError(f"Link path ({link}) already exists. Cannot create hard link.")
    elif not os.path.isfile(path):
        raise SymlinkError(f"File path ({link}) is not a file. Cannot create hard link.")

    tty.debug(f"Creating hard link {link} pointing to {path}")
    if not _CreateHardLinkW(link, path, None):
        raise _WinError(
            _get_last_error(), f"Failed to create hardlink for path {path} and link {link}"
        )


def readlink(path: str, *, dir_fd=None):
    """Spack utility to override of os.readlink method to work cross platform"""
    if is_hardlink(path):
        return read_hard_link(path)
    elif is_junction(path):
        return read_junction(path)
    else:
        return sanitize_win_longpath(os.readlink(path, dir_fd=dir_fd))


def read_hard_link(link: str) -> str:
    """Find all of the files that point to the same inode as the link"""
    link = os.path.abspath(link)
    fsutil_cmd = ["fsutil", "hardlink", "list", link]
    proc = subprocess.Popen(fsutil_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise SymlinkError(f"An error occurred while reading hard link: {err.decode()}")

    # fsutil response does not include the drive name, so append it back to each linked file.
    drive, link_tail = os.path.splitdrive(os.path.abspath(link))
    links = set([os.path.join(drive, p) for p in out.decode().splitlines()])
    links.remove(link)
    if len(links) == 1:
        return links.pop()
    elif len(links) > 1:
        # TODO: How best to handle the case where 3 or more paths point to a single inode?
        raise SymlinkError(f"Found multiple paths pointing to the same inode {links}")
    else:
        raise SymlinkError("Cannot determine hard link source path.")


def read_junction(link: str):
    """Find the path that a junction points to."""
    link = os.path.abspath(link)
    link_basename = os.path.basename(link)
    link_parent = os.path.dirname(link)
    # dir is a cmd builtin
    cmd = ["cmd", "/C", "dir", "/a:l", link_parent]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise SymlinkError(f"An error occurred while reading junction: {err.decode()}")
    matches = re.search(rf"<JUNCTION>\s+{link_basename} \[(.*)]", out.decode())
    if matches:
        return matches.group(1)
    else:
        raise SymlinkError("Could not find junction path.")
