# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RShiny(RPackage):
    """Makes it incredibly easy to build interactive web applications with R.
    Automatic "reactive" binding between inputs and outputs and extensive
    pre-built widgets make it possible to build beautiful, responsive, and
    powerful applications with minimal effort."""

    homepage = "http://shiny.rstudio.com/"
    url      = "https://cran.rstudio.com/src/contrib/shiny_1.0.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/shiny"

    version('1.0.5', '419dd5d3ea0bd87a07f8f0b1ef14fc13')
    version('0.13.2', 'cb5bff7a28ad59ec2883cd0912ca9611')

    depends_on('r-httpuv', type=('build', 'run'))
    depends_on('r-mime', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-sourcetools', type=('build', 'run'))
