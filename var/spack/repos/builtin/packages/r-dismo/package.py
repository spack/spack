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


class RDismo(RPackage):
    """Functions for species distribution modeling, that is, predicting
       entire geographic distributions form occurrences at a number of
       sites and the environment at these sites."""

    homepage = "http://rspatial.org/sdm"
    url      = "https://cran.r-project.org/src/contrib/dismo_1.1-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/dismo/"

    version('1.1-4', sha256='f2110f716cd9e4cca5fd2b22130c6954658aaf61361d2fe688ba22bbfdfa97c8')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-raster@2.5-2:', type=('build', 'run'))
    depends_on('r-sp@1.2-0:', type=('build', 'run'))
