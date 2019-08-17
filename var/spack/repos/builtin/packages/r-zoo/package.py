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
    url      = "https://cran.r-project.org/src/contrib/zoo_1.7-14.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/zoo"

    version('1.7-14', '8c577a7c1e535c899ab14177b1039c32')
    version('1.7-13', '99521dfa4c668e692720cefcc5a1bf30')

    depends_on('r-lattice', type=('build', 'run'))
