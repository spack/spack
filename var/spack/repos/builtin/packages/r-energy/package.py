# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REnergy(RPackage):
    """E-Statistics: Multivariate Inference via the Energy of Data"""

    homepage = "https://cran.r-project.org/web/packages/energy/index.html"
    url      = "https://cran.r-project.org/src/contrib/energy_1.7-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/energy"

    version('1.7-5', 'd13c76c26b5221ba29aade6a824f32d6')

    depends_on('r-rcpp@0.12.6:', type=('build', 'run'))
    depends_on('r-boot', type=('build', 'run'))
