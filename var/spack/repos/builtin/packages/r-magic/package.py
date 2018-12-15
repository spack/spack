# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMagic(RPackage):
    """A collection of efficient, vectorized algorithms for the creation and
    investigation of magic squares and hypercubes, including a variety of
    functions for the manipulation and analysis of arbitrarily dimensioned
    arrays."""

    homepage = "https://cran.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/magic_1.5-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/magic"

    version('1.5-6', 'a68e5ced253b2196af842e1fc84fd029')

    depends_on('r-abind', type=('build', 'run'))
