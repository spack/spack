# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRtsne(RPackage):
    """An R wrapper around the fast T-distributed Stochastic Neighbor
    Embedding implementation."""

    homepage = "https://CRAN.R-project.org/package=Rtsne"
    url      = "https://cran.r-project.org/src/contrib/Rtsne_0.13.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Rtsne"

    version('0.13', 'ea1d2ef2bda16735bbf219ffda5b0661')
    version('0.11', '9a1eaa9b71d67cc27a55780e6e9df733')
    version('0.10', 'c587e1b76fdcea2629424f74c6e92340')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-rcpp', type=('build', 'run'))
