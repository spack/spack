# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBookdown(RPackage):
    """Output formats and utilities for authoring books and technical
    documents with R Markdown."""

    homepage = "https://cran.r-project.org/package=bookdown"
    url      = "https://cran.rstudio.com/src/contrib/bookdown_0.5.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/bookdown"

    version('0.5', '7bad360948e2b22d28397870b9319f17')

    depends_on('r-yaml@2.1.14:', type=('build', 'run'))
    depends_on('r-rmarkdown@1.5:', type=('build', 'run'))
    depends_on('r-knitr@1.16:', type=('build', 'run'))
    depends_on('r-htmltools@0.3.6:', type=('build', 'run'))
