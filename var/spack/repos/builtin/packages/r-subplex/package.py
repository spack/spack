# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSubplex(RPackage):
    """Unconstrained Optimization using the Subplex Algorithm"""

    homepage = "https://cran.r-project.org/package=subplex"
    url      = "https://cran.r-project.org/src/contrib/subplex_1.4-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/subplex"

    version('1.4-1', '2ed963dbbb1dbef47ebec7003f39a117')
