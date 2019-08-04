# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTtr(RPackage):
    """Functions and data to construct technical trading rules with R."""

    homepage = "https://github.com/joshuaulrich/TTR"
    url      = "https://cloud.r-project.org/src/contrib/TTR_0.23-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/TTR"

    version('0.23-4', sha256='eb17604da986213b3b924f0af65c3d089502a658a253ee34f6b8f6caccf6bfa2')
    version('0.23-3', sha256='2136032c7a2cd2a82518a4412fc655ecb16597b123dbdebe5684caef9f15261f')
    version('0.23-1', '35f693ac0d97e8ec742ebea2da222986')

    depends_on('r-xts@0.10-0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-curl', when='@0.23-4:', type=('build', 'run'))
