# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RParty(RPackage):
    """A computational toolbox for recursive partitioning."""

    homepage = "https://cran.r-project.org/web/packages/party/index.html"
    url      = "https://cran.r-project.org/src/contrib/party_1.1-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/party"

    version('1.1-2', '40a00336cf8418042d2ab616675c8ddf')

    depends_on('r@2.14.0:')

    depends_on('r-mvtnorm@1.0-2:', type=('build', 'run'))
    depends_on('r-modeltools@0.1-21:', type=('build', 'run'))
    depends_on('r-strucchange', type=('build', 'run'))
    depends_on('r-survival@2.37-7:', type=('build', 'run'))
    depends_on('r-coin@1.1-0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-sandwich@1.1-1:', type=('build', 'run'))
