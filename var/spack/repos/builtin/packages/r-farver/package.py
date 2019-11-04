# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFarver(RPackage):
    """farver: Vectorised Colour Conversion and Comparison"""

    homepage = "https://github.com/thomasp85/farver"
    url      = "https://cloud.r-project.org/src/contrib/farver_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/farver"

    version('1.1.0', sha256='2086f309135f37705280fe2df851ad91dc886ad8f2a6eb1f3983aa20427f94b6')

    depends_on('r-rcpp@0.12.15:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
