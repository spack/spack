# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDiffusionmap(RPackage):
    """Allows to display a progress bar in the R console for long running
    computations taking place in c++ code, and support for interrupting those
    computations even in multithreaded code, typically using OpenMP."""

    homepage = "https://cran.r-project.org/web/packages/diffusionMap/index.html"
    url      = "https://cran.r-project.org/src/contrib/diffusionMap_1.1-0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/diffusionMap"

    version('1.1-0', 'cc7d728087ba08d9299ae3a64a8d8919')
    version('1.0-0', 'bca462e6efe45c5eaa48d38621f0bd6f')
    version('0.0-2', 'b599f47ebf30127e34ce2219dc3e43ae')
    version('0.0-1', '20c2cc2fffb5237d5c0216207016c2a1')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-scatterplot3d', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
