# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTigris(RPackage):
    """Download TIGER/Line shapefiles from the United States Census Bureau
    and load into R as 'SpatialDataFrame' or 'sf' objects."""

    homepage = "https://cran.r-project.org/package=tigris"
    url      = "https://cran.rstudio.com/src/contrib/tigris_0.5.3.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/tigris"

    version('0.5.3', 'c11cb459bf134d3deb1a641a60c86413')

    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-rgdal', type=('build', 'run'))
    depends_on('r-rgeos', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-rappdirs', type=('build', 'run'))
    depends_on('r-maptools', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-uuid', type=('build', 'run'))
    depends_on('r-sf', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
