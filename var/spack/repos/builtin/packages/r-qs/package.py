# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RQs(RPackage):
    """Quick Serialization of R Objects.

    Provides functions for quickly writing and reading any R object to and from
    disk."""

    cran = "qs"

    maintainers = ['dorton21']

    version('0.25.2', sha256='fe428ae5dc46f88fdf454ca74c4a073f5ac288d6d039080a3c0d66c4ebbd5cbf')
    version('0.23.6', sha256='c6e958e9741ee981bf2388c91b8f181718ffb0f32283cd7ebcd2d054817280e4')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r@3.0.2:', type=('build', 'run'), when='@0.25.2:')
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rapiserialize', type=('build', 'run'))
    depends_on('r-stringfish@0.14.1:', type=('build', 'run'))
    depends_on('r-stringfish@0.15.1:', type=('build', 'run'), when='@0.25.2:')
