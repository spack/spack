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


class RTopgo(RPackage):
    """topGO package provides tools for testing GO terms while accounting
    for the topology of the GO graph. Different test statistics and
    different methods for eliminating local similarities and dependencies
    between GO terms can be implemented and applied."""

    homepage = "https://www.bioconductor.org/packages/topGO/"
    git      = "https://git.bioconductor.org/packages/topGO.git"

    version('2.30.1', commit='b1469ce1d198ccb73ef79ca22cab81659e16dbaa')
    version('2.28.0', commit='066a975d460046cce33fb27e74e6a0ebc33fd716')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-sparsem@0.73:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.7.19:', type=('build', 'run'))
    depends_on('r-go-db@2.3.0:', type=('build', 'run'))
    depends_on('r-biobase@2.0.0:', type=('build', 'run'))
    depends_on('r-graph@1.14.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.13.6:', type=('build', 'run'))
