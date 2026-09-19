# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.package_prefs as pp
import spack.util.file_permissions as fp


def post_install(spec, explicit=None):
    if spec.external:
        return

    # Pre-calculate config variables (expensive to lookup for each file)
    dir_perms = pp.get_package_dir_permissions(spec)
    file_perms = pp.get_package_permissions(spec)
    group = pp.get_package_group(spec)

    # Set permissions on installation prefix
    fp.set_permissions(spec.prefix, dir_perms, group)

    # os.walk explicitly set not to follow links
    for root, dirs, files in os.walk(spec.prefix, followlinks=False):
        for d in dirs:
            if not os.path.islink(os.path.join(root, d)):
                fp.set_permissions(os.path.join(root, d), dir_perms, group)
        for f in files:
            if not os.path.islink(os.path.join(root, f)):
                fp.set_permissions(os.path.join(root, f), file_perms, group)
