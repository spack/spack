##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class RMixomics(RPackage):
    """Omics Data Integration Project"""

    homepage = "http://www.mixOmics.org"
    url      = "https://cran.r-project.org/src/contrib/mixOmics_6.1.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mixOmics"

    version('6.1.3', '31210a3041eccc6b2b7c7279431146da')

    depends_on('r@2.10:', type=('build', 'run'))

    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-rgl', type=('build', 'run'))
    depends_on('r-ellipse', type=('build', 'run'))
    depends_on('r-corpcor', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
