# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.config
import spack.package_prefs
import spack.util.file_permissions as fp


def post_install(spec, explicit=None):
    if spec.external:
        return
    perms = spack.package_prefs.package_permissions(spack.config.CONFIG, spec.name)
    spack.package_prefs.warn_if_sgid_on_afs(spec.prefix, perms.dir_mode)
    fp.set_permissions(
        spec.prefix, dir_perms=perms.dir_mode, file_perms=perms.file_mode, group=perms.group
    )
