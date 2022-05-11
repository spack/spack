# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.util.package import *


class RFda(RPackage):
    """Functional Data Analysis.

    These functions were developed to support functional data
    analysis as described in Ramsay, J. O. and Silverman, B. W. (2005)
    Functional Data Analysis. New York: Springer and in Ramsay, J. O.,
    Hooker, Giles, and Graves, Spencer (2009). """

    cran = 'fda'

    version('5.5.1', sha256='dcaa2f6ae226d35855bc79c6967f60d45404b984c0afaec215b139c4b8dea23a')

    depends_on('r@3.5:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-fds', type=('build', 'run'))
    depends_on('r-desolve', type=('build', 'run'))
