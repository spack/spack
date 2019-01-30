# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RFormatr(RPackage):
    """Provides a function tidy_source() to format R source code. Spaces and
    indent will be added to the code automatically, and comments will be
    preserved under certain conditions, so that R code will be more
    human-readable and tidy. There is also a Shiny app as a user interface in
    this package."""

    homepage = "https://cran.r-project.org/package=formatR"
    url      = "https://cran.r-project.org/src/contrib/formatR_1.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/formatR"

    version('1.5', 'ac735515b8e4c32097154f1b68c5ecc7')
    version('1.4', '98b9b64b2785b35f9df403e1aab6c73c')

    depends_on('r-codetools', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-testit', type=('build', 'run'))
    # depends_on('r-knitr', type=('build', 'run')) - mutual dependency
