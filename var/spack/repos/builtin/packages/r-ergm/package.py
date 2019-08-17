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
    url      = "https://cran.r-project.org/src/contrib/ergm_3.7.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ergm"

    version('3.7.1', '431ae430c76b2408988f469831d80126')

    depends_on('r-robustbase@0.9-10:', type=('build', 'run'))
    depends_on('r-coda@0.18-1:', type=('build', 'run'))
    depends_on('r-trust', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-lpsolve', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-statnet-common@3.3:', type=('build', 'run'))
    depends_on('r-network@1.13:', type=('build', 'run'))
