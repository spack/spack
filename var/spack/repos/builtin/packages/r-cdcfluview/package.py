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


class RCdcfluview(RPackage):
    """The 'U.S.' Centers for Disease Control ('CDC') maintains a portal
    <http://gis.cdc.gov/grasp/fluview/fluportaldashboard.html> for accessing
    state, regional and national influenza statistics as well as Mortality
    Surveillance Data. The web interface makes it difficult and time-consuming
    to select and retrieve influenza data. Tools are provided to access the
    data provided by the portal's underlying 'API'."""

    homepage = "https://cran.r-project.org/package=cdcfluview"
    url      = "https://cran.r-project.org/src/contrib/cdcfluview_0.7.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/cdcfluview"

    version('0.7.0', 'd592606fab3da3536f39a15c0fdbcd17')

    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-sf', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-readr', type=('build', 'run'))
    depends_on('r-mmwrweek', type=('build', 'run'))
    depends_on('r-units@0.4-6:', type=('build', 'run'))
    depends_on('r@3.2.0:', type=('build', 'run'))
