# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTmixclust(RPackage):
    """Implementation of a clustering method for time series gene expression
    data based on mixed-effects models with Gaussian variables and
    non-parametric cubic splines estimation. The method can robustly account
    for the high levels of noise present in typical gene expression time
    series datasets."""

    homepage = "https://bioconductor.org/packages/TMixClust/"
    git      = "https://git.bioconductor.org/packages/TMixClust.git"

    version('1.0.1', commit='0ac800210e3eb9da911767a80fb5582ab33c0cad')

    depends_on('r-gss', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-flexclust', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-spem', type=('build', 'run'))
    depends_on('r@3.4.3:3.4.9', when='@1.0.1')
