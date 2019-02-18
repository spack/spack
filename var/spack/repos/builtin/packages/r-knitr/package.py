# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RKnitr(RPackage):
    """Provides a general-purpose tool for dynamic report generation in R using
    Literate Programming techniques."""

    homepage = "https://cran.r-project.org/package=knitr"
    url      = "https://cran.rstudio.com/src/contrib/knitr_1.14.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/knitr"

    version('1.17', '4407ccf8f2a51629800d6d5243cf3e70')
    version('1.14', 'ef0fbeaa9372f99ffbc57212a7781511')
    version('0.6',  'c67d6db84cd55594a9e870c90651a3db')

    depends_on('r-evaluate', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-formatr', type=('build', 'run'))
    depends_on('r-highr', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-markdown', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
