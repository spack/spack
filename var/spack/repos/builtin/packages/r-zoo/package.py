# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RZoo(RPackage):
    """An S3 class with methods for totally ordered indexed observations. It is
    particularly aimed at irregular time series of numeric vectors/matrices and
    factors. zoo's key design goals are independence of a particular
    index/date/time class and consistency with ts and base R by providing
    methods to extend standard generics."""

    homepage = "http://zoo.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/zoo_1.7-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/zoo"

    version('1.8-6', sha256='2217a4f362f2201443b5fdbfd9a77d9a6caeecb05f02d703ee8b3b9bf2af37cc')
    version('1.8-5', sha256='8773969973d28d7d1a48f74b73be1dbd97acb3b22a4668a102e8bb585a7de826')
    version('1.7-14', '8c577a7c1e535c899ab14177b1039c32')
    version('1.7-13', '99521dfa4c668e692720cefcc5a1bf30')

    depends_on('r@2.10.0:', when='@:1.8-1', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@1.8-2:', type=('build', 'run'))
    depends_on('r-lattice@0.20-27:', type=('build', 'run'))
