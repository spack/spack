# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSourcetools(RPackage):
    """Tools for Reading, Tokenizing and Parsing R Code."""

    homepage = "https://cran.r-project.org/package=sourcetools"
    url      = "https://cran.r-project.org/src/contrib/sourcetools_0.1.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/sourcetools"

    version('0.1.6', 'c78a816384b168d04af41bd7ff4d909d')
    version('0.1.5', 'b4d7902ffafd9802e8fbff5ce824bb28')

    depends_on('r-testthat', type=('build', 'run'))
