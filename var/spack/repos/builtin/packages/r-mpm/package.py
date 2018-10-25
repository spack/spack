# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMpm(RPackage):
    """Exploratory graphical analysis of multivariate data, specifically
 gene expression data with different projection methods: principal
 component analysis, correspondence analysis, spectral map analysis."""

    homepage = "https://cran.rstudio.com/web/packages/mpm/index.html"
    url = "https://cran.rstudio.com/src/contrib/mpm_1.0-22.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mpm"
    version('1.0-22', '91885c421cafd89ce8893ccf827165a2')

    depends_on('r-kernsmooth', type=('build', 'run'))
