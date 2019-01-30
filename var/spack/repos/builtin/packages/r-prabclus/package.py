# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPrabclus(RPackage):
    """prabclus: Functions for Clustering of Presence-Absence, Abundance and
    Multilocus Genetic Data"""

    homepage = "http://www.homepages.ucl.ac.uk/~ucakche"
    url      = "https://cran.r-project.org/src/contrib/prabclus_2.2-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/prabclus"

    version('2.2-6', '7f835dcc113243e1db74aad28ce93d11')

    depends_on('r@2.1.0:')
    # depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
