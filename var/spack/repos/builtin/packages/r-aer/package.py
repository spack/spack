# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAer(RPackage):
    """Functions, data sets, examples, demos, and vignettes
    for the book Christian Kleiber and Achim Zeileis (2008),
    Applied Econometrics with R, Springer-Verlag, New York.
    ISBN 978-0-387-77316-2."""

    homepage = "https://cran.r-project.org/web/packages/AER/index.html"
    url      = "https://cran.r-project.org/src/contrib/AER_1.2-5.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/AER"

    version('1.2-5', '419df9dc8ee6e5edd79678fee06719ae')

    depends_on('r@2.13.0:', type=('build', 'run'))
    depends_on('r-car@2.10-19:', type=('build', 'run'))
    depends_on('r-lmtest', type=('build', 'run'))
    depends_on('r-sandwich', type=('build', 'run'))
    depends_on('r-survival@2.37-5:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-formula', type=('build', 'run'))
