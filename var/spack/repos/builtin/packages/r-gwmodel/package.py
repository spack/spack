# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGwmodel(RPackage):
    """GWmodel: Geographically-Weighted Models"""

    homepage = "http://gwr.nuim.ie/"
    url      = "https://cran.r-project.org/src/contrib/GWmodel_2.0-9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/GWmodel"

    version('2.0-9', sha256='b479af2c19d4aec30f1883d00193d52e342c609c1badcb51cc0344e4404cffa7')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-maptools@0.5-2:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-spacetime', type=('build', 'run'))
    depends_on('r-spatialreg', type=('build', 'run'))
    depends_on('r-spdep', type=('build', 'run'))
