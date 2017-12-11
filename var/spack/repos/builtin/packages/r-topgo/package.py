##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
    url      = "https://git.bioconductor.org/packages/topGO"

    version('2.28.0', git='https://git.bioconductor.org/packages/topGO', commit='066a975d460046cce33fb27e74e6a0ebc33fd716')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-sparsem', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
