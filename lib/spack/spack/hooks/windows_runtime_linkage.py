# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


def post_install(spec, explicit=None):
    if not spec.package.installed_from_binary_cache:
        spec.package.windows_establish_runtime_linkage()
