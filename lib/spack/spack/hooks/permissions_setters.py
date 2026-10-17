# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.file_permissions as fp


def post_install(spec, explicit=None):
    if not spec.external:
        fp.set_permissions_by_spec(spec.prefix, spec)
