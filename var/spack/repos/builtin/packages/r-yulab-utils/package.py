# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RYulabUtils(RPackage):
    """Supporting Functions for Packages Maintained by 'YuLab-SMU'.

    Miscellaneous functions commonly used by 'YuLab-SMU'."""

    cran = "yulab.utils"

    version('0.0.4', sha256='38850663de53a9166b8e85deb85be1ccf1a5b310bbe4355f3b8bc823ed1b49ae')
