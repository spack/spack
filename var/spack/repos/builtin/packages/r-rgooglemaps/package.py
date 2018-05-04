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


class RRgooglemaps(RPackage):
    """This package serves two purposes: (i) Provide a comfortable R interface
    to query the Google server for static maps, and (ii) Use the map as a
    background image to overlay plots within R. This requires proper coordinate
    scaling."""

    homepage = "https://cran.r-project.org/package=RgoogleMaps"
    url      = "https://cran.r-project.org/src/contrib/RgoogleMaps_1.2.0.7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RgoogleMaps"

    version('1.2.0.7', '2e1df804f0331b4122d841105f0c7ea5')

    depends_on('r-png', type=('build', 'run'))
    depends_on('r-rjsonio', type=('build', 'run'))
