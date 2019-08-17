# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RKernlab(RPackage):
    """Kernel-based machine learning methods for classification, regression,
    clustering, novelty detection, quantile regression and dimensionality
    reduction. Among other methods 'kernlab' includes Support Vector Machines,
    Spectral Clustering, Kernel PCA, Gaussian Processes and a QP solver."""

    homepage = "https://cran.r-project.org/package=kernlab"
    url      = "https://cran.r-project.org/src/contrib/kernlab_0.9-25.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/kernlab"

    version('0.9-25', '1182a2a336a79fd2cf70b4bc5a35353f')

    depends_on('r@2.10:')
