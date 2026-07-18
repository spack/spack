# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.repo


def post_install(spec, explicit=None):
    spack.repo.PATH.get(spec).windows_establish_runtime_linkage()
