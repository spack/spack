# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat as st
from typing import List, Optional, Union

import spack.package_prefs as pp
from spack.error import SpackError

#: os.chown sentinel to leave an id unchanged
_UNCHANGED = -1


def set_permissions_by_spec(path: str, spec) -> None:
    """Recursively set permissions and group of path as configured for spec."""
    set_permissions(
        path,
        dir_perms=pp.get_package_dir_permissions(spec),
        file_perms=pp.get_package_permissions(spec),
        group=pp.get_package_group(spec),
    )


def set_permissions(
    path: str, dir_perms: int, file_perms: int, group: Optional[Union[str, int]] = None
) -> None:
    """Recursively set permissions and group of path, without following symlinks."""
    if isinstance(group, int):
        gid = group
    elif group:
        import grp

        gid = grp.getgrnam(group).gr_gid
    else:
        gid = _UNCHANGED

    stack: List[str] = []

    def push(path: str, s: os.stat_result) -> None:
        if st.S_ISDIR(s.st_mode):
            _set_permissions(path, s, dir_perms, gid)
            stack.append(path)
        else:
            _set_permissions(path, s, file_perms, gid)

    push(path, os.lstat(path))
    while stack:
        with os.scandir(stack.pop()) as it:
            for entry in it:
                push(entry.path, entry.stat(follow_symlinks=False))


def _set_permissions(path: str, s: os.stat_result, perms: int, gid: int) -> None:
    """Set perms and gid on path given its lstat result, only changing what differs"""
    chown = gid != _UNCHANGED and s.st_gid != gid

    # Symlink permissions are meaningless, only its group matters
    if st.S_ISLNK(s.st_mode):
        if chown:
            os.lchown(path, _UNCHANGED, gid)
        return

    # Preserve higher-order bits of file permissions
    perms |= s.st_mode & (st.S_ISUID | st.S_ISGID | st.S_ISVTX)

    # Do not let users create world/group writable suid binaries
    if perms & st.S_ISUID:
        if perms & st.S_IWOTH:
            raise InvalidPermissionsError("Attempting to set suid with world writable")
        if perms & st.S_IWGRP:
            raise InvalidPermissionsError("Attempting to set suid with group writable")
    # Or world writable sgid binaries
    if perms & st.S_ISGID:
        if perms & st.S_IWOTH:
            raise InvalidPermissionsError("Attempting to set sgid with world writable")

    # Like chmod +X: only set executable bits on files that already have one
    if st.S_ISREG(s.st_mode) and not s.st_mode & (st.S_IXUSR | st.S_IXGRP | st.S_IXOTH):
        perms &= ~(st.S_IXUSR | st.S_IXGRP | st.S_IXOTH)

    # chown before chmod, since chown may clear suid and sgid bits
    if chown:
        os.chown(path, _UNCHANGED, gid, follow_symlinks=False)
    if chown or st.S_IMODE(s.st_mode) != perms:
        os.chmod(path, perms)


class InvalidPermissionsError(SpackError):
    """Error class for invalid permission setters"""
