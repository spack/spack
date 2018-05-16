##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
