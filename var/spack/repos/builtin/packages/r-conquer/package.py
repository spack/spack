# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RConquer(RPackage):
    """Convolution-Type Smoothed Quantile Regression.

    Fast and accurate convolution-type smoothed quantile regression.
    Implemented using Barzilai-Borwein gradient descent with a Huber regression
    warm start. Construct confidence intervals for regression coefficients
    using multiplier bootstrap."""

    cran = "conquer"

    version('1.2.1', sha256='1354f90f962a2124e155227cdc0ed2c6e54682f1e08934c49a827e51dc112f45')
    version('1.0.2', sha256='542f6154ce1ffec0c1b4dd4e1f5b86545015f4b378c4c66a0840c65c57d674ff')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-rcpp@1.0.3:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-caret', type=('build', 'run'), when='@1.2:')
    depends_on('r-rcpparmadillo@0.9.850.1.0:', type=('build', 'run'))
