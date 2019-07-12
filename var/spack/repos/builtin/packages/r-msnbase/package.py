# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMsnbase(RPackage):
    """Base Functions and Classes for Mass Spectrometry and Proteomics

       MSnbase provides infrastructure for manipulation, processing and
       visualisation of mass spectrometry and proteomics data, ranging from raw
       to quantitative and annotated data."""

    homepage = "https://bioconductor.org/packages/MSnbase"
    git      = "https://git.bioconductor.org/packages/MSnbase.git"

    version('2.10.1', commit='4d5899bc9c714f0b1a70cddd537cd4621b2b53b0')
    version('2.8.3', commit='ef883752c5e92d445647bc5b5d23d5df320db415')
    version('2.6.4', commit='46836860ce0281eef135303f2e2948303d67f68c')
    version('2.4.2', commit='c045d65daa730c7837852e6343a05cae9644ab5e')
    version('2.2.0', commit='d6e8fb7f106d05096fa9074da0f829ac8f02c197')

    depends_on('r@3.6.0:3.6.9', when='@2.10.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.8.3', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.6.4', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.4.2', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.2.0', type=('build', 'run'))

    depends_on('r-rcpp', when='@2.2.0:', type=('build', 'run'))
