# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFastmatrix(RPackage):
    """Fast Computation of some Matrices Useful in Statistics.

    Small set of functions to fast computation of some matrices and operations
    useful in statistics and econometrics. Currently, there are functions for
    efficient computation of duplication, commutation and symmetrizer matrices
    with minimal storage requirements. Some commonly used matrix decompositions
    (LU and LDL), basic matrix operations (for instance, Hadamard, Kronecker
    products and the Sherman-Morrison formula) and iterative solvers for linear
    systems are also available. In addition, the package includes a number of
    common statistical procedures such as the sweep operator, weighted mean and
    covariance matrix using an online algorithm, linear regression (using
    Cholesky, QR, SVD, sweep operator and conjugate gradients methods), ridge
    regression (with optimal selection of the ridge parameter considering the
    GCV procedure), functions to compute the multivariate skewness, kurtosis,
    Mahalanobis distance (checking the positive defineteness) and the
    Wilson-Hilferty transformation of chi squared variables. Furthermore, the
    package provides interfaces to C code callable by another C code from other
    R packages."""

    cran = "fastmatrix"

    version('0.3-8196', sha256='72fae07c627b995a091ccc3e14b2b2167474e3b1f14d723e87252538cf978fb6')
    version('0.3', sha256='d92e789454a129db5f6f5b23e0d2245f3d55ff34b167427af265b9a6331e7c21')

    depends_on('r@3.5.0:', type=('build', 'run'))
