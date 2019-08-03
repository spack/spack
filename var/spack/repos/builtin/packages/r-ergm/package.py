# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RErgm(RPackage):
    """An integrated set of tools to analyze and simulate networks based
       on exponential-family random graph models (ERGM). "ergm" is a
       part of the "statnet" suite of packages for network analysis."""

    homepage = "http://statnet.org"
    url      = "https://cloud.r-project.org/src/contrib/ergm_3.7.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ergm"

    version('3.10.1', sha256='a2ac249ff07ba55b3359242f20389a892543b4fff5956d74143d2d41fa6d4beb')
    version('3.7.1', '431ae430c76b2408988f469831d80126')

    depends_on('r-robustbase@0.93-5:', type=('build', 'run'))
    depends_on('r-coda@0.19-2:', type=('build', 'run'))
    depends_on('r-trust@01-7:', type=('build', 'run'))
    depends_on('r-matrix@1.2-17:', type=('build', 'run'))
    depends_on('r-lpsolve@5.6.13:', type=('build', 'run'))
    depends_on('r-mass@7.3-51.4:', type=('build', 'run'))
    depends_on('r-statnet-common@3.3:', type=('build', 'run'))
    depends_on('r-network@1.15:', type=('build', 'run'))
    depends_on('r-purrr@0.3.2:', when='@3.10.0:', type=('build', 'run'))
    depends_on('r-rlang@0.3.4:', when='@3.10.0:', type=('build', 'run'))
    depends_on('r-tibble@2.1.1:', when='@3.10.0:', type=('build', 'run'))
    depends_on('r-dplyr@0.8.0.1:', when='@3.10.0:', type=('build', 'run'))

