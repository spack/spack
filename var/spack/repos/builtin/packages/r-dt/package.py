# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDt(RPackage):
    """Data objects in R can be rendered as HTML tables using the JavaScript
    library 'DataTables' (typically via R Markdown or Shiny). The 'DataTables'
    library has been included in this R package. The package name 'DT' is an
    abbreviation of 'DataTables'."""

    homepage = "http://rstudio.github.io/DT"
    url      = "https://cran.r-project.org/src/contrib/DT_0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/DT"

    version('0.1', '5c8df984921fa484784ec4b8a4fb6f3c')

    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
