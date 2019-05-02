# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat as st
import llnl.util.filesystem as fs
import spack.package_prefs as pp
from spack.error import SpackError


def set_permissions_by_spec(path, spec):
    # Get permissions for spec
    if os.path.isdir(path):
        perms = pp.get_package_dir_permissions(spec)
    else:
        perms = pp.get_package_permissions(spec)

    # Preserve higher-order bits of file permissions
    perms |= os.stat(path).st_mode & (st.S_ISUID | st.S_ISGID | st.S_ISVTX)

    # Do not let users create world writable suid binaries
    if perms & st.S_ISUID and perms & st.S_IWGWP:
        raise InvalidPermissionsError(
            "Attepting to set suid with world writable")

    fs.chmod_x(path, perms)

    # Set group for spec
    group = pp.get_package_group(spec)
    if group:
        fs.chgrp(path, group)


class InvalidPermissionsError(SpackError):
    """Error class for invalid permission setters"""
