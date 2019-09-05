# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RExpm(RPackage):
    """Computation of the matrix exponential, logarithm, sqrt, and related
    quantities."""

    homepage = "http://r-forge.r-project.org/projects/expm"
    url      = "https://cloud.r-project.org/src/contrib/expm_0.999-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/expm"

    version('0.999-4', sha256='58d06427a08c9442462b00a5531e2575800be13ed450c5a1546261251e536096')
    version('0.999-3', sha256='511bac5860cc5b3888bca626cdf23241b6118eabcc82d100935386039e516412')
    version('0.999-2', 'e05fa3f995754af92bd03227625da984')

    depends_on('r-matrix', type=('build', 'run'))
