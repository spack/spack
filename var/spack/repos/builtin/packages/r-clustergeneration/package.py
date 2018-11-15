# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RClustergeneration(RPackage):
    """Random Cluster Generation (with Specified Degree of Separation)"""

    homepage = "https://cran.r-project.org/package=clusterGeneration"
    url      = "https://cran.r-project.org/src/contrib/clusterGeneration_1.3.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/clusterGeneration/"

    version('1.3.4', sha256='7c591ad95a8a9d7fb0e4d5d80dfd78f7d6a63cf7d11eb53dd3c98fdfb5b868aa')

    depends_on('r-mass', type=('build', 'run'))
