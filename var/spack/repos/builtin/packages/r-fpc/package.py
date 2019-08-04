# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFpc(RPackage):
    """fpc: Flexible Procedures for Clustering"""

    homepage = "http://www.homepages.ucl.ac.uk/~ucakche"
    url      = "https://cloud.r-project.org/src/contrib/fpc_2.1-10.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fpc"

    version('2.2-3', sha256='8100a74e6ff96b1cd65fd22494f2d200e54ea5ea533cfca321fa494914bdc3b7')
    version('2.2-2', sha256='b6907019eb161d5c8c814cf02a4663cc8aae6322699932881ce5b02f45ecf8d3')
    version('2.1-10', '75e5340e416cd13d7751e06f1c07866b')

    depends_on('r@2.0.0:')
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-flexmix', type=('build', 'run'))
    depends_on('r-prabclus', type=('build', 'run'))
    depends_on('r-class', type=('build', 'run'))
    depends_on('r-diptest', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-kernlab', type=('build', 'run'))
    depends_on('r-trimcluster', when='@:2.1-10', type=('build', 'run'))
