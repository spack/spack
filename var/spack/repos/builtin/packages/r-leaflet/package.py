# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLeaflet(RPackage):
    """Create and customize interactive maps using the 'Leaflet' JavaScript
    library and the 'htmlwidgets' package. These maps can be used directly from
    the R console, from 'RStudio', in Shiny apps and R Markdown documents."""

    homepage = "http://rstudio.github.io/leaflet/"
    url      = "https://cran.r-project.org/src/contrib/leaflet_1.0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/leaflet"

    version('1.0.1', '7f3d8b17092604d87d4eeb579f73d5df')

    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-markdown', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
