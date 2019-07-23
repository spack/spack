# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLimma(RPackage):
    """Linear Models for Microarray Data.

       Data analysis, linear models and differential expression for microarray
       data."""

    homepage = "https://bioconductor.org/packages/limma"
    git      = "https://git.bioconductor.org/packages/limma.git"

    version('3.40.4', commit='0cf2e6af70777fb7442d713e88c3842402ae8c8d')
    version('3.38.3', commit='77b292eb150cdedaa1db704bcfb01f0bb29e9849')
    version('3.36.5', commit='3148d1cb7eea9c6bdd60351d51abcfd665332d44')
    version('3.34.9', commit='6755278a929f942a49e2441fb002a3ed393e1139')
    version('3.32.10', commit='593edf28e21fe054d64137ae271b8a52ab05bc60')

    depends_on('r@3.6.0:3.6.9', when='@3.40.4', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@3.38.3', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@3.36.5', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@3.34.9', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@3.32.10', type=('build', 'run'))
