# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import grp
import os
import pwd
import sys
from typing import List, Optional, Union

#: Permissions to use on Linux and Darwin when creating an empty file
EMPTY_FILE_PERMISSIONS = os.O_WRONLY | os.O_CREAT | os.O_NONBLOCK | os.O_NOCTTY

#: Valid library extensions on Linux and Darwin
VALID_LIBRARY_EXTENSIONS = (".dylib", ".so", ".a")

#: Common directories where to find libraries
COMMON_LIBRARY_DIRECTORIES = ("lib", "lib64")


def group_ids(uid: Optional[int] = None) -> List[int]:
    """Get group ids that a uid is a member of.

    Arguments:
        uid (int): id of user, or None for current user

    Returns:
        (list of int): gids of groups the user is a member of
    """
    if uid is None:
        uid = os.getuid()

    pwd_entry = pwd.getpwuid(uid)
    user = pwd_entry.pw_name

    # user's primary group id may not be listed in grp (i.e. /etc/group)
    # you have to check pwd for that, so start the list with that
    gids = [pwd_entry.pw_gid]

    return sorted(set(gids + [g.gr_gid for g in grp.getgrall() if user in g.gr_mem]))


def chgrp(path: str, group: Union[str, int], follow_symlinks: bool = True) -> None:
    """Implement the bash chgrp function on a single path"""
    if isinstance(group, str):
        gid = grp.getgrnam(group).gr_gid
    else:
        gid = group
    if follow_symlinks:
        os.chown(path, -1, gid)
    else:
        os.lchown(path, -1, gid)


def library_suffixes(*, shared: bool, runtime: bool = True) -> List[str]:
    """Return the library suffixes to be searched on the current platform, based on
    the input parameters.

    Args:
        shared: if True search for shared libraries, if False for static libraries.
        runtime: Windows only option.
    """
    if shared and sys.platform == "darwin":
        return ["so", "dylib"]
    elif shared:
        return ["so"]
    return ["a"]


def uid_for_existing_path(path: str) -> int:
    p_stat = os.stat(path)
    return p_stat.st_uid
