# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHtmlwidgets(RPackage):
    """A framework for creating HTML widgets that render in various contexts
    including the R console, 'R Markdown' documents, and 'Shiny' web
    applications."""

    homepage = "https://cran.r-project.org/package=htmlTable"
    url      = "https://cran.rstudio.com/src/contrib/htmlwidgets_0.9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/htmlwidgets"

    version('0.9', 'b42730691eca8fc9a28903c272d11605')
    version('0.8', '06b0404a00e25736946607a36ee5351d')
    version('0.6', '7fa522d2eda97593978021bda9670c0e')

    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
