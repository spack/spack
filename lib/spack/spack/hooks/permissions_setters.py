# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat

from llnl.util.filesystem import chmod_x, chgrp

from spack.package_prefs import get_package_permissions, get_package_group
from spack.package_prefs import get_package_dir_permissions
from spack.error import SpackError


def forall_files(path, fn, args, dir_args=None):
    """Apply function to all files in directory, with file as first arg.

    Does not apply to the root dir. Does not apply to links"""
    # os.walk explicitly set not to follow links
    for root, dirs, files in os.walk(path, followlinks=False):
        for d in dirs:
            if not os.path.islink(os.path.join(root, d)):
                if dir_args:
                    fn(os.path.join(root, d), *dir_args)
                else:
                    fn(os.path.join(root, d), *args)
        for f in files:
            if not os.path.islink(os.path.join(root, f)):
                fn(os.path.join(root, f), *args)


def chmod_real_entries(path, perms):
    # Don't follow links so we don't change things outside the prefix
    if not os.path.islink(path):
        mode = os.stat(path).st_mode
        perms |= mode & (stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX)
        if perms & stat.S_ISUID and perms & stat.S_IWGRP:
            raise InvalidPermissionsError(
                'Attempting to set suid with world writable')
        chmod_x(path, perms)


def post_install(spec):
    if not spec.external:
        perms = get_package_permissions(spec)
        dir_perms = get_package_dir_permissions(spec)
        group = get_package_group(spec)

        forall_files(spec.prefix, chmod_real_entries, [perms], [dir_perms])

        if group:
            forall_files(spec.prefix, chgrp, [group])


class InvalidPermissionsError(SpackError):
    """Error class for invalid permission setters"""
