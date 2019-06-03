# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCrul(RPackage):
    """crul: HTTP Client"""

    homepage = "https://cran.r-project.org/package=crul"
    url      = "https://cran.r-project.org/src/contrib/crul_0.7.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/crul"

    version('0.7.4', sha256='c963dd666ae3fc89b661ce19fce2fa19a16fc3825e1502105cae98ceb92c6014')

    depends_on('r-curl@3.3:', type=('build', 'run'))
    depends_on('r-httpcode@0.2.0:', type=('build', 'run'))
    depends_on('r-mime', type=('build', 'run'))
    depends_on('r-r6@2.2.0:', type=('build', 'run'))
    depends_on('r-urltools@1.6.0:', type=('build', 'run'))
