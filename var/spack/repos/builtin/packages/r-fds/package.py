# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package_defs import *


class RFds(RPackage):
    """Functional data sets."""

    cran = 'fds'

    version('1.8', sha256='203a5e7671e542dcb83d4c75d0f4012aaebc32d54f94657afaf9e71e99dd0489')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-rainbow', type=('build', 'run'))
