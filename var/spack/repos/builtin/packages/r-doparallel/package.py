# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDoparallel(RPackage):
    """Provides a parallel backend for the %dopar% function using the parallel
    package."""

    homepage = "https://cran.r-project.org/web/packages/doParallel/index.html"
    url      = "https://cran.r-project.org/src/contrib/doParallel_1.0.10.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/doParallel"

    version('1.0.11', 'd7822f0efd7bdf7582d8b43c986be86c')
    version('1.0.10', 'd9fbde8f315d98d055483ee3493c9b43')

    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
