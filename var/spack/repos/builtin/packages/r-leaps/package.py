# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLeaps(RPackage):
    """leaps: Regression Subset Selection"""

    homepage = "https://CRAN.R-project.org/package=leaps"
    url      = "https://cran.r-project.org/src/contrib/leaps_3.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/leaps"

    version('3.0', '30823138890680e0493d1491c8f43edc')
