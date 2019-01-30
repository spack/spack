# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFpc(RPackage):
    """fpc: Flexible Procedures for Clustering"""

    homepage = "http://www.homepages.ucl.ac.uk/~ucakche"
    url      = "https://cran.r-project.org/src/contrib/fpc_2.1-10.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/fpc"

    version('2.1-10', '75e5340e416cd13d7751e06f1c07866b')

    depends_on('r@2.0.0:')
    # depends_on('r-mass', type=('build', 'run'))
    # depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-flexmix', type=('build', 'run'))
    depends_on('r-prabclus', type=('build', 'run'))
    # depends_on('r-class', type=('build', 'run'))
    depends_on('r-diptest', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-kernlab', type=('build', 'run'))
    depends_on('r-trimcluster', type=('build', 'run'))
