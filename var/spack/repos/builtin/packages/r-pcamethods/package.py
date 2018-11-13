# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPcamethods(RPackage):
    """Provides Bayesian PCA, Probabilistic PCA, Nipals PCA, Inverse
       Non-Linear PCA and the conventional SVD PCA. A cluster based method for
       missing value estimation is included for comparison. BPCA, PPCA and
       NipalsPCA may be used to perform PCA on incomplete data as well as for
       accurate missing value estimation. A set of methods for printing and
       plotting the results is also provided. All PCA methods make use of the
       same data structure (pcaRes) to provide a common interface to the PCA
       results. Initiated at the Max-Planck Institute for Molecular Plant
       Physiology, Golm, Germany."""

    homepage = "http://bioconductor.org/packages/pcaMethods/"
    git      = "https://git.bioconductor.org/packages/pcaMethods.git"

    version('1.68.0', commit='c8d7c93dcaf7ef728f3d089ae5d55771b320bdab')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.68.0')
