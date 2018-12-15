# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLimma(RPackage):
    """Data analysis, linear models and differential expression
    for microarray data."""

    homepage = "https://www.bioconductor.org/packages/limma/"
    git      = "https://git.bioconductor.org/packages/limma.git"

    version('3.36.2',  commit='0cd5c13e22565182226bd2937ffcf8c59de1ca59')
    version('3.34.9',  commit='6755278a929f942a49e2441fb002a3ed393e1139')
    version('3.32.10', commit='593edf28e21fe054d64137ae271b8a52ab05bc60')

    depends_on('r@3.5.0:3.5.9', when='@3.36.2')
    depends_on('r@3.4.2:3.4.9', when='@3.34.9')
    depends_on('r@3.4.0:3.4.9', when='@3.32.10')
