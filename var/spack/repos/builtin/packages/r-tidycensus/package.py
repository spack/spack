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


class RTidycensus(RPackage):
    """An integrated R interface to the decennial US Census and American
    Community Survey APIs and the US Census Bureau's geographic boundary
    files. Allows R users to return Census and ACS data as tidyverse-ready
    data frames, and optionally returns a list-column with feature
    geometry for many geographies."""

    homepage = "https://cran.r-project.org/package=tidycensus"
    url      = "https://cran.rstudio.com/src/contrib/tidycensus_0.3.1.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/tidycensus"

    version('0.3.1', '420d046b5a408d321e775c3d410e7699')

    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-sf', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-tigris', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-rvest', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-rappdirs', type=('build', 'run'))
    depends_on('r-readr', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
    depends_on('r-units', type=('build', 'run'))
