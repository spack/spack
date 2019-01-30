# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTseries(RPackage):
    """Time series analysis and computational finance."""

    homepage = "https://cran.r-project.org/package=tseries"
    url      = "https://cran.r-project.org/src/contrib/tseries_0.10-42.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/tseries"

    version('0.10-42', '3feaa5c463bc967d749323163d9bc836')

    depends_on('r-quadprog', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-quantmod', type=('build', 'run'))
