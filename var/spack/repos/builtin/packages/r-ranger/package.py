# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRanger(RPackage):
    """A fast implementation of Random Forests, particularly suited for high
    dimensional data."""

    homepage = "https://cloud.r-project.org/package=ranger"
    url      = "https://cloud.r-project.org/src/contrib/ranger_0.8.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ranger"

    version('0.11.2', sha256='13ac8a9433fdd92f62f66de44abc52477dcbb436b2045c1947951a266bffbeeb')
    version('0.11.1', sha256='999fb114602e27601ff0fe8ab461c39d667c6f5e8434e7feb3d21c7caf0dcffb')
    version('0.8.0', '1501380f418e784a6159bc1fb06fd32c')
    version('0.7.0', 'c7fbcbab7c195bc8e65b1ceb3baeb87f')
    version('0.6.0', '047ad26289c9b528b7476aa4811b4111')
    version('0.5.0', 'd45001c8ff58d3078de7353971219927')
    version('0.4.0', 'd404d8a9142372e3c77482b6b7dc469b')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rcpp@0.11.2:', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
