# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDiffusionmap(RPackage):
    """Allows to display a progress bar in the R console for long running
    computations taking place in c++ code, and support for interrupting those
    computations even in multithreaded code, typically using OpenMP."""

    homepage = "https://cloud.r-project.org/package=diffusionMap"
    url      = "https://cloud.r-project.org/src/contrib/diffusionMap_1.1-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/diffusionMap"

    version('1.1-0.1', sha256='b24cf841af2566ac36f4ede2885f2ff355a7905398444d6d89747315d99a8486')
    version('1.1-0', 'cc7d728087ba08d9299ae3a64a8d8919')
    version('1.0-0', 'bca462e6efe45c5eaa48d38621f0bd6f')
    version('0.0-2', 'b599f47ebf30127e34ce2219dc3e43ae')
    version('0.0-1', '20c2cc2fffb5237d5c0216207016c2a1')

    depends_on('r@2.4.0:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-scatterplot3d', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
