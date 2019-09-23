# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRtsne(RPackage):
    """An R wrapper around the fast T-distributed Stochastic Neighbor
    Embedding implementation."""

    homepage = "https://cloud.r-project.org/package=Rtsne"
    url      = "https://cloud.r-project.org/src/contrib/Rtsne_0.13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Rtsne"

    version('0.15', sha256='56376e4f0a382fad3d3d40e2cb0562224be5265b827622bcd235e8fc63df276c')
    version('0.13', 'ea1d2ef2bda16735bbf219ffda5b0661')
    version('0.11', '9a1eaa9b71d67cc27a55780e6e9df733')
    version('0.10', 'c587e1b76fdcea2629424f74c6e92340')

    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
