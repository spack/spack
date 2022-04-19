# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.directives import variant
from spack.package import PackageBase


class WindowsPackage(PackageBase):
    """Auxiliary class for managing Windows-specific variants of
    packages. This class establishes three major variants for use in
    individual package.py scripts:

        1. Static with links to the dynamic runtime library (/MD)
        2. Shared builds which link to /MD by necessity
        3. Static with links to the static runtime library (/MT)

    Variant 1, static with dynamic runtime, will be the default build
    and the other two (shared and staticmt) can be enabled by the
    user from the command line with behaviors varying depending on the
    package.
    """

    variant('staticmt', default=False,
            description="Build static version with static runtime libraries",
            when='platform=windows')
