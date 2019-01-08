# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDplyr(RPackage):
    """A fast, consistent tool for working with data frame like objects, both
    in memory and out of memory."""

    homepage = "https://cran.r-project.org/package=dplyr"
    url      = "https://cran.r-project.org/src/contrib/dplyr_0.7.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/dplyr"

    version('0.7.7', sha256='0553db5a55f0e6f5d2d111e88422c6d26e9d54cb36b860ad2ca28e3826e3d4a4')
    version('0.7.6', sha256='d489cc8b53854ec30737bb7d39b331b67ca35f4275ad19e97420d7a247808330')
    version('0.7.5', sha256='2fbd8f316a59670076d43a0fe854654621941ee5f621ea5f0185a3f5daafda50')
    version('0.7.4', sha256='7b1fc90750fbb46483423da6721832c545d37b157f4f3355784a65e50fada8c2')
    version('0.7.3', sha256='ae67ed4f629a74485626b8291b5219b81ee6fc4c5fe5a077bfbdfeae59dee573')
    version('0.7.2', sha256='2262d1ad9fefd5c7d1030dea0edd6ffe5747b827cabe088cc915b0a09818eb4a')
    version('0.7.1', sha256='8c7573464b2a808f711f8977d0039e043318f93e47f2e80ba85b1f4ca09d12f4')
    version('0.7.0', sha256='27b3593c09da5e99c0c4fb19ea826edd2cab619f8aaefd0cfd2a4140a0bd9410')
    version('0.5.0', sha256='93d3b829f1c2d38e14a4f2fa7d6398fc6c1a9e4189b3e78bc38a0eb0e864454f')

    depends_on('r-assertthat@0.2.0:', type=('build', 'run'))
    depends_on('r-bindrcpp@0.2.0:', type=('build', 'run'))
    depends_on('r-glue@1.1.1:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-pkgconfig@2.0.1:', type=('build', 'run'))
    depends_on('r-r6@2.2.2:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.19:', type=('build', 'run'))
    depends_on('r-rlang@0.3.0:', type=('build', 'run'))
    depends_on('r-tibble@1.4.2:', type=('build', 'run'))
    depends_on('r-tidyselect@0.2.3:', type=('build', 'run'))
